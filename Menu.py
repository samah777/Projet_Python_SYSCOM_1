import pygame
from constante import *


class Menu : 
    
    def __init__ (self,screen) : 
        self.screen =screen
        self.font = pygame.font.Font (None, 60) #pygame.font.Font(file, size) est une fonctionnalité de cgarger uene police et taille de la police
        self.title_font = pygame.font.Font (None,80) #pygame.font.Font(file, size) est une fonctionnalité de cgarger uene police et taille de la police
        self.play_button_rect = pygame.Rect(WIDTH // 2 -50, HEIGHT // 2 + 275, 200, 50) # dimension pour le bouton play largeur 200pixels et hauteur = 100pixels
        
        self.background_image = pygame.image.load("assets/accc.jpg").convert_alpha()  
        self.background_image = pygame.transform.smoothscale(self.background_image, (WIDTH, HEIGHT+MENU_HEIGHT)) # Adapter à la taille de l'écran
        
    def draw (self) : 
        self.screen.blit(self.background_image, (0, 0)) # afficher l'image en arriere plan 
       
        pygame.draw.rect(self.screen, (0, 255, 0), self.play_button_rect) #On dessine le rectangle PLAY avec ses dimension
        play_text = self.font.render("JOUER !!!", True, (0, 0, 0)) #Pour écrire PLAY avec ses dimension 
        self.screen.blit(play_text, (self.play_button_rect.x+5, self.play_button_rect.y +10))

        pygame.display.flip()
        
    def handle_events(self):
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):
                    return "play"  # Retourne "play" si le bouton Play est cliqué

        return None 




