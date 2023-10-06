import numpy as np

def region_growing(image, seed, threshold):
    height, width = image.shape
    visited = np.zeros_like(image)
    region = np.zeros_like(image)

    stack = []
    stack.append(seed)

    # Define connectivity (4 or 8 neighbors)
    connectivity = 4

    while len(stack) > 0:
        c_p = stack.pop()

        if (
            c_p[0] >= 0
            and c_p[1] >= 0
            and c_p[0] < height
            and c_p[1] < width
        ):
            if visited[c_p[0], c_p[1]] == 0:
                if abs(int(image[c_p]) - int(image[seed])) < threshold:
                    region[c_p] = image[c_p]
                    visited[c_p] = 255

                    if connectivity == 4:
                        neighbors = [
                            (c_p[0] - 1, c_p[1]),
                            (c_p[0] + 1, c_p[1]),
                            (c_p[0], c_p[1] - 1),
                            (c_p[0], c_p[1] + 1),
                        ]
                    elif connectivity == 8:
                        neighbors = [
                            (c_p[0] - 1, c_p[1]),
                            (c_p[0] + 1, c_p[1]),
                            (c_p[0], c_p[1] - 1),
                            (c_p[0], c_p[1] + 1),
                            (c_p[0] - 1, c_p[1] - 1),
                            (c_p[0] - 1, c_p[1] + 1),
                            (c_p[0] + 1, c_p[1] - 1),
                            (c_p[0] + 1, c_p[1] + 1),
                        ]

                    for neighbor in neighbors:
                        stack.append(neighbor)

    return region