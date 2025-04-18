import asyncio
import platform
import pygame
import random
import os

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 700
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

# Update message display in draw()
# Replace the section that displays the message:
# if message:
#     msg_text = font.render(message, True, BLACK)
#     screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, 120))
# With:
# if message:
#     msg_text = font.render(message, True, BLACK)
#     screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, 130))
#     if feedback_img:
#         screen.blit(feedback_img, (WIDTH // 2 - 70, 130))

# Replace message updates in update_loop():
# message = "✅ " + current_garbage["explanation"]
# with:
# message = current_garbage["explanation"]
# feedback_img = check_img

# message = "❌ " + current_garbage["explanation"]
# with:
# message = current_garbage["explanation"]
# feedback_img = cross_img

# These will be integrated into the full draw and update_loop functions in the code base
