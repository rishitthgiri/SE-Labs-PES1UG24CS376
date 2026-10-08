"""
GameEngine: owns the basket and all falling objects.
"""

import math
import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

MIN_SPAWN_INTERVAL_FRAMES = 20
MAX_SPAWN_INTERVAL_FRAMES = 60
MAX_OBJECTS = 8
MIN_SPAWN_DISTANCE = 90      # min horizontal gap between consecutive spawns
OBJECT_RADIUS = 14           # matches FallingObject's default radius
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _pick_spawn_x(self):
        low = OBJECT_RADIUS
        high = WIDTH - OBJECT_RADIUS
        if self.last_spawn_x is None:
            return random.randint(low, high)

        # Bounded retries so this can never loop forever.
        for _ in range(20):
            x = random.randint(low, high)
            if abs(x - self.last_spawn_x) >= MIN_SPAWN_DISTANCE:
                return x

        # Fallback: jump to whichever side has more room.
        if self.last_spawn_x - low >= high - self.last_spawn_x:
            return low
        return high

    def _spawn_object(self):
        x = self._pick_spawn_x()
        self.last_spawn_x = x
        self.objects.append(
            FallingObject(x=x, y=-OBJECT_RADIUS, radius=OBJECT_RADIUS, speed=3)
        )

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        self.basket.x = max(
            self.basket.width / 2,
            min(WIDTH - self.basket.width / 2, self.basket.x)
        )

    def handle_keydown(self, key):
        if self.game_over:
            if key == pygame.K_r:
                self.__init__()
            return

        if key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        self.basket.update_boost()

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            if len(self.objects) < MAX_OBJECTS:
                self._spawn_object()
                self.frames_until_spawn = random.randint(
                    MIN_SPAWN_INTERVAL_FRAMES,
                    MAX_SPAWN_INTERVAL_FRAMES
                )

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()
        for obj in self.objects[:]:
            if is_caught(basket_rect, obj):
                self.score += 1
                self.objects.remove(obj)

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))

        if self.basket.boosted_frames > 0:
            remaining_seconds = math.ceil(self.basket.boosted_frames / 60)
            renderer.draw_text(
                surface, font, f"BOOST ACTIVE: {remaining_seconds}s", (10, 62),
                renderer.COLOR_BASKET_BOOST,
            )

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")