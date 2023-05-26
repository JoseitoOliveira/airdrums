from threading import Thread

import cv2
import pygame
import numpy as np


class DrumElement:

    counter = 0

    def __init__(self, name: str, x: int, y: int, ax1: int, ax2: int, angle, sound: str) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.ax1 = ax1
        self.ax2 = ax2
        self.center = np.array([x, y])
        self.angle = angle
        self.channel = pygame.mixer.Channel(DrumElement.counter)
        self.sound = pygame.mixer.Sound(sound)
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

    def draw(self, frame):
        cv2.ellipse(
            img=frame,
            center=(self.x, self.y),
            axes=(self.ax1, self.ax2),
            angle=self.angle,
            startAngle=0,
            endAngle=360,
            color=(0, 0, 255),
            thickness=2
        )

    def ponto_mais_proximo(self, circle):
        cx, cy, r = circle

        # Calcula o ponto do circulo mais perto da elipse
        cc = np.array([cx, cy])
        v_dir = self.center - cc
        c_prox = cc + (v_dir / np.linalg.norm(v_dir)) * r

        return [round(e) for e in c_prox]

    def is_collided(self, circle):
        c_prox = self.ponto_mais_proximo(circle)

        dist_to_f1 = np.linalg.norm(self.f1 - c_prox)
        dist_to_f2 = np.linalg.norm(self.f2 - c_prox)

        return self.ax_sum > (dist_to_f1 + dist_to_f2)

    def interact(self, circle):
        collided = self.is_collided(circle)

        if collided and not self.collided:
            t = Thread(target=self.channel.play, args=(self.sound,), daemon=True)
            t.start()

        self.collided = collided
