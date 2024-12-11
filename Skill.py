class Skill:
    def __init__(self, name, attack_range, damage, cooldown, effect=None, effect_value=0):
        """
        Initialise une compétence.

        Paramètres
        ----------
        name : str
            Nom de la compétence.
        attack_range : int
            Portée de la compétence en cases.
        damage : int
            Dégâts infligés par la compétence.
        cooldown : int
            Nombre de tours avant de pouvoir réutiliser la compétence.
        effect : str, optionnel
            Type d'effet appliqué par la compétence (ex. 'shield', 'heal', 'stun', 'slow').
        effect_value : int, optionnel
            Valeur associée à l'effet (ex. durée du stun, quantité de heal).
        """
        self.name = name
        self.range = attack_range
        self.damage = damage
        self.cooldown = cooldown
        self.effect = effect  # Type d'effet
        self.effect_value = effect_value  # Intensité ou durée de l'effet
