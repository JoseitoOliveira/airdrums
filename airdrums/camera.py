import numpy as np

HFOV = 48.5  # degrees
VFOV = 37.5 # degrees
CAMERA_HEIGHT = 1  # meters
WIDTH_PIXELS = 800
HEIGHT_PIXELS = 600

# Converter ângulos de visão para radianos
HFOV_rad = np.radians(HFOV)
VFOV_rad = np.radians(VFOV)

# Calcular os parâmetros intrínsecos
# FOCAL_DIST = 890
FOCAL_DIST_X = WIDTH_PIXELS / (2 * np.tan(HFOV_rad / 2))
FOCAL_DIST_y = HEIGHT_PIXELS / (2 * np.tan(VFOV_rad / 2))
MAIN_POINT_X = WIDTH_PIXELS / 2
MAIN_POINT_Y = HEIGHT_PIXELS / 2

# Matriz de câmera
camera_matrix = np.array([[FOCAL_DIST_X, 0, MAIN_POINT_X],
                          [0, FOCAL_DIST_y, MAIN_POINT_Y],
                          [0, 0, 1]])

# Pose da câmera (matriz de transformação 4x4)
camera_pose = np.array([[1, 0, 0, 0],
                        [0, 1, 0, CAMERA_HEIGHT],
                        [0, 0, 1, 0],  # Altura da câmera a 1 metro do chão
                        [0, 0, 0, 1]])


def screen_to_real(
    x_screen,
    y_screen,
    r_scrern,
    real_diameter,
    cam_matrix: np.ndarray = camera_matrix,
    cam_pose: np.ndarray = camera_pose
) -> tuple[float, float, float]:
    homog_pixel_coords = np.array([x_screen, y_screen, 1])
    normalized_coords = np.linalg.inv(cam_matrix) @ homog_pixel_coords
    normalized_coords /= normalized_coords[2]

    # Calcular a profundidade da esfera em relação à câmera
    depth = (real_diameter * cam_matrix[0, 0]) / (2 * r_scrern)

    # Calcular a posição 3D da esfera em relação à câmera
    sphere_coords_camera = normalized_coords * depth

    # Calcular a posição 3D da esfera no sistema de coordenadas global
    sphere_coords_global = cam_pose @ np.append(sphere_coords_camera, 1)
    sphere_coords_global /= sphere_coords_global[3]

    return sphere_coords_global[:3]
