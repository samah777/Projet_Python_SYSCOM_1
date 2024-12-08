# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 02:24:01 2024

@author: samyc
"""

import pygame
import sys

# Constantes
GRID_SIZE = 15
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30

# Initialisation de Pygame
pygame.init()

# Créer la fenêtre du jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu avec fond dégradé")

def generate_background(width, height):
    """
    Génère un fond de jeu avec un dégradé doux de couleurs.
    Le fond va du bleu clair (en haut) au vert (en bas).
    
    Paramètres
    ----------
    width : int
        La largeur du fond.
    height : int
        La hauteur du fond.

    Retourne
    --------
    pygame.Surface
        Le fond généré avec dégradé.
    """
    # Créer une surface vide pour le fond
    background = pygame.Surface((width, height))
    
    # Créer un dégradé du bleu vers le vert
    for y in range(height):
        # Calculer la couleur en fonction de la position y
        r = int((y / height) * 0)  # Rouge (toujours 0)
        g = int((y / height) * 255)  # Vert (du bleu au vert)
        b = int((y / height) * 255)  # Bleu (du bleu au vert)
        pygame.draw.line(background, (r, g, b), (0, y), (width, y))  # Dessiner une ligne horizontale avec dégradé

    return background

# Générer le fond
background = generate_background(WIDTH, HEIGHT)

# Sauvegarder l'image générée en PNG
pygame.image.save(background, "background.png")

# Afficher un message de confirmation
print("Le fond a été sauvegardé sous 'background.png'.")

# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Afficher le fond
    screen.blit(background, (0, 0))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter le FPS
    pygame.time.Clock().tick(FPS)

# Quitter Pygame
pygame.quit()
sys.exit()
