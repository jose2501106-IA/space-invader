class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        self.bullet_cooldown_counter = 0
        # FIX: bullets/fired_bullets como atributos de instancia (no de clase)
        # para evitar listas compartidas entre Player y Enemy.
        self.bullets = []
        self.fired_bullets = []
        self.cool_down = 120

    def draw(self, window):
        if self.ship_img is not None:
            window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width() if self.ship_img is not None else 0

    def get_height(self):
        return self.ship_img.get_height() if self.ship_img is not None else 0
