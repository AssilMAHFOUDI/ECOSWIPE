
# ECOSWIPE

## Overview
ECOSWIPE is an educational game built with Pygame to teach players about waste sorting. Players swipe or click to categorize garbage items into recycling, organic, or glass bins. The goal is to score points by correctly sorting items while maintaining lives, with a win condition at 10 points and a loss if lives reach zero.

## Features
- **Interactive Gameplay**: Swipe or click arrows to sort garbage into the correct bins (Recycling, Organic, Glass).
- **Educational Feedback**: Displays explanations for correct/incorrect sorting choices.
- **Visual and Audio Cues**: Includes images for garbage items, feedback icons (check/cross), sound effects for correct/wrong answers, and background music.
- **Start Screen**: Features a logo and slogan, with a click-to-start prompt.
- **Game Mechanics**: Players start with 3 lives, gain lives (up to 5) for correct answers, lose lives for incorrect ones, and win at 10 points.

## Requirements
- Python 3.x
- Pygame library (`pip install pygame`)
- Asset files (images and sounds) in the specified `./` folder:
  - Images: `check.png`, `cross.png`, `fleche_haut.png`, `fleche_gauche.png`, `fleche_droite.png`, `logo.png`, `bouteille_plastique.png`, `papier_journal.png`, `peau_de_banane.png`, `restes.png`, `bouteille_de_vin.png`, `pot_de_confiture.png`
  - Sounds: `Green_Whisper.mp3`, `correct.wav`, `wrong.wav`

## Installation
1. Clone or download the repository.
2. Ensure Python and Pygame are installed:
   ```bash
   pip install pygame
   ```
3. Place all required image and sound files in the `./` folder relative to the main script.
4. Run the game:
   ```bash
   python ecoswipe.py
   ```

## How to Play
1. **Start Screen**: Click anywhere to begin.
2. **Gameplay**:
   - A garbage item appears with its name.
   - Swipe or click one of three arrows:
     - **Up**: Recycling bin
     - **Left**: Organic bin
     - **Right**: Glass bin
   - Correct sorting earns 1 point and adds a life (up to 5).
   - Incorrect sorting loses 1 life and shows an explanation.
3. **Objective**:
   - Reach 10 points to win.
   - Lose all lives to end the game.
4. **Controls**:
   - **Mouse**: Click arrows or swipe to sort.
   - **M Key**: Toggle background music.
   - **R Key**: Restart after game over.
5. **Feedback**: A check (correct) or cross (incorrect) appears with an explanation after each sort.

## File Structure
- `ecoswipe.py`: Main game script.
- `./` (asset folder):
  - Images: Garbage items, arrows, logo, and feedback icons.
  - Sounds: Background music and sound effects.

## Notes
- The game uses Pyodide-compatible structure for potential browser deployment, with `asyncio` and platform checks.
- Ensure all asset files are present in the `./` folder, or the game may crash or skip certain assets (e.g., `restes.png` has a fallback check).
- The game window is 700x700 pixels, with a light blue background and Comic Sans MS font for text.

## Future Improvements
- Add more garbage items and categories.
- Implement difficulty levels or time-based challenges.
- Enhance accessibility with keyboard-only controls.
- Optimize asset loading for better performance.

## License
This project is for educational purposes and does not include a specific license. Feel free to modify and share, but ensure all assets are used with permission.

