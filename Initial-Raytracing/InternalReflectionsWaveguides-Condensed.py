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

def PlotPairedInternalReflections(commonPath, pairName, pathLeft, pathRight):
    
    fullPlotPath = os.path.join(commonPath, "Plots", pairName)

    if not os.path.exists(fullPlotPath):
        os.makedirs(fullPlotPath, exist_ok=True)

    dataframe = pd.read_csv(f"{commonPath}/InternalReflectionsWaveguide.csv")

    # Create a figure with 1 row, 2 columns. sharey=True aligns their Y-axis.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 10), sharey=True)

    cmap = plt.get_cmap('magma')
    colors = [cmap(i / 15) for i in range(15)]

    # Loop over both axes and their respective path string
    for ax, specificPath in zip([ax1, ax2], [pathLeft, pathRight]):
        
        for i in range(1, 16):
            folder_name = f"QD{i}"
            display_label = f"{i} QDs"

            powerPercent = dataframe[f"{specificPath}_{folder_name}_CapturedPower"] / dataframe[f"{specificPath}_{folder_name}_StartRays"] * 100

            ax.plot(dataframe["Layers"], powerPercent, label=display_label, color=colors[i-1])

        # Set individual titles from our paths dictionary
        ax.set_title(f"TIR Power Absorbed: {paths[specificPath]}")
        ax.set_xlabel("Number of Layers")
        ax.grid(True, alpha=0.6)
        
        # Only set the Y label on the leftmost graph
        if ax == ax1:
            ax.set_ylabel("Absorbed Power (%)")

    # Add one legend to the rightmost graph, placing it outside the plot area
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.tight_layout()
    plt.savefig(f"{fullPlotPath}/Internal_Reflection_Power_Absorbed_{pairName}_Combined.png")
    plt.close()

# Simplified definitions baked into titles
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

# Define the pairs I want to plot together
# Format: ("Save_Folder_Name", "Left_Graph_Key", "Right_Graph_Key")
pairs = [
    ("Cone_Large", "Cone_Large_Regular", "Cone_Large_MothEye"),
    ("Cone_UnitCell", "Cone_UnitCell_Regular", "Cone_UnitCell_MothEye"),
    ("QD_Large", "QD_Large_Regular", "QD_Large_MothEye"),
    ("QD_UnitCell", "QD_UnitCell_Regular", "QD_UnitCell_MothEye")
]

# Uncomment to extract data
# ExtractData("Initial-Raytracing/InternalReflections", list(paths.keys()))

# Loop through the pairs and plot them
for pair in pairs:
    PlotPairedInternalReflections("Initial-Raytracing/InternalReflections", pair[0], pair[1], pair[2])