import pygame
import random

pygame.init()

WIDTH, HEIGHT = 700, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hacker Clicker Game")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)

font = pygame.font.SysFont("consolas", 40)
small_font = pygame.font.SysFont("consolas", 22)

clock = pygame.time.Clock()

texts = ["ACCESS GRANTED", "ACCESS DENIED", "HACKING..."]

# == GAMBAR VIRUS ==
virus_img = pygame.image.load("virus.png")
virus_img = pygame.transform.scale(virus_img, (70, 70))

def reset_game():
    return 0, 3, random.choice(texts), []

score, lives, current_text, viruses = reset_game()
game_state = "tutorial"

CHANGE_EVENT = pygame.USEREVENT
pygame.time.set_timer(CHANGE_EVENT, 1500)


# == MATRIX RAIN  (Hujan Kode) ==
columns = WIDTH // 20
drops = [random.randint(-20, 0) for _ in range(columns)]

def draw_matrix():
    for i in range(len(drops)):
        char = chr(random.randint(33, 126))
        char_surface = small_font.render(char, True, DARK_GREEN)
        x = i * 20
        y = drops[i] * 20
        screen.blit(char_surface, (x, y))
        drops[i] += 1
        if drops[i] * 20 > HEIGHT:
            drops[i] = random.randint(-5, 0)

# == VIRUS ==
def spawn_virus():
    x = random.randint(50, WIDTH - 50)
    y = -40
    rect = virus_img.get_rect(topleft=(x, y))
    return rect

running = True
while running:
    screen.fill(BLACK)
    draw_matrix()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # == TUTORIAL ==
        if game_state == "tutorial":
            if event.type == pygame.KEYDOWN:
                game_state = "playing"

        # == PLAYING ==
        elif game_state == "playing":
            if event.type == CHANGE_EVENT:
                current_text = random.choice(texts)

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Klik pas access granted
                if text_rect.collidepoint(event.pos):
                    if current_text == "ACCESS GRANTED":
                        score += 1
                        for i in range(3):  # Munculkan 3 virus sekaligus
                            viruses.append(spawn_virus())

                    else:
                        lives -= 1
                        if lives <= 0:
                            game_state = "game_over"

                # Virus diklik
                for virus in viruses:
                    if virus.collidepoint(event.pos):
                        score += 2
                        viruses.remove(virus)
        elif game_state == "win":
            if event.type == pygame.MOUSEBUTTONDOWN:
                score, lives, current_text, viruses = reset_game()
                game_state = "playing"
    


        # == GAME OVER ==
        elif game_state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    score, lives, current_text, viruses = reset_game()
                    game_state = "playing"

    # == TUTORIAL SCREEN ==
    if game_state == "tutorial":
        title = font.render("HACKER GAME", True, GREEN)
        t1 = small_font.render("Klik hanya saat muncul 'ACCESS GRANTED'", True, GREEN)
        t2 = small_font.render("Click virus yang jatuh!", True, GREEN)
        t3 = small_font.render("Tekan tombol pada keyboard untuk mulai...", True, RED)

        screen.blit(title, (150, 120))
        screen.blit(t1, (150, 200))
        screen.blit(t2, (150, 230))
        screen.blit(t3, (150, 280))

    # == PLAYING SCREEN ==
    elif game_state == "playing":

        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)

        text_surface = font.render(current_text, True, GREEN)
        text_rect = text_surface.get_rect(
            center=(WIDTH//2 + offset_x, HEIGHT//2 + offset_y)
        )
        screen.blit(text_surface, text_rect)

        # Virus
        for virus in viruses[:]:
            virus.y += 3
            screen.blit(virus_img, virus)

            if virus.y > HEIGHT:
                lives -= 1
                viruses.remove(virus)
                if lives <= 0:
                    game_state = "game_over"

        score_text = small_font.render(f"Score: {score}", True, GREEN)
        lives_text = small_font.render(f"Live: {lives}", True, RED)

        if score >= 100:
            game_state = "win"

        screen.blit(lives_text, (10, 35))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 35))

    # == GAME OVER SCREEN ==
    elif game_state == "game_over":
        over_text = font.render("SYSTEM LOCKED!", True, RED)
        retry_text = small_font.render("TRY AGAIN", True, GREEN)

        retry_rect = retry_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))

        screen.blit(over_text, (200, 170))
        screen.blit(retry_text, retry_rect)

    # == WIN SCREEN ==
    elif game_state == "win":
        win_text = font.render("SYSTEM SUCCESSFULLY PROTECTED!", True, GREEN)
        info_text = small_font.render("PROTECT AGAIN", True, RED)

        win_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
        retry_rect = info_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))

        screen.blit(win_text, win_rect)
        screen.blit(info_text, retry_rect)


    pygame.display.update()
    clock.tick(30)

pygame.quit()
