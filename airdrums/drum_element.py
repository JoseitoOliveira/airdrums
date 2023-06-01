import time
from threading import Thread

import numpy as np
import pygame
import pygame as pg
from camera import screen_to_real, HEIGHT_PIXELS


class DrumstickTip:

    def __init__(self, x, y, r, real_size=0.05) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.real_size = real_size

        real_x, real_y, real_z = screen_to_real(x, y, r, real_size)
        self.real_x = real_x
        self.real_y = real_y
        self.real_z = real_z

        self.vel_x = 0  # m/s
        self.vel_y = 0  # m/s
        self.vel_z = 0  # m/s

        self.last_tick = time.perf_counter()

    def update_position(self, x, y, r):
        real_x, real_y, real_z = screen_to_real(x, y, r, self.real_size)

        tick = time.perf_counter()
        time_delta = tick - self.last_tick

        self.vel_x = (real_x - self.real_x) / time_delta
        self.vel_y = (real_y - self.real_y) / time_delta
        self.vel_z = (real_z - self.real_z) / time_delta

        self.last_tick = tick

        self.x = x
        self.y = y
        self.r = r

        self.real_x = real_x
        self.real_y = real_y
        self.real_z = real_z
    
    def draw_top(self, surface):
        H_MAX = 40
        H_MIN = 20
        h = H_MAX - (self.x / HEIGHT_PIXELS) * (H_MAX - H_MIN)
        pg.draw.circle(surface, (0, 255, 0), (b, d), h)


class DrumElement:

    counter = 0

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        d: int,
        ax1: int,
        ax2: int,
        angle: int,
        image: str,
        sound: str
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.d = d
        self.ax1 = ax1
        self.ax2 = ax2
        self.front_center = np.array([x, y])
        self.top_center = np.array([d, y])
        self.angle = angle
        self.channel = pygame.mixer.Channel(DrumElement.counter)
        self.sound = pygame.mixer.Sound(sound)
        self.image = pg.transform.scale(
            pg.image.load(image),
            (self.ax2 * 2, self.ax2 * 2)
        )
        self.collided = False

        self.ax_sum = 2 * max(ax1, ax2)

        angle_rad = np.radians(angle)

        # distancia do centro aos focos
        c_dist = np.sqrt((ax2 ** 2) - (ax1 ** 2))  # Distância entre os focos
        c1x = x + c_dist * np.sin(angle_rad)
        c1y = y - c_dist * np.cos(angle_rad)
        c2x = x - c_dist * np.sin(angle_rad)
        c2y = y + c_dist * np.cos(angle_rad)

        self.f1 = np.array([round(c1x), round(c1y)])
        self.f2 = np.array([round(c2x), round(c2y)])

        DrumElement.counter += 1

    def __repr__(self) -> str:
        return f'DrumElement(name={self.name})'

    def draw_top(self, surface: pg.Surface):
        surface.blit(
            self.image,
            (
                round(self.y - self.ax2),
                round(self.d - self.ax2),
            )
        )

    def draw_front(self, surface):
        pg.draw.ellipse(
            surface,
            color=(0, 0, 0, 100),
            rect=(self.y - self.ax2, self.x - self.ax1, self.ax2 * 2, self.ax1 * 2)
        )

    def ponto_mais_proximo(self, cx, cy, r):

        # Calcula o ponto do circulo mais perto da elipse
        cc = np.array([cx, cy])
        v_dir = self.front_center - cc
        c_prox = cc + (v_dir / np.linalg.norm(v_dir)) * r
        return c_prox

    def is_collided(self, circle):
        cx, cy, cd, r = circle
        c_prox = self.ponto_mais_proximo(cx, cy, r)

        dist_to_f1 = np.linalg.norm(self.f1 - c_prox)
        dist_to_f2 = np.linalg.norm(self.f2 - c_prox)

        top_dist = np.linalg.norm(np.array([cd, cy]) - np.array([self.d, self.y]))

        front_collided = self.ax_sum > (dist_to_f1 + dist_to_f2)
        top_collided = top_dist <= self.ax2 + r

        return front_collided and top_collided

    def play(self):
        t = Thread(target=self.channel.play, args=(self.sound,), daemon=True)
        t.start()

    def interact_with_circles(self, circles):
        frame_collision = False
        for c in circles:
            frame_collision = frame_collision or self.is_collided(c)
            if (
                not self.collided and
                frame_collision
            ):
                self.collided = True
                self.play()
                return

        self.collided = frame_collision
