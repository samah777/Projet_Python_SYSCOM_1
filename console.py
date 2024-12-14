from constante import * 
import pygame

class Console:
    def __init__(self, screen):
        """
        Initialise la console avec une barre verticale pour les messages.
        """
        self.screen = screen  # L'écran Pygame sur lequel dessiner
        self.messages = []  # Liste pour stocker les messages récents

    def add_message(self, message):
        """
        Ajoute un message à la liste des messages récents.
        """
        self.messages.append(message)
        if len(self.messages) > 10:  # Limiter à 10 messages affichés
            self.messages.pop(0)

    def draw_message_bar(self):
        """
        Dessine la barre verticale et affiche les messages.
        """
        bar_width = 200
        bar_x = WIDTH  # Position x de la barre noire (à droite de la grille)

        pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, 0, bar_width, HEIGHT))  # Barre noire

        font = pygame.font.Font(None, 24)
        y_offset = 10
        for message in self.messages:
            text_surface = font.render(message, True, (255, 255, 255))  # Texte blanc
            self.screen.blit(text_surface, (bar_x + 10, y_offset))
            y_offset += 30
