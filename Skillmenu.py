from constante import *
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
        unit : Unit
            L'unité dont les compétences seront affichées.
        """
        self.unit = unit
        self.skills = unit.skills if unit else []  # Liste des compétences de l'unité
        self.selected_index = 0  # Index de la compétence sélectionnée
        self.is_active = False  # Si le menu est actif ou non

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
        self.selected_index = (self.selected_index + direction) % len(self.skills)
    def update_unit(self, unit):
        """
        Met à jour le menu avec l'unité donnée.
    
        Paramètres
        ----------
        unit : Unit
            L'unité dont les compétences seront affichées.
        """
        self.unit = unit
        self.skills = unit.skills  # Mettre à jour la liste des compétences


    def draw(self, screen):
        # Définir la hauteur de la barre noire
        HEIGHT = screen.get_height() - MENU_HEIGHT  # Hauteur du jeu sans la barre
    
        # Dessiner la barre noire
        menu_rect = pygame.Rect(0, HEIGHT, screen.get_width(), MENU_HEIGHT)
        pygame.draw.rect(screen, (0, 0, 0), menu_rect)  # Barre noire
    
        # Afficher les compétences
        font = pygame.font.Font(None, 24)
        x_offset = 10  # Décalage horizontal initial
        for i, skill in enumerate(self.skills):
            if i == 0:
                skill_text = f"{skill.name} (Appuyez sur A)"
            elif i == 1:
                skill_text = f"{skill.name} (Appuyez sur Z)"
            else:
                # Si vous avez plus de compétences, vous pouvez gérer d'autres touches ou juste afficher le nom
                skill_text = f"{skill.name} (Appuyez sur E)"
    
            text_surface = font.render(skill_text, True, (255, 255, 255))  # Texte blanc
            screen.blit(text_surface, (x_offset, HEIGHT + 10))  # Texte dans la barre noire
            x_offset += 300  # Décalage horizontal pour les compétences suivantes

