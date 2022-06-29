import pygame, sys, random
from pygame.locals import *
from ball import *
from dot import *

pygame.init()

# sets width and height to the dimensions of any screen
size = (width, height) = (400, 700)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
bg_color = (0, 0, 0)
min_y = 0
state = None
ball_images = ["images/sphere-04.png", "images/sphere-06.png",
               "images/sphere-11.png", "images/sphere-07.png",
               "images/sphere-12.png", "images/sphere-02.png"]
big_font = pygame.font.SysFont("impact", 80)
sub_font = pygame.font.SysFont("impact", 30)


def initialize(balls, dots, current_ball):
    global min_y, state
    state = "aiming"
    balls.empty()
    for i in range(6):
        if i % 2 == 0:
            for j in range(11):
                balls.add(Ball((7+34*j, 10+30*i), random.choice(ball_images)))
        else:
            for j in range(10):
                balls.add(Ball((24+34*j, 10+30*i), random.choice(ball_images)))
    min_y = 10
    current_ball.add(Ball((200 - 17, 650 - 17), random.choice(ball_images)))
    if len(dots) == 0:
        for i in range(3):
            dots.add(AimingDot(30+35*i))


def color_check(color, ball, balls, to_delete):
    ball.rect.x -= 2
    hit_list = pygame.sprite.spritecollide(ball, balls, False)
    ball.rect.x += 4
    hit_list += pygame.sprite.spritecollide(ball, balls, False)
    ball.rect.x -= 2
    for b in hit_list:
        if b.path == color:
            if not to_delete.has(b):
                to_delete.add(b)
                if b is not ball:
                    color_check(color, b, balls, to_delete)


def find_connected(ball, balls, in_play):
    ball.rect.x -= 2
    hit_list = pygame.sprite.spritecollide(ball, balls, False)
    ball.rect.x += 4
    hit_list += pygame.sprite.spritecollide(ball, balls, False)
    ball.rect.x -= 2
    for b in hit_list:
        if not in_play.has(b):
            in_play.add(b)
            find_connected(b, balls, in_play)


def check_in_play(balls, in_play):
    for b in balls:
        if b.rect.y == min_y:
            if not in_play.has(b):
                in_play.add(b)
                find_connected(b, balls, in_play)


def check_and_delete(ball, balls):
    to_delete = pygame.sprite.Group()
    in_play = pygame.sprite.Group()
    color = ball.path
    color_check(color, ball, balls, to_delete)
    if len(to_delete) < 3:
        return
    for b in to_delete:
        b.kill()
    check_in_play(balls, in_play)
    for b in balls:
        if not in_play.has(b):
            b.kill()


def move_down(backboard, balls, line):
    global min_y, state
    min_y += 30
    backboard.y += 30
    for b in balls.sprites():
        b.rect.y += 30
        if b.rect.bottom > line.top:
            state = "game over"


def display_text(main_text, sub):
    text = big_font.render(main_text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (width / 2, height / 2)
    subtext = sub_font.render(sub, True, (255, 255, 255))
    subtext_rect = subtext.get_rect()
    subtext_rect.midtop = (width / 2, text_rect.bottom)
    screen.blit(text, text_rect)
    screen.blit(subtext, subtext_rect)


def main():
    global screen, state
    balls = pygame.sprite.Group()
    dots = pygame.sprite.Group()
    current_ball = pygame.sprite.GroupSingle()
    initialize(balls, dots, current_ball)
    backboard = pygame.Rect(0, 0, 400, 10)
    line = pygame.Rect(0, 600, 400, 10)
    shot_count = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                # screen controls
                if event.key == K_f:
                    screen = pygame.display.set_mode(size, FULLSCREEN)
                elif event.key == K_ESCAPE:
                    screen = pygame.display.set_mode(size)
                elif event.key == K_SPACE:
                    if state == 'aiming':
                        state = 'fired'
                        current_ball.sprite.set_speed(dots.sprites()[0].angle)
                    elif state in ["game over", "level cleared"]:
                        backboard.y = 0
                        shot_count = 0
                        initialize(balls, dots, current_ball)
        keys = pygame.key.get_pressed()
        if state == "aiming":
            if keys[K_RIGHT]:
                dots.update(1)
            if keys[K_LEFT]:
                dots.update(-1)
        if state == "fired":
            if current_ball.sprite.update(balls, backboard):
                check_and_delete(current_ball.sprite, balls)
                if len(current_ball) == 1 and current_ball.sprite.rect.bottom > line.top:
                    state = "game over"
                if len(balls) == 0:
                    state = "level cleared"
                shot_count += 1
                if shot_count % 10 == 0:
                    move_down(backboard, balls, line)
                if state not in ["game over", "level cleared"]:
                    state = "aiming"
                    current_ball.add(Ball((200-16.5, 650-16.5), random.choice(ball_images)))
        screen.fill(bg_color)
        pygame.draw.rect(screen, (153, 0, 0), backboard)
        pygame.draw.rect(screen, (0, 77, 153), line)
        balls.draw(screen)
        current_ball.draw(screen)
        if state == 'aiming':
            dots.draw(screen)
        elif state == "game over":
            display_text("Game Over", "Press space to try again")
        elif state == 'level cleared':
            display_text("You Win!", "Press space to play again")
        pygame.display.flip()


if __name__ == "__main__":
    main()
