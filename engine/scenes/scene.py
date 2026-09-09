from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def draw(self, renderer):
        """Desenha a cena - OBRIGATÓRIO implementar nas subclasses"""
        pass

    @abstractmethod
    def handle_click(self, button, x, y):
        """Manipula cliques - OBRIGATÓRIO implementar nas subclasses"""
        pass

    def update(self, dt):
        """Atualiza a lógica - OPCIONAL implementar"""
        pass
