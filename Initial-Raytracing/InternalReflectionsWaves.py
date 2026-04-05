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

def GetPowerFromFile(file, fullPath):
    
    with open(os.path.join(fullPath, file), "r") as f:
        data = json.load(f)
        
    Stats = data["Stats"]
    return Stats["CapturedPower"] / Stats["StartRays"]

# Use this Format for all Other Upcoming Data
def ExtractPowerAndRays(file, fullPath):
    with open(os.path.join(fullPath, file), "r") as f:
        data = json.load(f)
        
    Stats = data["Stats"]
    
    return [Stats["CapturedPower"], Stats["StartRays"], Stats["CapturedRays"]]

def ExtractData(commonPath, specificPaths : list[str]):
    cols = []
    
    for path in specificPaths:
        cols.append(path + "_CapturedPower")
        cols.append(path + "_CapturedRays")
        cols.append(path + "_StartRays")
    
    dataframe = pd.DataFrame(columns=cols)
    
    for i in range(len(specificPaths)):
        
        path = specificPaths[i]
        
        fullDataPath = os.path.join(commonPath, "Data", path)
        
        files = [f for f in os.listdir(fullDataPath) if os.path.isfile(os.path.join(fullDataPath, f))]
        
        for j in range(len(files)):
            
            f = files[j]
            
            data = ExtractPowerAndRays(f, fullDataPath)
            
            dataframe.loc[j, f"{path}_CapturedPower"] = data[0]
            dataframe.loc[j, f"{path}_StartRays"] = data[1]
            dataframe.loc[j, f"{path}_CapturedRays"] = data[2]
        
    dataframe.to_csv(f"{commonPath}/InternalReflectionsWaves.csv", index=False)

def PlotInternalReflections(commonPath, specificPath):
    
    fullDataPath = os.path.join(commonPath, "Data", specificPath)
    fullPlotPath = os.path.join(commonPath, "Plots", specificPath)
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files = [f for f in os.listdir(fullDataPath) if os.path.isfile(os.path.join(fullDataPath, f))]

    power = []
    QDs = []

    plt.figure(figsize=(16, 10))
    
    cmap = plt.get_cmap('magma')

    for i in range(len(files)):
        
        file = files[i]

        power.append(GetPowerFromFile(file, fullDataPath)*100)
        QDs.append(i+1)

    plt.plot(QDs, power, color=cmap(0.5))
    plt.title(f"Solar Power Absorbed from QD Emission Unit Cell (From Source : {specificPath}) (Moth Eye Representation : Wave)")
    plt.xlabel("Number of Sources")
    plt.ylabel("Power (%)")
    plt.grid(True, alpha=0.6)
    plt.savefig(f"{fullPlotPath}/Power_Absorbed_{specificPath}_Wave.png")
    plt.close()
    
def PlotInternalReflectionsComparison(commonPath, specificPath1, specificPath2):
    
    fullDataPath1 = os.path.join(commonPath, "Data", specificPath1)
    fullDataPath2 = os.path.join(commonPath, "Data", specificPath2)
    fullPlotPath = os.path.join(commonPath, "Plots", "Comparison")
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files1 = [f for f in os.listdir(fullDataPath1) if os.path.isfile(os.path.join(fullDataPath1, f))]
    files2 = [f for f in os.listdir(fullDataPath2) if os.path.isfile(os.path.join(fullDataPath2, f))]

    power1 = []
    power2 = []
    QDs = []

    plt.figure(figsize=(16, 10))
    
    cmap = plt.get_cmap('magma')
    colors = [cmap(i / 2) for i in range(2)]

    for i in range(len(files1)):
        
        file1 = files1[i]
        file2 = files2[i]

        power1.append(GetPowerFromFile(file1, fullDataPath1)*100)
        power2.append(GetPowerFromFile(file2, fullDataPath2)*100)
        QDs.append(i+1)

    plt.plot(QDs, power1, label=specificPath1, color=colors[0])
    plt.plot(QDs, power2, label=specificPath2, color=colors[1])
    plt.title(f"TIR Power Absorbed from QD Emission using Moth Eye Sinusoidal Geometric Representation")
    plt.xlabel("Number of Sources")
    plt.ylabel("Reflected Power (%)")
    plt.grid(True, alpha=0.6)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(f"{fullPlotPath}/Comparison_Power_Absorbed_Wave.png")
    plt.close()

#ExtractData("Initial-Raytracing/InternalReflectionsWaves", ["Cone", "QD"])
#PlotInternalReflections("RaytracingResults/InternalReflectionsWaves", "Cone")
#PlotInternalReflections("RaytracingResults/InternalReflectionsWaves", "QD")
#PlotInternalReflectionsComparison("Initial-Raytracing/InternalReflectionsWaves", "QD", "Cone")