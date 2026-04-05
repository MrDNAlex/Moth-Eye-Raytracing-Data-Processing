import os
import re 
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import pandas as pd

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

def ExtractPowerAndRays(file, fullPath):
    with open(os.path.join(fullPath, file), "r") as f:
        data = json.load(f)
        
    Stats = data["Stats"]
    
    return [Stats["CapturedPower"], Stats["StartRays"], Stats["CapturedRays"]]

def GetPowerFromFile(file, fullPath):
    
    with open(os.path.join(fullPath, file), "r") as f:
        data = json.load(f)
        
    Stats = data["Stats"]
    return Stats["CapturedPower"] / Stats["StartRays"]

def ExtractData(commonPath, specificPaths : list[str]):

    dataframe = pd.DataFrame()
    
    for i in range(len(specificPaths)):
        
        path = specificPaths[i]
        
        fullDataPath = os.path.join(commonPath, "Data", path)
        
        folders = [f for f in os.listdir(fullDataPath) if os.path.isdir(os.path.join(fullDataPath, f))]
        
        for fol in folders:
            
            def extract_number(filename):
                match = re.search(r"Waveguide(\d+)", filename)
                return int(match.group(1)) if match else -1
            
            # Sort numerically by waveguide number
            files = sorted(
                [f for f in os.listdir(os.path.join(fullDataPath, fol)) if f.endswith(".json")],
                key=extract_number
            )
        
            for j in range(len(files)):
                
                f = files[j]
                
                dataframe.loc[j, "Layers"] = f.split("Waveguide")[1].split("Large")[0].split("UnitCell")[0]
                
                data = ExtractPowerAndRays(f, os.path.join(fullDataPath, fol))
                
                dataframe.loc[j, f"{path}_{fol}_CapturedPower"] = data[0]
                dataframe.loc[j, f"{path}_{fol}_CapturedRays"] = data[1]
                dataframe.loc[j, f"{path}_{fol}_StartRays"] = data[2]
        
    dataframe.to_csv(f"{commonPath}/InternalReflectionsWaveguide.csv", index=False)

def PlotInternalReflections(commonPath, specificPath):

    fullPlotPath = os.path.join(commonPath, "Plots", specificPath)

    # Re-applied the makedirs fix to prevent crashes
    if not os.path.exists(fullPlotPath):
        os.makedirs(fullPlotPath, exist_ok=True)

    dataframe = pd.read_csv(f"{commonPath}/InternalReflectionsWaveguide.csv")

    plt.figure(figsize=(16, 10))

    cmap = plt.get_cmap('magma')
    colors = [cmap(i / 15) for i in range(15)]

    for i in range(1, 16):

        # Use the original folder name for the dataframe lookup
        folder_name = f"QD{i}"
        
        # Use the formatted name for the graph legend
        display_label = f"{i} QDs"

        powerPercent = dataframe[f"{specificPath}_{folder_name}_CapturedPower"] / dataframe[f"{specificPath}_{folder_name}_StartRays"] * 100

        plt.plot(dataframe["Layers"], powerPercent, label=display_label, color=colors[i-1])

    # The title now pulls the combined name and simplified definition directly from the dictionary below
    plt.title(f"TIR Power Absorbed from QD Emission using a {paths[specificPath]}")
    plt.xlabel("Number of Layers")
    plt.ylabel("Absorbed Power (%)")
    plt.grid(True, alpha=0.6)
    
    # Centered outside legend
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    
    plt.savefig(f"{fullPlotPath}/Internal_Reflection_Power_Absorbed_{specificPath}_Waveguide.png")
    plt.close()

# The simplified definitions are now baked right into the titles with a newline character (\n)
paths = {
    "Cone_Large_Regular" : "Cone QD and Linear GRIN\n(Isolated Device-Scale Structure)",
    "Cone_Large_MothEye": "Cone QD and Approximated GRIN\n(Isolated Device-Scale Structure)",
    "Cone_UnitCell_Regular": "Cone QD and Linear GRIN\n(Single Repeating Unit Cell)",
    "Cone_UnitCell_MothEye": "Cone QD and Approximated GRIN\n(Single Repeating Unit Cell)",
    "QD_Large_Regular" : "Circular QD and Linear GRIN\n(Isolated Device-Scale Structure)",
    "QD_Large_MothEye": "Circular QD and Approximated GRIN\n(Isolated Device-Scale Structure)",
    "QD_UnitCell_Regular": "Circular QD and Linear GRIN\n(Single Repeating Unit Cell)",
    "QD_UnitCell_MothEye": "Circular QD and Approximated GRIN\n(Single Repeating Unit Cell)",
}

#ExtractData("Initial-Raytracing/InternalReflections", list(paths.keys()))

#for path in paths.keys():
#    PlotInternalReflections("Initial-Raytracing/InternalReflections", path)