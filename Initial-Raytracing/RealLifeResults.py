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
                
                dataframe.loc[j, "Layers"] = f.split("Waveguide")[1].split("Angle")[0]
                
                data = ExtractPowerAndRays(f, os.path.join(fullDataPath, fol))
                
                dataframe.loc[j, f"{path}_{fol}_CapturedPower"] = data[0]
                dataframe.loc[j, f"{path}_{fol}_CapturedRays"] = data[1]
                dataframe.loc[j, f"{path}_{fol}_StartRays"] = data[2]
        
    dataframe.to_csv(f"{commonPath}/RealLifeResultsWaveguide.csv", index=False)

def PlotInternalReflections(commonPath, specificPath:str):
    
    fullPlotPath = os.path.join(commonPath, "Plots", specificPath)
        
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    dataframe = pd.read_csv(f"{commonPath}/RealLifeResultsWaveguide.csv")
    
    QDNums = [f"QD{i}" for i in range(0, 450, 50)]
    
    plt.figure(figsize=(16, 10))
    
    cmap = plt.get_cmap('magma')
    colors = [cmap(i / len(QDNums)) for i in range(len(QDNums))]
    
    for i in range(len(QDNums)):
        
        qd = QDNums[i]
        
        powerPercent = dataframe[f"{specificPath}_{qd}_CapturedPower"] / dataframe[f"{specificPath}_{qd}_StartRays"] * 100
        
        plt.plot(dataframe["Layers"], powerPercent, label=f"{qd.replace('QD', '')} QDs", color=colors[i])
        
    plt.title(f"Transmitted Power in a Real Life Scenario from a {specificPath.removeprefix('Angle')}° Incident Angle")
    plt.xlabel("Number of Layers")
    plt.ylabel("Absorbed Power (%)")
    plt.grid(True, alpha=0.6)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(f"{fullPlotPath}/Real_Life_Power_Absorbed_{specificPath}_Waveguide.png")
    plt.close()
    
def PlotPairedRealLifeResults(commonPath, pathLeft, pathRight):
    
    fullPlotPath = os.path.join(commonPath, "Plots", "CombinedAngles")
        
    if not os.path.exists(fullPlotPath):
        os.makedirs(fullPlotPath, exist_ok=True)
    
    dataframe = pd.read_csv(f"{commonPath}/RealLifeResultsWaveguide.csv")
    
    QDNums = [f"QD{i}" for i in range(0, 450, 50)]
    
    # Create a 1x2 subplot with a shared Y-axis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 10), sharey=True)
    
    cmap = plt.get_cmap('magma')
    colors = [cmap(i / len(QDNums)) for i in range(len(QDNums))]
    
    # Loop over both axes and their target paths
    for ax, specificPath in zip([ax1, ax2], [pathLeft, pathRight]):
        
        for i in range(len(QDNums)):
            qd = QDNums[i]
            powerPercent = dataframe[f"{specificPath}_{qd}_CapturedPower"] / dataframe[f"{specificPath}_{qd}_StartRays"] * 100
            
            ax.plot(dataframe["Layers"], powerPercent, label=f"{qd.replace('QD', '')} QDs", color=colors[i])
            
        angle = specificPath.removeprefix('Angle')
        ax.set_title(f"Transmitted Power from a {angle}° Incident Angle")
        ax.set_xlabel("Number of Layers")
        ax.grid(True, alpha=0.6)
        
        # Only set the Y-axis label on the left graph
        if ax == ax1:
            ax.set_ylabel("Absorbed Power (%)")

    # Add the legend outside the rightmost graph
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    # Optional: Add a master title for the whole figure
    fig.suptitle("Real Life Scenario: Transmitted Power vs Layers", y=1.05)
    
    plt.tight_layout()
    plt.savefig(f"{fullPlotPath}/Real_Life_Power_Absorbed_Combined_Waveguide.png", bbox_inches='tight')
    plt.close()

#ExtractData("Initial-Raytracing/RealLifeResults", ["Angle0", "Angle26"])
#PlotInternalReflections("Initial-Raytracing/RealLifeResults", "Angle0")
#PlotInternalReflections("Initial-Raytracing/RealLifeResults", "Angle26")
PlotPairedRealLifeResults("Initial-Raytracing/RealLifeResults", "Angle0", "Angle26")