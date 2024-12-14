import pygame
from constante import *
from unit import Unit
from vision import *
from Skill import *


class Magicarpe(Unit):
    """
    Classe représentant Magicarpe, héritant de Unit.
    """

    def __init__(self, x, y,console):
        """
        Initialise Magicarpe avec des caractéristiques spécifiques.

        Paramètres
        ----------
        x : int
            Position x de Magicarpe sur la grille.
        y : int
            Position y de Magicarpe sur la grille.
        """
        # Caractéristiques spécifiques à Magicarpe
        self.n=2

        health = 10
        self.cooldown=2
        health_max = 10
        self.attack_power = 2.5
        velocity = 2
        self.team = 'enemy'
        self.attack_range = 3  # Portée de l'attaque en nombre de cases
        self.invulnerable_turns=0

        # Charger l'image dans self.icon
        icon_path = 'assets/Magicarpe.png'
        self.icon = pygame.image.load(icon_path)  # Charger l'image depuis le chemin
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionner
        self.transformed_icon = pygame.image.load('assets/leviator.png')
        self.transformed_icon = pygame.transform.scale(self.transformed_icon, (CELL_SIZE, CELL_SIZE))
        
        
        self.transformation_sound = pygame.mixer.Sound('assets\evolution\pokemon.mp3')
        # Appeler le constructeur parent avec une icône spécifique à Magicarpe
        super().__init__(x, y, health, health_max, self.attack_power, velocity,self.team ,self.icon, self.transformed_icon, self.transformation_sound,console)
        
        attack_offensive = Skill(name="Charge", attack_range=self.attack_range, damage=self.attack_power, cooldown=self.cooldown,effect="attack", effect_value=5)
        self.add_skills([attack_offensive])
        # Supposons qu'on ait déjà ajouté une compétence offensive
        # On ajoute maintenant une compétence défensive
        attack_defensive =Skill(name="Protéction", attack_range=self.attack_range, damage=self.attack_power, cooldown=self.cooldown,effect="shield", effect_value=2)
        self.add_skills([attack_defensive])
        
        attack_special =Skill(name="Cascade", attack_range=self.attack_range, damage=self.attack_power+1, cooldown=self.cooldown,effect="stun", effect_value=1)
        self.add_skills([attack_special])



    def transform(self):
        """Transforme l'unité en une version plus puissante."""
        if self.transformed_icon and not self.is_transformed:
            print(f"{self.team} unit at ({self.x}, {self.y}) transforms!")
            self.console.add_message(f"{self.team} unit at ({self.x}, {self.y}) transforms!")
            self.icon = self.transformed_icon  # Changer l'icône
            
            
            self.health+= 2  # Exemple : augmenter la puissance d'attaque
            self.skills[0]= Skill(name="Charge", attack_range=self.attack_range+1, damage=5, cooldown=self.cooldown+1,effect="attack", effect_value=5)
            self.skills[1]= Skill(name="Protéctionr", attack_range=self.attack_range+1, damage=0, cooldown=self.cooldown,effect="shield", effect_value=2)
            self.skills[2]= Skill(name="Cascade", attack_range=self.attack_range+1, damage=6, cooldown=self.cooldown+1,effect="attack", effect_value=5)
            
            
            self.is_transformed = True  # Marquer l'unité comme transformée
            # Jouer le son de transformation
        if self.transformation_sound:
            pygame.mixer.Sound(self.transformation_sound).play()
            
            
    def check_health(self):
        # Vérifier si l'unité doit se transformer
        if self.health <= 0:
            print(f"magicarpe unit at ({self.x}, {self.y}) died!")  # L'unité est morte
            self.console.add_message(f"{self.team} unit at ({self.x}, {self.y}) died!")
        elif self.health == 1 and not self.is_transformed:
            self.transform()  # Transforme l'unité si elle atteint 1 PV

    def move(self, dx, dy, game):
        """
        Déplace Magicarpe de dx, dy si la position cible est valide (pas d'obstacle).

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

    # def show_attack_range(self, screen):
    #     """
    #     Affiche la portée de l'attaque de Magicarpe avec des cases rouges claires.

    #     Paramètres
    #     ----------
    #     screen : pygame.Surface
    #         L'écran sur lequel dessiner.
    #     """
    #     light_red = (255, 102, 102)  # Rouge clair
    #     for dx in range(-self.attack_range, self.attack_range + 1):
    #         for dy in range(-self.attack_range, self.attack_range + 1):
    #             if abs(dx) + abs(dy) <= self.attack_range:  # Vérifie que la case est dans la portée
    #                 target_x = self.x + dx
    #                 target_y = self.y + dy
    #                 if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:  # Vérifie que la case est valide
    #                     pygame.draw.rect(
    #                         screen, light_red,  # Rouge clair pour Magicarpe
    #                         (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
    #                         3  # Épaisseur de la bordure
    #                     )

    # def draw(self, screen):
    #     """
    #     Dessine Magicarpe et affiche sa portée si sélectionné.

    #     Paramètres
    #     ----------
    #     screen : pygame.Surface
    #         L'écran sur lequel dessiner.
    #     """
    #     # Si Magicarpe est sélectionné, montrer sa portée d'attaque
    #     if self.is_selected:
    #         self.show_attack_range(screen)

    #     # Dessiner l'icône avec la méthode parent
    #     super().draw(screen)