import asyncio
import platform
import pygame
import random
import os

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()
# Image path
IMAGE_FOLDER = r"C:\\Users\\Théo\\Desktop\\Ynov_M1\\hackathon_ia"
# Load background music
pygame.mixer.music.load(os.path.join(IMAGE_FOLDER, "Green_Whisper.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Screen dimensions
WIDTH = 700
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ECOSWIPE")

# Colors
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
RED = (255, 69, 0)
BLACK = (0, 0, 0)

# Game settings
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 24)
large_font = pygame.font.SysFont("Comic Sans MS", 32, bold=True)

# Sounds
correct_sound = pygame.mixer.Sound("correct.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")



# Load feedback images
check_img = pygame.image.load(os.path.join(IMAGE_FOLDER, "check.png"))
cross_img = pygame.image.load(os.path.join(IMAGE_FOLDER, "cross.png"))
check_img = pygame.transform.scale(check_img, (40, 40))
cross_img = pygame.transform.scale(cross_img, (40, 40))

# Load arrow buttons
arrow_up = pygame.image.load(os.path.join(IMAGE_FOLDER, "fleche_haut.png"))
arrow_left = pygame.image.load(os.path.join(IMAGE_FOLDER, "fleche_gauche.png"))
arrow_right = pygame.image.load(os.path.join(IMAGE_FOLDER, "fleche_droite.png"))

arrow_up = pygame.transform.scale(arrow_up, (60, 60))
arrow_left = pygame.transform.scale(arrow_left, (60, 60))
arrow_right = pygame.transform.scale(arrow_right, (60, 60))

# Load logo
logo_img = pygame.image.load(os.path.join(IMAGE_FOLDER, "logo.png"))
logo_img = pygame.transform.scale(logo_img, (330, 250))

# Load logo

# Load garbage images
IMAGES = {
    "bouteille_en_plastique": pygame.image.load(os.path.join(IMAGE_FOLDER, "bouteille_plastique.png")),
    "journal": pygame.image.load(os.path.join(IMAGE_FOLDER, "papier_journal.png")),
    "peau_de_banane": pygame.image.load(os.path.join(IMAGE_FOLDER, "peau_de_banane.png")),
    "restes": pygame.image.load(os.path.join(IMAGE_FOLDER, "restes.png")) if os.path.exists(os.path.join(IMAGE_FOLDER, "restes.png")) else None,
    "bouteille_de_vin": pygame.image.load(os.path.join(IMAGE_FOLDER, "bouteille_de_vin.png")),
    "pot_de_confiture": pygame.image.load(os.path.join(IMAGE_FOLDER, "pot_de_confiture.png")),
}

# Garbage items
GARBAGE = [
    {"name": "Bouteille en plastique", "type": "recycle", "image": IMAGES["bouteille_en_plastique"], "explanation": "Les bouteilles plastiques vont au recyclage, bien vidées."},
    {"name": "Journal", "type": "recycle", "image": IMAGES["journal"], "explanation": "Les journaux sont en papier, donc recyclables."},
    {"name": "Peau de banane", "type": "organic", "image": IMAGES["peau_de_banane"], "explanation": "Les épluchures vont au compost ou bac biodéchets."},
    {"name": "Restes de repas", "type": "organic", "image": IMAGES["restes"], "explanation": "Les restes de nourriture vont dans le compost."},
    {"name": "Bouteille de vin", "type": "glass", "image": IMAGES["bouteille_de_vin"], "explanation": "Les bouteilles en verre se recyclent dans la borne à verre."},
    {"name": "Pot de confiture", "type": "glass", "image": IMAGES["pot_de_confiture"], "explanation": "Les pots en verre vont dans le conteneur à verre."},
]

# Game state
music_on = True
lives = 3
score = 0
current_garbage = random.choice(GARBAGE)
game_over = False
win = False
swipe_direction = None
swipe_start = None
swipe_threshold = 50
message = ""
feedback_img = None
start_screen = True
float_offset = 0
float_direction = 1

# Button rectangles
button_up = pygame.Rect(WIDTH // 2 - 30, 100, 60, 60)
button_left = pygame.Rect(60, HEIGHT // 2 - 30, 60, 60)
button_right = pygame.Rect(WIDTH - 120, HEIGHT // 2 - 30, 60, 60)

def setup():
    global lives, score, current_garbage, game_over, win, message, feedback_img
    lives = 3
    score = 0
    current_garbage = random.choice(GARBAGE)
    game_over = False
    win = False
    message = ""
    feedback_img = None

def draw_start_screen():
    screen.fill((200, 255, 200))  # Light green background
    screen.blit(logo_img, (WIDTH // 2 - 165, 40))
    # No title needed below the logo
    slogan = large_font.render("Apprends à trier en t'amusant !", True, BLACK)
    prompt = large_font.render("Clique pour commencer", True, BLACK)
    screen.blit(slogan, (WIDTH // 2 - slogan.get_width() // 2, 400))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 450))
    pygame.display.flip()


def draw():
    global float_offset, float_direction
    screen.fill(LIGHT_BLUE)

    if game_over:
        msg = "Perdu !" if not win else "Bravo, tu as gagné !"
        text = font.render(msg, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        restart_text = font.render("Appuie sur R pour recommencer", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    else:
        float_offset += float_direction * 0.5
        if float_offset > 5 or float_offset < -5:
            float_direction *= -1

        img = current_garbage["image"]
        if img:
            img = pygame.transform.scale(img, (200, 150))
            screen.blit(img, (WIDTH // 2 - 100, HEIGHT // 2 - 100 + float_offset))

        text = font.render(current_garbage["name"], True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 60 + float_offset))

        for i in range(lives):
            pygame.draw.circle(screen, RED, (30 + i * 40, 50), 15)

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 20))

        screen.blit(arrow_up, button_up.topleft)
        screen.blit(arrow_left, button_left.topleft)
        screen.blit(arrow_right, button_right.topleft)

        screen.blit(font.render("Recyclage", True, BLACK), (button_up.x + 5, button_up.y - 30))
        screen.blit(font.render("Organique", True, BLACK), (button_left.x - 10, button_left.y + 70))
        screen.blit(font.render("Verre", True, BLACK), (button_right.x + 5, button_right.y + 70))

        if message:
            msg_text = font.render(message, True, BLACK)
            screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, 500))
            if feedback_img:
                screen.blit(feedback_img, (WIDTH // 2 -30, 470))

    pygame.display.flip()

def handle_swipe(start_pos, end_pos):
    global swipe_direction
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    if abs(dx) > swipe_threshold or abs(dy) > swipe_threshold:
        if abs(dy) > abs(dx) and dy < 0:
            swipe_direction = "recycle"
        elif dx < 0:
            swipe_direction = "organic"
        elif dx > 0:
            swipe_direction = "glass"

def update_loop():
    global lives, score, current_garbage, game_over, win, swipe_direction, swipe_start, message, feedback_img, start_screen, music_on
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            music_on = not music_on
            if music_on:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()

        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif start_screen and event.type == pygame.MOUSEBUTTONDOWN:
            start_screen = False
            setup()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            swipe_start = event.pos
            if button_up.collidepoint(event.pos):
                swipe_direction = "recycle"
            elif button_left.collidepoint(event.pos):
                swipe_direction = "organic"
            elif button_right.collidepoint(event.pos):
                swipe_direction = "glass"
        elif event.type == pygame.MOUSEBUTTONUP and swipe_start:
            handle_swipe(swipe_start, event.pos)
            swipe_start = None
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                setup()

    if start_screen:
        draw_start_screen()
        return

    if game_over:
        draw()
        return

    if swipe_direction:
        correct = current_garbage["type"] == swipe_direction
        if correct:
            lives = min(lives + 1, 5)
            score += 1
            correct_sound.play()
            message = current_garbage["explanation"]
            feedback_img = check_img
        else:
            lives -= 1
            wrong_sound.play()
            message = current_garbage["explanation"]
            feedback_img = cross_img

        if lives <= 0:
            game_over = True
            win = False
        elif score >= 10:
            game_over = True
            win = True

        current_garbage = random.choice(GARBAGE)
        swipe_direction = None

    draw()

async def main():
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
