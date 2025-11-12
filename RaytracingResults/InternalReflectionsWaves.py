import os
import re 
import matplotlib.pyplot as plt
import json

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


def PlotInternalReflections(commonPath, specificPath):
    
    fullDataPath = os.path.join(commonPath, "Data", specificPath)
    fullPlotPath = os.path.join(commonPath, "Plots", specificPath)
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files = [f for f in os.listdir(fullDataPath) if os.path.isfile(os.path.join(fullDataPath, f))]

    power = []
    QDs = []

    plt.figure(figsize=(16, 10))

    for i in range(len(files)):
        
        file = files[i]

        power.append(GetPowerFromFile(file, fullDataPath)*100)
        QDs.append(i+1)

    plt.plot(QDs, power)
    plt.title(f"Solar Power Absorbed from QD Emission Unit Cell (From Source : {specificPath}) (Moth Eye Representation : Wave)")
    plt.xlabel("Number of Sources")
    plt.ylabel("Power (%)")
    plt.grid()
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

    for i in range(len(files1)):
        
        file1 = files1[i]
        file2 = files2[i]

        power1.append(GetPowerFromFile(file1, fullDataPath1)*100)
        power2.append(GetPowerFromFile(file2, fullDataPath2)*100)
        QDs.append(i+1)

    plt.plot(QDs, power1, label=specificPath1)
    plt.plot(QDs, power2, label=specificPath2)
    plt.title(f"Comparison of Solar Power Absorbed from QD Emission Unit Cell (Moth Eye Representation : Wave)")
    plt.xlabel("Number of Sources")
    plt.ylabel("Power (%)")
    plt.grid()
    plt.legend()
    plt.savefig(f"{fullPlotPath}/Comparison_Power_Absorbed_Wave.png")
    plt.close()

PlotInternalReflections("RaytracingResults/InternalReflectionsWaves", "Cone")
PlotInternalReflections("RaytracingResults/InternalReflectionsWaves", "QD")
PlotInternalReflectionsComparison("RaytracingResults/InternalReflectionsWaves", "QD", "Cone")