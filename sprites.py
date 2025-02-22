"""Contains all our sprites"""

import pygame
from math import cos, sin, radians
import global_variables as G


class Missile(pygame.sprite.Sprite):
    """These missiles rain from the sky to attack the player"""

    m1_speed = 3
    m2_speed = 4
    m3_speed = 6
    m1_dmg = -5
    m2_dmg = -3
    m3_dmg = -1
    m1_pts = 3
    m2_pts = 2
    m3_pts = 1
    
    missile_stats = [
        {"speed": m1_speed, "damage": m1_dmg, "points": m1_pts},
        {"speed": m2_speed, "damage": m2_dmg, "points": m2_pts},
        {"speed": m3_speed, "damage": m3_dmg, "points": m3_pts},
    ]

    def __init__(self, pos, missile_type):
        super(Missile, self).__init__()
        self.images = []
        self.missile_type = missile_type
        for i in range(10):
            self.images.append(
                pygame.image.load(
                    f"assets/missiles/missile-{missile_type}_fly-{i}.png"
                ).convert_alpha()
            )
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30
        self.stats = self.missile_stats[missile_type - 1]

    def update(self):
        self.rect.y += self.stats["speed"]
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index == len(self.images):
                self.index = 0
            self.image = self.images[self.index]

    def off_screen(self):
        """Check if missile is off screen"""
        return self.rect.y > G.DISPLAY_HEIGHT - (self.image.get_height() * 0.8)


class Missile_Explosion(pygame.sprite.Sprite):
    """A missile explosion"""

    def __init__(self, pos, missile_type):
        super(Missile_Explosion, self).__init__()
        self.images = []
        for i in range(9):
            self.images.append(
                pygame.image.load(
                    f"assets/missiles/missile-{missile_type}_exp-{i}.png"
                ).convert_alpha()
            )
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 45

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index == len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]


class Button(pygame.sprite.Sprite):
    """Generic button with text"""

    def __init__(self, button_text, rect, color, function):
        super(Button, self).__init__()
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size)
        button_rect = button_text.get_rect()
        button_rect.center = (
            pygame.Vector2(self.rect.center) - self.rect.topleft
        )
        pygame.draw.rect(
            self.image, color, self.image.get_rect(), border_radius=12
        )
        self.image.blit(button_text, button_rect)
        self.function = function

    def hit(self):
        """What the button does when hit"""
        self.function()


class Projectile(pygame.sprite.Sprite):
    """This is what the rotating gun fires"""

    def __init__(self, pos, angle, initial_offset=0):
        super(Projectile, self).__init__()
        self.image = pygame.image.load("assets/projectile.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=(
                pos[0] - round(initial_offset * sin(radians(angle))),
                pos[1] - round(initial_offset * cos(radians(angle))),
            )
        )
        self.speed = 5
        self.x_vel = -round(self.speed * sin(radians(angle)))
        self.y_vel = -round(self.speed * cos(radians(angle)))

    def update(self):
        """Update position of projectile"""
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def off_screen(self):
        """Check to see if projectile is off screen"""

        return (
            self.rect.x > G.DISPLAY_WIDTH
            or self.rect.x < 0
            or self.rect.y > G.DISPLAY_HEIGHT
            or self.rect.y < 0
        )


class Gun(pygame.sprite.Sprite):
    """The rotating gun the player fires"""

    def __init__(self, pos):
        super(Gun, self).__init__()

        self.original_image = pygame.image.load(
            "assets/gun.png"
        ).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        self.turning_left = True
        self.angle = 0

    def update(self):
        """Rotate the gun"""
        max_angle = 90

        if self.angle >= max_angle:
            self.turning_left = False
        elif self.angle <= -max_angle:
            self.turning_left = True

        if self.turning_left:
            self.angle += 4
        else:
            self.angle -= 4

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Power_Up(pygame.sprite.Sprite):
    """Power ups!"""

    power_up_list = [
        {"type": "higher_max_health", "color": "Red", "temporary": False},
        {"type": "higher_max_ammo", "color": "Blue", "temporary": False},
        {"type": "piercing_rounds", "color": "Yellow", "temporary": True},
        {"type": "fan_of_projectiles", "color": "Green", "temporary": True},
    ]

    def __init__(self, pos, power_up_type):
        super(Power_Up, self).__init__()

        self.power_up = power_up_type

        self.images = []
        for i in range(1, 7):
            self.images.append(
                pygame.image.load(
                    f"assets/power-ups/{self.power_up['color']}/frame_{i}.png"
                ).convert_alpha()
            )

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index == len(self.images):
                self.index = 0
            self.image = self.images[self.index]
