import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 150, 50)
HOVER_COLOR = (100, 200, 100)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-Нолики")

# Загрузка изображений (замените на свои спрайты)
try:
    x_image = pygame.image.load('x.png')
    o_image = pygame.image.load('o.png')
    background = pygame.image.load('background.jpg')
    restart_img = pygame.image.load('restart.png')
except Exception as e:
    print(f"Ошибка загрузки изображений: {e}")
    sys.exit()

# Масштабирование изображений
x_image = pygame.transform.scale(x_image, (CELL_SIZE - 20, CELL_SIZE - 20))
o_image = pygame.transform.scale(o_image, (CELL_SIZE - 20, CELL_SIZE - 20))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
restart_img = pygame.transform.scale(restart_img, (200, 50))

# Звуки
pygame.mixer.music.load('background_music.mp3')
click_sound = pygame.mixer.Sound('click.wav')
win_sound = pygame.mixer.Sound('draw.wav')
draw_sound = pygame.mixer.Sound('draw.wav')

# Шрифты
font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)


class Game:
    def __init__(self, game_mode):
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player_turn = 'X'
        self.game_mode = game_mode
        self.scores = {'X': 0, 'O': 0}
        self.running = True
        self.game_over = False


    def draw_grid(self):
        for i in range(1, GRID_SIZE):
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 3)
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT - 100), 3)

    def draw_symbols(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 'X':
                    screen.blit(x_image, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
                elif self.board[row][col] == 'O':
                    screen.blit(o_image, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))

    def draw_score(self):
        score_text = button_font.render(f"X: {self.scores['X']}  O: {self.scores['O']}", True, BLACK)
        screen.blit(score_text, (20, 0))

    def check_winner(self):
        lines = [
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[0][2], self.board[1][1], self.board[2][0]],
        ]

        for line in lines:
            if line[0] == line[1] == line[2] != '':
                return line[0]
        return None

    def is_board_full(self):
        for row in self.board:
            if '' in row:
                return False
        return True

    def computer_move(self):
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '']
        return random.choice(empty_cells) if empty_cells else None

    def handle_click(self, pos):
        x, y = pos
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            if self.board[row][col] == '' and not self.game_over:
                self.board[row][col] = self.player_turn
                click_sound.play()
                winner = self.check_winner()
                if winner:
                    self.scores[winner] += 1
                    win_sound.play()
                    self.game_over = True
                elif self.is_board_full():
                    draw_sound.play()
                    self.game_over = True
                else:
                    self.player_turn = 'O' if self.player_turn == 'X' else 'X'
                    if self.game_mode == 'vs_computer' and not self.game_over:
                        self.computer_turn()

    def computer_turn(self):
        if move := self.computer_move():
            row, col = move
            self.board[row][col] = 'O'
            click_sound.play()
            winner = self.check_winner()
            if winner:
                self.scores[winner] += 1
                win_sound.play()
                self.game_over = True
            elif self.is_board_full():
                draw_sound.play()
                self.game_over = True
            self.player_turn = 'X'

    def restart(self):
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player_turn = 'X'
        self.game_over = False
        if self.game_mode == 'vs_computer' and random.choice([True, False]):
            self.computer_turn()

    def draw_buttons(self):
        # Кнопка рестарта
        restart_btn = pygame.Rect(WIDTH // 2 - 300, HEIGHT - 60, 300, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, restart_btn, border_radius=15)
        if restart_btn.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, HOVER_COLOR, restart_btn, border_radius=15)
        restart_text = button_font.render("Играть снова", True, WHITE)
        screen.blit(restart_text, (restart_btn.x + 50, restart_btn.y + 10))

        # Кнопка выхода в меню
        menu_btn = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 60, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, menu_btn, border_radius=15)
        if menu_btn.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, HOVER_COLOR, menu_btn, border_radius=15)
        menu_text = button_font.render("меню", True, WHITE)
        screen.blit(menu_text, (menu_btn.x + 50, menu_btn.y + 10))

        return restart_btn, menu_btn


class Menu:
    def __init__(self):
        self.buttons = [
            {"rect": pygame.Rect(WIDTH // 2 - 150, 300, 300, 60), "text": "Два игрока", "mode": "two_players"},
            {"rect": pygame.Rect(WIDTH // 2 - 150, 400, 360, 60), "text": "Против компьютера", "mode": "vs_computer"}
        ]
        self.selected_mode = None

    def draw(self):
        screen.blit(background, (0, 0))
        title = font.render("Крестики-Нолики", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for button in self.buttons:
            color = HOVER_COLOR if button["rect"].collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
            pygame.draw.rect(screen, color, button["rect"], border_radius=15)
            text = button_font.render(button["text"], True, WHITE)
            screen.blit(text, (button["rect"].x + 30, button["rect"].y + 15))

    def handle_click(self, pos):
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                self.selected_mode = button["mode"]
                return True
        return False


def main():
    menu = Menu()
    game = None
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)

    while True:
        screen.fill(WHITE)

        if game:
            # Отрисовка игры
            restart_btn, menu_btn = game.draw_buttons()
            game.draw_grid()
            game.draw_symbols()
            game.draw_score()
        else:
            # Отрисовка меню
            menu.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game:
                    if restart_btn.collidepoint(event.pos):
                        game.restart()
                    elif menu_btn.collidepoint(event.pos):
                        game = None  # Возврат в меню
                    else:
                        game.handle_click(event.pos)
                else:
                    if menu.handle_click(event.pos):
                        game = Game(menu.selected_mode)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()