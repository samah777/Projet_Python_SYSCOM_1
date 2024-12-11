import pygame
import random
from constante import *
from vision import *



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

    def __init__(self, x, y, health, health_max, attack_power,velocity, team, icon,transformed_icon=None,transformation_sound=None):
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
            print(f"{unit.team} unit at ({unit.x}, {unit.y}) died!")  # L'unité est morte
        elif self.health == 1 and not self.is_transformed:
            self.transform()  # Transforme l'unité si elle atteint 1 PV


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
            return
        
        # Si pas invulnérable, on applique les dégâts
        target.health -= damage
        print(f"{self.team} unit attacked {target.team} unit at ({target.x}, {target.y}). Damage: {damage}. Remaining health: {target.health}")
        
        if target.health <= 0:
            print(f"{target.team} unit at ({target.x}, {target.y}) is dead.")

    

    
    

        

            
    def check_death(self, game):
        """Vérifie si l'unité est morte et la retire de la liste des unités actives."""
        if self.health <= 0:
            print(f"{self.team} unit at ({self.x}, {self.y}) is dead!")
            if self.team == 'player':
                game.player_units.remove(self)
            else:
                game.enemy_units.remove(self)
            return True
        return False


            
    def draw(self, screen):
        """Affiche l'unité sur l'écran avec une barre de vie et une icône."""
        
        # Si l'unité est sélectionnée, dessiner un fond vert pour la case
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Si l'unité a une icône, on l'affiche
        if self.icon:
            # Afficher l'icône à l'emplacement de l'unité
            screen.blit(self.icon, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            # Si aucune icône, dessiner un cercle
            color = BLUE if self.team == 'player' else RED
            pygame.draw.circle(screen, color, 
                               (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), 
                               CELL_SIZE // 3)
        
        # Définir une santé maximale par défaut
        max_health = 10  # Exemple : santé maximale
        if not hasattr(self, 'health') or self.health is None:
            self.health = max_health  # Fixe une valeur par défaut si self.health est manquant
    
        # Calculer la largeur de la barre de vie
        health_ratio = max(self.health / max_health, 0)  # Ratio de santé entre 0 et 1
        health_bar_width = int(CELL_SIZE * health_ratio)  # Longueur proportionnelle à la santé
    
        # Dessiner la barre de vie (fond en rouge)
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, CELL_SIZE, 5))
        # Dessiner la barre de santé restante (en vert)
        pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE - 10, health_bar_width, 5))




