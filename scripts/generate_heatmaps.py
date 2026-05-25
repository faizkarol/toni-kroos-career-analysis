import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def draw_pitch(ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 7))
    # Pitch outline and center line
    ax.plot([0, 0, 100, 100, 0], [0, 100, 100, 0, 0], color="black", linewidth=2)
    ax.plot([50, 50], [0, 100], color="black", linewidth=2)
    # Left penalty area
    ax.plot([0, 17, 17, 0], [30, 30, 70, 70], color="black", linewidth=2)
    # Right penalty area
    ax.plot([100, 83, 83, 100], [30, 30, 70, 70], color="black", linewidth=2)
    # Circles
    centre_circle = plt.Circle((50, 50), 9, color="black", fill=False, linewidth=2)
    centre_spot = plt.Circle((50, 50), 0.8, color="black")
    left_pen_spot = plt.Circle((11, 50), 0.8, color="black")
    right_pen_spot = plt.Circle((89, 50), 0.8, color="black")
    ax.add_patch(centre_circle)
    ax.add_patch(centre_spot)
    ax.add_patch(left_pen_spot)
    ax.add_patch(right_pen_spot)
    # Limit axes
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax

def generate_heatmap(data, title, save_path):
    # Create a 2D heatmap array
    heatmap_data = np.zeros((100, 100))
    for index, row in data.iterrows():
        x, y = int(row["X"]), int(row["Y"])
        heatmap_data[y, x] += 1  # Increment intensity at the given position
    
    # Normalize heatmap data for better visualization
    heatmap_data = heatmap_data / np.max(heatmap_data)
    
    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 7))
    ax = draw_pitch(ax=ax)
    pos = ax.imshow(
        heatmap_data,
        extent=(0, 100, 0, 100),
        cmap="Reds",
        alpha=0.6,
        interpolation="bilinear",
        origin="lower",
    )
    # Add title and colorbar
    ax.set_title(title, fontsize=16)
    plt.colorbar(pos, ax=ax, orientation="vertical", label="Intensity")
    # Save the heatmap
    fig.savefig(save_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {save_path}")

# Example Usage
# Load match data from CSV (Example CSV structure provided separately)
data = pd.read_csv("toni_kroos_match_data.csv")  # Replace with your data file

# Group by season or tournament
for group_name, group_data in data.groupby("Season/Tournament"):
    title = f"Toni Kroos Heatmap: {group_name}"
    save_path = f"Toni_Kroos_Heatmap_{group_name.replace(' ', '_')}.png"
    generate_heatmap(group_data, title, save_path)
