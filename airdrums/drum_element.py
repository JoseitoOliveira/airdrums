from threading import Thread

import cv2
import pygame


class DrumElement:

    counter = 0

    def __init__(self, name: str, x: int, y: int, w: int, h: int, sound: str) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.channel = pygame.mixer.Channel(DrumElement.counter)
        self.sound = pygame.mixer.Sound(sound)
        self.is_collided = True

        DrumElement.counter += 1

    def draw(self, frame):
        cv2.rectangle(
            img=frame,
            pt1=(self.x, self.y),
            pt2=(self.x + self.w, self.y + self.h),
            color=(0, 0, 255),
            thickness=2
        )

    def interact(self, circle):
        x, y, r = circle
        collided = (
            x + r < self.x or
            y + r < self.y or
            x - r > self.x + self.w or
            y - r > self.y + self.h
        )
        if collided and not self.is_collided:
            t = Thread(target=self.channel.play, args=(self.sound,), daemon=True)
            t.start()
        
        self.is_collided = collided
