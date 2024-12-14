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
from bonus import *
from trap import *
from PIL import Image
from console import Console


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
        self.console = Console(screen)

        self.messages=[]
        
        self.skill_menu = SkillMenu()
        
        # Initialiser les obstacles et les positions valides


        self.background = pygame.image.load('assets/background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
   
           
        # Créer les unités (avant de générer les positions valides)
        self.player_units = [
            Pikachu(0, 0,console=self.console),Salameche(1,0,console=self.console),Carapuce(2,0,console=self.console),Bulbizarre(3, 0,console=self.console)]
            # ,Salameche(1,0),Carapuce(2,0),Bulbizarre(3, 0)

        self.enemy_units = [Magicarpe(6,6,console=self.console),Qulbutoke(7,6,console=self.console),Chovsouris(8,6,console=self.console),Miaouss(9,6,console=self.console)]
           # Magicarpe(6,6),Qulbutoke(7,6), ,Miaouss(9,6)
            
        # Générer les positions valides (unités et obstacles exclus)
        self.obstacles = Obstacle('assets/obstacle.png')
        
        self.valid_positions = self.generate_valid_positions()
        
        self.obstacles.generate_obstacles(GRID_SIZE, num_obstacles=30, unit_positions=self.get_unit_positions())
        
           
         # Créer un piège et un bonus aléatoires
        self.bonus = BonusItem('assets/star.jpg', 'assets/star_sound.mp3',console=self.console)
        self.bonus.generate_bonus(GRID_SIZE, num_bonus=7, obstacles=self.obstacles.positions, valid_positions=self.valid_positions)
        self.trap = Trap('assets/animations/animation_caitlyne', 'assets/trap_sound.mp3',console=self.console)
        self.trap.generate_traps(GRID_SIZE, num_traps=7, obstacles=self.obstacles.positions, valid_positions=self.valid_positions)
        

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
        """
        Gère le tour des unités alliées, permettant de se déplacer, attaquer ou utiliser des compétences.
        """
        current_turn = 'player'
        for selected_unit in self.player_units[:]:
            self.console.add_message("====== Nouvelle unité ======")
            

            # Mettre à jour le carré de mouvement pour l'unité
            selected_unit.update_movement_square(GRID_SIZE)
    
            if selected_unit.health <= 0:
                print(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is dead.")
                self.console.add_message(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is dead.")
                self.player_units.remove(selected_unit)
                continue
    
            if selected_unit.stunned_turns > 0:
                print(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is stunned and cannot act this turn.")
                self.console.add_message(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is stunned and cannot act this turn.")
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
                                if self.bonus.check_for_bonus(selected_unit.x, selected_unit.y):
                                    self.bonus.trigger_bonus(selected_unit)  # generer l'etoile et augmenter les points de vie

                            else:
                                print(f"Déplacement interdit à ({new_x}, {new_y}). En dehors du carré de mouvement.")
                                self.console.add_message(f"Déplacement interdit à ({new_x}, {new_y}). En dehors du carré de mouvement.")
    
                        # Utilisation d'une compétence
                        elif event.key == pygame.K_a and selected_unit.skills:
                            skill = selected_unit.skills[0]
                            cooldown = selected_unit.current_cooldowns[skill.name]
                            if cooldown == 0:
                                print(f"Player used skill: {skill.name}")
                                self.console.add_message(f"Player used skill: {skill.name}")
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
                                print(f"{selected_unit.team} used defense skill: {skill.name}")
                                self.console.add_message(f"{selected_unit.team} used defense skill: {skill.name}")
                                self.execute_skill(selected_unit, skill)
                                selected_unit.current_cooldowns[skill.name] = skill.cooldown
                                print(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                self.console.add_message(f"La compétence {skill.name} est mise en cooldown pour {skill.cooldown} tours.")
                                has_acted = True
                            else:
                                print(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
                                console.add_message(f"La compétence {skill.name} est en cooldown pour encore {cooldown} tours.")
                                
    
                        elif event.key == pygame.K_e and len(selected_unit.skills) > 2:
                            skill = selected_unit.skills[2]  # On prend la troisième compétence
                            cooldown = selected_unit.current_cooldowns[skill.name]
                            if cooldown == 0:
                                print(f"{selected_unit.team} used skill: {skill.name}")
                                self.console.add_message(f"{selected_unit.team} used skill: {skill.name}")
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

    

    
    
    def handle_enemy_turn(self):
        """
        Gère le tour des unités ennemies.
        """
        
        current_turn = 'enemy'
        for selected_unit in self.enemy_units[:]:
            self.console.add_message("====== Nouvelle unité ======")
            
            
            # Mettre à jour le carré de mouvement pour l'unité
            selected_unit.update_movement_square(GRID_SIZE)
    
            if selected_unit.health <= 0:
                print(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is dead.")
                self.console.add_message(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is dead.")
                self.enemy_units.remove(selected_unit)
                continue
            if selected_unit.stunned_turns > 0:
                print(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is stunned and cannot act this turn.")
                self.console.add_message(f"{selected_unit.team} unit at ({selected_unit.x}, {selected_unit.y}) is stunned and cannot act this turn.")
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
                                if self.bonus.check_for_bonus(selected_unit.x, selected_unit.y):
                                    self.bonus.trigger_bonus(selected_unit)  # generer l'etoile et augmenter les points de viee
                            else:
                                print(f"Déplacement interdit à ({new_x}, {new_y}). En dehors du carré de mouvement.")
                                self.console.add_message(f"Déplacement interdit à ({new_x}, {new_y}). En dehors du carré de mouvement.")
    
                        # Utilisation d'une compétence
                        elif event.key == pygame.K_a and selected_unit.skills:
                            skill = selected_unit.skills[0]
                            cooldown = selected_unit.current_cooldowns[skill.name]
                            if cooldown == 0:
                                print(f"Enemy used skill: {skill.name}")
                                self.console.add_message(f"Enemy used skill: {skill.name}")
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
                                print(f"{selected_unit.team} used defense skill: {skill.name}")
                                self.console.add_message(f"{selected_unit.team} used defense skill: {skill.name}")
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
                                print(f"{selected_unit.team} used skill: {skill.name}")
                                self.console.add_message(f"{selected_unit.team} used skill: {skill.name}")
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
                print(f"{unit.team} unit at ({unit.x}, {unit.y}) healed for {skill.effect_value} points. Current health: {unit.health}.")
                self.console.add_message(f"{unit.team} unit at ({unit.x}, {unit.y}) healed for {skill.effect_value} points. Current health: {unit.health}.")
            elif skill.effect == "shield":
                unit.invulnerable_turns = skill.effect_value
                print(f"{unit.team} unit at ({unit.x}, {unit.y}) is now invulnerable for {skill.effect_value} turn(s).")
                self.console.add_message(f"{unit.team} unit at ({unit.x}, {unit.y}) is now invulnerable for {skill.effect_value} turn(s).")
    
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
                                    print(f"{target.team} unit at ({target.x}, {target.y}) is stunned for {skill.effect_value} turn(s).")
                                    self.console.add_message(f"{target.team} unit at ({target.x}, {target.y}) is stunned for {skill.effect_value} turn(s).")
                                 
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
    
        # Dessiner les étoiles
        self.bonus.draw(self.screen)

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
            # Affiche toutes les unités ennemies
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
            image=None, pos=(bg_width // 2, bg_height // 2 - 50), text_input="PLAY",
            font=get_font(75), base_color="White", hovering_color="Green"
        )
        QUIT_BUTTON = Button(
            image=None, pos=(bg_width // 2, bg_height // 2 + 100), text_input="QUIT",
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
    # Initialisation de Pygame
    pygame.init()
    
    # Hauteur pour la barre noire en bas
    NEW_HEIGHT = HEIGHT + MENU_HEIGHT  # Nouvelle hauteur de l'écran
    NEW_WIDTH = WIDTH + 600
    # Modification de l'écran
    screen = pygame.display.set_mode((NEW_WIDTH, NEW_HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    action = main_menu(screen)

    if action == "play":
        game = Game(screen)

    print("Position des étoiles générés :")
    for bonus_position in game.bonus.positions:
            print(bonus_position)  # Affiche les positions des étoiles générés

    print("Position des pièges générés :")
    for trap_position in game.trap.positions:
        print(trap_position)  # Affiche les positions des pièges générés


    # Boucle principale du jeu
    while True:
        # Mettre à jour l'affichage en fonction du tour
        

        # Gérer le tour actuel
        
        game.handle_player_turn()
        
        
        game.handle_enemy_turn()
           

        # Terminer le tour
        game.end_turn()


if __name__ == "__main__":
    main() 