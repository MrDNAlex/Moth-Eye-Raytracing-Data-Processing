import os 
import matplotlib.pyplot as plt
import numpy as np
import json

files = [f for f in os.listdir('MaxCaptureAngle/Data') if os.path.isfile(os.path.join('MaxCaptureAngle/Data', f))]



for file in files:
    with open(os.path.join('MaxCaptureAngle/Data', file), "r") as f:
            data = json.load(f)

    power = data["Power"]
    angles = data["Angle"]
    
    plt.figure(figsize=(16, 10))

    plt.plot(angles, power)
    plt.title(f"Power vs Angle for {file.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json")} Linear Waveguide Layers")
    plt.xlabel("Angle (degrees)")
    plt.ylabel("Power (W)")
    plt.grid()
    plt.savefig(f"MaxCaptureAngle/Plots/Power_vs_Angle_{file.removeprefix("MaxCaptureAngleWaveguide").removesuffix(".json")}_Waveguide_Layers.png")