#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# PySDL2 Physics Example
# Copyright (C) 2014, William Edwards <shadowapex@gmail.com>,
#
# physics.py Main game
#

import sys
import os

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.dirname(os.path.realpath(__file__))

import sdl2
import sdl2.ext
import sdl2.sdlgfx

import pymunk
import math, sys
import random
import time


class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        # Fill the screen with black every frame.
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


class SpaceObject(object):
    def __init__(self, sprite, sprite_original):
        self.body = pymunk.Body(1,moment=66)
        self.sprite = sprite
        self.sprite_original = sprite_original
        self.shapes = [
            pymunk.Circle(body=self.body, radius=17)
        ]
        self.shapes[0].elasticity = .85
        self.shapes[0].friction - 0.5

    def update(self):
        surface = sdl2.sdlgfx.rotozoomSurface(self.sprite_original.surface,
                                              self.body.angle,
                                              1.0,
                                              1).contents
        self.sprite.surface = surface

        self.sprite.x = int(self.body.position[0]) - (self.sprite.size[0] / 2)
        self.sprite.y = int(self.body.position[1]) - (self.sprite.size[1] / 2)


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Physics PySDL2", size=(800, 600))
    window.show()

    world = sdl2.ext.World()
    space = pymunk.Space()
    space.gravity = 0.0, 0.0

    # Set up our renderer.
    spriterenderer = SoftwareRenderer(window)

    # Add our systems that our world will run every frame.
    world.add_system(spriterenderer)

    # Create our paddle sprites from our sprite factory.
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    asteroids = []
    asteroid_sprites = []

    # Set the number of asteroids and their velocity.
    count = 100
    vel = 100   # velocity
    avel = 500  # angular velocity

    for i in range(count):
        sp_asteroid = factory.from_image('resources/gfx/asteroid_1.png')
        sp_asteroid_original = factory.from_image('resources/gfx/asteroid_1.png')
        asteroid = SpaceObject(sp_asteroid, sp_asteroid_original)
        asteroid.body.velocity = random.randrange(-vel, vel), random.randrange(-vel, vel)
        asteroid.body.position = random.randrange(0, 800), random.randrange(0, 600)
        asteroid.body.angular_velocity = random.randrange(-avel, avel)
        space.add(asteroid.body)
        for shape in asteroid.shapes:
            space.add(shape)

        asteroids.append(asteroid)
        asteroid_sprites.append(sp_asteroid)

    # Calculate our framerate.
    time_new = time.time()
    time_old = time.time()

    running = True
    while running:
        time_elapsed = time_new - time_old
        time_old = time_new
        time_new = time.time()

        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

        # Step through physics.
        space.step(0.016)

        # Update the sprite positions of our asteroids.
        for item in asteroids:
            item.update()

        # Render our asteroids.
        spriterenderer.render(asteroid_sprites)
        window.refresh()

        # Print our FPS to the console.
        if time_elapsed:
            print "FPS:", int(1/time_elapsed)

    return 0

if __name__ == "__main__":
    sys.exit(run())
