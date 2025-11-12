import os
import re 
import matplotlib.pyplot as plt
import json

def GetPowerFromFile(file, fullPath):
    
    with open(os.path.join(fullPath, file), "r") as f:
        data = json.load(f)
        
    Stats = data["Stats"]
    return Stats["CapturedPower"] / Stats["StartRays"]

def ExtractData(commonPath, specificPaths : list[str]):
    cols = []
    
    for path in specificPaths:
        cols.append(path + "_CapturedPower")
        cols.append(path + "_CapturedRays")
        cols.append(path + "_StartRays")
    
    dataframe = pd.DataFrame(columns=cols)
    
    print(dataframe)
    
    for i in range(len(specificPaths)):
        
        path = specificPaths[i]
        
        fullDataPath = os.path.join(commonPath, "Data", path)
        
        print(fullDataPath)
        
        files = [f for f in os.listdir(fullDataPath) if os.path.isfile(os.path.join(fullDataPath, f))]
        
        for j in range(len(files)):
            
            f = files[j]
            
            data = ExtractPowerAndRays(f, fullDataPath)
            
            dataframe.loc[j, f"{path}_CapturedPower"] = data[0]
            dataframe.loc[j, f"{path}_CapturedRays"] = data[1]
            dataframe.loc[j, f"{path}_StartRays"] = data[2]
        
    print(dataframe)
    
    dataframe.to_csv("Test.csv")
    
    #PlotMaxCaptureAngle("RaytracingResults/MaxCaptureAngle", "MothEye")
    #PlotMaxCaptureAngle("RaytracingResults/MaxCaptureAngle", "Regular")


def PlotInternalReflections(commonPath, specificPath):
    
    fullDataPath = os.path.join(commonPath, "Data", specificPath)
    fullPlotPath = os.path.join(commonPath, "Plots", specificPath)
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
        
    plt.figure(figsize=(16, 10))    
    
    QDFolders = [f for f in os.listdir(fullDataPath) if os.path.isdir(os.path.join(fullDataPath, f))]
    
    for j in range(QDFolders):
        QDFolder = QDFolders[j]
        
        files = [f for f in os.listdir(os.path.join(fullDataPath, QDFolder)) if os.path.isfile(os.path.join(fullDataPath, QDFolder, f))]

        power = []
        QDs = []

        for i in range(len(files)):
            
            file = files[i]

            power.append(GetPowerFromFile(file, os.path.join(fullDataPath, QDFolder))*100)
            QDs.append(i+1)

        plt.plot(QDs, power)
    plt.title(f"Solar Power Absorbed from QD Emission Unit Cell (From Source : {specificPath}) (Moth Eye Representation : Waveguide)")
    plt.xlabel("Number of Sources")
    plt.ylabel("Power (%)")
    plt.grid()
    plt.savefig(f"{fullPlotPath}/Power_Absorbed_{specificPath}_Wave.png")
    plt.close()
    
    
    
    