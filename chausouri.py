import pygame
from constante import *
from unit import Unit
from vision import *

class Chovsouris(Unit):
    """
    Classe représentant Chovsouris, héritant de Unit.
    """

    def __init__(self, x, y):
        """
        Initialise Chovsouris avec des caractéristiques spécifiques.

        Paramètres
        ----------
        x : int
            Position x de Chovsouris sur la grille.
        y : int
            Position y de Chovsouris sur la grille.
        """
        # Caractéristiques spécifiques à Chovsouris
        health = 10
        health_max = 100  # Santé modérée
        attack_power = 2  # Attaque modérée
        velocity = 3  # Vitesse rapide
        team = 'enemy'  # Chovsouris est un ennemi
        self.attack_range = 2  # Portée légèrement augmentée

        # Charger l'image dans self.icon
        icon_path = 'assets/Chovsourir.png'
        self.icon = pygame.image.load(icon_path)  # Charger l'image depuis le chemin
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionner

        # Appeler le constructeur parent avec une icône spécifique à Chovsouris
        super().__init__(x, y, health, health_max, attack_power, velocity, team, self.icon)

    def move(self, dx, dy, game):
        """
        Déplace Chovsouris de dx, dy si la position cible est valide (pas d'obstacle).

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
        Affiche la portée de l'attaque de Chovsouris avec des cases jaunes claires.

        Paramètres
        ----------
        screen : pygame.Surface
            L'écran sur lequel dessiner.
        """
        light_yellow = (255, 255, 102)  # Jaune clair
        for dx in range(-self.attack_range, self.attack_range + 1):
            for dy in range(-self.attack_range, self.attack_range + 1):
                if abs(dx) + abs(dy) <= self.attack_range:  # Vérifie que la case est dans la portée
                    target_x = self.x + dx
                    target_y = self.y + dy
                    if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:  # Vérifie que la case est valide
                        pygame.draw.rect(
                            screen, light_yellow,  # Jaune clair pour Chovsouris
                            (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                            10  # Épaisseur de la bordure
                        )

    def draw(self, screen):
        """
        Dessine Chovsouris et affiche sa portée si sélectionné.

        Paramètres
        ----------
        screen : pygame.Surface
            L'écran sur lequel dessiner.
        """
        # Si Chovsouris est sélectionné, montrer sa portée d'attaque
        if self.is_selected:
            self.show_attack_range(screen)

        # Dessiner l'icône avec la méthode parent
        super().draw(screen)
