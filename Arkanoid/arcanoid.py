import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 600
fps = 60

paddle_w = 300
paddle_h = 30
paddle_s = 10
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

ball_r = 20
ball_s = 5
ball_rect = int(ball_r * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_r), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

bloc_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

img = pygame.image.load('1.jpg').convert()


def de_col(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - rect.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - rect.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(bloc_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_r)

    ball.x += ball_s * dx
    ball.y += ball_s * dy
    if ball.centerx < ball_r or ball.centerx > WIDTH - ball_r:
        dx = -dx

    if ball.centery < ball_r:
        dy = -dy

    if ball.colliderect(paddle) and dy > 0:
        dx, dy = de_col(dx, dy, ball, paddle)

    hit_i = ball.collidelist(bloc_list)
    if hit_i != -1:
        hit_r = bloc_list.pop(hit_i)
        hit_c = color_list.pop(hit_i)
        dx, dy = de_col(dx, dy, ball, hit_r)

        hit_r.inflate_ip(ball.width * 2, ball.height * 2)
        pygame.draw.rect(sc, hit_c, hit_r, )
        fps += 2

    if ball.bottom > HEIGHT:
        print('GAME OVER!!!!')
        exit()
    elif not len(bloc_list):
        print('WIN!!!')
        exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_s
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_s

    pygame.display.flip()
    clock.tick(fps)
