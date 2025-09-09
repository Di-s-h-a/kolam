import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

def rounded_rect_path(x, y, w, h, r):
    """
    Return a matplotlib Path for a rounded rectangle centered at (x,y)
    with width w, height h, corner radius r.
    """
    left = x - w/2
    right = x + w/2
    bottom = y - h/2
    top = y + h/2
    
    # Bezier constant
    k = 4*(math.sqrt(2)-1)/3
    
    verts = []
    codes = []
    
    # Start at right-middle
    verts.append((right, y))
    codes.append(Path.MOVETO)
    
    # Top-right arc
    verts.append((right, y + k*r))
    verts.append((x + w/2 - k*r, top))
    verts.append((x + w/2 - r, top))
    codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
    
    # Top-left arc
    verts.append((x - w/2 + r, top))
    verts.append((left, y + k*r))
    verts.append((left, y))
    codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
    
    # Bottom-left arc
    verts.append((left, y - k*r))
    verts.append((x - w/2 + k*r, bottom))
    verts.append((x - w/2 + r, bottom))
    codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
    
    # Bottom-right arc
    verts.append((x + w/2 - r, bottom))
    verts.append((right, y - k*r))
    verts.append((right, y))
    codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
    
    return Path(verts, codes)


def make_grid(rows, cols, spacing=1.0):
    xs = np.arange(cols) * spacing
    ys = np.arange(rows) * spacing
    X, Y = np.meshgrid(xs - xs.mean(), ys - ys.mean())
    return X, Y
def plot_kolam(rows=5, cols=5, spacing=1.0, 
               cell_selection='all', symmetry=('h','v'), 
               loop_radius=0.25, show_dots=True, title=None):
    X, Y = make_grid(rows, cols, spacing)
    fig, ax = plt.subplots(figsize=(6,6))
    
    # Draw dots
    if show_dots:
        ax.scatter(X.flatten(), Y.flatten(), s=40, zorder=3)
    
    patches_list = []
    for i in range(rows-1):
        for j in range(cols-1):
            # Cell center
            cx = (X[0,j] + X[0,j+1])/2
            cy = (Y[i,0] + Y[i+1,0])/2
            
            # Selection rule
            sel = True
            if callable(cell_selection):
                sel = cell_selection(i, j)
            elif cell_selection == 'checker':
                sel = (i + j) % 2 == 0
            elif cell_selection == 'border':
                sel = (i==0 or j==0 or i==rows-2 or j==cols-2)
            
            if not sel:
                continue
            
            # Make loop
            p = rounded_rect_path(cx, cy, spacing, spacing, loop_radius)
            patch = patches.PathPatch(p, fill=False, linewidth=2)
            patches_list.append(patch)
            
            # Apply symmetries
            if 'h' in symmetry:
                verts = [(vx, -vy) for vx,vy in p.vertices]
                patches_list.append(patches.PathPatch(Path(verts, p.codes), fill=False, linewidth=2))
            if 'v' in symmetry:
                verts = [(-vx, vy) for vx,vy in p.vertices]
                patches_list.append(patches.PathPatch(Path(verts, p.codes), fill=False, linewidth=2))
            if 'rot' in symmetry:
                verts = [(-vx, -vy) for vx,vy in p.vertices]
                patches_list.append(patches.PathPatch(Path(verts, p.codes), fill=False, linewidth=2))
    
    # Add patches
    for patch in patches_list:
        ax.add_patch(patch)
    
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(title)
    plt.show()

# Example 1: All cells with horizontal + vertical symmetry
plot_kolam(rows=5, cols=5, spacing=1.0, cell_selection='all',
           symmetry=('h','v'), loop_radius=0.22, title="Kolam - Full Grid")

# Example 2: Checkerboard with 180° rotation
plot_kolam(rows=7, cols=7, spacing=1.0, cell_selection='checker',
           symmetry=('rot',), loop_radius=0.25, title="Kolam - Checkerboard")

# Example 3: Custom diamond pattern
def diamond_selector(i, j):
    center = 4
    dist = abs(i-center) + abs(j-center)
    return dist <= 3

plot_kolam(rows=9, cols=9, spacing=0.9, cell_selection=diamond_selector,
           symmetry=('h','v','rot'), loop_radius=0.18, show_dots=False,
           title="Kolam - Diamond Motif")
