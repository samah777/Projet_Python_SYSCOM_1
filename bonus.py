import pygame
import random
from constante import *

# Définir la couleur des obstacles
OBSTACLE_COLOR = (128, 128, 128)  # Gris

class BonusItem:
    """
    Classe pour gérer les objets bonus dans le jeu avec une gestion des messages via Console..
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

    def generate_bonus(self, grid_size, num_bonus, obstacles, valid_positions):
        """
        Génère plusieurs objets bonus à des positions valides de la grille.
        """
        while len(self.positions) < num_bonus:
            pos = random.choice(valid_positions)
            if pos not in obstacles and pos not in self.positions:
                self.positions.append(pos)
                valid_positions.remove(pos)  # Retirer cette position des positions valides

    def check_for_bonus(self, x, y):
        """
        Vérifie si une position contient un bonus.
        """
        return (x, y) in self.positions
    
    def trigger_bonus(self, unit):
        """
        Applique l'effet du bonus à l'unité qui le collecte.
        """
        health_max = 10  # Définir la santé maximale
        bonus_points = 3  # L'unité gagne 2 point de vie
        # Sauvegarder la santé actuelle de l'unité
        current_health = unit.health
        # Ajouter les points du bonus
        new_health = current_health + bonus_points
        # Vérification pour s'assurer que la santé ne dépasse pas la valeur maximale
        if new_health >= health_max:
            unit.health = health_max  # Limiter la santé à la valeur maximale
            self.console.add_message(f"{unit.team} unit's health is now at max value: {unit.health}.")

        else:
            unit.health = new_health  # Mettre à jour la santé avec le bonus
            self.console.add_message(f"{unit.team} unit at ({unit.x}, {unit.y}) collected a health bonus!")
            self.console.add_message(f"{unit.team} unit's health is now {unit.health}.")
            self.sound.play()  # Jouer le son du bonus
            unit.check_health()
            # Retirer le bonus de la liste des positions après collecte
            for pos in self.positions:
                if pos == (unit.x, unit.y):
                    self.positions.remove(pos)
                    break

    def draw(self, screen):
        """
        Dessine les bonus non collectés sur l'écran.
        """
        for bonus_position in self.positions:
            screen.blit(self.icon, (bonus_position[0] * CELL_SIZE, bonus_position[1] * CELL_SIZE))  # Dessiner l'icône
