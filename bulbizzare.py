import pygame
from constante import *
from unit import Unit
from vision import *

from Skill import *

class Bulbizarre(Unit):
    """
    Classe représentant Bulbizarre, héritant de Unit.
    """

    def __init__(self, x, y,console,team = 'player'):
        """
        Initialise Bulbizarre avec des caractéristiques spécifiques.

        Paramètres
        ----------
        x : int
            Position x de Bulbizarre sur la grille.
        y : int
            Position y de Bulbizarre sur la grille.
        """
        # Caractéristiques spécifiques à Bulbizarre
        self.n=2
        self.name='Bulbizarre'
        health = 10
        self.cooldown=2
        health_max = 10
        self.attack_power = 1.5
        velocity = 2
        
        self.attack_range = 3  # Portée de l'attaque en nombre de cases
        self.invulnerable_turns=0

        # Charger l'image dans self.icon
        icon_path = 'assets/Bulbizarre.png'
        self.icon = pygame.image.load(icon_path)  # Charger l'image depuis le chemin
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Redimensionner

        self.transformed_icon = pygame.image.load('assets/Florizar.png')
        self.transformed_icon = pygame.transform.scale(self.transformed_icon, (CELL_SIZE, CELL_SIZE))
        
        
        self.transformation_sound = pygame.mixer.Sound('assets\evolution\pokemon.mp3')

        # Appeler le constructeur parent avec une icône spécifique à Pikachu
        super().__init__(x, y, health, health_max, self.attack_power, velocity,team ,self.icon, self.transformed_icon, self.transformation_sound,console)
        
        attack_offensive = Skill(name="Tranch'Herbe", attack_range=self.attack_range, damage=self.attack_power, cooldown=self.cooldown,effect="attack", effect_value=5)
        self.add_skills([attack_offensive])
        # Supposons qu'on ait déjà ajouté une compétence offensive
        # On ajoute maintenant une compétence défensive
        attack_defensive =Skill(name="Mur d'herbe", attack_range=self.attack_range, damage=0, cooldown=self.cooldown,effect="shield", effect_value=2)
        self.add_skills([attack_defensive])
        
        attack_special =Skill(name="Mégafouet", attack_range=self.attack_range+2, damage=self.attack_power+2, cooldown=self.cooldown+2,effect="special", effect_value=1)
        self.add_skills([attack_special])

        
        
        
    def transform(self):
        """Transforme l'unité en une version plus puissante."""
        if self.transformed_icon and not self.is_transformed:
            print(f"{self.team} unit at ({self.x}, {self.y}) transforms!")
            self.console.add_message(f"{self.team} {self.name} a ({self.x}, {self.y}) a évolué!")
            self.icon = self.transformed_icon  # Changer l'icône
            
            self.n=3
            self.health+= 3  # Exemple : augmenter la puissance d'attaque
            self.skills[0]= Skill(name="Tranch'Herbe", attack_range=self.attack_range+1, damage=5, cooldown=self.cooldown+1,effect="attack", effect_value=5)
            self.skills[1]= Skill(name="Mur d'herbe", attack_range=self.attack_range+1, damage=0, cooldown=self.cooldown,effect="shield", effect_value=2)
            self.skills[2]= Skill(name="Mégafouet", attack_range=self.attack_range+1, damage=5, cooldown=self.cooldown+3,effect="attack", effect_value=5)
            
            
            self.is_transformed = True  # Marquer l'unité comme transformée
            # Jouer le son de transformation
        if self.transformation_sound:
            pygame.mixer.Sound(self.transformation_sound).play()
            
            
    def check_health(self):
        # Vérifier si l'unité doit se transformer
        if self.health <= 0:
            print(f"magicarpe unit at ({self.x}, {self.y}) died!")  # L'unité est morte
            self.console.add_message(f"{self.team} {self.name}  à ({self.x}, {self.y}) est mort !")
        elif self.health == 1 and not self.is_transformed:
            self.transform()  # Transforme l'unité si elle atteint 1 PV

    def move(self, dx, dy, game):
        """
        Déplace Bulbizarre de dx, dy si la position cible est valide (pas d'obstacle).

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

    def area_attack(self, enemies, attack_range=None, attack_power=None):
        """
        Effectue une attaque de zone sur les ennemis dans une certaine portée.

        Paramètres
        ----------
        enemies : list[Unit]
            Liste des unités ennemies présentes sur la grille.
        attack_range : int, facultatif
            Portée spécifique de l'attaque. Si None, utilise self.attack_range.
        attack_power : int, facultatif
            Puissance spécifique de l'attaque. Si None, utilise self.attack_power.
        """
        effective_range = attack_range if attack_range is not None else self.attack_range
        effective_power = attack_power if attack_power is not None else self.attack_power

        for enemy in enemies:
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)  # Distance de Manhattan
            if distance <= effective_range:
                enemy.health = max(0, enemy.health - effective_power)
                print(f"Enemy at ({enemy.x}, {enemy.y}) hit! Remaining health: {enemy.health}")

    # def show_attack_range(self, screen):
    #     """
    #     Affiche la portée de l'attaque de Bulbizarre avec des cases bleues claires.

    #     Paramètres
    #     ----------
    #     screen : pygame.Surface
    #         L'écran sur lequel dessiner.
    #     """
    #     for dx in range(-self.attack_range, self.attack_range + 1):
    #         for dy in range(-self.attack_range, self.attack_range + 1):
    #             if abs(dx) + abs(dy) <= self.attack_range:  # Vérifie que la case est dans la portée
    #                 target_x = self.x + dx
    #                 target_y = self.y + dy
    #                 if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:  # Vérifie que la case est valide
    #                     pygame.draw.rect(
    #                         screen, (0, 255,0 ),  # Vert clair pour Bulbizarre
    #                         (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
    #                         3  # Épaisseur de la bordure
    #                     )

    # def draw(self, screen):
    #     """
    #     Dessine Bulbizarre et affiche sa portée si sélectionné.

    #     Paramètres
    #     ----------
    #     screen : pygame.Surface
    #         L'écran sur lequel dessiner.
    #     """
    #     # Si Bulbizarre est sélectionné, montrer sa portée d'attaque
    #     if self.is_selected:
    #         self.show_attack_range(screen)

    #     # Dessiner l'icône avec la méthode parent
    #     super().draw(screen)
