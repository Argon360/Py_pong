import pygame
import sys
import time
import random
from pygame.locals import MOUSEBUTTONDOWN

# Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

# Player class
class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

# Ball class
class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0
	self.speed_increment = speed_increment

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.active:
            self.speed_x += self.speed_increment
            self.speed_y += self.speed_increment
		
	if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(plob_sound)
            self.speed_y *= -1

        for paddle in self.paddles:
            if self.rect.colliderect(paddle.rect):
                pygame.mixer.Sound.play(plob_sound)
		hit_pos = (self.rect.centery - paddle.rect.top) / paddle.rect.height
        	if abs(self.rect.right - paddle.rect.left) < 10 and self.speed_x > 0:
                    self.speed_x *= -1
                    self.speed_y = -1 + 2 * hit_pos  # Adjust the angle here
                if abs(self.rect.left - paddle.rect.right) < 10 and self.speed_x < 0:
                    self.speed_x *= -1
                    self.speed_y = -1 + 2 * hit_pos  # Adjust the angle here
                if abs(self.rect.top - paddle.rect.bottom) < 10 and self.speed_y < 0:
                    self.rect.top = paddle.rect.bottom
                    self.speed_y *= -1
                if abs(self.rect.bottom - paddle.rect.top) < 10 and self.speed_y > 0:
                    self.rect.bottom = paddle.rect.top
                    self.speed_y *= -1
	
    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = basic_font.render(str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)

# Opponent class
class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, initial_speed, speed_increment):
        super().__init__(path, x_pos, y_pos)
        self.initial_speed = initial_speed
        self.speed_increment = speed_increment
        self.speed = initial_speed

    def update(self, ball_group):
        if self.rect.centery < ball_group.sprite.rect.centery:
            self.rect.y += self.speed
            self.speed += self.speed_increment
        if self.rect.centery > ball_group.sprite.rect.centery:
            self.rect.y -= self.speed
            self.speed += self.speed_increment

        self.constrain(ball_group.sprite.rect)

    def constrain(self, ball_rect):
        min_y = ball_rect.centery - 50  # Adjust the range as needed
        max_y = ball_rect.centery + 50  # Adjust the range as needed

        if self.rect.top <= min_y:
            self.rect.top = min_y
            self.speed = self.initial_speed
        if self.rect.bottom >= max_y:
            self.rect.bottom = max_y
            self.speed = self.initial_speed

# GameManager class
class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.game_over = False

    def run_game(self):
        # Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = basic_font.render(str(self.player_score), True, accent_color)
        opponent_score = basic_font.render(str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

    def check_game_over(self):
        if self.player_score >= 3 or self.opponent_score >= 3:
            self.game_over = True

    def show_game_over(self, winner):
        screen.fill(bg_color)
        game_over_text = basic_font.render("Game Over", True, accent_color)
        winner_text = basic_font.render(f"{winner} wins!", True, accent_color)
        game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
        winner_rect = winner_text.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(winner_text, winner_rect)
        pygame.display.flip()
        time.sleep(2)

# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Global Variables
bg_color = pygame.Color('#FFF6F6')
accent_color = (27, 35, 43)
basic_font = pygame.font.Font('freesansbold.ttf', 32)
plob_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
middle_strip = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)

# Game objects
player = Player('Paddle.png', screen_width - 20, screen_height / 2, 5)
opponent = Opponent('Paddle.png', 20, screen_height / 2, 5, 0.5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group, speed_increment=0.1)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)
game_over = False
reset_game = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                reset_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed
				
	

    # Background Stuff
    screen.fill(bg_color)
    pygame.draw.rect(screen, accent_color, middle_strip)

    # Run the game
    game_manager.run_game()

	# Check for score limit
    game_manager.check_game_over()
    if game_manager.game_over:
        winner = "Player 1" if game_manager.player_score >= 3 else "Player 2"
        game_manager.show_game_over(winner)
        game_over = True

    if game_over:
        pygame.display.flip()
        pygame.event.clear()  
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
		if event.type == MOUSEBUTTONDOWN:  # Check for a mouse click
            		if reset_game:  # If reset_game is True, restart the game
                		player = Player('Paddle.png', screen_width - 20, screen_height / 2, 5)
                		opponent = Opponent('Paddle.png', 20, screen_height / 2, 5, 0.5)
                		paddle_group = pygame.sprite.Group()
                		paddle_group.add(player)
		                paddle_group.add(opponent)

                		ball = Ball('Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
                		ball_sprite = pygame.sprite.GroupSingle()
                		ball_sprite.add(ball)

                		game_manager = GameManager(ball_sprite, paddle_group)
		                game_over = False
                		reset_game = False	

    # Rendering
    pygame.display.flip()
    clock.tick(120)
