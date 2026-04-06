import os
import glob
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt

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

def GetTestLabel(filename):
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

def ExtractAndPlotData():
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    folderPath = os.path.join(scriptDir, "Data", "RCWA-1")
    filePattern = os.path.join(folderPath, "*.csv")
    allFiles = glob.glob(filePattern)
    
    if not allFiles:
        print(f"Couldn't find any CSV files in {folderPath}.")
        return

    structureGroups = {}
    allData = []

    print(f"--- Analyzing {len(allFiles)} files in {folderPath} ---")
    
    for file in allFiles:
        df = pd.read_csv(file)
        filename = os.path.basename(file)
        cleanName = filename.replace('.csv', '')
        
        displayLabel = GetTestLabel(filename)
            
        print(f"Loaded: '{filename}'\n   -> Mapped to Label: '{displayLabel}'")
            
        missingCategories = [cat for cat in ['R', 'T', 'A'] if cat not in df.columns or df[cat].isnull().all()]
        if missingCategories:
            print(f"   -> WARNING: Missing categories: {missingCategories}")
            
        try:
            if 'shape_' in filename:
                structureName = filename.split('shape_')[1].split('_')[0]
            else:
                structureName = "Custom_Shape"
        except IndexError:
            structureName = "Unknown_Structure"
            
        if structureName not in structureGroups:
            structureGroups[structureName] = []
        
        fileInfo = {
            'filename': cleanName, 
            'label': displayLabel, 
            'data': df, 
            'structure': structureName
        }
        structureGroups[structureName].append(fileInfo)
        allData.append(fileInfo)

    allData = sorted(allData, key=lambda x: (x['structure'], x['label']))

    print("\n--- Generating Individual Global Plots ---")
    
    def CreateGlobalPlot(category, title, ylabel, outputFilename):
        plt.figure(figsize=(12, 7))
        
        numItems = len(allData)
        cmap = plt.get_cmap('magma')
        start, stop = 0.1, 0.85
        colors = [cmap(start + (stop - start) * i / max(1, numItems - 1)) for i in range(numItems)]
        
        for i, item in enumerate(allData):
            df = item['data']
            if category in df.columns:
                globalLabel = f"{item['structure']} - {item['label']}"
                plt.plot(df['wavelength_nm'], df[category] * 100, "--", label=globalLabel, color=colors[i])
                
        plt.title(title)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel(ylabel)
        
        plt.tight_layout()
        plt.legend(bbox_to_anchor=(1, 0.5), loc='center left', fontsize='small')
        
        outputPath = os.path.join(scriptDir, "Plots", outputFilename)
        plt.savefig(outputPath, bbox_inches='tight')
        plt.close()
        print(f"Saved Global Plot: {outputPath}")

    os.makedirs(os.path.join(scriptDir, "Plots"), exist_ok=True)

    CreateGlobalPlot('T', "Global Transmittance Comparison", "Transmittance (%)", "Plot_1_Global_Transmittance.png")
    CreateGlobalPlot('A', "Global Absorbance Comparison", "Absorbance (%)", "Plot_2_Global_Absorbance.png")
    CreateGlobalPlot('R', "Global Reflectance Comparison", "Reflectance (%)", "Plot_3_Global_Reflectance.png")

    print("\n--- Generating Category-Specific Comparisons ---")
    
    testStyles = {
        "Test 1": {"linestyle": "-", "linewidth": 4, "alpha": 0.4},
        "Test 2": {"linestyle": "--", "linewidth": 2, "alpha": 1.0},
        "Test 3": {"linestyle": ":", "linewidth": 2.5, "alpha": 1.0},
        "Test 4": {"linestyle": "-.", "linewidth": 2, "alpha": 1.0},
        "Test 5": {"linestyle": (0, (8, 4)), "linewidth": 2, "alpha": 1.0}, 
        "Custom Test": {"linestyle": "-", "linewidth": 2, "alpha": 0.8}
    }
    
    for structure, items in structureGroups.items():
        items = sorted(items, key=lambda x: x['label'])
        
        fig, axes = plt.subplots(1, 3, figsize=(24, 8))
        fig.suptitle(f"Comparison within Category: {structure}", fontsize=22, weight='bold', y=0.98)
        
        numItems = len(items)
        cmap = plt.get_cmap('magma')
        start, stop = 0.1, 0.85
        colors = [cmap(start + (stop - start) * i / max(1, numItems - 1)) for i in range(numItems)]
        
        for i, item in enumerate(items):
            df = item['data']
            label = item['label']
            c = colors[i]
            
            style = testStyles.get(label, testStyles["Custom Test"])
            ls = style["linestyle"]
            lw = style["linewidth"]
            a = style["alpha"]
            
            if 'T' in df.columns: 
                axes[0].plot(df['wavelength_nm'], df['T'] * 100, label=label, linestyle=ls, linewidth=lw, alpha=a, color=c)
            if 'R' in df.columns: 
                axes[1].plot(df['wavelength_nm'], df['R'] * 100, label=label, linestyle=ls, linewidth=lw, alpha=a, color=c)
            if 'A' in df.columns: 
                axes[2].plot(df['wavelength_nm'], df['A'] * 100, label=label, linestyle=ls, linewidth=lw, alpha=a, color=c)

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
        fig.subplots_adjust(top=0.85, bottom=0.25, wspace=0.35)
        
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=len(items), fontsize='medium')
        
        outputPath = os.path.join(scriptDir, "Plots", f"Plot_Category_{structure}.png")
        plt.savefig(outputPath, bbox_inches='tight')
        plt.close()
        print(f"Saved Category Plot: {outputPath}")

    print("\n--- Generating Average Curve Comparisons ---")
    
    avgCurves = {}
    for structure, items in structureGroups.items():
        combinedDf = pd.concat([item['data'] for item in items], ignore_index=True)
        avgCurve = combinedDf.groupby('wavelength_nm').mean().reset_index()
        avgCurves[structure] = avgCurve

    def CreateAverageCurvePlot(category, title, ylabel, outputFilename):
        plt.figure(figsize=(12, 7))
        
        numItems = len(avgCurves)
        cmap = plt.get_cmap('magma')
        start, stop = 0.1, 0.85
        colors = [cmap(start + (stop - start) * i / max(1, numItems - 1)) for i in range(numItems)]
        
        for i, (structure, df) in enumerate(avgCurves.items()):
            if category in df.columns:
                plt.plot(df['wavelength_nm'], df[category] * 100, label=structure, color=colors[i])
                
        plt.title(title)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel(ylabel)
        
        plt.tight_layout()
        plt.legend(title="Structure Shape", bbox_to_anchor=(1, 0.5), loc='center left', fontsize='small')
        
        outputPath = os.path.join(scriptDir, "Plots", outputFilename)
        plt.savefig(outputPath, bbox_inches='tight')
        plt.close()
        print(f"Saved Average Curve Plot: {outputPath}")

    CreateAverageCurvePlot('T', "Average Transmittance by Structure Type", "Average Transmittance (%)", "Plot_4_Average_Transmittance.png")
    CreateAverageCurvePlot('A', "Average Absorbance by Structure Type", "Average Absorbance (%)", "Plot_5_Average_Absorbance.png")
    CreateAverageCurvePlot('R', "Average Reflectance by Structure Type", "Average Reflectance (%)", "Plot_6_Average_Reflectance.png")

    print("\nFinished Generating Analysis Plots!")

if __name__ == "__main__":
    ExtractAndPlotData()