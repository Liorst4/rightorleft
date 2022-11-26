#!/usr/bin/env python3

import pygame
import random

should_quit = False
display_score = False

score = 0
attempt = 0

# "LEFT" or "RIGHT"
prompt = None

# Positive - Seconds until a "new prompt" event
# Negative - Seconds since a "new prompt" event
prompt_timer = 3

pygame.init()
pygame.display.set_caption("<- OR ->")
pygame.mouse.set_visible(False)

FRAMES_PER_SECOND = 60

clock = pygame.time.Clock()
screen = pygame.display.set_mode((480, 360))
background = pygame.surface.Surface(screen.get_size())
background.fill(pygame.color.Color("black"))
font = pygame.font.Font(None, 60)

while not should_quit:
    round_is_over = False
    time_passed = clock.tick(FRAMES_PER_SECOND)

    prompt_timer -= (time_passed / 1000)

    if prompt_timer <= 0 and prompt is None:
        prompt = random.choice(("RIGHT", "LEFT"))

    if prompt_timer < min(-3 + (0.2 * attempt), -0.5):
        round_is_over = True

    screen.blit(background, (0,0))
    screen.blit(font.render(f"score: {score}", True, pygame.color.Color("white")), (0,300))
    if prompt is not None:
        screen.blit(font.render(prompt, True, pygame.color.Color(255,255,255)), (0,0))
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            should_quit = True
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            if event.key == pygame.K_RIGHT and prompt == "RIGHT":
                score += 1
            elif event.key == pygame.K_LEFT and prompt == "LEFT":
                score += 1
            round_is_over = True
            break # Prevent holding left and right

    if round_is_over:
        print(prompt_timer)
        attempt += 1
        prompt = None
        prompt_timer = (250 + random.randint(0, max(3000 - (attempt * 100), 1))) / 1000
        print(prompt_timer)
        print("")
        if attempt > 100:
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
