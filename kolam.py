import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches    

def draw_dots(ax, spacing=1, size=0.05):
    """Draws the dot grid for kolam."""
    coords = []
    for i in range(-3, 4):   # 7x7 grid
        for j in range(-3, 4):
            if abs(i) + abs(j) <= 5:  # diamond-shaped arrangement
                coords.append((i*spacing, j*spacing))
    for (x, y) in coords:
        dot = plt.Circle((x, y), size, color="orange", zorder=3)
        ax.add_patch(dot)
    return coords

def draw_arc(ax, x, y, direction="up", r=0.5):
    """Draws a small arc at dot (x,y)."""
    theta = np.linspace(0, np.pi, 100)
    if direction == "down":
        theta = -theta
    if direction == "left":
        theta = np.linspace(np.pi/2, 3*np.pi/2, 100)
    if direction == "right":
        theta = np.linspace(-np.pi/2, np.pi/2, 100)
    
    X = x + r*np.cos(theta)
    Y = y + r*np.sin(theta)
    ax.plot(X, Y, color="black", linewidth=2, zorder=2)

def draw_kolam():
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    
    # Step 1: Draw dots
    coords = draw_dots(ax, spacing=1, size=0.07)
    
    # Step 2: Draw arcs around main diamond
    for (x, y) in coords:
        if abs(x) + abs(y) == 3:   # outer arcs
            if x == 0 and y > 0:
                draw_arc(ax, x, y, "up", 0.6)
            elif x == 0 and y < 0:
                draw_arc(ax, x, y, "down", 0.6)
            elif y == 0 and x > 0:
                draw_arc(ax, x, y, "right", 0.6)
            elif y == 0 and x < 0:
                draw_arc(ax, x, y, "left", 0.6)
    
    # Step 3: Central diamond
    diamond = plt.Polygon([[0,1],[1,0],[0,-1],[-1,0]], closed=True,
                          edgecolor="black", facecolor="none", linewidth=2)
    ax.add_patch(diamond)
    
    # Step 4: Central flower (circle + petals)
    circle = plt.Circle((0,0), 0.4, fill=False, color="black", linewidth=2)
    ax.add_patch(circle)
    for k in range(12):
        theta = 2*np.pi*k/12
        x = 0.4*np.cos(theta)
        y = 0.4*np.sin(theta)
        ax.plot([0, x], [0, y], color="black", linewidth=1)
    
    plt.show()

draw_kolam()