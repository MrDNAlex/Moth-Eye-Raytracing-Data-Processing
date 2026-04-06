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

def draw_base_unit_cell(ax, sx=-125, ex=125, ty=-500):
    ax.plot([sx, ex], [ty, ty], color='crimson', lw=5, label='Target')
    ax.plot([sx, sx], [500, ty], color='slategray', lw=2, label='Mirrors')
    ax.plot([ex, ex], [500, ty], color='slategray', lw=2)

def draw_internal_unit_cell(ax, sx=-125, ex=125, ty=500):
    ax.plot([sx, ex], [ty, ty], color='crimson', lw=5, label='Target')
    ax.plot([sx, sx], [ty, -1000], color='slategray', lw=2, label='Mirrors')
    ax.plot([ex, ex], [ty, -1000], color='slategray', lw=2)

def draw_perturbed_normals(ax, y_levels, sx=-125, ex=125, dev=15, A=0, B=0):
    """Helper to visualize rotated surface normals on flat or wavy layers"""
    sample_x = np.linspace(sx + 25, ex - 25, 5)
    first = True
    for y_base in y_levels:
        for x in sample_x:
            # Calculate base normal angle
            if A != 0:
                # Wavy surface: normal is perpendicular to the derivative
                # y = A*sin(B*x), dy/dx = A*B*cos(B*x)
                slope = A * B * np.cos(B * x)
                base_angle = np.arctan(-1/slope) if slope != 0 else np.pi/2
                if base_angle < 0: base_angle += np.pi
                y_pos = A * np.sin(B * x) + y_base
            else:
                # Flat surface
                base_angle = np.pi/2
                y_pos = y_base

            # Apply Gaussian perturbation
            angle = base_angle + np.deg2rad(np.random.normal(0, dev))
            nx, ny = np.cos(angle), np.sin(angle)
            
            ax.quiver(x, y_pos, nx, ny, color='royalblue', alpha=0.4, 
                      scale=20, width=0.005, headwidth=3, 
                      label='Perturbed Surface Normals' if first else "")
            first = False

# --- Simulation Category Plotters ---

def plot_sim_1():
    fig, ax = plt.subplots(figsize=(10, 8))
    draw_base_unit_cell(ax)
    for i, y in enumerate(np.linspace(250, 0, 3)):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (3)' if i==0 else "")
    ax.quiver(100, 400, -0.7, -0.7, color='orange', scale=5, label='Ray Source (0 - 60°) \n(300 - 1000 nm)')
    ax.set_title("Wavelength Sweep (Transmittance) - Simulation 1")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-1-Wavelength-Sweep.png"), bbox_inches='tight')
    plt.close()

def plot_sim_2():
    fig, ax = plt.subplots(figsize=(10, 8))
    draw_base_unit_cell(ax)
    y_levels = np.linspace(250, 0, 3)
    for i, y in enumerate(np.linspace(250, 0, 3)):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (3)' if i==0 else "")
    draw_perturbed_normals(ax, y_levels, dev=12)
    ax.quiver(100, 400, -0.7, -0.7, color='orange', scale=5, label='Ray Source (0 - 60°) \n(300 - 1000 nm)')
    ax.set_title("Wavelength Sweep with Perturbance (Transmittance) - Simulation 2")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-2-Perturbance-Sweep.png"), bbox_inches='tight')
    plt.close()

def plot_sim_3():
    fig, ax = plt.subplots(figsize=(10, 8))
    draw_base_unit_cell(ax)
    y_levels = np.linspace(250, 0, 3)
    xw = np.linspace(-125, 125, 200)
    A, B = 10, (2 * np.pi / 100)
    for i, y in enumerate(np.linspace(250, 0, 3)):
        yw = A * np.sin(B * xw) + y
        ax.plot(xw, yw, color='royalblue', alpha=0.3, lw=1, label='Waveguide Layers (3)' if i==0 else "")
    
    # Added Perturbed Normals for Wavy Layers
    draw_perturbed_normals(ax, y_levels, dev=12, A=A, B=B)
    
    ax.quiver(100, 400, -0.7, -0.7, color='orange', scale=5, label='Ray Source (0 - 60°) \n(300 - 1000 nm)')
    ax.set_title("Wavelength Sweep with Wavy Layers (Transmittance) - Simulation 3")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-3-Wavy-Sweep.png"), bbox_inches='tight')
    plt.close()

