from constante import *
from unit import *
import pygame





class SkillMenu:
    """
    Classe pour afficher le menu des compétences d'une unité.
    """

    def __init__(self, unit=None):
        """
        Initialise le menu avec les compétences de l'unité.

        Paramètres
        ----------
        unit : Unit, optionnel
            L'unité dont les compétences seront affichées. Par défaut, None.
        """
        self.unit = unit
        self.skills = unit.skills if unit else []  # Liste des compétences de l'unité ou une liste vide
        self.selected_index = 0  # Index de la compétence sélectionnée
        self.is_active = False  # Si le menu est actif ou non

    def update_unit(self, unit):
        """
        Met à jour le menu avec une nouvelle unité.

        Paramètres
        ----------
        unit : Unit
            L'unité dont les compétences seront affichées.
        """
        self.unit = unit
        self.skills = unit.skills if unit else []
        self.selected_index = 0  # Réinitialiser l'index sélectionné

    def toggle(self):
        """Active ou désactive le menu."""
        self.is_active = not self.is_active

    def navigate(self, direction):
        """
        Navigue dans le menu.

        Paramètres
        ----------
        direction : int
            Direction (1 pour bas, -1 pour haut).
        """
        if self.skills:
            self.selected_index = (self.selected_index + direction) % len(self.skills)

    def draw(self, screen):
        """
        Dessine la barre noire et affiche les compétences.

        Paramètres
        ----------
        screen : pygame.Surface
            Surface où dessiner le menu.
        """
        # MENU_HEIGHT = 50  # Hauteur de la barre noire
        HEIGHT = screen.get_height() - MENU_HEIGHT  # Hauteur effective du jeu sans la barre

        # Dessiner la barre noire
        menu_rect = pygame.Rect(0, HEIGHT, screen.get_width(), MENU_HEIGHT)
        pygame.draw.rect(screen, (0, 0, 0), menu_rect)  # Barre noire

        # Afficher les compétences
        font = pygame.font.Font(None, 24)
        x_offset = 10  # Décalage horizontal initial
        for i, skill in enumerate(self.skills):
            # Indique la compétence sélectionnée avec un astérisque
            skill_text = f"{'*' if i == self.selected_index else ''} {skill.name} (Appuyez sur A)"
            text_surface = font.render(skill_text, True, (255, 255, 255))  # Texte blanc
            screen.blit(text_surface, (x_offset, HEIGHT + 10))  # Texte dans la barre noire
            x_offset += 200  # Décalage pour chaque compétence
