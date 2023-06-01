

import numpy as np

HFOV = 66.3  # degrees
VFOV = 52.2  # degrees
FOCAL_DIST = 890
CAMERA_HEIGHT = 1  # meters
WIDTH_PIXELS = 800
HEIGHT_PIXELS = 600


# Converter ângulos de visão para radianos
HFOV_rad = np.radians(HFOV)
VFOV_rad = np.radians(VFOV)

# Calcular os parâmetros intrínsecos
focal_length_x = WIDTH_PIXELS / (2 * np.tan(HFOV_rad / 2))
focal_length_y = HEIGHT_PIXELS / (2 * np.tan(VFOV_rad / 2))
principal_point_x = WIDTH_PIXELS / 2
principal_point_y = HEIGHT_PIXELS / 2

# Construir a matriz intrínseca
K = np.array([[focal_length_x, 0, principal_point_x],
              [0, focal_length_y, principal_point_y],
              [0, 0, 1]])

print("Matriz Intrínseca:")
print(K)
