import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# --- Global Style Configuration ---
plt.style.use('seaborn-v0_8-whitegrid') # Cleaner base than ggplot for engineering
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

def setup_directory():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(script_dir, "Plots")
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    return plots_dir

def plot_scene_1_point_source():
    fig, ax = plt.subplots(figsize=(10, 10))
    plots_dir = setup_directory()

    # 1. Boundaries
    mirror_color = '#546e7a'
    target_color = '#e91e63'
    
    # Mirrors
    ax.plot([-10, 10, 10, -10, -10], [10, 10, -10, -10, 10], 
            color=mirror_color, lw=2.5, label='Mirror Boundary', zorder=2)
    
    # Target (Highlighting just the bottom)
    ax.plot([-10, 10], [-10, -10], color=target_color, lw=5, label='Target Surface', zorder=3)

    # 2. Waveguide Segments
    wave_color = '#5c6bc0'
    wave_y_levels = [-5, -5.5, -6, -6.5]
    for i, y in enumerate(wave_y_levels):
        ax.hlines(y, -10, 10, colors=wave_color, linestyles='--', lw=2, alpha=0.6,
                  label='Waveguide Segments' if i == 0 else "")

    # 3. Ray Emission (Quiver is cleaner than 100 arrows)
    num_rays = 100
    angles = np.linspace(0, 2 * np.pi, num_rays, endpoint=False)
    x0, y0 = np.zeros(num_rays), np.zeros(num_rays)
    u = np.cos(angles)
    v = np.sin(angles)
    
    ax.quiver(x0, y0, u, v, color='gray', alpha=0.3, scale=5, width=0.002, 
              label='Emitted Rays', zorder=1)

    # 4. Point Source
    ax.scatter(0, 0, color='#fbc02d', marker='*', s=350, edgecolors='black', 
               linewidth=1, zorder=10, label='Point Source')

    # Formatting
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal')
    ax.set_title("Scene 1: Waveguide Approximation")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)

    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "Python-Raytracer-Scene-1.png"), bbox_inches='tight')
    plt.close()

def plot_scene_2_sinusoidal():
    fig, ax = plt.subplots(figsize=(10, 10))
    plots_dir = setup_directory()

    # 1. Boundaries (Same as Scene 1)
    mirror_color = '#546e7a'
    target_color = '#e91e63'
    ax.plot([-10, 10, 10, -10, -10], [10, 10, -10, -10, 10], color=mirror_color, lw=2.5)
    ax.plot([-10, 10], [-10, -10], color=target_color, lw=5, label='Target Surface')

    # 2. Sinusoidal Wave
    x_wave = np.linspace(-10, 10, 500)
    y_wave = np.sin(x_wave) - 6
    ax.plot(x_wave, y_wave, color='#3f51b5', lw=3, linestyle='--', alpha=0.8, label='Sinusoidal Segments')

    # 3. Ray Emission (Quiver)
    num_rays = 100
    angles = np.linspace(0, 2 * np.pi, num_rays, endpoint=False)
    ax.quiver(np.zeros(num_rays), np.zeros(num_rays), np.cos(angles), np.sin(angles), 
              color='gray', alpha=0.3, scale=5, width=0.002, label='Emitted Rays')

    # 4. Point Source
    ax.scatter(0, 0, color='#fbc02d', marker='*', s=350, edgecolors='black', zorder=10, label='Point Source')

    # Formatting
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal')
    ax.set_title("Scene 2: Sinusoidal Interface")
    ax.set_xlabel("X Position (nm)")
    ax.set_ylabel("Y Position (nm)")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, shadow=True)

    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "Python-Raytracer-Scene-2.png"), bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_scene_1_point_source()
    plot_scene_2_sinusoidal()