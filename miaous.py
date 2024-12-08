import pygame
from constante import *
from unit import Unit
from vision import *

class Miaouss(Unit):
    """
    Classe représentant Miaouss, héritant de Unit.
    """

    def __init__(self, x, y):
        """
        Initialise Miaouss avec des caractéristiques spécifiques.

        Paramètres
        ----------
        x : int
            Position x de Miaouss sur la grille.
        y : int
            Position y de Miaouss sur la grille.
        """
        # Caractéristiques spécifiques à Miaouss
        health = 10
        health_max = 100  # Santé modérée
        attack_power = 2  # Puissance d'attaque supérieure
        velocity = 2  # Vitesse moyenne
        team = 'enemy'  # Miaouss est un ennemi
        self.attack_range = 1  # Portée standard

        # Charger l'image dans self.icon
        icon_path = 'assets/miaous.png'
        self.icon = pygame.image.load(icon_path)  # Charger l'image depuis le chemin
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionner
        self.transformed_icon = pygame.image.load('assets/persian.png')
        self.transformed_icon = pygame.transform.scale(self.transformed_icon, (CELL_SIZE, CELL_SIZE))
        
        
        self.transformation_sound = pygame.mixer.Sound('assets\evolution\pokemon.mp3')
        # Appeler le constructeur parent avec une icône spécifique à Miaouss
        super().__init__(x, y, health, health_max, attack_power,velocity, team, self.icon,self.transformed_icon,self.transformation_sound)


    def transform(self):
        """Transforme l'unité en une version plus puissante."""
        if self.transformed_icon and not self.is_transformed:
            print(f"{self.team} unit at ({self.x}, {self.y}) transforms!")
            self.icon = self.transformed_icon  # Changer l'icône
            # self.attack += 2  # Exemple : augmenter la puissance d'attaque
            # self.health += 4
            self.is_transformed = True  # Marquer l'unité comme transformée
            # Jouer le son de transformation
        if self.transformation_sound:
            pygame.mixer.Sound(self.transformation_sound).play()
            
            
    def check_health(self):
        # Vérifier si l'unité doit se transformer
        if self.health <= 0:
            print(f"miaous unit at ({self.x}, {self.y}) died!")  # L'unité est morte
        elif self.health == 1 and not self.is_transformed:
            self.transform()  # Transforme l'unité si elle atteint 1 PV

    def move(self, dx, dy, game):
        """
        Déplace Miaouss de dx, dy si la position cible est valide (pas d'obstacle).

        Paramètres
        ----------
        dx : int
            Déplacement en x.
        dy : int
            Déplacement en y.
        game : Game
            Instance du jeu, utilisée pour vérifier les obstacles.
        """
        new_x = self.x + dx
        new_y = self.y + dy

        if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
            if not game.obstacles.is_obstacle(new_x, new_y):
                self.x = new_x
                self.y = new_y

    def area_attack(self, players, attack_range=None, attack_power=None):
        """
        Effectue une attaque de zone sur les joueurs dans une certaine portée.

        Paramètres
        ----------
        players : list[Unit]
            Liste des unités joueurs présentes sur la grille.
        attack_range : int, facultatif
            Portée spécifique de l'attaque. Si None, utilise self.attack_range.
        attack_power : int, facultatif
            Puissance spécifique de l'attaque. Si None, utilise self.attack_power.
        """
        effective_range = attack_range if attack_range is not None else self.attack_range
        effective_power = attack_power if attack_power is not None else self.attack_power

        for player in players:
            distance = abs(self.x - player.x) + abs(self.y - player.y)  # Distance de Manhattan
            if distance <= effective_range:
                player.health -= effective_power
                print(f"Player at ({player.x}, {player.y}) hit! Remaining health: {player.health}")

    def show_attack_range(self, screen):
        """
        Affiche la portée de l'attaque de Miaouss avec des cases dorées.

        Paramètres
        ----------
        screen : pygame.Surface
            L'écran sur lequel dessiner.
        """
        gold = (255, 215, 0)  # Couleur dorée
        for dx in range(-self.attack_range, self.attack_range + 1):
            for dy in range(-self.attack_range, self.attack_range + 1):
                if abs(dx) + abs(dy) <= self.attack_range:  # Vérifie que la case est dans la portée
                    target_x = self.x + dx
                    target_y = self.y + dy
                    if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:  # Vérifie que la case est valide
                        pygame.draw.rect(
                            screen, gold,  # Couleur dorée pour Miaouss
                            (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                            10  # Épaisseur de la bordure
                        )

    def draw(self, screen):
        """
        Dessine Miaouss et affiche sa portée si sélectionné.

        Paramètres
        ----------
        screen : pygame.Surface
            L'écran sur lequel dessiner.
        """
        # Si Miaouss est sélectionné, montrer sa portée d'attaque
        if self.is_selected:
            self.show_attack_range(screen)

        # Dessiner l'icône avec la méthode parent
        super().draw(screen)