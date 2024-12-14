import pygame
import random
from constante import *
from vision import *
from console import Console


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, health_max, attack_power,velocity, team, icon,transformed_icon=None,transformation_sound=None,console=None):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.is_using_skill = False
        self.icon = icon #ico
        self.health_max = health_max
        self.vision = Vision(self, GRID_SIZE)  # Champ de vision associé
        self.velocity = velocity
        self.vision = Vision(self, GRID_SIZE)  # Champ de vision associé
        self.transformed_icon = transformed_icon  if transformed_icon else None  # Icône pour l'unité transformée
        self.transformation_sound = transformation_sound  # Fichier son pour la transformation
        self.is_transformed = False  # Indique si l'unité est transformée*
        self.skills=[]
        self.current_cooldowns = {}
        self.stunned_turns = 0  # Nombre de tours où l'unité est étourdie
        self.invulnerable_turns = 0  # Nombre de tours où l'unité est invulnérable
        self.console=console
        
        
        
        
        
        
        
    def transform(self):
        """Transforme l'unité en une version plus puissante."""
        if self.transformed_icon and not self.is_transformed:
            print(f"{self.team} unit at ({self.x}, {self.y}) transforms!")
            self.console.add_message(f"{self.team} unit at ({self.x}, {self.y}) transforms!")
            self.icon = self.transformed_icon  # Changer l'icône
            # self.attack += 2  # Exemple : augmenter la puissance d'attaque
            # self.health += 4
            self.is_transformed = True  # Marquer l'unité comme transformée
            # Jouer le son de transformation
        if self.transformation_sound:
            pygame.mixer.Sound(self.transformation_sound).play()
    
    
    def reduce_cooldowns(self):
        for skill_name in self.current_cooldowns:
            if self.current_cooldowns[skill_name] > 0:
                self.current_cooldowns[skill_name] -= 1
    def add_skills(self, skills):
        """
        Ajoute des compétences à l'unité et initialise leurs cooldowns.
        
        Paramètres
        ----------
        skills : list[Skill]
            Liste des compétences à ajouter.
        """
        for skill in skills:
            self.skills.append(skill)
            self.current_cooldowns[skill.name] = 0  # Initialiser le cooldown à 0



            
    def check_health(self):
        # Vérifier si l'unité doit se transformer
        if self.health <= 0:
            
            # Log de la mort
            self.console.add_message("zebi")
            print(f"{self.team} unit at ({self.x}, {self.y}) is dead!")
            self.console.add_message(f"{self.team} unit at ({self.x}, {self.y}) is dead!")
    
            # Supprimer l'unité des listes actives
            if self.team == 'player':
                game.player_units.remove(self)
                
            elif self.team == 'enemy':
                self.console.add_message("zebi")
                game.enemy_units.remove(self)
            self.icon=None
            game.flip_display(self.team)
        elif self.health == 1 and not self.is_transformed:
            self.transform()  # Transforme l'unité si elle atteint 1 PV
    
    
    def update_movement_square(self, grid_size):
        """
        Met à jour le carré de mouvement autorisé pour cette unité en fonction de sa position actuelle.
    
        Paramètres
        ----------
        grid_size : int
            Taille de la grille (pour éviter de dépasser les limites).
        """
        self.movement_square = []  # Réinitialiser le carré
        for dx in range(-self.n, self.n + 1):
            for dy in range(-self.n, self.n + 1):
                x, y = self.x + dx, self.y + dy
                if 0 <= x < grid_size and 0 <= y < grid_size:  # S'assurer que la position est dans la grille
                    self.movement_square.append((x, y))



    def move(self, dx, dy, game):
        new_x = self.x + dx
        new_y = self.y + dy
        if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and
                not game.obstacles.is_obstacle(new_x, new_y)):
            self.x = new_x
            self.y = new_y


    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power
    
    
    
    
    def apply_damage(self, target, damage):
        if target.invulnerable_turns > 0:
            print(f"{target.team} unit is invulnerable and takes no damage!")
            self.console.add_message(f"{target.team} unit is invulnerable and takes no damage!")
            return
        
        # Si pas invulnérable, on applique les dégâts
        target.health -= damage
        print(f"{self.team} unit attacked {target.team} unit at ({target.x}, {target.y}). Damage: {damage}. Remaining health: {target.health}")
        self.console.add_message(f"{self.team} unit attacked {target.team} unit at ({target.x}, {target.y}). Damage: {damage}. Remaining health: {target.health}") 
        
        if target.health <= 0:
            print(f"{target.team} unit at ({target.x}, {target.y}) is dead.")
            
            
            self.console.add_message(f"{target.team} unit at ({target.x}, {target.y}) is dead.")

            

    

    
    

        

            
    # def check_death(self, game):
    #     """Vérifie si l'unité est morte et la retire de la liste des unités actives."""
    #     if self.health <= 0:
    #         print(f"{self.team} unit at ({self.x}, {self.y}) is dead!")
    #         self.console.add_message(f"{self.team} unit at ({self.x}, {self.y}) is dead!")
    #         if self.team == 'player':
    #             game.player_units.remove(self)
    #         else:
    #             game.enemy_units.remove(self)
    #         return True
    #     return False
    
    def show_movement_range(self, screen):
        """
        Affiche les cases où l'unité peut se déplacer en bleu.
    
        Paramètres
        ----------
        screen : pygame.Surface
            L'écran sur lequel dessiner.
        """
        for x, y in self.movement_square:
            pygame.draw.rect(
                screen, (0, 0, 255),  # Bleu pour les cases de mouvement
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                2  # Épaisseur de la bordure
            )



            
    def draw(self, screen):
        """
        Dessine l'unité et affiche sa portée si une compétence est utilisée ou sa zone de déplacement.
    
        Paramètres
        ----------
        screen : pygame.Surface
            L'écran sur lequel dessiner.
        """
        # Afficher la zone de déplacement en bleu si l'unité est sélectionnée
        if self.is_selected:
            self.show_movement_range(screen)
        # Afficher la portée si une compétence est utilisée
        if self.is_using_skill:
            self.show_attack_range(screen)
    

    
        # Dessiner un rectangle vert pour les joueurs et rouge pour les ennemis
        if self.is_selected:
            rect_color = (0, 255, 0) if self.team == 'player' else (255, 0, 0)
            pygame.draw.rect(screen, rect_color, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
        # Dessiner l'icône
        if self.icon:
            screen.blit(self.icon, (self.x * CELL_SIZE, self.y * CELL_SIZE))

    
        # Dessiner la barre de vie
        health_ratio = max(self.health / 10, 0)  # Ratio de santé entre 0 et 1
        health_bar_width = int(CELL_SIZE * health_ratio)
        pygame.draw.rect(screen, (255, 0, 0), (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, CELL_SIZE, 5))  # Fond rouge
        pygame.draw.rect(screen, (0, 255, 0), (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, health_bar_width, 5))  # Barre verte




        
    def show_attack_range(self, screen):
        """
        Affiche la portée de l'attaque avec une couleur spécifique selon l'équipe.
    
        Paramètres
        ----------
        screen : pygame.Surface
            L'écran sur lequel dessiner.
        """
        # Choisir la couleur selon l'équipe
        range_color = (255, 255, 0) if self.team == 'player' else (255, 0, 0)  # Jaune pour les joueurs, rouge pour les ennemis
        
        for dx in range(-self.attack_range, self.attack_range + 1):
            for dy in range(-self.attack_range, self.attack_range + 1):
                if abs(dx) + abs(dy) <= self.attack_range:  # Vérifie que la case est dans la portée
                    target_x = self.x + dx
                    target_y = self.y + dy
                    if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:  # Vérifie que la case est valide
                        pygame.draw.rect(
                            screen, range_color,  # Couleur selon l'équipe
                            (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                            3  # Épaisseur de la bordure
                        )





