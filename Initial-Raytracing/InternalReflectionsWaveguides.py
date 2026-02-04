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
                
                dataframe.loc[j, "Layers"] = f.split("Waveguide")[1].split("Large")[0].split("UnitCell")[0]
                
                data = ExtractPowerAndRays(f, os.path.join(fullDataPath, fol))
                
                dataframe.loc[j, f"{path}_{fol}_CapturedPower"] = data[0]
                dataframe.loc[j, f"{path}_{fol}_CapturedRays"] = data[1]
                dataframe.loc[j, f"{path}_{fol}_StartRays"] = data[2]
        
    dataframe.to_csv(f"{commonPath}/InternalReflectionsWaveguide.csv", index=False)
    
def PlotInternalReflections(commonPath, specificPath):
    
    fullPlotPath = os.path.join(commonPath, "Plots", specificPath)
        
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    dataframe = pd.read_csv(f"{commonPath}/InternalReflectionsWaveguide.csv")
    
    QDNums = [f"QD{i}" for i in range(1, 16)]
    
    plt.figure(figsize=(16, 10))
    
    cmap = plt.get_cmap('magma')
    colors = [cmap(i / len(QDNums)) for i in range(len(QDNums))]
    
    for i in range(len(QDNums)):
        
        qd = QDNums[i]
        
        powerPercent = dataframe[f"{specificPath}_{qd}_CapturedPower"] / dataframe[f"{specificPath}_{qd}_StartRays"] * 100
        
        plt.plot(dataframe["Layers"], powerPercent, label=qd, color=colors[i])
        
    plt.title(f"Total Internal Reflection from QD Emission Unit Cell (From Source : {specificPath}) (Moth Eye Representation : Waveguide)")
    plt.xlabel("Number of Layers")
    plt.ylabel("Absorbed Power (%)")
    plt.grid()
    plt.legend()
    plt.savefig(f"{fullPlotPath}/Internal_Reflection_Power_Absorbed_{specificPath}_Waveguide.png")
    plt.close()

#paths = ["Cone_Large_Regular", "Cone_Large_MothEye", "Cone_UnitCell_Regular", "Cone_UnitCell_MothEye", "QD_Large_Regular", "QD_Large_MothEye", "QD_UnitCell_Regular", "QD_UnitCell_MothEye"]
#
#ExtractData("RaytracingResults/InternalReflections", ["Cone_Large_Regular", "Cone_Large_MothEye", "Cone_UnitCell_Regular", "Cone_UnitCell_MothEye", "QD_Large_Regular", "QD_Large_MothEye", "QD_UnitCell_Regular", "QD_UnitCell_MothEye"])
#
#for path in paths:
#    PlotInternalReflections("RaytracingResults/InternalReflections", path)
    