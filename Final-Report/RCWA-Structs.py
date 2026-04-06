import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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

def LinearRadius250(z, baseDiameter, ax):
    r = (baseDiameter / 2) * z / (ax / 2)
    return np.clip(r, 0, 0.4166666)

def LinearRadius300(z, baseDiameter, ax):
    r = (baseDiameter / 2) * z / (ax / 2)
    return np.clip(r, 0, 0.499)

def HillLikeRadius(z, baseDiameter, ax):
    r = (baseDiameter / 2) * np.sin((np.pi / 2) * z) / (ax / 2)
    return np.clip(r, 0, 0.4166666)

def RealisticShape(z, layersNum):
    raw = np.sqrt(z) + np.tan(((20 * np.pi) / layersNum) * z)
    scale = 0.49 / (np.sqrt(1) + np.tan(((20 * np.pi) / layersNum) * 1))
    r = scale * raw
    return np.clip(r, 0, 0.4999)

def PlotCrossSections():
    baseDiameter = 1.0
    ax = 2.0
    layersNum = 100
    zValues = np.linspace(0, 1, 500)

    lin250Radius = LinearRadius250(zValues, baseDiameter, ax)
    lin300Radius = LinearRadius300(zValues, baseDiameter, ax)
    hillRadius = HillLikeRadius(zValues, baseDiameter, ax)
    realRadius = RealisticShape(zValues, layersNum)

    plt.figure(figsize=(10, 10))

    numItems = 4
    cmap = plt.get_cmap('magma')

    start, stop = 0.05, 0.70 
    colors = [cmap(start + (stop - start) * i / max(1, numItems - 1)) for i in range(numItems)]

    plt.plot(lin250Radius, 1-zValues, label='Linear 250', color=colors[0], linestyle='-')
    plt.plot(-lin250Radius, 1-zValues, color=colors[0], linestyle='-') 

    plt.plot(lin300Radius, 1-zValues, label='Linear 300', color=colors[1], linestyle='--')
    plt.plot(-lin300Radius, 1-zValues, color=colors[1], linestyle='--') 

    plt.plot(hillRadius, 1-zValues, label='Hill-Like', color=colors[2], linestyle='-.')
    plt.plot(-hillRadius, 1-zValues, color=colors[2], linestyle='-.') 

    plt.plot(realRadius, 1-zValues, label='Realistic Shape', color=colors[3], linestyle=':')
    plt.plot(-realRadius, 1-zValues, color=colors[3], linestyle=':') 

    plt.title('Cross-Sectional Comparison of Cone Structures', weight='bold', y=1.02)
    plt.xlabel('Normalized Radius / Cell Width')
    plt.ylabel('Normalized Height')

    plt.gca().set_aspect('equal', adjustable='box')

    plt.xlim(-0.6, 0.6)
    plt.ylim(0, 1.05)

    plt.grid(True, alpha=0.6)
    plt.tight_layout()

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, fontsize='medium')

    scriptDir = os.path.dirname(os.path.abspath(__file__))
    plotsDir = os.path.join(scriptDir, "Plots")
    os.makedirs(plotsDir, exist_ok=True)

    outputPath = os.path.join(plotsDir, "Cross-Section-Comparison.png")
    plt.savefig(outputPath, bbox_inches='tight')
    plt.close()

    print(f"Saved Plot: {outputPath}")

if __name__ == "__main__":
    PlotCrossSections()