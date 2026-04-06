import os
import re 
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np

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
        plt.title(f"Power vs Angle for {file.removeprefix('MaxCaptureAngleWaveguide').removesuffix('.json').replace('_', ' ')} Linear Waveguide Layers")
        plt.xlabel("Angle (degrees)")
        plt.ylabel("Power (%)")
        plt.grid()
        plt.savefig(f"{fullPlotPath}/Power_vs_Angle_{file.removeprefix('MaxCaptureAngleWaveguide').removesuffix('.json')}_Waveguide_Layers.png")
        plt.close()

def PlotMaxCaptureAngleComparison(commonPath, specificPath1, specificPath2):
    
    fullDataPath1 = os.path.join(commonPath, "Data", specificPath1)
    fullDataPath2 = os.path.join(commonPath, "Data", specificPath2)
    fullPlotPath = os.path.join(commonPath, "Plots", "Comparison")
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files1 = [f for f in os.listdir(fullDataPath1) if os.path.isfile(os.path.join(fullDataPath1, f))]
    files2 = [f for f in os.listdir(fullDataPath2) if os.path.isfile(os.path.join(fullDataPath2, f))]

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
        plt.title(f"Comparison of Captured Power vs Incident Angle for {file1.removeprefix('MaxCaptureAngleWaveguide').removesuffix('.json').replace('_', ' ')} Linear Waveguide Layers")
        plt.xlabel("Angle (degrees)")
        plt.ylabel("Power (%)")
        plt.grid()
        plt.legend()
        plt.savefig(f"{fullPlotPath}/Comparison_Power_vs_Angle_{file1.removeprefix('MaxCaptureAngleWaveguide').removesuffix('.json')}_Waveguide_Layers.png")
        plt.close()
        
def PlotMaxCaptureAngleFullComparison(commonPath, specificPath1, specificPath2):
    
    fullDataPath1 = os.path.join(commonPath, "Data", specificPath1)
    fullDataPath2 = os.path.join(commonPath, "Data", specificPath2)
    fullPlotPath = os.path.join(commonPath, "Plots", "FullComparison")
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files1 = [f for f in os.listdir(fullDataPath1) if os.path.isfile(os.path.join(fullDataPath1, f))]
    files2 = [f for f in os.listdir(fullDataPath2) if os.path.isfile(os.path.join(fullDataPath2, f))]

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
        
        plt.plot(angles1, power1, color=colors[i], label="Approximated GRIN" + " (" + file1.removeprefix("MaxCaptureAngleWaveguide").split("_")[0] + " Layers)")
        plt.plot(angles2, power2, color=colors[i], label="Linear GRIN" + " (" + file2.removeprefix("MaxCaptureAngleWaveguide").split("_")[0] + " Layers)")
        
    plt.title(f"Transmitted Power at various Incident Angles for a\n Waveguide interpretation of a Moth Eye AR Layer")
    plt.xlabel("Incident Angle (°)")
    plt.ylabel("Transmitted Power (%)")
    plt.grid(True, alpha=0.6)
    
    # --- Legend Grouping Logic ---
    handles, labels = plt.gca().get_legend_handles_labels()
    
    approx_handles = [h for h, l in zip(handles, labels) if "Approximated" in l]
    approx_labels = [l for h, l in zip(handles, labels) if "Approximated" in l]
    
    linear_handles = [h for h, l in zip(handles, labels) if "Linear" in l]
    linear_labels = [l for h, l in zip(handles, labels) if "Linear" in l]
    
    sorted_handles = approx_handles + linear_handles
    sorted_labels = approx_labels + linear_labels
    
    plt.legend(sorted_handles, sorted_labels, loc='center left', bbox_to_anchor=(1.02, 0.5))
    
    plt.tight_layout()
    plt.savefig(f"{fullPlotPath}/Full_Comparison_Power_vs_Angle_Waveguide_Layers.png")
    plt.close()
    
