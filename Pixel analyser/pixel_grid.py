from PIL import Image
import math

# Define your accepted named colors and their RGB values
color = {
    'red':     (255, 0, 0),
    'blue':    (0, 0, 255),
    'green':   (0, 128, 0),
    'yellow':  (255, 255, 0),
    'cyan':    (0, 255, 255),
    'orange':  (255, 165, 0),
    'white':   (255, 255, 255),
    'black':   (0, 0, 0),
    'gray':    (128, 128, 128),
    'purple':  (128, 0, 128)
}

def closest_named_color(r, g, b):
    min_dist = float('inf')
    closest = None
    for name, (cr, cg, cb) in color.items():
        dist = math.sqrt((r-cr)**2 + (g-cg)**2 + (b-cb)**2)
        if dist < min_dist:
            min_dist = dist
            closest = name
    return closest

def map_grid(image_path, grid_size=40):
    img = Image.open(image_path).convert("RGB")
    W, H = img.size
    cell_w = W / grid_size
    cell_h = H / grid_size
    pixels = img.load()

    grid = []
    for row in range(grid_size):
        grid_row = []
        for col in range(grid_size):
            cx = int((col + 0.5) * cell_w)  # No horizontal flip
            cy = int((grid_size - 1 - row + 0.5) * cell_h)  # Vertical flip only
            r, g, b = pixels[cx, cy]
            name = closest_named_color(r, g, b)
            grid_row.append(name)
        grid.append(grid_row)
    return grid






def extract_vertical_segments(grid, target_color):
    X, Y, lengths = [], [], []
    size = len(grid)

    for col in range(size):
        row = 0
        while row < size:
            if grid[row][col] == target_color:
                start_row = row
                length = 1
                while row + 1 < size and grid[row + 1][col] == target_color:
                    length += 1
                    row += 1
                X.append(col + 1)
                Y.append(start_row + 1)
                lengths.append(length)
            row += 1
    return X, Y, lengths

if __name__ == "__main__":
    grid = map_grid("avatar.jpg", grid_size=40)

    for name in color.keys():
        X, Y, L = extract_vertical_segments(grid, name)
        if X:
            print(f"{name}X =", X)
            print(f"{name}Y =", Y)
            print(f"length{name[0].upper()} =", L)
            print()
