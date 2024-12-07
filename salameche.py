import pygame
from constante import *
from unit import Unit

class Salameche(Unit):
    """
    Classe représentant Pikachu, héritant de Unit.
    """

    def __init__(self, x, y):
        """
        Initialise Pikachu avec des caractéristiques spécifiques.

        Paramètres
        ----------
        x : int
            Position x de Pikachu sur la grille.
        y : int
            Position y de Pikachu sur la grille.
        """
        # Caractéristiques spécifiques à Pikachu
        health = 10
        health_max = 100
        attack_power = 25
        velocity = 2
        team = 'player'
        
        # Charger l'image dans self.icon
        icon_path = 'assets/salameche.png'
        self.icon = pygame.image.load(icon_path)  # Charger l'image depuis le chemin
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionner

        # Appeler le constructeur parent avec une icône spécifique à Pikachu
        super().__init__(x, y, health, health_max, attack_power, velocity, team, self.icon)


    def move(self, dx, dy, game):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy
    

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):

        # Dessiner l'icône avec la méthode parent
        super().draw(screen)