def PlotMaxCaptureAngleFullComparisonLinear(commonPath, specificPath1, specificPath2):
    
    fullDataPath1 = os.path.join(commonPath, "Data", specificPath1)
    fullDataPath2 = os.path.join(commonPath, "Data", specificPath2)
    fullPlotPath = os.path.join(commonPath, "Plots", "FullComparison")
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files2 = [f for f in os.listdir(fullDataPath1) if os.path.isfile(os.path.join(fullDataPath1, f))]

    def extract_number(filename):
        match = re.search(r"Waveguide(\d+)", filename)
        return int(match.group(1)) if match else -1
    
    # Sort numerically by waveguide number
    files2 = sorted(
        [f for f in os.listdir(fullDataPath2) if f.endswith(".json")],
        key=extract_number
    )

    plt.figure(figsize=(16, 10))
    
    cmap = plt.get_cmap('magma')
    colors = [cmap(i / ((len(files2)))) for i in range(0, len(files2))]

    for i in range(0, len(files2), 4):
        file2 = files2[i]
        
        with open(os.path.join(fullDataPath2, file2), "r") as f:
                data2 = json.load(f)

        power2 = np.array(data2["Power"]) * 100
        angles2 = np.array(data2["Angle"])
        
        plt.plot(angles2, power2, color=colors[i], label="Linear GRIN" + " (" + file2.removeprefix("MaxCaptureAngleWaveguide").split("_")[0] + " Layers)")
        
    plt.title(f"Transmitted Power at various Incident Angles for a\nWaveguide interpretation of a Moth Eye AR Layer")
    plt.xlabel("Incident Angle (degrees)")
    plt.ylabel("Transmitted Power (%)")
    plt.grid(True, alpha=0.6)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(f"{fullPlotPath}/Full_Comparison_Power_vs_Angle_Waveguide_Layers_Linear.png")
    plt.close()

def PlotMaxCaptureAngleFullComparisonApproximated(commonPath, specificPath1, specificPath2):
    
    fullDataPath1 = os.path.join(commonPath, "Data", specificPath1)
    fullPlotPath = os.path.join(commonPath, "Plots", "FullComparison")
    
    if not os.path.exists(fullPlotPath):
        os.mkdir(fullPlotPath)
    
    files1 = [f for f in os.listdir(fullDataPath1) if os.path.isfile(os.path.join(fullDataPath1, f))]

    def extract_number(filename):
        match = re.search(r"Waveguide(\d+)", filename)
        return int(match.group(1)) if match else -1
    
    # Sort numerically by waveguide number
    files1 = sorted(
        [f for f in os.listdir(fullDataPath1) if f.endswith(".json")],
        key=extract_number
    )

    plt.figure(figsize=(16, 10))
    
    cmap = plt.get_cmap('magma')
    colors = [cmap(i / ((len(files1)))) for i in range(0, len(files1))]

    for i in range(0, len(files1), 4):
        
        file1 = files1[i]
        
        with open(os.path.join(fullDataPath1, file1), "r") as f:
                data1 = json.load(f)
                
        power1 = np.array(data1["Power"]) * 100
        angles1 = np.array(data1["Angle"])
        
        plt.plot(angles1, power1, color=colors[i], label="Approximated GRIN" + " (" + file1.removeprefix("MaxCaptureAngleWaveguide").split("_")[0] + " Layers)")
        
    plt.title(f"Transmitted Power at various Incident Angles for a\nWaveguide interpretation of a Moth Eye AR Layer")
    plt.xlabel("Incident Angle (degrees)")
    plt.ylabel("Transmitted Power (%)")
    plt.grid(True, alpha=0.6)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(f"{fullPlotPath}/Full_Comparison_Power_vs_Angle_Waveguide_Layers_Approximated.png")
    plt.close()

