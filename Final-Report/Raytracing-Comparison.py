import os
import glob
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt
import re

plt.style.use('ggplot')
mpl.rcParams['lines.linewidth'] = 4
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['font.size'] = 16  
mpl.rcParams['figure.titlesize'] = 22 
plt.rcParams['axes.titlepad'] = 20
mpl.rcParams['font.weight'] = 'light'
mpl.rcParams['figure.facecolor'] = 'white'
mpl.rcParams['axes.facecolor'] = 'white'
mpl.rcParams['axes.edgecolor'] = '#0E0A1F'
mpl.rcParams['grid.color'] = '#0E0A1F'
mpl.rcParams['axes.labelcolor'] = '#0E0A1F'
mpl.rcParams['lines.color'] = '#0E0A1F'
mpl.rcParams['xtick.color'] = '#0E0A1F'
mpl.rcParams['ytick.color'] = '#0E0A1F'
mpl.rcParams['lines.markersize'] = 10

def get_test_info(filename):
    # 1. Grab every single number found in the filename
    numbers = re.findall(r'\d+', filename)
    
    # 2. The first number is ALWAYS the angle, default to 0 if none found
    angle = int(numbers[0]) if numbers else 0
    label = f"Angle {angle}°"
    
    # 3. Try to gracefully extract the category (e.g., Regular) if the format matches
    match = re.search(r'_Layers_\d+_(.+)\.csv', filename)
    category = match.group(1) if match else "Custom_Category"
        
    return category, label, angle

def get_sim_title(sim_folder):
    # Extract the simulation number directly from the folder string (e.g., "Sim4" -> 4)
    match = re.search(r'\d+', sim_folder)
    if not match:
        return sim_folder, None
        
    sim_num = int(match.group())
    
    # Clean, grammatically correct titles mapped to the simulation number
    titles = {
        1: "Device Stack Optical Properties (3 Layers)",
        2: "Device Stack Optical Properties (3 Layers, Surface Normal Perturbance)",
        3: "Device Stack Optical Properties (3 Layers, Wavy + Perturbance)",
        4: "Device Stack TIR Optical Properties (40 Layers)",
        5: "Device Stack TIR Optical Properties (40 Layers, Surface Normal Perturbance)",
        6: "Device Stack TIR Optical Properties (40 Layers, Wavy + Perturbance)",
        7: "Single PDMS Layer Optical Properties"
    }
    
    return titles.get(sim_num, sim_folder), sim_num

def main():
    # Get the exact directory where my script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate up two levels to the root of my FYDP-SunDOG repository, then into the Data folder
    folder_path = os.path.abspath(os.path.join(script_dir, "Data", "Raytracing-Solcore"))
    
    # Create the search pattern for my CSV files to look INSIDE subfolders
    file_pattern = os.path.join(folder_path, "**", "*.csv")
    all_files = glob.glob(file_pattern, recursive=True)
    
    if not all_files:
        print(f"I couldn't find any CSV files in {folder_path} or its subfolders.")
        return

    structure_groups = {}
    
    print(f"--- Analyzing my {len(all_files)} files in {folder_path} ---")
    
    # Loop through my files and group them by BOTH their simulation folder and category
    for file in all_files:
        df = pd.read_csv(file)
        filename = os.path.basename(file)
        
        sim_folder = os.path.basename(os.path.dirname(file))
        category, label, sort_key = get_test_info(filename)
        print(f"Loaded: '{filename}'\n   -> Folder: '{sim_folder}', Category: '{category}', Label: '{label}'")
        
        group_key = f"{sim_folder}_{category}"
        
        if group_key not in structure_groups:
            structure_groups[group_key] = {
                'sim_folder': sim_folder,
                'category': category,
                'items': []
            }
            
        structure_groups[group_key]['items'].append({
            'filename': filename, 
            'label': label, 
            'sort_key': sort_key,
            'data': df
        })

    print("\n--- Generating Folder-Specific Comparisons ---")
    
    output_dir = os.path.join(script_dir, "Plots")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create subplots comparing files strictly within their own folder and category
    for group_key, group_data in structure_groups.items():
        sim_folder = group_data['sim_folder']
        category = group_data['category']
        
        items = sorted(group_data['items'], key=lambda x: x['sort_key'])
        num_items = len(items)
        
        fig, axes = plt.subplots(1, 3, figsize=(24, 7))
        
        # Grab the clean title and simulation number based on the folder string
        base_title, sim_num = get_sim_title(sim_folder)
        
        # Replace the category suffix with "Simulation X"
        if sim_num is not None:
            display_title = f"{base_title} - Simulation {sim_num}"
        else:
            display_title = f"{base_title} - {sim_folder}"
            
        fig.suptitle(display_title, fontsize=22, weight='bold', y=0.98)
        
        # Extract magma colormap and generate a color for each item
        cmap = plt.get_cmap('magma')
        # We sample from 0.1 to 0.85 to avoid pure black or pure white/yellow on the white background
        start, stop = 0.1, 0.85
        colors = [cmap(start + (stop - start) * i / max(1, num_items - 1)) for i in range(num_items)]
        
        for i, item in enumerate(items):
            df = item['data']
            label = item['label']
            c = colors[i]
            
            if 'Transmittance' in df.columns: 
                axes[0].plot(df['Wavelength'], df['Transmittance'] * 100, label=label, color=c)
            if 'Reflectance' in df.columns: 
                axes[1].plot(df['Wavelength'], df['Reflectance'] * 100, label=label, color=c)
            if 'Absorbance' in df.columns: 
                axes[2].plot(df['Wavelength'], df['Absorbance'] * 100, label=label, color=c)

        # Style my axes
        axes[0].set_title("Transmittance (T)")
        axes[0].set_ylabel("Transmittance (%)")
        axes[1].set_title("Reflectance (R)")
        axes[1].set_ylabel("Reflectance (%)")
        axes[2].set_title("Absorbance (A)")
        axes[2].set_ylabel("Absorbance (%)")
        
        for ax in axes:
            ax.set_xlabel("Wavelength (nm)")
            ax.grid(True, alpha=0.6)
            ax.margins(y=0.1) 
            
        plt.tight_layout()
        
        fig.subplots_adjust(top=0.80, bottom=0.25, wspace=0.35)
        
        num_cols = min(len(items), 5) 
        
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=num_cols, fontsize='medium')
        
        output_path = os.path.join(output_dir, f"Plot_{sim_folder}_{category}.png")
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        print(f"Saved Folder-Specific Plot: {output_path}")

    print("\nAll of my analysis plots have been generated successfully!")

if __name__ == "__main__":
    main()