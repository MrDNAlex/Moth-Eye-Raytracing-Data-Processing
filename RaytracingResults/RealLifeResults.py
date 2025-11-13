import os
import re 
import matplotlib.pyplot as plt
import json
import pandas as pd

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
        
        plt.plot(dataframe["Layers"], powerPercent, label=qd, color=colors[i])
        
    plt.title(f"Absorbtion of Power in a Real Life Scenario (From Angle : {specificPath.removeprefix("Angle")}) (Moth Eye Representation : Waveguide)")
    plt.xlabel("Number of Layers")
    plt.ylabel("Absorbed Power (%)")
    plt.grid()
    plt.legend()
    plt.savefig(f"{fullPlotPath}/Real_Life_Power_Absorbed_{specificPath}_Waveguide.png")
    plt.close()

#ExtractData("RaytracingResults/RealLifeResults", ["Angle0", "Angle26"])
#PlotInternalReflections("RaytracingResults/RealLifeResults", "Angle0")
#PlotInternalReflections("RaytracingResults/RealLifeResults", "Angle26")