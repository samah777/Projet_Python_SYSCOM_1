import pygame
import random
from unit import Unit
from constante import *
from pikachu import *
from salameche import *
from carapuce import *
from vision import *
from bulbizzare import *
from magicarpe import *
from quolbutoqe import *
from chausouri import *
from miaous import *

# Définir la couleur des obstacles
OBSTACLE_COLOR = (128, 128, 128)  # Gris


class Trap:
    """
    Classe pour gérer les pièges dans le jeu.
    """

    def __init__(self, icon_path, sound_path):
        """Initialise la position du piège et ses autres attributs."""
        self.positions = []  # Liste des positions des pièges invisibles
        self.visible_traps = []  # Liste des pièges visibles
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'icône
        self.sound = pygame.mixer.Sound(sound_path)  # Charger le son du piège

    def generate_traps(self, grid_size, num_traps, obstacles, valid_positions):
        """ 
        Génère plusieurs pièges à une position valide de la grille (pas un obstacle, ni une unité).
        """
        while len(self.positions) < num_traps:
            pos = random.choice(valid_positions)
            if pos not in obstacles and pos not in self.positions:
                self.positions.append(pos)
                valid_positions.remove(pos)  # Retirer cette position des positions valides

    def check_for_trap(self, x, y):
        """Vérifie si la position donnée contient un piège."""
        return (x, y) in self.positions

    def trigger_trap(self, unit):
        """Déclenche l'effet du piège lorsque l'unité tombe dessus."""
        print(f"{unit.team} unit at ({unit.x}, {unit.y}) stepped on a trap!")
        unit.health -= 4.5  # Par exemple, une réduction de 5 points de vie
        print(f"{unit.team} unit's health is now {unit.health}.")
        
        unit.check_health()
        
        # Rendre le piège visible lorsqu'il est déclenché
        if (unit.x, unit.y) in self.positions:
            self.visible_traps.append((unit.x, unit.y))
            # self.positions.remove((unit.x, unit.y))  # Retirer le piège de la liste des pièges invisibles
            self.sound.play()  # Jouer le son du piège

    def draw(self, screen):
        """Dessine les pièges visibles sur l'écran."""
        for trap_position in self.visible_traps:
            # Dessiner chaque piège à sa position (en utilisant son icône)
            screen.blit(self.icon, (trap_position[0] * CELL_SIZE, trap_position[1] * CELL_SIZE))


class Obstacle:
    """
    Classe pour gérer les obstacles dans le jeu.
    """

    def __init__(self, image_path):
        """Initialise la liste des positions des obstacles et charge l'image de l'obstacle."""
        self.positions = []  # Liste des positions des obstacles
        self.obstacle_image = pygame.image.load(image_path)  # Charger l'image de l'obstacle
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'image à la taille de la cellule

    def generate_obstacles(self, grid_size, num_obstacles, unit_positions):
        """
        Génère des obstacles aléatoires sur la grille, en excluant les positions des unités.
        """
        self.positions = []
        while len(self.positions) < num_obstacles:
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - 1)
            if (x, y) not in self.positions and (x, y) not in unit_positions:  # Exclure les positions des unités
                self.positions.append((x, y))

    def is_obstacle(self, x, y):
        """Vérifie si une case est un obstacle."""
        return (x, y) in self.positions

    def draw(self, screen):
        """Dessine les obstacles sur l'écran en utilisant l'image."""
        for x, y in self.positions:
            screen.blit(self.obstacle_image, (x * CELL_SIZE, y * CELL_SIZE))  # Dessiner l'image de l'obstacle à la position correspondante


