import math
import pygame

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
        self.image = pygame.Surface([40, 30])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):

    speed = 10.0

    x = 0.0
    y = 180.0

    direction = 200

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
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

        elif self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        elif self.y > 688:
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([90, 20])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - 90

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > SCREEN_WIDTH - 90:
            self.rect.x = SCREEN_WIDTH - 90


class Game(object):

    def __init__(self):
        self.score = 0
        self.game_over = False

        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        top = 40
        block_height = 30

        for row in range(4):

            for column in range(0, 27):

                block = Block(DARK_RED, column * 50 + 8, top)
                self.block_list.add(block)
                self.all_sprites_list.add(block)

            top += block_height + 10

        self.player = Player()
        self.all_sprites_list.add(self.player)

    def process_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

        return False

    def run_logic(self):
        if not self.game_over:
            self.all_sprites_list.update()

            blocks_hit_list = pygame.sprite.spritecollide(self.player, self.block_list, True)

            for block in blocks_hit_list:
                self.score += 1
                print(self.score)

            if len(self.block_list) == 0:
                self.game_over = True

    def display_frame(self, screen):
        screen.fill(BLACK)

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            self.all_sprites_list.draw(screen)

        pygame.display.flip()


def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

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
