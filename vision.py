import pygame
import random

# Constantes
GRID_SIZE = 15
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)






class Vision:
    """
    Classe pour gérer le champ de vision d'une unité.
    """

    def __init__(self, unit, grid_size):
        """
        Initialise le champ de vision pour une unité donnée.

        Paramètres
        ----------
        unit : Unit
            L'unité à laquelle est associée cette vision.
        grid_size : int
            Taille de la grille (pour éviter de dépasser les limites).
        """
        self.unit = unit
        self.grid_size = grid_size

    def get_visible_positions(self):
        """
        Retourne une liste des positions visibles par l'unité.

        Retourne
        --------
        List[Tuple[int, int]]
            Liste des coordonnées visibles dans le champ de vision.
        """
        visible_positions = []
        for dx in range(-2, 3):  # Champ de vision 5x5
            for dy in range(-2, 3):
                x, y = self.unit.x + dx, self.unit.y + dy
                if 0 <= x < self.grid_size and 0 <= y < self.grid_size:  # Limites de la grille
                    visible_positions.append((x, y))
        return visible_positions

    def get_visible_enemies(self, all_units):
        """
        Retourne les ennemis visibles dans le champ de vision.

        Paramètres
        ----------
        all_units : List[Unit]
            Liste de toutes les unités sur la grille.

        Retourne
        --------
        List[Unit]
            Liste des ennemis visibles.
        """
        visible_positions = self.get_visible_positions()
        visible_enemies = []
        for unit in all_units:
            if unit.team != self.unit.team and (unit.x, unit.y) in visible_positions:  # Ennemis seulement dans le champ de vision
                visible_enemies.append(unit)
        return visible_enemies
    
    def draw(self, screen):
        """
        Dessine les bordures autour des cases visibles par l'unité.
    
        Paramètres
        ----------
        screen : pygame.Surface
            Surface de jeu où dessiner les bordures.
        """
        for x, y in self.get_visible_positions():
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 0, 139), rect, width=2)  # Bordure fine
