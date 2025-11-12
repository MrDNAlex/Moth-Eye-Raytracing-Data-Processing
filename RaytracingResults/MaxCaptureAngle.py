import os
import re 
import matplotlib.pyplot as plt
import json
import pandas as pd

def ExtractPowerAndAngles(file, fullPath):
    with open(os.path.join(fullPath, file), "r") as f:
        data = json.load(f)
    
    print(data)
    
    Stats = data["Stats"]
    
    return [Stats["CapturedPower"], Stats["StartRays"], Stats["CapturedRays"]]


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
    
def PlotMaxCaptureAngle(commonPath, specificPath):
    
    fullDataPath = os.path.join(commonPath, "Data", specificPath)
    fullPlotPath = os.path.join(commonPath, "Plots", specificPath)
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files = [f for f in os.listdir(fullDataPath) if os.path.isfile(os.path.join(fullDataPath, f))]

    for file in files:
        
        with open(os.path.join(fullDataPath, file), "r") as f:
                data = json.load(f)

        power = data["Power"]
        angles = data["Angle"]
        
        plt.figure(figsize=(16, 10))

        plt.plot(angles, power)
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

        power1 = data1["Power"] * 100
        angles1 = data1["Angle"]
        
        power2 = data2["Power"] * 100
        angles2 = data2["Angle"]
        
        plt.figure(figsize=(16, 10))

        plt.plot(angles1, power1, label=specificPath1)
        plt.plot(angles2, power2, label=specificPath2)
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

    for i in range(0, len(files1), 4):
        
        file1 = files1[i]
        file2 = files2[i]
        
        print(file1)
        
        with open(os.path.join(fullDataPath1, file1), "r") as f:
                data1 = json.load(f)
                
        with open(os.path.join(fullDataPath2, file2), "r") as f:
                data2 = json.load(f)

        power1 = data1["Power"] * 100
        angles1 = data1["Angle"]
        
        power2 = data2["Power"] * 100
        angles2 = data2["Angle"]
        
        plt.plot(angles1, power1, label=specificPath1 + file1.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json").replace("_", " "))
        plt.plot(angles2, power2, label=specificPath2 + file1.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json").replace("_", " "))
        
    plt.title(f"Comparison of Power vs Angle for Linear Waveguide Layers")
    plt.xlabel("Angle (degrees)")
    plt.ylabel("Power (%)")
    plt.grid()
    plt.legend()
    plt.savefig(f"{fullPlotPath}/Full_Comparison_Power_vs_Angle_Waveguide_Layers.png")
    plt.close()

ExtractData("RaytracingResults/MaxCaptureAngle", ["MothEye", "Regular"])