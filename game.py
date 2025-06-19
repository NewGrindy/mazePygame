import threading

import pygame
import time

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()  # Define clock for FPS control

blue_wins = 0
green_wins = 0
p1 = "luigi.png"
p2 = "mario.png"
done = False
wm2Width = 50
wm1_y = 50


def resize_part():
    global wm2Width
    while not done:
        for i in range(101):
            wm2Width = wm2Width + 1
            time.sleep(0.01)
        time.sleep(1)
        for i in range(101):
            wm2Width = wm2Width -1
            time.sleep(0.01)
        time.sleep(1)


resize_thread = threading.Thread(target=resize_part)
resize_thread.daemon = True
resize_thread.start()

def move_part():
    global wm1_y
    while not done:
        for i in range(61):
            wm1_y = wm1_y + 1
            time.sleep(0.01)
        time.sleep(1)
        for i in range(61):
            wm1_y = wm1_y -1
            time.sleep(0.01)
        time.sleep(1)


move_thread = threading.Thread(target=move_part)
move_thread.daemon = True
move_thread.start()


for current_round in range(1, 4):  # 3 rounds
    x = 30
    y = 30
    x1 = 720
    y1 = 30
    ts1 = time.time()
    ts2 = time.time()
    tol1 = 0
    tol2 = 0
    game_over = False


    while not done and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pressed = pygame.key.get_pressed()
        pressed2 = pygame.key.get_pressed()
        if not game_over:
            if pressed[pygame.K_UP]: y -= 3
            if pressed[pygame.K_DOWN]: y += 3
            if pressed[pygame.K_LEFT]: x -= 3
            if pressed[pygame.K_RIGHT]: x += 3

            if pressed2[pygame.K_w]: y1 -= 3
            if pressed2[pygame.K_s]: y1 += 3
            if pressed2[pygame.K_a]: x1 -= 3
            if pressed2[pygame.K_d]: x1 += 3

        screen.fill((0, 0, 0))
        Font = pygame.font.SysFont("comicsansms", 60, True, True)
        Title = Font.render("Super Mario Brothers!", True, (255, 255, 255))
        screen.blit(Title, (50, 350))

        surf = pygame.image.load(p1).convert_alpha()
        surf = pygame.transform.scale(surf, (70, 100))
        rec1 = surf.get_rect()
        rec1.center = (x, y)
        screen.blit(surf, rec1)

        surf = pygame.image.load(p2).convert_alpha()
        surf = pygame.transform.scale(surf, (70, 100))
        rec2 = surf.get_rect()
        rec2.center = (x1, y1)
        screen.blit(surf, rec2)




        wu = pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(0, 0, 800, 20))
        wr = pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(780, 0, 20, 800))
        wd = pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(0, 780, 800, 20))
        wl = pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(0, 0, 20, 800))

        wm1 = pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(200, wm1_y, 50, 300))
        wm2 = pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(380, 450, wm2Width, 300))
        wm3 = pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(550, 50, 50, 300))
        psq = pygame.draw.rect(screen, (200, 0, 150), pygame.Rect(370, 50, 70, 70))

        if not game_over:
            if rec1.colliderect(wu): y += 3
            if rec1.colliderect(wd): y -= 3
            if rec1.colliderect(wr): x -= 3
            if rec1.colliderect(wl): x += 3

            if rec2.colliderect(wu): y1 += 3
            if rec2.colliderect(wd): y1 -= 3
            if rec2.colliderect(wr): x1 -= 3
            if rec2.colliderect(wl): x1 += 3

            if rec1.colliderect(wm1) or rec1.colliderect(wm3):
                if pressed[pygame.K_UP]: y += 3
                if pressed[pygame.K_LEFT]: x += 3
                if pressed[pygame.K_RIGHT]: x -= 3

            if rec2.colliderect(wm1) or rec2.colliderect(wm3):
                if pressed[pygame.K_w]: y1 += 3
                if pressed[pygame.K_a]: x1 += 3
                if pressed[pygame.K_d]: x1 -= 3

            if rec1.colliderect(wm2) or rec2.colliderect(wm2):
                if pressed[pygame.K_DOWN]: y -= 3
                if pressed[pygame.K_LEFT]: x += 3
                if pressed[pygame.K_RIGHT]: x -= 3
                if pressed[pygame.K_s]: y1 -= 3
                if pressed[pygame.K_a]: x1 += 3
                if pressed[pygame.K_d]: x1 -= 3

            if rec1.colliderect(rec2):
                x = 30
                y = 30
                x1 = 720
                y1 = 30

            if rec1.colliderect(psq):
                x = 30
                y = 30
                te1 = time.time()
                tol1 = round(te1 - ts1, 2)
                game_over = True
                if tol1 > 0 and (tol2 == 0 or tol1 < tol2):
                    blue_wins += 1

            if rec2.colliderect(psq):
                x1 = 720
                y1 = 30
                te2 = time.time()
                tol2 = round(te2 - ts2, 2)
                game_over = True
                if tol2 > 0 and (tol1 == 0 or tol2 < tol1):
                    green_wins += 1

        Font1 = pygame.font.SysFont("comicsansms", 20, True, True)
        Time1 = Font1.render("Time for Luigi: " + str(tol1), True, (0, 0, 255))
        screen.blit(Time1, (50, 650))

        Font2 = pygame.font.SysFont("comicsansms", 20, True, True)
        Time2 = Font2.render("Time for Mario: " + str(tol2), True, (0, 255, 0))
        screen.blit(Time2, (560, 650))

        Font3 = pygame.font.SysFont("comicsansms", 20, True, True)
        winner = "None"
        if tol1 > 0 and (tol2 == 0 or tol1 < tol2):
            winner = "Blue"
        elif tol2 > 0 and (tol1 == 0 or tol2 < tol1):
            winner = "Green"
        RoundLabel = Font3.render("Round " + str(current_round) + " Winner: " + winner, True, (255, 255, 255))
        screen.blit(RoundLabel, (300, 700))

        Font4 = pygame.font.SysFont("comicsansms", 20, True, True)
        ScoreLabel = Font4.render("Luigi Wins: " + str(blue_wins) + "  Mario Wins: " + str(green_wins), True, (255, 255, 255))
        screen.blit(ScoreLabel, (300, 730))

        pygame.display.flip()
        clock.tick(240)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 0, 255))

    Font3 = pygame.font.SysFont("comicsansms", 38, True, True)
    winner = "None"
    if tol1 > 0 and (tol2 == 0 or tol1 < tol2):
        winner = "Luigi"
    elif tol2 > 0 and (tol1 == 0 or tol2 < tol1):
        winner = "Mario"
    RoundLabel = Font3.render(" Winner: " + winner, True, (0, 0, 0))
    screen.blit(RoundLabel, (200, 500))

    Font4 = pygame.font.SysFont("comicsansms", 38, True, True)
    ScoreLabel = Font4.render("Luigi Wins: " + str(blue_wins) + "  Mario Wins: " + str(green_wins), True,
                              (0, 0, 0))
    screen.blit(ScoreLabel, (100, 400))

    pygame.display.flip()
    clock.tick(240)
