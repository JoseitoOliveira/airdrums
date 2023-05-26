import time


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
