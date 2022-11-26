#!/usr/bin/env python3

# Copyright © 2022 Lior Stern
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# “Software”), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pygame
import random
import typing

should_quit = False
display_score = False

score = 0
attempt = 0

prompt: typing.Optional[typing.Literal["LEFT", "RIGHT"]] = None

# Positive - Seconds until a "new prompt" event
# Negative - Seconds since a "new prompt" event
prompt_timer = 3.0

pygame.init()
pygame.display.set_caption("<- OR ->")
pygame.mouse.set_visible(False)

FRAMES_PER_SECOND = 60

clock = pygame.time.Clock()
screen = pygame.display.set_mode((480, 360))
background = pygame.surface.Surface(screen.get_size())
background.fill(pygame.color.Color("black"))
font = pygame.font.Font(None, 60)

def add_attempt_record(color):
    block = pygame.surface.Surface((10, 10))
    block.fill(color)
    background.blit(block, ((attempt * 15), 200))

while not should_quit:
    round_is_over = False
    time_passed = clock.tick(FRAMES_PER_SECOND)

    prompt_timer -= (time_passed / 1000)

    if prompt_timer <= 0 and prompt is None:
        prompt = random.choice(["RIGHT", "LEFT"])

    if prompt_timer < min(-3 + (0.2 * attempt), -0.5):
        round_is_over = True
        add_attempt_record("grey")

    screen.blit(background, (0,0))
    screen.blit(font.render(f"score: {score}", True, pygame.color.Color("white")), (0,300))
    if prompt is not None:
        screen.blit(font.render(prompt, True, pygame.color.Color(255,255,255)), (0,0))
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            should_quit = True
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT) and not round_is_over:
            if (event.key == pygame.K_RIGHT and prompt == "RIGHT") or (event.key == pygame.K_LEFT and prompt == "LEFT"):
                score += 1
                add_attempt_record("green")
            else:
                add_attempt_record("red")

            round_is_over = True
            break # Prevent holding left and right

    if round_is_over:
        attempt += 1
        prompt = None
        prompt_timer = (250 + random.randint(0, max(3000 - (attempt * 100), 1))) / 1000
        if attempt > 20:
            should_quit = True
            display_score = True

if display_score:
    score_text = font.render(f"Score: {score}", True, pygame.color.Color("white"))
    should_quit = False
    while not should_quit:
        clock.tick(FRAMES_PER_SECOND)
        screen.blit(background, (0,0))
        screen.blit(score_text, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                should_quit = True


pygame.quit()