class Game:
    """
    Classe pour représenter le jeu.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.
        """
        self.screen = screen
        
        # Initialiser les obstacles et les positions valides
        self.background = pygame.image.load('assets/background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
   
        # Créer les unités (avant de générer les positions valides)
        self.player_units = [Pikachu(5, 3), Salameche(6,3), Carapuce(7,3), Bulbizarre(8, 3)]
        self.enemy_units = [Magicarpe(6,11), Qulbutoke(7,11), Chovsouris(8,11), Miaouss(9,11)]

        # Générer les positions valides (unités et obstacles exclus)
        self.obstacles = Obstacle('assets/obstacle.png')
        self.valid_positions = self.generate_valid_positions()
        self.obstacles.generate_obstacles(GRID_SIZE, num_obstacles=30, unit_positions=self.get_unit_positions())
        
           
        # Créer un piège aléatoire
        self.trap = Trap('assets/trap.png', 'assets/trap_sound.mp3')
        self.trap.generate_traps(GRID_SIZE, num_traps=4, obstacles=self.obstacles.positions, valid_positions=self.valid_positions)
        
        
    def get_unit_positions(self):
        """Retourne la liste des positions occupées par les unités."""
        unit_positions = []
        for unit in self.player_units + self.enemy_units:
            unit_positions.append((unit.x, unit.y))
        return unit_positions

    def generate_valid_positions(self):
        """Génère toutes les positions valides sur la grille."""
        valid_positions = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if not self.obstacles.is_obstacle(x, y) and not self.is_unit_occupied(x, y):
                    valid_positions.append((x, y))
        return valid_positions

    def is_unit_occupied(self, x, y):
        """Vérifie si une unité existe déjà à cette position."""
        for unit in self.player_units + self.enemy_units:
            if unit.x == x and unit.y == y:
                return True
        return False
    
    def is_unit_visible(self, unit, vision_sources):
        """
        Vérifie si une unité est visible depuis une liste de sources de vision.
    
        Paramètres
        ----------
        unit : Unit
            L'unité à vérifier.
        vision_sources : list[Unit]
            Liste des unités dont le champ de vision est considéré.
    
        Retourne
        --------
        bool
            True si l'unité est visible, False sinon.
        """
        for source in vision_sources:
            if (unit.x, unit.y) in source.vision.get_visible_positions():
                return True
        return False
    
    
    def handle_player_turn(self):
        
        current_turn='player'
        """Tour du joueur"""
        selected_pik = self.player_units[0]
        for selected_unit in self.player_units[:]:  # Utilisation d'une copie de la liste pour éviter les problèmes lors de la suppression d'unités
            # Vérifier si l'unité est en vie avant de lui permettre de jouer
            if selected_unit.health <= 0:  # Si l'unité est morte
                print(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is dead.")
                self.player_units.remove(selected_unit)  # Retirer l'unité morte de la liste
                continue  # Passer à l'unité suivante
    
            selected_unit.is_selected = True  # Sélectionner l'unité
            has_acted = False  # Flag pour vérifier si l'unité a agi
            self.flip_display(current_turn)  # Afficher l'écran avant que l'unité n'agisse
    
            while not has_acted:  # Tant que l'unité n'a pas terminé son tour
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
    
                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                        elif event.key == pygame.K_d:
                            selected_pik.special_defense()  # Activer la défense avec la touche D
        
                        # Vérifier si l'unité est en vie avant de lui permettre de se déplacer
                        if selected_unit.health > 0:
                            selected_unit.move(dx, dy, self)  # Déplacer l'unité
                            # Vérifier si l'unité est tombée sur un piège
                            if self.trap.check_for_trap(selected_unit.x, selected_unit.y):
                                self.trap.trigger_trap(selected_unit)  # Déclencher le piège et réduire les points de vie
                                if selected_unit.health <= 0:  # Si l'unité meurt après le piège
                                    self.player_units.remove(selected_unit)
                                    continue  # Passer à l'unité suivante
                    
                        # Afficher les changements
                        self.flip_display(current_turn)
    
                        # Si l'unité a appuyé sur la barre d'espace, elle attaque l'ennemi
                        if (event.key == pygame.K_SPACE) or(selected_unit.health <= 0) :
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
    
                            # L'unité a agi, on termine son tour
                            has_acted = True
                            selected_unit.is_selected = False  # L'unité n'est plus sélectionnée



    
    # def handle_enemy_turn(self):
    #     """IA très simple pour les ennemis."""
    #     for enemy in self.enemy_units[:]:  # Itérer sur une copie de la liste pour gérer les suppressions
    #         if enemy.health <= 0:  # Vérification immédiate de la mort de l'ennemi
    #             self.enemy_units.remove(enemy)  # Retirer l'ennemi mort de la liste
    #             continue  # Passer à l'ennemi suivant
    
    #         target = random.choice(self.player_units)
    #         dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
    #         dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
    #         enemy.move(dx, dy, self)
    
    #         # Vérification si l'ennemi est tombé sur un piège
    #         if self.trap.check_for_trap(enemy.x, enemy.y):
    #             self.trap.trigger_trap(enemy)
    
    #         if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
    #             enemy.attack(target)
    #             if target.health <= 0:
    #                 self.player_units.remove(target)


    def handle_enemy_turn(self):
        
        current_turn='enemy'
        
        """Tour de l'adversaire (contrôlé par un autre joueur)."""
        for selected_unit in self.enemy_units[:]:  # Utilisation d'une copie de la liste pour éviter les problèmes lors de la suppression d'unités
            # Vérifier si l'unité est en vie avant de lui permettre de jouer
            if selected_unit.health <= 0:  # Si l'unité est morte
                print(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is dead.")
                self.enemy_units.remove(selected_unit)  # Retirer l'unité morte de la liste
                continue  # Passer à l'unité suivante
    
            selected_unit.is_selected = True  # Sélectionner l'unité
            has_acted = False  # Flag pour vérifier si l'unité a agi
            self.flip_display(current_turn)  # Afficher l'écran avant que l'unité n'agisse
    
            while not has_acted:  # Tant que l'unité n'a pas terminé son tour
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
    
                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:  # Déplacement à gauche
                            dx = -1
                        elif event.key == pygame.K_RIGHT:  # Déplacement à droite
                            dx = 1
                        elif event.key == pygame.K_UP:  # Déplacement vers le haut
                            dy = -1
                        elif event.key == pygame.K_DOWN:  # Déplacement vers le bas
                            dy = 1
    
                        # Vérifier si l'unité est en vie avant de lui permettre de se déplacer
                        if selected_unit.health > 0:
                            selected_unit.move(dx, dy, self)  # Déplacer l'unité
                            # Vérifier si l'unité est tombée sur un piège
                            if self.trap.check_for_trap(selected_unit.x, selected_unit.y):
                                self.trap.trigger_trap(selected_unit)  # Déclencher le piège et réduire les points de vie
                                if selected_unit.health <= 0:  # Si l'unité meurt après le piège
                                    self.enemy_units.remove(selected_unit)
                                    continue
                        
                        # Afficher les changements
                        self.flip_display(current_turn)

                        if event.key == pygame.K_SPACE:
                            player_pik =  self.player_units[0]
                            if (abs(selected_unit.x - player_pik.x) <= 1 and abs(selected_unit.y - player_pik.y) <= 1) and (player_pik.is_defending):
                                player_pik.deactivate_defense()
                            elif (abs(selected_unit.x - player_pik.x) <= 1 and abs(selected_unit.y - player_pik.y) <= 1) and (not(player_pik.is_defending)):
                                 selected_unit.attack(player_pik)
                                 if player_pik.health <= 0:
                                    self.player_units.remove(player_pik)

                            for player_unit in self.player_units[1:]:
                                if (abs(selected_unit.x - player_unit.x) <= 1 and abs(selected_unit.y - player_unit.y) <= 1):
                                    selected_unit.attack(player_unit)
                                    if player_unit.health <= 0:
                                        self.player_units.remove(player_unit)
    
                            # L'unité a agi, on termine son tour
                            has_acted = True
                            selected_unit.is_selected = False  # L'unité n'est plus sélectionnée



    # 1 seul joueur avec l'ia
    # def flip_display(self):
    #     """Affiche le jeu."""
    #     self.screen.fill(BLACK)
    
    #     # Dessiner l'image de fond
    #     self.screen.blit(self.background, (0, 0))
    
    #     # Dessiner la grille
    #     for x in range(0, WIDTH, CELL_SIZE):
    #         for y in range(0, HEIGHT, CELL_SIZE):
    #             rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    #             pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    #     # Dessiner le champ de vision des unités sélectionnées
    #     for unit in self.player_units + self.enemy_units:
    #         if unit.is_selected:
    #             unit.vision.draw(self.screen)
    
    #     # Dessiner les obstacles
    #     self.obstacles.draw(self.screen)
    
    #     # Dessiner les pièges visibles
    #     self.trap.draw(self.screen)
    
    #     # Dessiner uniquement les unités visibles
    #     for unit in self.player_units + self.enemy_units:
    #         if unit.team == "player" or (
    #             unit.team == "enemy" and self.is_unit_visible(unit)
    #         ):
    #             unit.draw(self.screen)
    
    #     pygame.display.flip()
    
    #2 joueurs

    def flip_display(self, current_turn):
        """
        Affiche le jeu, ne montrant les unités adverses que si elles sont dans le champ de vision.
    
        Paramètres
        ----------
        current_turn : str
            Identifie à qui appartient le tour actuel ('player' ou 'enemy').
        """
        self.screen.fill(BLACK)
    
        # Dessiner l'image de fond
        self.screen.blit(self.background, (0, 0))
    
        # Dessiner la grille
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
    
        # Dessiner le champ de vision des unités sélectionnées
        for unit in self.player_units + self.enemy_units:
            if unit.is_selected:
                unit.vision.draw(self.screen)
    
        # Dessiner les obstacles
        self.obstacles.draw(self.screen)
    
        # Dessiner les pièges visibles
        self.trap.draw(self.screen)
        
        # Dessiner les unités visibles en fonction du tour
        if current_turn == "player":
            for unit in self.player_units:
                unit.draw(self.screen)  # Dessiner toutes les unités des joueurs
            for enemy in self.enemy_units:
                if self.is_unit_visible(enemy, self.player_units):  # Vérifie si visible par un joueur
                    enemy.draw(self.screen)
    
        elif current_turn == "enemy":
            for enemy in self.enemy_units:
                enemy.draw(self.screen)  # Dessiner toutes les unités ennemies
            for unit in self.player_units:
                if self.is_unit_visible(unit, self.enemy_units):  # Vérifie si visible par un ennemi
                    unit.draw(self.screen)
    
        pygame.display.flip()



        
def main():

    # Initialisation de Pygame
    pygame.init()
    

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)
    
    print("Position des pièges générés :")
    for trap_position in game.trap.positions:
            print(trap_position)  # Affiche les positions des pièges générés
    
    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()

if __name__ == "__main__":
    main()

