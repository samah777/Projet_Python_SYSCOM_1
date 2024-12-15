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
import os
from Skillmenu import SkillMenu
from Menu import *
from buton import *
from trap import *
from PIL import Image
from console import Console
from choixdejoueurs import *


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

    def __init__(self, screen,player_pokemons, enemy_pokemons):
        """
        Construit le jeu avec la surface de la fenêtre.
        """
        self.screen = screen
        self.console = Console(screen)

        self.messages=[]
        
        self.skill_menu = SkillMenu()
        
        # Initialiser les obstacles et les positions valides


        self.background = pygame.image.load('assets/background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.obstacles = Obstacle('assets/obstacle.png')
   
           
        # Créer les unités (avant de générer les positions valides)
        upper_zone = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE // 2)]
        lower_zone = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE // 2, GRID_SIZE)]

        # Filtrer les positions valides dans les zones
        upper_zone = [pos for pos in upper_zone if pos not in self.obstacles.positions]
        lower_zone = [pos for pos in lower_zone if pos not in self.obstacles.positions]

        # Mélanger les positions pour un placement aléatoire
        random.shuffle(upper_zone)
        random.shuffle(lower_zone)

        self.player_units = []
        for pokemon_class in player_pokemons:
            if not callable(pokemon_class) or not isinstance(pokemon_class, type):  # Vérifie que c'est une classe
                raise TypeError(f"Invalid Pokémon class: {pokemon_class}")
            if upper_zone:
                pos = upper_zone.pop()
                self.player_units.append(pokemon_class(pos[0], pos[1], console=self.console, team='player'))
    
        self.enemy_units = []
        for pokemon_class in enemy_pokemons:
            if not callable(pokemon_class) or not isinstance(pokemon_class, type):  # Vérifie que c'est une classe
                raise TypeError(f"Invalid Pokémon class: {pokemon_class}")
            if lower_zone:
                pos = lower_zone.pop()
                self.enemy_units.append(pokemon_class(pos[0], pos[1], console=self.console, team='enemy'))
            
        # Générer les positions valides (unités et obstacles exclus)
        
        self.valid_positions = self.generate_valid_positions()
        
        self.obstacles.generate_obstacles(GRID_SIZE, num_obstacles=30, unit_positions=self.get_unit_positions())
        
           
        # Créer un piège aléatoire
        self.trap = Trap('assets/animations/animation_caitlyne', 'assets/trap_sound.mp3',console=self.console)
        self.trap.generate_traps(GRID_SIZE, num_traps=5, obstacles=self.obstacles.positions, valid_positions=self.valid_positions)

    def highlight_units(self, screen):
        """
        Met en surbrillance les cases des unités alliées et ennemies.
    
        screen : pygame.Surface
            La surface de l'écran où dessiner les surbrillances.
        """
        # Surbrillance verte pour les unités alliées (joueurs)
        for unit in self.player_units:
            rect = pygame.Rect(unit.x * CELL_SIZE, unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)  # Vert, bordure de 2px
    
        # Surbrillance rouge pour les unités ennemies
        for unit in self.enemy_units:
            rect = pygame.Rect(unit.x * CELL_SIZE, unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)  # Rouge, bordure de 2px

            
            
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
    
    
    def check_winner(self):
        """
        Vérifie si une équipe a gagné le jeu.
        Si une équipe est vide, elle perd et l'autre équipe gagne.
        """
        if not self.player_units:  # Si l'équipe des joueurs est vide
            self.display_winner("Enemy Team Wins!")
            return True  # Le jeu est terminé
        elif not self.enemy_units:  # Si l'équipe ennemie est vide
            self.display_winner("Player Team Wins!")
            return True  # Le jeu est terminé
        return False  # Le jeu continue


    def display_winner(self, message):
        """
        Affiche le message de victoire à l'écran et termine le jeu.
        """
        self.screen.fill(BLACK)  # Efface l'écran
        font = pygame.font.Font("assets/font.ttf", 60)  # Charge la police
        text_surface = font.render(message, True, (255, 255, 255))  # Texte blanc
        text_rect = text_surface.get_rect(center=((WIDTH+600) // 2, HEIGHT // 2))  # Centrer le texte
        self.screen.blit(text_surface, text_rect)  # Afficher le texte
        pygame.display.flip()  # Mettre à jour l'écran
    
        # Pause pour afficher le message pendant 3 secondes
        pygame.time.wait(3000)
        pygame.quit()
        exit()




    
    def handle_player_turn(self):
        """
        Gère le tour des unités alliées, permettant de se déplacer, attaquer ou utiliser des compétences.
        """
        current_turn = 'player'
        for selected_unit in self.player_units[:]:
            
            if self.check_winner():
                return
            self.console.add_message("====== Nouvelle unité ======")
            

            # Mettre à jour le carré de mouvement pour l'unité
            selected_unit.update_movement_square(GRID_SIZE)
    
            if selected_unit.health <= 0:
                print(f"{selected_unit.team} unit a ({selected_unit.x}, {selected_unit.y}) est mort.")
                self.console.add_message(f"{selected_unit.team} {selected_unit.name} à ({selected_unit.x}, {selected_unit.y}) est mort.")
                self.player_units.remove(selected_unit)
                continue
    
            if selected_unit.stunned_turns > 0:
                print(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is stunned and cannot act this turn.")
                self.console.add_message(f"{selected_unit.team} {selected_unit.name} à ({selected_unit.x}, {selected_unit.y}) est étourdi et ne peut pas jouer son tour.")
                selected_unit.stunned_turns -= 1
                continue
    
            selected_unit.is_selected = True
            has_acted = False
    
            while not has_acted:
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
    
                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
    
                        # Gestion des déplacements
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
    
                        if dx != 0 or dy != 0:
                            # Calculer la nouvelle position
                            new_x, new_y = selected_unit.x + dx, selected_unit.y + dy
    
                            # Vérifier si la nouvelle position est dans le carré autorisé
                            if (new_x, new_y) in selected_unit.movement_square:
                                selected_unit.move(dx, dy, self)
                                if self.trap.check_for_trap(selected_unit.x, selected_unit.y):
                                    self.trap.trigger_trap(selected_unit)
                                    if selected_unit.health <= 0:
                                        self.player_units.remove(selected_unit)
                                        has_acted = True
                                        break
                            else:
                                print(f"Déplacement interdit à ({new_x}, {new_y}). En dehors du carré de mouvement.")
                                self.console.add_message(f"Déplacement interdit à ({new_x}, {new_y}). En dehors du carré de mouvement.")
    
                        # Utilisation d'une compétence
                        elif event.key == pygame.K_a and selected_unit.skills:
                            skill = selected_unit.skills[0]
                            cooldown = selected_unit.current_cooldowns[skill.name]
                            if cooldown == 0:
                                print(f"Player used skill: {skill.name}")
                                self.console.add_message(f"Player {selected_unit.name}  a utilisé: {skill.name}")
                                self.execute_skill(selected_unit, skill)
                                selected_unit.current_cooldowns[skill.name] = skill.cooldown
                                print(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                has_acted=True
                                
                            else:
                                print(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
    
                        elif event.key == pygame.K_z and len(selected_unit.skills) > 1:
                            skill = selected_unit.skills[1]  # On prend la seconde compétence (défensive)
                            cooldown = selected_unit.current_cooldowns[skill.name]
                            if cooldown == 0:
                                print(f"Player used skill: {skill.name}")
                                self.console.add_message(f"Player {selected_unit.name}  a utilisé: {skill.name}")
                                self.execute_skill(selected_unit, skill)
                                selected_unit.current_cooldowns[skill.name] = skill.cooldown
                                print(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                has_acted=True
                            else:
                                print(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
                                
    
                        elif event.key == pygame.K_e and len(selected_unit.skills) > 2:
                            skill = selected_unit.skills[2]  # On prend la troisième compétence
                            cooldown = selected_unit.current_cooldowns[skill.name]
                            if cooldown == 0:
                                print(f"Player used skill: {skill.name}")
                                self.console.add_message(f"Player {selected_unit.name}  a utilisé: {skill.name}")
                                self.execute_skill(selected_unit, skill)
                                selected_unit.current_cooldowns[skill.name] = skill.cooldown
                                print(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                has_acted=True
                            else:
                                print(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
    
                        elif event.key == pygame.K_SPACE:
                            has_acted = True
                            selected_unit.is_selected = False
    
                    self.trap.update_animation()
                    self.flip_display(current_turn)
    
            selected_unit.is_selected = False

    

    
    
    def handle_enemy_turn(self):
        """
        Gère le tour des unités ennemies.
        """
        
        current_turn = 'enemy'
        for selected_unit in self.enemy_units[:]:
            if self.check_winner():
                return
            self.console.add_message("====== Nouvelle unité ======")
            
            
            # Mettre à jour le carré de mouvement pour l'unité
            selected_unit.update_movement_square(GRID_SIZE)
    
            if selected_unit.health <= 0:
                print(f"{selected_unit.team} {selected_unit.name} à ({selected_unit.x}, {selected_unit.y}) est mort.")
                self.console.add_message(f"{selected_unit.team} {selected_unit.name} à ({selected_unit.x}, {selected_unit.y}) est mort.")
                self.enemy_units.remove(selected_unit)
                continue
            if selected_unit.stunned_turns > 0:
                print(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is stunned and cannot act this turn.")
                self.console.add_message(f"{selected_unit.team} {selected_unit.name} à ({selected_unit.x}, {selected_unit.y}) est étourdi et ne peut pas jouer son tour.")
                selected_unit.stunned_turns -= 1
                continue
    
            selected_unit.is_selected = True
            has_acted = False
    
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
    
                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
    
                        # Gestion des déplacements
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
    
                        if dx != 0 or dy != 0:
                            # Calculer la nouvelle position
                            new_x, new_y = selected_unit.x + dx, selected_unit.y + dy
    
                            # Vérifier si la nouvelle position est dans le carré autorisé
                            if (new_x, new_y) in selected_unit.movement_square:
                                selected_unit.move(dx, dy, self)
                                if self.trap.check_for_trap(selected_unit.x, selected_unit.y):
                                    self.trap.trigger_trap(selected_unit)
                                    if selected_unit.health <= 0:
                                        self.enemy_units.remove(selected_unit)
                                        has_acted = True
                                        break
                            else:
                                print(f"Déplacement interdit à ({new_x}, {new_y}). En dehors du carré de mouvement.")
                                self.console.add_message(f"Déplacement interdit à ({new_x}, {new_y}). En dehors du carré de mouvement.")
    
                        # Utilisation d'une compétence
                        elif event.key == pygame.K_a and selected_unit.skills:
                            skill = selected_unit.skills[0]
                            cooldown = selected_unit.current_cooldowns[skill.name]
                            if cooldown == 0:
                                print(f"Enemy {selected_unit.name} used skill: {skill.name}")
                                self.console.add_message(f"Enemy {selected_unit.name} used skill: {skill.name}")
                                self.execute_skill(selected_unit, skill)
                                
                                selected_unit.current_cooldowns[skill.name] = skill.cooldown
                                print(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                has_acted = True
                            else:
                                print(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
    
                        elif event.key == pygame.K_z and len(selected_unit.skills) > 1:
                            skill = selected_unit.skills[1]  # On prend la seconde compétence (défensive)
                            cooldown = selected_unit.current_cooldowns[skill.name]
                            if cooldown == 0:
                                print(f"Enemy {selected_unit.name} used skill: {skill.name}")
                                self.console.add_message(f"Enemy {selected_unit.name} used skill: {skill.name}")
                                self.execute_skill(selected_unit, skill)
                                
                                selected_unit.current_cooldowns[skill.name] = skill.cooldown
                                print(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                has_acted = True
                                
                            else:
                                print(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
    
                        elif event.key == pygame.K_e and len(selected_unit.skills) > 2:
                            skill = selected_unit.skills[2]  # On prend la troisième compétence
                            cooldown = selected_unit.current_cooldowns[skill.name]
                            if cooldown == 0:
                                print(f"Enemy {selected_unit.name} used skill: {skill.name}")
                                self.console.add_message(f"Enemy {selected_unit.name} used skill: {skill.name}")
                                self.execute_skill(selected_unit, skill)
                                
                                selected_unit.current_cooldowns[skill.name] = skill.cooldown
                                print(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                has_acted = True
                            else:
                                print(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
    
                        elif event.key == pygame.K_SPACE:
                            has_acted = True
                            selected_unit.is_selected = False
    
                    self.trap.update_animation()
                    self.flip_display(current_turn)
    
            selected_unit.is_selected = False






        






    def execute_skill(self, unit, skill):
        """
        Exécute une compétence depuis une unité. Gère les effets (shield, heal, stun, etc.).
    
        Paramètres
        ----------
        unit : Unit
            L'unité qui utilise la compétence.
        skill : Skill
            La compétence à exécuter.
        """
        unit.is_using_skill = True  # Activer l'état de compétence
        # Compétences défensives ou qui s'appliquent directement
        if skill.effect in ["shield", "heal"]:
            if skill.effect == "heal":
                unit.health = min(unit.health + skill.effect_value, 10)
                print(f"{unit.team} {unit.name} at ({unit.x}, {unit.y}) s'est soigné à {skill.effect_value} points. PV actuel: {unit.health}.")
                self.console.add_message(f"{unit.team} {unit.name} à ({unit.x}, {unit.y}) s'est soigné à {skill.effect_value} points. PV actuel: {unit.health}.")
            elif skill.effect == "shield":
                unit.invulnerable_turns = skill.effect_value
                print(f"{unit.team} {unit.name} à ({unit.x}, {unit.y}) est invulnérable pour  {skill.effect_value} tour(s).")
                self.console.add_message(f"{unit.team} {unit.name} à ({unit.x}, {unit.y}) est invulnérable pour  {skill.effect_value} tour(s).")
    
            # Mettre la compétence en cooldown
            unit.current_cooldowns[skill.name] = skill.cooldown
            print(f"{skill.name} mis en cooldown pour {skill.cooldown} tours.")
            self.console.add_message(f"{skill.name} mis en cooldown pour {skill.cooldown} tours.")
            unit.is_using_skill = False  # Désactiver immédiatement après l'exécution
            return
    
        # Compétences offensives nécessitant une sélection de cible
        if skill.damage > 0 or skill.effect == "stun":
            cursor_x, cursor_y = unit.x, unit.y
            targets = self.enemy_units if unit in self.player_units else self.player_units
    
            selecting_target = True
            while selecting_target:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            # Calculer la distance entre l'unité et la case sélectionnée
                            distance = abs(unit.x - cursor_x) + abs(unit.y - cursor_y)
                            if distance > skill.range:
                                print(f"Case hors de portée (distance : {distance}, portée maximale : {skill.range}).")
                                self.console.add_message(f"Case hors de portée (distance : {distance}, portée maximale : {skill.range}).")
                                selecting_target = False
                                unit.is_using_skill = False
                                return
    
                            # Vérifier si une cible est présente à la position du curseur
                            target = next(
                                (t for t in targets if t.x == cursor_x and t.y == cursor_y), None
                            )
                            if target:
                                # Appliquer les dégâts
                                if skill.damage > 0:
                                    unit.apply_damage(target, skill.damage)
                                    target.check_health()
                                    if target.health<=0:
                                        if target.team == 'player':
                                            self.player_units.remove(target)
                                        elif target.team == 'enemy':
                                            self.enemy_units.remove(target)
                                        # target.icon=None
                                        self.flip_display(target.team)
    
                                # Appliquer les effets
                                if skill.effect == "stun":
                                    target.stunned_turns = skill.effect_value
                                    print(f"{target.team} {target.name} at ({target.x}, {target.y}) est étourdi pendant {skill.effect_value} turn(s).")
                                    self.console.add_message(f"{target.team} {target.name} at ({target.x}, {target.y}) est étourdi pendant {skill.effect_value} tour(s).")
                                 
                            else:
                                print(f"Aucune cible trouvée à la case ({cursor_x}, {cursor_y}).")
                                self.console.add_message(f"Aucune cible trouvée à la case ({cursor_x}, {cursor_y}).")
    
                            selecting_target = False
                            unit.is_using_skill = False  # Désactiver après avoir terminé l'action
    
                        # Déplacer le curseur
                        elif event.key == pygame.K_LEFT:
                            cursor_x = max(0, cursor_x - 1)
                        elif event.key == pygame.K_RIGHT:
                            cursor_x = min(GRID_SIZE - 1, cursor_x + 1)
                        elif event.key == pygame.K_UP:
                            cursor_y = max(0, cursor_y - 1)
                        elif event.key == pygame.K_DOWN:
                            cursor_y = min(GRID_SIZE - 1, cursor_y + 1)
    
                current_turn = 'player' if unit in self.player_units else 'enemy'
                self.flip_display(current_turn, skill_position=(cursor_x, cursor_y), skill_mode=True)
    
            # Mettre la compétence en cooldown après sélection
            unit.current_cooldowns[skill.name] = skill.cooldown
            print(f"{skill.name} mis en cooldown pour {skill.cooldown} tours.")
            self.console.add_message(f"{skill.name} mis en cooldown pour {skill.cooldown} tours.")
        
            
    def end_turn(self):
        # Réduire les cooldowns
        for unit in self.player_units + self.enemy_units:
            unit.reduce_cooldowns()
            
            # Réduire l'invulnérabilité s'il en reste
            if unit.invulnerable_turns > 0:
                unit.invulnerable_turns -= 1

    

 
    #2 joueurs
    def flip_display(self, current_turn, skill_position=None, skill_mode=False):
        """
        Affiche le jeu, avec la possibilité de gérer l'affichage de compétences.
    
        Paramètres
        ----------
        current_turn : str
            Identifie à qui appartient le tour actuel ('player' ou 'enemy').
        skill_position : tuple[int, int], optionnel
            Position actuelle du rectangle de compétence. Si None, aucune compétence n'est affichée.
        skill_mode : bool, optionnel
            Si True, désactive l'affichage du rectangle vert pour éviter les conflits.
        """
        self.screen.fill(BLACK)
    
        # Dessiner l'image de fond
        self.screen.blit(self.background, (0, 0))
    
        # Dessiner la grille
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
    
        # Dessiner les obstacles
        self.obstacles.draw(self.screen)
    
        # Dessiner les pièges visibles
        self.trap.draw(self.screen)
        
    
        # Afficher les unités visibles en fonction du tour
        if current_turn == "player":
        # Affiche toutes les unités alliées
          for unit in self.player_units:
              unit.draw(self.screen)
                
    
            # Affiche les ennemis visibles par les joueurs
          for enemy in self.enemy_units:
                if self.is_unit_visible(enemy, self.player_units):  # Vérifie si visible par les joueurs
                    enemy.draw(self.screen)
    
        elif current_turn == "enemy":
            for enemy in self.enemy_units:
                enemy.draw(self.screen)
    
            # Affiche les joueurs visibles par les ennemis
            for unit in self.player_units:
                if self.is_unit_visible(unit, self.enemy_units):  # Vérifie si visible par les ennemis
                    unit.draw(self.screen)
    
        # Dessiner le rectangle jaune pour la position de la compétence (si activé)
        if skill_position:
            pygame.draw.rect(
                self.screen, (255, 255, 0),
                (skill_position[0] * CELL_SIZE, skill_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
    
        # Afficher les compétences dans la barre noire
        selected_unit = next((u for u in self.player_units + self.enemy_units if u.is_selected), None)
        if selected_unit and selected_unit.skills:
            self.skill_menu.update_unit(selected_unit)  # Mettre à jour le menu avec l'unité sélectionnée
            self.skill_menu.draw(self.screen)  # Dessiner le menu
        
        self.console.draw_message_bar()
        pygame.display.flip()

def get_font(size):
    """Renvoie une police de taille donnée."""
    return pygame.font.Font("assets/font.ttf", size)
    
def main_menu(screen):
    """Affiche le menu principal et gère les interactions."""

    # Charger l'image avec Pillow
    
    original_image = Image.open("assets/FONDDD.png")
    
    # Redimensionner avec une interpolation de haute qualité
    
    resized_image = original_image.resize((WIDTH+600, HEIGHT + MENU_HEIGHT), Image.LANCZOS)

    # Sauvegarder l'image redimensionnée temporairement
    
    resized_image.save("assets/FONDDD_resized.png")

     # Charger l'image redimensionnée avec Pygame
     
    BG = pygame.image.load("assets/FONDDD_resized.png")

    
    bg_width, bg_height = BG.get_width(), BG.get_height()

    while True:
        # Obtenir la position de la souris
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Afficher l'image de fond
        screen.blit(BG, (0, 0))
        
        # Définir les boutons
        PLAY_BUTTON = Button(
            image=None, pos=(bg_width // 2, bg_height // 2 -100), text_input="PLAY",
            font=get_font(75), base_color="White", hovering_color="Green"
        )
        QUIT_BUTTON = Button(
            image=None, pos=(bg_width // 2, bg_height // 2+ 100 ), text_input="QUIT",
            font=get_font(75), base_color="White", hovering_color="Red"
        )

        # Afficher les boutons
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return "play"  # Lancer le jeu
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    exit()

        pygame.display.update()



        
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + 600, HEIGHT + MENU_HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    action = main_menu(screen)

    if action == "play":
        available_pokemons = [Pikachu, Salameche, Carapuce, Bulbizarre, Magicarpe, Qulbutoke, Chovsouris, Miaouss]
        print("Sélection des Pokémon pour le joueur...")
        player_menu = SelectionMenu(screen, available_pokemons)
        player_pokemons = player_menu.run()
        print("Sélection des Pokémon pour l'ennemi...")
        enemy_menu = SelectionMenu(screen, available_pokemons)
        enemy_pokemons = enemy_menu.run()

        # Création de l'instance du jeu
        game = Game(screen, player_pokemons, enemy_pokemons)

        # Afficher les positions des pièges après avoir créé l'instance du jeu
        print("Position des pièges générés :")
        for trap_position in game.trap.positions:
            print(trap_position)  # Affiche les positions des pièges générés

        
    # Boucle principale
    while True:
        if game.check_winner():
            break  # Quitte la boucle si une équipe gagne
        game.handle_player_turn()
        if game.check_winner():
            break  # Vérifiez encore après le tour du joueur
        game.handle_enemy_turn()
        if game.check_winner():
            break  # Vérifiez après le tour de l'ennemi
        game.end_turn()



if __name__ == "__main__":
    main()
