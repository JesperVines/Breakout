import math
import pygame
import random

# GLOBALA KONSTANTER

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_RED = (120, 0, 0)
DARK_BLUE = (0, 0, 120)
DARK_GREEN = (0, 120, 0)

SCREEN_HEIGHT = 688
SCREEN_WIDTH = 1366


class Block(pygame.sprite.Sprite):

    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([55, 30])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):

    speed = 10.0
    width = 10
    height = 10

    x = 0.0
    y = 180.0

    direction = 10

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(DARK_GREEN)
        self.rect = self.image.get_rect()

    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        direction_radians = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        self.rect.x = self.x
        self.rect.y = self.y

        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        elif self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        elif self.x > SCREEN_WIDTH - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = SCREEN_WIDTH - self.width - 1

        elif self.y > 768:
            return True


class Player(pygame.sprite.Sprite):

    width = 90
    height = 20

    def __init__(self):

        super().__init__()
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - 50

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > SCREEN_WIDTH - self.width:
            self.rect.x = SCREEN_WIDTH - self.width


class Game(object):

    def __init__(self):
        self.score = 0
        self.game_over = False

        self.block_list = pygame.sprite.Group()
        self.ball_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        top = 40
        block_height = 30

        for row in range(4):

            for column in range(0, 21):

                block = Block(DARK_RED, column * 65 + 6, top)
                self.block_list.add(block)
                self.all_sprites_list.add(block)

            top += block_height + 10

        self.player = Player()
        self.all_sprites_list.add(self.player)

        self.ball = Ball()
        self.ball_list.add(self.ball)
        self.all_sprites_list.add(self.ball)

    def process_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K.ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

            return False

    def run_logic(self):

        if not self.game_over:

            self.all_sprites_list.update()

            if self.ball.y > 768:
                self.ball_list.remove(self.ball)
                self.all_sprites_list.remove(self.ball)

                if len(self.ball_list) < 1:
                    self.game_over = True

            bounce_balls = pygame.sprite.spritecollide(self.player, self.ball_list, False)

            if len(bounce_balls) > 0:

                for b in bounce_balls:

                    diff = (self.player.rect.x + self.player.width/2) - (b.rect.x+b.width/2)
                    b.rect.y = SCREEN_HEIGHT - self.player.width - b.rect.height - 2
                    b.bounce(diff)

            for ball in self.ball_list:

                dead_blocks = pygame.sprite.spritecollide(ball, self.block_list, True)

                if len(dead_blocks) > 0:
                    ball.bounce(0)

                    power1 = random.randrange(0, 10)
                    if power1 == 1:
                        self.ball = Ball()
                        self.ball_list.add(self.ball)
                        self.all_sprites_list.add(self.ball)

                if len(self.block_list) == 0:
                    self.game_over = True

    def display_frame(self, screen):

        screen.fill(BLACK)

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            self.all_sprites_list.draw(screen)

        pygame.display.flip()


def main():

    pygame.init()
    screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)

    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(False)

    done = False
    clock = pygame.time.Clock()

    game = Game()

    while not done:

        done = game.process_events()

        game.run_logic()

        game.display_frame(screen)

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
