import os
import glob
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')
mpl.rcParams['lines.linewidth'] = 4
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['font.size'] = 16  # Reduced slightly from 18
mpl.rcParams['figure.titlesize'] = 22 # Reduced slightly from 25
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

def get_test_label(filename):
    # Map the filename parameters to the corresponding Test based on the Julia scripts
    if "N_3" in filename and "angle_0.0" in filename and "nlayers_200" in filename and "t_1" in filename:
        return "Test 1"
    elif "N_3" in filename and "angle_45.0" in filename and "nlayers_200" in filename and "t_1" in filename:
        return "Test 2"
    elif "N_5" in filename and "angle_0.0" in filename and "nlayers_200" in filename and "t_1" in filename:
        return "Test 3"
    elif "N_3" in filename and "angle_0.0" in filename and "nlayers_80" in filename and "t_2" in filename:
        return "Test 4"
    elif "N_3" in filename and "angle_0.0" in filename and "nlayers_80" in filename and "t_3" in filename:
        return "Test 5"
    else:
        return "Custom Test"

def main():
    # 1. Get the exact directory where my script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Define the folder path relative to my script's location
    folder_path = os.path.join(script_dir, "Data", "RCWA-1")
    
    # 3. Create the search pattern for my CSV files
    file_pattern = os.path.join(folder_path, "*.csv")
    all_files = glob.glob(file_pattern)
    
    if not all_files:
        print(f"I couldn't find any CSV files in {folder_path}.")
        return

    structure_groups = {}
    all_data = []

    print(f"--- Analyzing my {len(all_files)} files in {folder_path} ---")
    
    # 4. Loop through my files and check for missing data categories
    for file in all_files:
        df = pd.read_csv(file)
        filename = os.path.basename(file)
        clean_name = filename.replace('.csv', '')
        
        # Use my new mapping function to grab the right test name
        display_label = get_test_label(filename)
            
        print(f"Loaded: '{filename}'\n   -> Mapped to Label: '{display_label}'")
            
        missing_categories = [cat for cat in ['R', 'T', 'A'] if cat not in df.columns or df[cat].isnull().all()]
        if missing_categories:
            print(f"   -> WARNING: Missing categories: {missing_categories}")
            
        # Extract the structure shape name from my filename formatting safely
        try:
            if 'shape_' in filename:
                structure_name = filename.split('shape_')[1].split('_')[0]
            else:
                structure_name = "Custom_Shape"
        except IndexError:
            structure_name = "Unknown_Structure"
            
        if structure_name not in structure_groups:
            structure_groups[structure_name] = []
        
        file_info = {'filename': clean_name, 'label': display_label, 'data': df}
        structure_groups[structure_name].append(file_info)
        all_data.append(file_info)

    print("\n--- Generating Individual Global Plots ---")
    
    def create_global_plot(category, title, ylabel, output_filename):
        # Increased size for global plots
        plt.figure(figsize=(12, 7))
        
        # Generate magma colors based on the total number of items
        num_items = len(all_data)
        cmap = plt.get_cmap('magma')
        start, stop = 0.1, 0.85
        colors = [cmap(start + (stop - start) * i / max(1, num_items - 1)) for i in range(num_items)]
        
        for i, item in enumerate(all_data):
            df = item['data']
            if category in df.columns:
                # Add the structure name to the test label so global plots are distinguishable 
                # (e.g., "Test 1 - hillLikeRadius")
                global_label = f"{item['label']} - {item['filename'].split('shape_')[1].split('_')[0]}" if 'shape_' in item['filename'] else item['label']
                plt.plot(df['wavelength_nm'], df[category], "--", label=global_label, color=colors[i])
                
        plt.title(title)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel(ylabel)
        
        plt.tight_layout()
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        
        output_path = os.path.join(script_dir, "Plots", output_filename)
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        print(f"Saved Global Plot: {output_path}")

    # Ensure Plots directory exists
    os.makedirs(os.path.join(script_dir, "Plots"), exist_ok=True)

    # 5. Create my individual global graphs for T, A, and R
    create_global_plot('T', "Global Transmittance Comparison", "Transmittance", "Plot_1_Global_Transmittance.png")
    create_global_plot('A', "Global Absorbance Comparison", "Absorbance", "Plot_2_Global_Absorbance.png")
    create_global_plot('R', "Global Reflectance Comparison", "Reflectance", "Plot_3_Global_Reflectance.png")

    print("\n--- Generating Category-Specific Comparisons ---")
    
    # Define a cleaner style map
    test_styles = {
        "Test 1": {"linestyle": "-", "linewidth": 4, "alpha": 0.4},
        "Test 2": {"linestyle": "--", "linewidth": 2, "alpha": 1.0},
        "Test 3": {"linestyle": ":", "linewidth": 2.5, "alpha": 1.0},
        "Test 4": {"linestyle": "-.", "linewidth": 2, "alpha": 1.0},
        "Test 5": {"linestyle": (0, (8, 4)), "linewidth": 2, "alpha": 1.0}, 
        "Custom Test": {"linestyle": "-", "linewidth": 2, "alpha": 0.8}
    }
    
    # 6. Create subplots comparing files strictly within their own category
    for structure, items in structure_groups.items():
        # Sort items so Test 1 appears before Test 2, etc. in the legend
        items = sorted(items, key=lambda x: x['label'])
        
        # Widened figure size to 24x8
        fig, axes = plt.subplots(1, 3, figsize=(24, 8))
        fig.suptitle(f"Comparison within Category: {structure}", fontsize=22, weight='bold', y=0.98)
        
        # Generate magma colors for this specific category
        num_items = len(items)
        cmap = plt.get_cmap('magma')
        start, stop = 0.1, 0.85
        colors = [cmap(start + (stop - start) * i / max(1, num_items - 1)) for i in range(num_items)]
        
        for i, item in enumerate(items):
            df = item['data']
            label = item['label']
            c = colors[i]
            
            # Fetch the specific style for this test, fallback to a default if not found
            style = test_styles.get(label, test_styles["Custom Test"])
            ls = style["linestyle"]
            lw = style["linewidth"]
            a = style["alpha"]
            
            # Apply the styles and the dynamic color to the plots
            if 'T' in df.columns: axes[0].plot(df['wavelength_nm'], df['T'], label=label, linestyle=ls, linewidth=lw, alpha=a, color=c)
            if 'R' in df.columns: axes[1].plot(df['wavelength_nm'], df['R'], label=label, linestyle=ls, linewidth=lw, alpha=a, color=c)
            if 'A' in df.columns: axes[2].plot(df['wavelength_nm'], df['A'], label=label, linestyle=ls, linewidth=lw, alpha=a, color=c)

        axes[0].set_title("Transmittance (T)")
        axes[0].set_ylabel("Transmittance")
        axes[1].set_title("Reflectance (R)")
        axes[1].set_ylabel("Reflectance")
        axes[2].set_title("Absorbance (A)")
        axes[2].set_ylabel("Absorbance")
        
        for ax in axes:
            ax.set_xlabel("Wavelength (nm)")
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.margins(y=0.1)
            
        # Clean layout and add heavy spacing for text and legend
        plt.tight_layout()
        fig.subplots_adjust(top=0.85, bottom=0.25, wspace=0.35)
        
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=len(items), fontsize='medium')
        
        output_path = os.path.join(script_dir, "Plots", f"Plot_Category_{structure}.png")
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        print(f"Saved Category Plot: {output_path}")

    print("\n--- Generating Average Structure Comparison ---")
    print("\n--- Generating Average Curve Comparisons ---")
    
    # 7. Calculate my average curves for each structure
    avg_curves = {}
    for structure, items in structure_groups.items():
        combined_df = pd.concat([item['data'] for item in items], ignore_index=True)
        avg_curve = combined_df.groupby('wavelength_nm').mean().reset_index()
        avg_curves[structure] = avg_curve

    # Helper function to plot my average comparison curves
    def create_average_curve_plot(category, title, ylabel, output_filename):
        plt.figure(figsize=(12, 7))
        
        # Generate magma colors based on the number of structures being compared
        num_items = len(avg_curves)
        cmap = plt.get_cmap('magma')
        start, stop = 0.1, 0.85
        colors = [cmap(start + (stop - start) * i / max(1, num_items - 1)) for i in range(num_items)]
        
        for i, (structure, df) in enumerate(avg_curves.items()):
            if category in df.columns:
                plt.plot(df['wavelength_nm'], df[category], label=structure, color=colors[i])
                
        plt.title(title)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel(ylabel)
        
        plt.tight_layout()
        plt.legend(title="Structure Shape", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        
        output_path = os.path.join(script_dir, "Plots", output_filename)
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        print(f"Saved Average Curve Plot: {output_path}")

    # 8. Plot my final average curves for T, A, and R
    create_average_curve_plot('T', "Average Transmittance by Structure Type", "Average Transmittance", "Plot_4_Average_Transmittance.png")
    create_average_curve_plot('A', "Average Absorbance by Structure Type", "Average Absorbance", "Plot_5_Average_Absorbance.png")
    create_average_curve_plot('R', "Average Reflectance by Structure Type", "Average Reflectance", "Plot_6_Average_Reflectance.png")

    print("\nAll of my analysis plots have been generated successfully!")

if __name__ == "__main__":
    main()