def PlotSideBySideIsolated(commonPath, pathApprox, pathLinear):
    
    fullDataPathApprox = os.path.join(commonPath, "Data", pathApprox)
    fullDataPathLinear = os.path.join(commonPath, "Data", pathLinear)
    fullPlotPath = os.path.join(commonPath, "Plots", "FullComparison")
    
    os.makedirs(fullPlotPath, exist_ok=True)
    
    def extract_number(filename):
        match = re.search(r"Waveguide(\d+)", filename)
        return int(match.group(1)) if match else -1
    
    filesApprox = sorted(
        [f for f in os.listdir(fullDataPathApprox) if f.endswith(".json")],
        key=extract_number
    )
    
    filesLinear = sorted(
        [f for f in os.listdir(fullDataPathLinear) if f.endswith(".json")],
        key=extract_number
    )

    # Added sharey=True here to link the y-axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 10), sharey=True)
    cmap = plt.get_cmap('magma')
    
    max_files = max(len(filesApprox), len(filesLinear))
    colors = [cmap(i / max_files) for i in range(max_files)]

    # Plot Approximated Data (Left)
    for i in range(0, len(filesApprox), 4):
        file = filesApprox[i]
        
        with open(os.path.join(fullDataPathApprox, file), "r") as f:
            data = json.load(f)
                
        power = np.array(data["Power"]) * 100
        angles = np.array(data["Angle"])
        layers = file.removeprefix("MaxCaptureAngleWaveguide").split("_")[0]
        
        ax1.plot(angles, power, color=colors[i], label=f"Approximated GRIN ({layers} Layers)")
        
    ax1.set_title("Transmitted Power through a Empirically Approximated GRIN\nMoth Eye AR Layer using various discretizations")
    ax1.set_xlabel("Incident Angle (degrees)")
    ax1.set_ylabel("Transmitted Power (%)")
    ax1.grid(True, alpha=0.6)
    ax1.legend(loc='best')

    # Plot Linear Data (Right)
    for i in range(0, len(filesLinear), 4):
        file = filesLinear[i]
        
        with open(os.path.join(fullDataPathLinear, file), "r") as f:
            data = json.load(f)

        power = np.array(data["Power"]) * 100
        angles = np.array(data["Angle"])
        layers = file.removeprefix("MaxCaptureAngleWaveguide").split("_")[0]
        
        ax2.plot(angles, power, color=colors[i], label=f"Linear GRIN ({layers.split('.')[0]} Layers)")
        
    ax2.set_title("Transmitted Power through a Linear GRIN\nMoth Eye AR Layer using various discretizations")
    ax2.set_xlabel("Incident Angle (degrees)")
    # Removed ax2.set_ylabel so it doesn't clutter the shared axis
    ax2.grid(True, alpha=0.6)
    ax2.legend(loc='best')
    
    plt.tight_layout()
    plt.savefig(f"{fullPlotPath}/Side_By_Side_Isolated_Power_vs_Angle.png", bbox_inches='tight')
    plt.close()
#ExtractData("Initial-Raytracing/MaxCaptureAngle", ["MothEye", "Regular"])
#PlotMaxCaptureAngle("Initial-Raytracing/MaxCaptureAngle", "MothEye")
#PlotMaxCaptureAngle("Initial-Raytracing/MaxCaptureAngle", "Regular")
#PlotMaxCaptureAngleComparison("Initial-Raytracing/MaxCaptureAngle", "MothEye", "Regular")
#PlotMaxCaptureAngleFullComparison("Initial-Raytracing/MaxCaptureAngle", "MothEye", "Regular")
#PlotMaxCaptureAngleFullComparisonLinear("Initial-Raytracing/MaxCaptureAngle", "MothEye", "Regular")
#PlotMaxCaptureAngleFullComparisonApproximated("Initial-Raytracing/MaxCaptureAngle", "MothEye", "Regular")
PlotSideBySideIsolated("Initial-Raytracing/MaxCaptureAngle", "MothEye", "Regular")