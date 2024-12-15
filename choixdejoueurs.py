import pygame
from constante import *  # Contient WIDTH, HEIGHT, etc.

def get_font(size):
    """Renvoie une police avec la taille spécifiée."""
    return pygame.font.Font("assets/font.ttf", size)

class SelectionMenu:
    """
    Classe pour gérer le menu de sélection des Pokémon.
    """

    def __init__(self, screen, available_pokemons,current_player):
        """
        Initialise le menu de sélection des Pokémon.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de l'écran où afficher le menu.
        available_pokemons : list
            Liste des classes des Pokémon disponibles pour la sélection.
        """
        self.screen = screen
        self.available_pokemons = available_pokemons
        self.selected_pokemons = []  # Pokémon sélectionnés par l'utilisateur.
        self.max_selection = 4  # Nombre maximum de Pokémon sélectionnés.
        self.font = get_font(30)  # Police pour le texte.
        self.alert_font = get_font(20)  # Police pour les messages d'alerte.
        self.selection_font = get_font(25)  # Police pour les instructions.
        self.current_player = current_player
        # Commence avec Joueur 1

        # Charger les sprites des Pokémon
        self.pokemon_sprites = {
            pokemon_class.__name__: pygame.transform.scale(
                pygame.image.load(f"assets/sprites/{pokemon_class.__name__}.png").convert_alpha(), (55, 55)
            )
            for pokemon_class in self.available_pokemons
        }

    def draw_menu(self):
        """
        Affiche le menu de sélection à l'écran.
        """
        self.screen.fill((0, 0, 0))  # Fond noir.

        # Affiche le titre.
        title = self.font.render("Choisissez vos Pokémon (Max 4) : ", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        # Texte du joueur en cours
        joueur_text = f" Joueur {self.current_player} "
        joueur_color = (0, 255, 0)  if self.current_player ==1 else (255,0,0)
        Joueur = self.font.render(joueur_text, True, joueur_color)
        self.screen.blit(Joueur, (WIDTH , 20))  # Positionnement centré

        # Affiche les Pokémon disponibles
        y_offset = 100
        for i, pokemon_class in enumerate(self.available_pokemons):
            # Sprite du Pokémon
            sprite = self.pokemon_sprites[pokemon_class.__name__]
            self.screen.blit(sprite, (50, y_offset + i * 60))

            # Nom du Pokémon
            color = (255, 255, 255) if pokemon_class not in self.selected_pokemons else (0, 255, 0)
            pokemon_name = self.font.render(pokemon_class.__name__, True, color)
            self.screen.blit(pokemon_name, (100, y_offset + i * 60))

        # Instructions
        instructions = self.selection_font.render(
            "Cliquez pour sélectionner, appuyez sur Entrée pour valider",
            True, (255, 255, 255)
        )
        self.screen.blit(instructions, (50, HEIGHT - 80))

        # Affiche les Pokémon sélectionnés
        selected_title = self.font.render("Sélectionnés :", True, (255, 255, 0))
        self.screen.blit(selected_title, (WIDTH - 300, 100))
        for i, pokemon_class in enumerate(self.selected_pokemons):
            sprite = self.pokemon_sprites[pokemon_class.__name__]
            self.screen.blit(sprite, (WIDTH - 350, 140 + i * 60))
            selected_name = self.font.render(pokemon_class.__name__, True, (0, 255, 0))
            self.screen.blit(selected_name, (WIDTH - 300, 140 + i * 60))

        # Message d'alerte si nécessaire
        if len(self.selected_pokemons) == self.max_selection:
            alert = self.alert_font.render("Max atteint ! Appuyez sur Entrée pour valider.", True, (255, 0, 0))
            self.screen.blit(alert, (100, HEIGHT - 50))

        # Compteur de sélection
        progress_text = self.font.render(
            f"Pokémon sélectionnés : {len(self.selected_pokemons)} / {self.max_selection}",
            True, (255, 255, 255)
        )
        self.screen.blit(progress_text, (WIDTH // 2 - progress_text.get_width() // 2, HEIGHT - 120))

        pygame.display.flip()

    def handle_events(self):
        """
        Gère les événements utilisateur pour sélectionner les Pokémon.

        Retourne
        --------
        bool
            True si la sélection est validée (Entrée appuyée).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtenir la position de la souris.
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Vérifier si un Pokémon a été cliqué.
                y_offset = 100
                for i, pokemon_class in enumerate(self.available_pokemons):
                    pokemon_name_rect = pygame.Rect(50, y_offset + i * 60, 250, 50)
                    if pokemon_name_rect.collidepoint(mouse_x, mouse_y):
                        if pokemon_class in self.selected_pokemons:
                            self.selected_pokemons.remove(pokemon_class)  # Retirer si déjà sélectionné.
                        elif len(self.selected_pokemons) < self.max_selection:
                            self.selected_pokemons.append(pokemon_class)  # Ajouter si pas au max.

            if event.type == pygame.KEYDOWN:
                # Appuyer sur Entrée pour valider la sélection.
                if event.key == pygame.K_RETURN and len(self.selected_pokemons) == self.max_selection:
                    return True
                # Appuyer sur Échap pour quitter.
                if event.key == pygame.K_ESCAPE:
                    return False

        return False

    def transition_effect(self):
        """
        Ajoute un effet de transition avec un fondu au noir lors de la validation.
        """
        fade_surface = pygame.Surface((WIDTH + 600, HEIGHT + MENU_HEIGHT))
        fade_surface.fill((0, 0, 0))  # Couleur noire
        self.current_player=2

        for alpha in range(0, 255, 10):  # Graduellement augmenter l'opacité
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(50)  # Délai pour lisser la transition


     

    def run(self):
        """
        Affiche le menu et retourne les Pokémon sélectionnés.

        Retourne
        --------
        list
            Liste des classes des Pokémon sélectionnés.
        """
        while True:
            self.draw_menu()
            if self.handle_events():
                self.transition_effect()
                return self.selected_pokemons
