import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# 1. Setup Professional Styling
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

def setup_directory():
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_path = os.getcwd()
    plots_dir = os.path.join(base_path, "Plots")
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    return plots_dir

# --- Unified Legend Style: loc='center left', bbox_to_anchor=(1, 0.5) ---

def plot_max_capture_waveguide():
    fig, ax = plt.subplots(figsize=(12, 6))
    layers = 15
    y_pos = np.linspace(250, 0, layers)
    
    for i, y in enumerate(y_pos):
        ax.plot([-1000, 1000], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (2 - 250)' if i==0 else "")
    
    ax.plot([-1000, 1000], [-200, -200], color='crimson', lw=5, label='Target')
    ax.plot([-1000, -1000], [400, -200], color='slategray', lw=2, label='Mirrors')
    ax.plot([1000, 1000], [400, -200], color='slategray', lw=2)
    
    angle = 45 
    rad = np.deg2rad(angle)
    ax.quiver(500, 500, -np.cos(rad), -np.sin(rad), color='orange', scale=5, label=f'Incident Source ($45^\circ$)')

    ax.set_title("Max Capture Angle Moth-Eye Test Configuration")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.set_xlim(-1200, 1200); ax.set_ylim(-300, 700)
    # Applied Fixed Legend Position
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-Max-Capture-Waveguide.png"), bbox_inches='tight')
    plt.close()

def plot_circular_qd_unit_cell():
    fig, ax = plt.subplots(figsize=(8, 10))
    y_pos = np.linspace(250, 0, 20)
    
    for i, y in enumerate(y_pos):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (2 - 250)' if i==0 else "")
    
    ax.plot([-125, 125], [-200, -200], color='crimson', lw=5, label='Target')
    ax.plot([-125, -125], [250, -200], color='slategray', lw=2, label='Mirrors')
    ax.plot([125, 125], [250, -200], color='slategray', lw=2)
    
    ax.scatter(0, -100, color='magenta', s=150, zorder=10, label='Circular QD (1 - 15)')
    ax.scatter(-75, -100, color='magenta', s=150, zorder=10)
    ax.scatter(75, -100, color='magenta', s=150, zorder=10)
    angles = np.linspace(0, 2*np.pi, 36)
    ax.quiver([0]*36, [-100]*36, np.cos(angles), np.sin(angles), color='gray', alpha=0.4, scale=15, label='360° Emission')

    ax.set_title("TIR Circular QD Unit Cell Test Configuration")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.set_aspect('equal'); ax.set_xlim(-200, 200); ax.set_ylim(-250, 350)
    # Applied Fixed Legend Position
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-Circular-QD-Unit-Cell.png"), bbox_inches='tight')
    plt.close()
    
def plot_circular_qd_large_scale():
    fig, ax = plt.subplots(figsize=(8, 10))
    y_pos = np.linspace(250, 0, 20)
    
    for i, y in enumerate(y_pos):
        ax.plot([-500, 500], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (2 - 250)' if i==0 else "")
    
    ax.plot([-500, 500], [-200, -200], color='crimson', lw=5, label='Target')
    ax.plot([-500, -500], [250, -200], color='slategray', lw=2, label='Mirrors')
    ax.plot([500, 500], [250, -200], color='slategray', lw=2)
    
    ax.scatter(0, -100, color='magenta', s=150, zorder=10, label='Circular QD (1 - 15)')
    ax.scatter(-75, -100, color='magenta', s=150, zorder=10)
    ax.scatter(75, -100, color='magenta', s=150, zorder=10)
    angles = np.linspace(0, 2*np.pi, 36)
    ax.quiver([0]*36, [-100]*36, np.cos(angles), np.sin(angles), color='gray', alpha=0.4, scale=15, label='360° Emission')

    ax.set_title("TIR Circular QD Large Scale Test Configuration")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.set_aspect('equal'); ax.set_xlim(-550, 550); ax.set_ylim(-250, 600)
    # Applied Fixed Legend Position
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-Circular-QD-Large-Scale.png"), bbox_inches='tight')
    plt.close()

def plot_cone_qd_waveguide():
    fig, ax = plt.subplots(figsize=(8, 10))
    y_pos = np.linspace(250, 0, 20)
    
    for i, y in enumerate(y_pos):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (2 - 250)' if i==0 else "")
    
    ax.plot([-125, 125], [-200, -200], color='crimson', lw=5, label='Target')
    ax.plot([-125, -125], [250, -200], color='slategray', lw=2, label='Mirrors')
    ax.plot([125, 125], [250, -200], color='slategray', lw=2)
    
    ax.fill([0, -125, 125, 0], [-100, 0, 0, -100], color='magenta', alpha=0.3, label='ConeLight Emission')
    ax.scatter(0, -100, color='magenta', s=150, zorder=10, label='Cone QD (1 - 15)')
    ax.scatter(-75, -100, color='magenta', s=150, zorder=10)
    ax.scatter(75, -100, color='magenta', s=150, zorder=10)

    ax.set_title("TIR Cone QD Waveguide Unit Cell Test Configuration")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.set_aspect('equal'); ax.set_xlim(-200, 200); ax.set_ylim(-250, 350)
    # Applied Fixed Legend Position
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-Cone-QD-Waveguide.png"), bbox_inches='tight')
    plt.close()
    
def plot_cone_qd_waveguide_large_scale():
    fig, ax = plt.subplots(figsize=(8, 10))
    y_pos = np.linspace(250, 0, 20)
    
    for i, y in enumerate(y_pos):
        ax.plot([-500, 500], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (2 - 250)' if i==0 else "")
    
    ax.plot([-500, 500], [-200, -200], color='crimson', lw=5, label='Target')
    ax.plot([-500, -500], [250, -200], color='slategray', lw=2, label='Mirrors')
    ax.plot([500, 500], [250, -200], color='slategray', lw=2)
    
    ax.fill([0, -500, 500, 0], [-100, 0, 0, -100], color='magenta', alpha=0.3, label='ConeLight Emission')
    ax.scatter(0, -100, color='magenta', s=150, zorder=10, label='Cone QD (1 - 15)')
    ax.scatter(-75, -100, color='magenta', s=150, zorder=10)
    ax.scatter(75, -100, color='magenta', s=150, zorder=10)

    ax.set_title("TIR Cone QD Waveguide Large Scale Test Configuration")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.set_aspect('equal'); ax.set_xlim(-550, 550); ax.set_ylim(-250, 600)
    # Applied Fixed Legend Position
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-Cone-QD-Waveguide-Large-Scale.png"), bbox_inches='tight')
    plt.close()

def plot_real_life_test():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot([-500, 500], [-200, -200], color='crimson', lw=5, label='Target')
    ax.plot([-500, -500], [1000, -200], color='slategray', lw=2, label='Mirrors')
    ax.plot([500, 500], [1000, -200], color='slategray', lw=2)
    
    for i, y in enumerate(np.linspace(250, 0, 10)):
        ax.plot([-500, 500], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (2 - 250)' if i==0 else "")
        
    qdx = np.linspace(-400, 400, 9)
    ax.scatter(qdx, [-100]*len(qdx), color='magenta', s=50, label='QD Array (0-400)')
    
    ax.quiver(400, 800, -0.7, -0.7, color='orange', scale=8, label='Solar Incident Source ($0 & 26^\circ$)')

    ax.set_title("Real Life Device Performance Test Configuration")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.set_xlim(-700, 700); ax.set_ylim(-300, 1100)
    # Applied Fixed Legend Position
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-Real-Life-Test.png"), bbox_inches='tight')
    plt.close()
    
def plot_wave_unit_cell_sinusoidal():
    fig, ax = plt.subplots(figsize=(10, 8))
    sx, ex = 0, 250
    dy = -200
    xw = np.linspace(sx, ex, 500)
    yw_interface = 15 * np.sin(2 * np.pi * xw / 125) + 250
    
    ax.fill_between(xw, yw_interface, dy, color='#3f51b5', alpha=0.1, zorder=0, label='Substrate Structure')
    ax.plot(xw, yw_interface, color='#3f51b5', lw=3, ls='--', label=r'Sinusoidal Moth-Eye')

    ax.plot([sx, ex], [dy, dy], color='crimson', lw=5, label='Target')
    ax.plot([sx, sx], [250, dy], color='slategray', lw=2, label='Mirrors')
    ax.plot([ex, ex], [250, dy], color='slategray', lw=2)
    
    source_x, source_y = 125, -100
    ax.fill([125, 0, 250, 125], [-100, 250, 250, -100], color='magenta', alpha=0.3, label='ConeLight Emission')
    ax.scatter(125, -100, color='magenta', s=150, zorder=10, label='Cone QD (1 - 15)')
    
    ax.set_title("TIR Sinusoidal Moth-Eye Unit Cell Test Configuration")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.set_aspect('equal'); ax.set_xlim(-50, 300); ax.set_ylim(-250, 350)
    # Applied Fixed Legend Position
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    
    plt.savefig(os.path.join(setup_directory(), "Sim-Wave-Unit-Cell.png"), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating Benchmark Simulation Scenes with Fixed Legends...")
    plot_max_capture_waveguide()
    plot_circular_qd_unit_cell()
    plot_circular_qd_large_scale()
    plot_cone_qd_waveguide()
    plot_cone_qd_waveguide_large_scale()
    plot_real_life_test()
    plot_wave_unit_cell_sinusoidal()
    print(f"Success! Corrected plots saved to: {setup_directory()}")