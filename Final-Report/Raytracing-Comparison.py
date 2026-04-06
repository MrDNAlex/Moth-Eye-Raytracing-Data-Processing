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

def GetTestInfo(filename):
    # Grab every single number found in the filename
    numbers = re.findall(r'\d+', filename)
    
    # The first number is ALWAYS the angle, default to 0 if none found
    angle = int(numbers[0]) if numbers else 0
    label = f"Angle {angle}°"
    
    # Try to gracefully extract the category (e.g., Regular) if the format matches
    match = re.search(r'_Layers_\d+_(.+)\.csv', filename)
    category = match.group(1) if match else "Custom_Category"
        
    return category, label, angle

def GetSimTitle(simFolder):
    # Extract the simulation number directly from the folder string
    match = re.search(r'\d+', simFolder)
    if not match:
        return simFolder, None
        
    simNum = int(match.group())
    
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
    
    return titles.get(simNum, simFolder), simNum

def ExtractAndPlotData():
    # Get the exact directory where the script is saved
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate up two levels to the root repository, then into the Data folder
    folderPath = os.path.abspath(os.path.join(scriptDir, "Data", "Raytracing-Solcore"))
    
    # Create the search pattern for CSV files to look INSIDE subfolders
    filePattern = os.path.join(folderPath, "**", "*.csv")
    allFiles = glob.glob(filePattern, recursive=True)
    
    if not allFiles:
        print(f"Couldn't find any CSV files in {folderPath} or its subfolders.")
        return

    structureGroups = {}
    
    print(f"--- Analyzing {len(allFiles)} files in {folderPath} ---")
    
    # Loop through files and group them by BOTH their simulation folder and category
    for file in allFiles:
        df = pd.read_csv(file)
        filename = os.path.basename(file)
        
        simFolder = os.path.basename(os.path.dirname(file))
        category, label, sortKey = GetTestInfo(filename)
        print(f"Loaded: '{filename}'\n   -> Folder: '{simFolder}', Category: '{category}', Label: '{label}'")
        
        groupKey = f"{simFolder}_{category}"
        
        if groupKey not in structureGroups:
            structureGroups[groupKey] = {
                'simFolder': simFolder,
                'category': category,
                'items': []
            }
            
        structureGroups[groupKey]['items'].append({
            'filename': filename, 
            'label': label, 
            'sortKey': sortKey,
            'data': df
        })

    print("\n--- Generating Folder-Specific Comparisons ---")
    
    outputDir = os.path.join(scriptDir, "Plots")
    os.makedirs(outputDir, exist_ok=True)
    
    # Create subplots comparing files strictly within their own folder and category
    for groupKey, groupData in structureGroups.items():
        simFolder = groupData['simFolder']
        category = groupData['category']
        
        items = sorted(groupData['items'], key=lambda x: x['sortKey'])
        numItems = len(items)
        
        fig, axes = plt.subplots(1, 3, figsize=(24, 7))
        
        # Grab the clean title and simulation number based on the folder string
        baseTitle, simNum = GetSimTitle(simFolder)
        
        # Replace the category suffix with "Simulation X"
        if simNum is not None:
            displayTitle = f"{baseTitle} - Simulation {simNum}"
        else:
            displayTitle = f"{baseTitle} - {simFolder}"
            
        fig.suptitle(displayTitle, fontsize=22, weight='bold', y=0.98)
        
        # Extract magma colormap and generate a color for each item
        cmap = plt.get_cmap('magma')
        
        # Sample from 0.1 to 0.85 to avoid pure black or pure white/yellow on the white background
        start, stop = 0.1, 0.85
        colors = [cmap(start + (stop - start) * i / max(1, numItems - 1)) for i in range(numItems)]
        
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

        # Style axes
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
        
        numCols = min(len(items), 5) 
        
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=numCols, fontsize='medium')
        
        outputPath = os.path.join(outputDir, f"Plot_{simFolder}_{category}.png")
        plt.savefig(outputPath, bbox_inches='tight')
        plt.close()
        
        print(f"Saved Folder-Specific Plot: {outputPath}")

    print("\nFinished Generating Analysis Plots")

if __name__ == "__main__":
    ExtractAndPlotData()