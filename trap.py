import pygame
import random
import os
from constante import *

# Définir la couleur des obstacles
OBSTACLE_COLOR = (128, 128, 128)  # Gris

class Trap:
    """Classe pour gérer les pièges dans le jeu avec une animation et la gestion des messages via Console."""

    def __init__(self, animation_folder, sound_path, console):
        """Initialise les pièges avec animations, sons et console."""
        self.positions = []  # Liste des positions des pièges invisibles
        self.visible_traps = []  # Liste des pièges visibles

        # Charger les frames d'animation
        self.frames = self.load_animation_frames(animation_folder)
        self.current_frame_index = 0
        self.animation_speed = 3
        self.animation_counter = 0

        self.sound = pygame.mixer.Sound(sound_path)  # Charger le son du piège
        self.console = console  # Stocker l'instance de Console pour les messages

    def load_animation_frames(self, folder_path):
        """Charge toutes les frames d'animation depuis un dossier."""
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                frame = pygame.image.load(os.path.join(folder_path, filename))
                frame = pygame.transform.scale(frame, (CELL_SIZE, CELL_SIZE))
                frames.append(frame)
        return frames

    def generate_traps(self, grid_size, num_traps, obstacles, valid_positions):
        """Génère plusieurs pièges à une position valide."""
        while len(self.positions) < num_traps:
            pos = random.choice(valid_positions)
            if pos not in obstacles and pos not in self.positions:
                self.positions.append(pos)
                valid_positions.remove(pos)

    def check_for_trap(self, x, y):
        """Vérifie si une position contient un piège."""
        return (x, y) in self.positions

    def trigger_trap(self, unit):
        """Déclenche l'effet d'un piège."""
        self.console.add_message(f"{unit.team} unit at ({unit.x}, {unit.y}) stepped on a trap!")
        unit.health -= 4.5
        self.console.add_message(f"{unit.team} unit's health is now {unit.health:.1f}.")
        unit.check_health()
        if (unit.x, unit.y) in self.positions:
            self.visible_traps.append((unit.x, unit.y))
            self.sound.play()

    def update_animation(self):
        """Met à jour l'index de l'animation."""
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

    def draw(self, screen):
        """Dessine les pièges visibles avec animation."""
        self.update_animation()
        for trap_position in self.visible_traps:
            frame = self.frames[self.current_frame_index]
            screen.blit(frame, (trap_position[0] * CELL_SIZE, trap_position[1] * CELL_SIZE))
