import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams.update({
    'figure.dpi': 300,
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 20,
    'legend.fontsize': 12,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'grid.alpha': 0.6,
    'axes.edgecolor': '#2c3e50',
    'axes.labelcolor': '#2c3e50',
    'xtick.color': '#2c3e50',
    'ytick.color': '#2c3e50'
})

def SetupDirectory():
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    plotsDir = os.path.join(scriptDir, "Plots")
    if not os.path.exists(plotsDir):
        os.makedirs(plotsDir)
        
    return plotsDir

def PlotScene1PointSource():
    fig, ax = plt.subplots(figsize=(10, 10))
    plotsDir = SetupDirectory()

    mirrorColor = '#546e7a'
    targetColor = '#e91e63'
    
    ax.plot([-10, 10, 10, -10, -10], [10, 10, -10, -10, 10], 
            color=mirrorColor, lw=2.5, label='Mirror Boundary', zorder=2)
    
    ax.plot([-10, 10], [-10, -10], color=targetColor, lw=5, label='Target Surface', zorder=3)

    waveColor = '#5c6bc0'
    waveYLevels = [-5, -5.5, -6, -6.5]
    for i, y in enumerate(waveYLevels):
        ax.hlines(y, -10, 10, colors=waveColor, linestyles='--', lw=2, alpha=0.6,
                  label='Waveguide Segments' if i == 0 else "")

    numRays = 100
    angles = np.linspace(0, 2 * np.pi, numRays, endpoint=False)
    x0, y0 = np.zeros(numRays), np.zeros(numRays)
    u = np.cos(angles)
    v = np.sin(angles)
    
    ax.quiver(x0, y0, u, v, color='gray', alpha=0.3, scale=5, width=0.002, 
              label='Emitted Rays', zorder=1)

    ax.scatter(0, 0, color='#fbc02d', marker='*', s=350, edgecolors='black', 
               linewidth=1, zorder=10, label='Point Source')

    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal')
    ax.set_title("Scene 1: Waveguide Approximation")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)

    plt.tight_layout()
    plt.savefig(os.path.join(plotsDir, "Python-Raytracer-Scene-1.png"), bbox_inches='tight')
    plt.close()

def PlotScene2Sinusoidal():
    fig, ax = plt.subplots(figsize=(10, 10))
    plotsDir = SetupDirectory()

    mirrorColor = '#546e7a'
    targetColor = '#e91e63'
    
    ax.plot([-10, 10, 10, -10, -10], [10, 10, -10, -10, 10], color=mirrorColor, lw=2.5)
    ax.plot([-10, 10], [-10, -10], color=targetColor, lw=5, label='Target Surface')

    xWave = np.linspace(-10, 10, 500)
    yWave = np.sin(xWave) - 6
    ax.plot(xWave, yWave, color='#3f51b5', lw=3, linestyle='--', alpha=0.8, label='Sinusoidal Segments')

    numRays = 100
    angles = np.linspace(0, 2 * np.pi, numRays, endpoint=False)
    ax.quiver(np.zeros(numRays), np.zeros(numRays), np.cos(angles), np.sin(angles), 
              color='gray', alpha=0.3, scale=5, width=0.002, label='Emitted Rays')

    ax.scatter(0, 0, color='#fbc02d', marker='*', s=350, edgecolors='black', zorder=10, label='Point Source')

    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal')
    ax.set_title("Scene 2: Sinusoidal Interface")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)

    plt.tight_layout()
    plt.savefig(os.path.join(plotsDir, "Python-Raytracer-Scene-2.png"), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating Scene 1 and Scene 2 Plots...")
    PlotScene1PointSource()
    PlotScene2Sinusoidal()
    print("Plots generated successfully!")