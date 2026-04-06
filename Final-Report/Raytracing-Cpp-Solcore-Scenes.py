import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams.update({
    'figure.dpi': 300,
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'legend.fontsize': 11,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'grid.alpha': 0.6,
    'axes.edgecolor': '#2c3e50',
    'axes.labelcolor': '#2c3e50',
    'xtick.color': '#2c3e50',
    'ytick.color': '#2c3e50'
})

def SetupDirectory():
    try:
        basePath = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        basePath = os.getcwd()
        
    plotsDir = os.path.join(basePath, "Plots")
    if not os.path.exists(plotsDir):
        os.makedirs(plotsDir)
        
    return plotsDir

def DrawBaseUnitCell(ax, sx=-125, ex=125, ty=-500):
    ax.plot([sx, ex], [ty, ty], color='crimson', lw=5, label='Target')
    ax.plot([sx, sx], [500, ty], color='slategray', lw=2, label='Mirrors')
    ax.plot([ex, ex], [500, ty], color='slategray', lw=2)

def DrawInternalUnitCell(ax, sx=-125, ex=125, ty=500):
    ax.plot([sx, ex], [ty, ty], color='crimson', lw=5, label='Target')
    ax.plot([sx, sx], [ty, -1000], color='slategray', lw=2, label='Mirrors')
    ax.plot([ex, ex], [ty, -1000], color='slategray', lw=2)

def DrawPerturbedNormals(ax, yLevels, sx=-125, ex=125, dev=15, A=0, B=0):
    sampleX = np.linspace(sx + 25, ex - 25, 5)
    first = True
    for yBase in yLevels:
        for x in sampleX:
            if A != 0:
                slope = A * B * np.cos(B * x)
                baseAngle = np.arctan(-1/slope) if slope != 0 else np.pi/2
                if baseAngle < 0: 
                    baseAngle += np.pi
                yPos = A * np.sin(B * x) + yBase
            else:
                baseAngle = np.pi/2
                yPos = yBase

            angle = baseAngle + np.deg2rad(np.random.normal(0, dev))
            nx, ny = np.cos(angle), np.sin(angle)
            
            ax.quiver(x, yPos, nx, ny, color='royalblue', alpha=0.4, 
                      scale=20, width=0.005, headwidth=3, 
                      label='Perturbed Surface Normals' if first else "")
            first = False

def PlotSim1():
    fig, ax = plt.subplots(figsize=(10, 8))
    DrawBaseUnitCell(ax)
    
    for i, y in enumerate(np.linspace(250, 0, 3)):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (3)' if i==0 else "")
        
    ax.quiver(100, 400, -0.7, -0.7, color='orange', scale=5, label='Ray Source (0 - 60°) \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep (Transmittance) - Simulation 1")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(SetupDirectory(), "Sim-1-Wavelength-Sweep.png"), bbox_inches='tight')
    plt.close()

def PlotSim2():
    fig, ax = plt.subplots(figsize=(10, 8))
    DrawBaseUnitCell(ax)
    
    yLevels = np.linspace(250, 0, 3)
    for i, y in enumerate(yLevels):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (3)' if i==0 else "")
        
    DrawPerturbedNormals(ax, yLevels, dev=12)
    ax.quiver(100, 400, -0.7, -0.7, color='orange', scale=5, label='Ray Source (0 - 60°) \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep with Perturbance (Transmittance) - Simulation 2")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(SetupDirectory(), "Sim-2-Perturbance-Sweep.png"), bbox_inches='tight')
    plt.close()

def PlotSim3():
    fig, ax = plt.subplots(figsize=(10, 8))
    DrawBaseUnitCell(ax)
    
    yLevels = np.linspace(250, 0, 3)
    xw = np.linspace(-125, 125, 200)
    A, B = 10, (2 * np.pi / 100)
    
    for i, y in enumerate(yLevels):
        yw = A * np.sin(B * xw) + y
        ax.plot(xw, yw, color='royalblue', alpha=0.3, lw=1, label='Waveguide Layers (3)' if i==0 else "")
    
    DrawPerturbedNormals(ax, yLevels, dev=12, A=A, B=B)
    
    ax.quiver(100, 400, -0.7, -0.7, color='orange', scale=5, label='Ray Source (0 - 60°) \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep with Wavy Layers (Transmittance) - Simulation 3")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(SetupDirectory(), "Sim-3-Wavy-Sweep.png"), bbox_inches='tight')
    plt.close()

def PlotSim4():
    fig, ax = plt.subplots(figsize=(10, 8))
    DrawInternalUnitCell(ax)
    
    for i, y in enumerate(np.linspace(250, 0, 10)):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (40)' if i==0 else "")
    
    ax.fill([0, -125, 125, 0], [-400, 0, 0, -400], color='magenta', alpha=0.3, label='ConeLight Emission')
    ax.scatter(0, -400, color='magenta', s=150, zorder=10, label='Cone Source \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep (TIR) - Simulation 4")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(SetupDirectory(), "Sim-4-Internal-Sweep.png"), bbox_inches='tight')
    plt.close()

def PlotSim5():
    fig, ax = plt.subplots(figsize=(10, 8))
    DrawInternalUnitCell(ax)
    
    yLevels = np.linspace(250, 0, 10)
    for i, y in enumerate(yLevels):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (40)' if i==0 else "")
        
    DrawPerturbedNormals(ax, yLevels, dev=12)
    
    ax.fill([0, -125, 125, 0], [-400, 0, 0, -400], color='magenta', alpha=0.3, label='ConeLight Emission')
    ax.scatter(0, -400, color='magenta', s=150, zorder=10, label='Cone Source \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep with Perturbance (TIR) - Simulation 5")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(SetupDirectory(), "Sim-5-Internal-Perturbance.png"), bbox_inches='tight')
    plt.close()

def PlotSim6():
    fig, ax = plt.subplots(figsize=(10, 8))
    DrawInternalUnitCell(ax)
    
    yLevels = np.linspace(250, 0, 10)
    xw = np.linspace(-125, 125, 200)
    A, B = 8, (2 * np.pi / 80)
    
    for i, y in enumerate(yLevels):
        yw = A * np.sin(B * xw) + y
        ax.plot(xw, yw, color='royalblue', alpha=0.3, label='Waveguide Layers (40)' if i==0 else "")
    
    DrawPerturbedNormals(ax, yLevels, dev=12, A=A, B=B)
    
    ax.fill([0, -125, 125, 0], [-400, 0, 0, -400], color='magenta', alpha=0.3, label='ConeLight Emission')
    ax.scatter(0, -400, color='magenta', s=150, zorder=10, label='Cone Source \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep with Wavy Layers (TIR) - Simulation 6")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(SetupDirectory(), "Sim-6-Internal-Wavy.png"), bbox_inches='tight')
    plt.close()

def PlotSim7():
    fig, ax = plt.subplots(figsize=(10, 8))
    DrawBaseUnitCell(ax)
    
    ax.plot([-125, 125], [250, 250], color='royalblue', lw=4, label='Waveguide Layer (1)')
    ax.quiver(100, 400, -0.7, -0.7, color='orange', scale=5, label='Ray Source (0 - 60°) \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep Control (Transmittance) - Simulation 7")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(SetupDirectory(), "Sim-7-Single-Layer.png"), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating Simulation Configurations 1-7...")
    PlotSim1()
    PlotSim2()
    PlotSim3()
    PlotSim4()
    PlotSim5()
    PlotSim6()
    PlotSim7()
    print(f"Success! All 7 scenes saved to: {SetupDirectory()}")