def plot_sim_4():
    fig, ax = plt.subplots(figsize=(10, 8))
    draw_internal_unit_cell(ax)
    for i, y in enumerate(np.linspace(250, 0, 10)):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (40)' if i==0 else "")
    
    # ConeLight visualization emitting from -400
    ax.fill([0, -125, 125, 0], [-400, 0, 0, -400], color='magenta', alpha=0.3, label='ConeLight Emission')
    ax.scatter(0, -400, color='magenta', s=150, zorder=10, label='Cone Source \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep (TIR) - Simulation 4")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-4-Internal-Sweep.png"), bbox_inches='tight')
    plt.close()

def plot_sim_5():
    fig, ax = plt.subplots(figsize=(10, 8))
    draw_internal_unit_cell(ax)
    y_levels = np.linspace(250, 0, 10)
    for i, y in enumerate(np.linspace(250, 0, 10)):
        ax.plot([-125, 125], [y, y], color='royalblue', alpha=0.3, label='Waveguide Layers (40)' if i==0 else "")
    draw_perturbed_normals(ax, y_levels, dev=12)
    
    # ConeLight visualization emitting from -400
    ax.fill([0, -125, 125, 0], [-400, 0, 0, -400], color='magenta', alpha=0.3, label='ConeLight Emission')
    ax.scatter(0, -400, color='magenta', s=150, zorder=10, label='Cone Source \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep with Perturbance (TIR) - Simulation 5")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-5-Internal-Perturbance.png"), bbox_inches='tight')
    plt.close()

def plot_sim_6():
    fig, ax = plt.subplots(figsize=(10, 8))
    draw_internal_unit_cell(ax)
    y_levels = np.linspace(250, 0, 10)
    xw = np.linspace(-125, 125, 200)
    A, B = 8, (2 * np.pi / 80)
    for i, y in enumerate(np.linspace(250, 0, 10)):
        yw = A * np.sin(B * xw) + y
        ax.plot(xw, yw, color='royalblue', alpha=0.3, label='Waveguide Layers (40)' if i==0 else "")
    
    # Added Perturbed Normals for Internal Wavy Layers
    draw_perturbed_normals(ax, y_levels, dev=12, A=A, B=B)
    
    # ConeLight visualization emitting from -400
    ax.fill([0, -125, 125, 0], [-400, 0, 0, -400], color='magenta', alpha=0.3, label='ConeLight Emission')
    ax.scatter(0, -400, color='magenta', s=150, zorder=10, label='Cone Source \n(300 - 1000 nm)')
    
    ax.set_title("Wavelength Sweep with Wavy Layers (TIR) - Simulation 6")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-6-Internal-Wavy.png"), bbox_inches='tight')
    plt.close()

def plot_sim_7():
    fig, ax = plt.subplots(figsize=(10, 8))
    draw_base_unit_cell(ax)
    ax.plot([-125, 125], [250, 250], color='royalblue', lw=4, label='Waveguide Layer (1)')
    ax.quiver(100, 400, -0.7, -0.7, color='orange', scale=5, label='Ray Source (0 - 60°) \n(300 - 1000 nm)')
    ax.set_title("Wavelength Sweep Control (Transmittance) - Simulation 7")
    ax.set_xlabel("X Position (nm)"); ax.set_ylabel("Y Position (nm)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)
    plt.savefig(os.path.join(setup_directory(), "Sim-7-Single-Layer.png"), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating Simulation Configurations 1-7 with updated ConeLight sources...")
    plot_sim_1(); plot_sim_2(); plot_sim_3(); plot_sim_4(); plot_sim_5(); plot_sim_6(); plot_sim_7()
    print(f"Success! All 7 scenes saved to: {setup_directory()}")