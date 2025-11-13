import os
import re 
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np

def ExtractPowerAndAngles(file, fullPath):
    with open(os.path.join(fullPath, file), "r") as f:
        data = json.load(f)
    
    return [data["Angle"], data["Power"]]


def ExtractData(commonPath, specificPaths : list[str]):
    dataframe = pd.DataFrame()
    
    for i in range(len(specificPaths)):
        
        path = specificPaths[i]
        
        fullDataPath = os.path.join(commonPath, "Data", path)
        
        files = [f for f in os.listdir(fullDataPath) if os.path.isfile(os.path.join(fullDataPath, f))]
        
        for j in range(len(files)):
            
            f = files[j]
            
            data = ExtractPowerAndAngles(f, fullDataPath)
            
            colName = f.removeprefix("MaxCaptureAngle").removesuffix(".json")
            
            dataframe[f"{colName}_Angle"] = data[0]
            dataframe[f"{colName}_Power"] = data[1]
        
    dataframe.to_csv(f"{commonPath}/MaxCaptureAngle.csv", index=False)
    
def PlotMaxCaptureAngle(commonPath, specificPath):
    
    fullDataPath = os.path.join(commonPath, "Data", specificPath)
    fullPlotPath = os.path.join(commonPath, "Plots", specificPath)
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files = [f for f in os.listdir(fullDataPath) if os.path.isfile(os.path.join(fullDataPath, f))]

    for file in files:
        
        with open(os.path.join(fullDataPath, file), "r") as f:
                data = json.load(f)

        power = np.array(data["Power"]) * 100
        angles = np.array(data["Angle"])
        
        plt.figure(figsize=(16, 10))
        
        cmap = plt.get_cmap('magma')

        plt.plot(angles, power, color=cmap(0.5))
        plt.title(f"Power vs Angle for {file.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json").replace("_", " ")} Linear Waveguide Layers")
        plt.xlabel("Angle (degrees)")
        plt.ylabel("Power (%)")
        plt.grid()
        plt.savefig(f"{fullPlotPath}/Power_vs_Angle_{file.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json")}_Waveguide_Layers.png")
        plt.close()

def PlotMaxCaptureAngleComparison(commonPath, specificPath1, specificPath2):
    
    fullDataPath1 = os.path.join(commonPath, "Data", specificPath1)
    fullDataPath2 = os.path.join(commonPath, "Data", specificPath1)
    fullPlotPath = os.path.join(commonPath, "Plots", "Comparison")
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files1 = [f for f in os.listdir(fullDataPath1) if os.path.isfile(os.path.join(fullDataPath1, f))]
    files2 = [f for f in os.listdir(fullDataPath1) if os.path.isfile(os.path.join(fullDataPath1, f))]

    for i in range(len(files1)):
        
        file1 = files1[i]
        file2 = files2[i]
        
        with open(os.path.join(fullDataPath1, file1), "r") as f:
                data1 = json.load(f)
                
        with open(os.path.join(fullDataPath2, file2), "r") as f:
                data2 = json.load(f)

        power1 = np.array(data1["Power"]) * 100
        angles1 = np.array(data1["Angle"])
        
        power2 = np.array(data2["Power"]) * 100
        angles2 = np.array(data2["Angle"])
        
        plt.figure(figsize=(16, 10))
        
        cmap = plt.get_cmap('magma')

        plt.plot(angles1, power1, label=specificPath1, color=cmap(0))
        plt.plot(angles2, power2, label=specificPath2, color=cmap(1))
        plt.title(f"Comparison of Power vs Angle for {file1.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json").replace("_", " ")} Linear Waveguide Layers")
        plt.xlabel("Angle (degrees)")
        plt.ylabel("Power (%)")
        plt.grid()
        plt.legend()
        plt.savefig(f"{fullPlotPath}/Comparison_Power_vs_Angle_{file1.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json")}_Waveguide_Layers.png")
        plt.close()
        
def PlotMaxCaptureAngleFullComparison(commonPath, specificPath1, specificPath2):
    
    fullDataPath1 = os.path.join(commonPath, "Data", specificPath1)
    fullDataPath2 = os.path.join(commonPath, "Data", specificPath1)
    fullPlotPath = os.path.join(commonPath, "Plots", "FullComparison")
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files1 = [f for f in os.listdir(fullDataPath1) if os.path.isfile(os.path.join(fullDataPath1, f))]
    files2 = [f for f in os.listdir(fullDataPath1) if os.path.isfile(os.path.join(fullDataPath1, f))]

    def extract_number(filename):
        match = re.search(r"Waveguide(\d+)", filename)
        return int(match.group(1)) if match else -1
    
    # Sort numerically by waveguide number
    files1 = sorted(
        [f for f in os.listdir(fullDataPath1) if f.endswith(".json")],
        key=extract_number
    )
    files2 = sorted(
        [f for f in os.listdir(fullDataPath2) if f.endswith(".json")],
        key=extract_number
    )

    plt.figure(figsize=(16, 10))
    
    cmap = plt.get_cmap('magma')
    colors = [cmap(i / ((len(files1)))) for i in range(0, len(files1))]

    for i in range(0, len(files1), 4):
        
        file1 = files1[i]
        file2 = files2[i]
        
        with open(os.path.join(fullDataPath1, file1), "r") as f:
                data1 = json.load(f)
                
        with open(os.path.join(fullDataPath2, file2), "r") as f:
                data2 = json.load(f)

        power1 = np.array(data1["Power"]) * 100
        angles1 = np.array(data1["Angle"])
        
        power2 = np.array(data2["Power"]) * 100
        angles2 = np.array(data2["Angle"])
        
        plt.plot(angles1, power1, color=colors[i], label=specificPath1 + file1.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json").replace("_", " "))
        plt.plot(angles2, power2, color=colors[i], label=specificPath2 + file2.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json").replace("_", " "))
        
    plt.title(f"Comparison of Power vs Angle for Linear Waveguide Layers")
    plt.xlabel("Angle (degrees)")
    plt.ylabel("Power (%)")
    plt.grid()
    plt.legend()
    plt.savefig(f"{fullPlotPath}/Full_Comparison_Power_vs_Angle_Waveguide_Layers.png")
    plt.close()
    
#ExtractData("RaytracingResults/MaxCaptureAngle", ["MothEye", "Regular"])
#PlotMaxCaptureAngle("RaytracingResults/MaxCaptureAngle", "MothEye")
#PlotMaxCaptureAngle("RaytracingResults/MaxCaptureAngle", "Regular")
#PlotMaxCaptureAngleComparison("RaytracingResults/MaxCaptureAngle", "MothEye", "Regular")
PlotMaxCaptureAngleFullComparison("RaytracingResults/MaxCaptureAngle", "MothEye", "Regular")