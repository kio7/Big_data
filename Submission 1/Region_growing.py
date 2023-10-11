import numpy as np

def region_growing(img, seed, threshold):
    rows, cols = img.shape
    visited = np.zeros_like(img)
    region = np.zeros_like(img)
    stack = []
    stack.append(seed)

    while len(stack) > 0:
        pixel = stack.pop()
        x, y = pixel

        if x < 0 or y < 0 or x >= rows or y >= cols:
            continue

        if visited[x, y] == 1:
            continue

        if abs(int(img[x, y]) - int(img[seed])) <= threshold:  # Threshold, adjust as needed
            region[x, y] = img[x, y]
            visited[x, y] = 1
            stack.append((x - 1, y))
            stack.append((x + 1, y))
            stack.append((x, y - 1))
            stack.append((x, y + 1))

    return region
