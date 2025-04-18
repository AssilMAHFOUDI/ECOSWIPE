import asyncio
import platform
import pygame
import random
import os
 
# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()
 
# Screen dimensions
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le Tinder du Tri Sélectif")
 
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
 
# Image path
IMAGE_FOLDER = r"C:\\Users\\Théo\\Desktop\\Ynov_M1\\hackathon_ia"
 
# Load images
IMAGES = {
    "bouteille_en_plastique": pygame.image.load(os.path.join(IMAGE_FOLDER, "bouteille_plastique.png")),
    "journal": pygame.image.load(os.path.join(IMAGE_FOLDER, "papier_journal.png")),
    "peau_de_banane": pygame.image.load(os.path.join(IMAGE_FOLDER, "peau_de_banane.png")),
    "restes": pygame.image.load(os.path.join(IMAGE_FOLDER, "restes_de_repas.png")),
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
lives = 3
score = 0
current_garbage = random.choice(GARBAGE)
game_over = False
win = False
swipe_direction = None
swipe_start = None
swipe_threshold = 50
message = ""
start_screen = True
float_offset = 0
float_direction = 1
 
def setup():
    global lives, score, current_garbage, game_over, win, message
    lives = 3
    score = 0
    current_garbage = random.choice(GARBAGE)
    game_over = False
    win = False
    message = ""
 
def draw_start_screen():
    screen.fill((255, 228, 225))
    title = large_font.render("Le Tinder du Tri Sélectif", True, BLACK)
    slogan = font.render("Apprends à trier en t'amusant !", True, BLACK)
    prompt = font.render("Clique pour commencer", True, RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(slogan, (WIDTH // 2 - slogan.get_width() // 2, 220))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 300))
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
            screen.blit(img, (WIDTH // 2 - 100, 200 + float_offset))
 
        text = font.render(current_garbage["name"], True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 370 + float_offset))
 
        for i in range(lives):
            pygame.draw.circle(screen, RED, (30 + i * 40, 50), 15)
 
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 130, 20))
 
        inst1 = font.render("⬆ Recyclage", True, BLACK)
        inst2 = font.render("⬅ Déchets Organiques", True, BLACK)
        inst3 = font.render("➡ Verre", True, BLACK)
        screen.blit(inst1, (10, HEIGHT - 90))
        screen.blit(inst2, (10, HEIGHT - 60))
        screen.blit(inst3, (10, HEIGHT - 30))
 
        if message:
            msg_text = font.render(message, True, BLACK)
            screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, 120))
 
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
    global lives, score, current_garbage, game_over, win, swipe_direction, swipe_start, message, start_screen
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif start_screen and event.type == pygame.MOUSEBUTTONDOWN:
            start_screen = False
            setup()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            swipe_start = event.pos
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
            message = "✅ " + current_garbage["explanation"]
        else:
            lives -= 1
            wrong_sound.play()
            message = "❌ " + current_garbage["explanation"]
 
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
 
