import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# --- Apply Graphic Style ---
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

# Define knowns and assumptions
baseDiameter = 1.0
ax = 2.0
layersNum = 100
zValues = np.linspace(0, 1, 500)

# Define Cross Section functions
def linearRadius250(z):
    r = (baseDiameter / 2) * z / (ax / 2)
    return np.clip(r, 0, 0.4166666)

def linearRadius300(z):
    r = (baseDiameter / 2) * z / (ax / 2)
    return np.clip(r, 0, 0.499)

def hillLikeRadius(z):
    r = (baseDiameter / 2) * np.sin((np.pi / 2) * z) / (ax / 2)
    return np.clip(r, 0, 0.4166666)

def realisticShape(z):
    raw = np.sqrt(z) + np.tan(((20 * np.pi) / layersNum) * z)
    scale = 0.49 / (np.sqrt(1) + np.tan(((20 * np.pi) / layersNum) * 1))
    r = scale * raw
    return np.clip(r, 0, 0.4999)

# Calculate radius values for each shape
lin250Radius = linearRadius250(zValues)
lin300Radius = linearRadius300(zValues)
hillRadius = hillLikeRadius(zValues)
realRadius = realisticShape(zValues)

# Plotting the graph
plt.figure(figsize=(10, 10))

# Generate magma colors for the 4 structures
num_items = 4
cmap = plt.get_cmap('magma')

# Stopped sampling at 0.7 so the lightest color is a highly visible orange
start, stop = 0.05, 0.70 
colors = [cmap(start + (stop - start) * i / max(1, num_items - 1)) for i in range(num_items)]

# Linear 250 
plt.plot(lin250Radius, 1-zValues, label='Linear 250', color=colors[0], linestyle='-')
plt.plot(-lin250Radius, 1-zValues, color=colors[0], linestyle='-') # Reflected side

# Linear 300 
plt.plot(lin300Radius, 1-zValues, label='Linear 300', color=colors[1], linestyle='--')
plt.plot(-lin300Radius, 1-zValues, color=colors[1], linestyle='--') # Reflected side

# Hill-Like 
plt.plot(hillRadius, 1-zValues, label='Hill-Like', color=colors[2], linestyle='-.')
plt.plot(-hillRadius, 1-zValues, color=colors[2], linestyle='-.') # Reflected side

# Realistic Shape 
plt.plot(realRadius, 1-zValues, label='Realistic Shape', color=colors[3], linestyle=':')
plt.plot(-realRadius, 1-zValues, color=colors[3], linestyle=':') # Reflected side

# Add labels, title, and formatting
plt.title('Cross-Sectional Comparison of Cone Structures', weight='bold', y=1.02)
plt.xlabel('Normalized Radius / Cell Width')
plt.ylabel('Normalized Height')

# Ensure the aspect ratio is equal so the cones aren't artificially stretched
plt.gca().set_aspect('equal', adjustable='box')

# Add breathing room so the cones don't hit the absolute edges of the plot box
plt.xlim(-0.6, 0.6)
plt.ylim(0, 1.05)

# Make dashed grid lines
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Push the legend to the RIGHT SIDE so it stays completely out of the way
plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), ncol=1, fontsize='medium')

# Ensure the Plots directory exists before saving
scriptDir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(scriptDir, "Plots")
os.makedirs(plots_dir, exist_ok=True)

# bbox_inches='tight' guarantees the side legend won't get cut off when exporting to PNG
plt.savefig(os.path.join(plots_dir, "Cross-Section-Comparison.png"), bbox_inches='tight')

plt.show()