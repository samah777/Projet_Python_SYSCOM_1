import pygame
import random
from constante import *
from abc import ABC, abstractmethod

# Définir la couleur des obstacles
OBSTACLE_COLOR = (128, 128, 128)  # Gris

class BonusItem:
    """
    Classe pour gérer les objets bonus dans le jeu avec une gestion des messages via Console.
    """
    def __init__(self, icon_path, sound_path, console):
        """
        Initialise les bonus avec leur icône, son et type (points ou santé).
        """
        self.positions = []  # Liste des positions des bonus
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'icône
        self.sound = pygame.mixer.Sound(sound_path)  # Charger le son du bonus
        self.console = console  # Stocker l'instance de Console pour les messages
        self.player_units = []
        self.enemy_units = []
    
    @abstractmethod
    def generate_bonus(self, grid_size, num_bonus, obstacles, valid_positions):
        """
        Génère plusieurs objets bonus à des positions valides de la grille.
        """
        while len(self.positions) < num_bonus:
            pos = random.choice(valid_positions)
            if pos not in obstacles and pos not in self.positions:
                self.positions.append(pos)
                valid_positions.remove(pos)  # Retirer cette position des positions valides

    @abstractmethod
    def check_for_bonus(self, x, y):
        """
        Vérifie si une position contient un bonus.
        """
        return (x, y) in self.positions
    
    @abstractmethod
    def trigger_bonus(self, unit):
        """
        Applique l'effet du bonus à l'unité qui le collecte.
        """
        bonus_points = 3  # L'unité gagne 2 point de vie
        # Sauvegarder la santé actuelle de l'unité
        current_health = unit.health
        # Ajouter les points du bonus
        if current_health < 10:
           self.sound.play()
        new_health = min(current_health + bonus_points,10)
        for pos in self.positions :
            if pos == (unit.x, unit.y) and unit.health < 10:
                self.positions.remove(pos)
        unit.health=new_health
        self.console.add_message(f"{unit.team} {unit.name} a maintenant : {unit.health} PV.")
        

    @abstractmethod
    def draw(self, screen):
        """
        Dessine les bonus non collectés sur l'écran.
        """
        for bonus_position in self.positions:
            screen.blit(self.icon, (bonus_position[0] * CELL_SIZE, bonus_position[1] * CELL_SIZE))  # Dessiner l'icône
