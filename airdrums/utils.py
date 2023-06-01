import time
from typing import Iterable, Any


def find_closest_pairs(set1: Iterable, set2: Iterable) -> tuple[list[tuple[Any, Any]], set, set]:
    set1 = set(set1)
    set2 = set(set2)

    cache: dict = {}
    num_pairs = min(len(set1), len(set2))
    result = []
    for _ in range(num_pairs):
        min_square_dist = float('inf')
        for p1 in set1:
            for p2 in set2:

                if (p1.x, p1.y, p2.x, p2.y) in cache:
                    square_dist = cache[(p1.x, p1.y, p2.x, p2.y)]
                else:
                    square_dist = (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2
                    cache[(p1.x, p1.y, p2.x, p2.y)] = square_dist

                if square_dist < min_square_dist:
                    min_square_dist = square_dist
                    p1_min = p1
                    p2_min = p2

        set1.remove(p1_min)
        set2.remove(p2_min)

        result.append((p1_min, p2_min))

    return result, set1, set2


class FPSMedidor:
    def __init__(self):
        self.contagem_frames = 0
        self.tempo_inicio = time.perf_counter()

    def update(self):
        self.contagem_frames += 1
        tempo_atual = time.perf_counter()

        if tempo_atual - self.tempo_inicio >= 1.0:
            fps = self.contagem_frames / (tempo_atual - self.tempo_inicio)
            self.contagem_frames = 0
            self.tempo_inicio = tempo_atual
            return fps

        return None
