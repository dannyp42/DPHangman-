import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 1000, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images.
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
lives = 6  # Maximum lives
words = ["IDE", "APPLE", "STEAK", "BONNYRIGG", "TEA", "ABG", "IPAD", "CABRAMATTA"]
word = random.choice(words)
guessed = []


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# hint button variables
HINT_BUTTON_X = WIDTH - 150
HINT_BUTTON_Y = 20
HINT_BUTTON_WIDTH = 120
HINT_BUTTON_HEIGHT = 50
hint_used = False



def draw():
    win.fill(WHITE)

    # draw fancy title with shadow
    shadow_text = TITLE_FONT.render("DP HANGMAN", 1, (150, 150, 150))  # Gray shadow
    win.blit(shadow_text, (WIDTH / 2 - shadow_text.get_width() / 2 + 4, 24))  # Offset shadow

    text = TITLE_FONT.render("DP HANGMAN", 1, (0, 102, 204))  # Blue title
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 0)  # Filled circle with black color
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)  # Black border
            text = LETTER_FONT.render(ltr, 1, WHITE)  # White text for contrast
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # draw hangman image
    win.blit(images[hangman_status], (150, 100))

    # draw hint button
    pygame.draw.rect(win, (0, 255, 0), (HINT_BUTTON_X, HINT_BUTTON_Y, HINT_BUTTON_WIDTH, HINT_BUTTON_HEIGHT))
    hint_text = LETTER_FONT.render("HINT", 1, BLACK)
    win.blit(hint_text, (HINT_BUTTON_X + HINT_BUTTON_WIDTH / 2 - hint_text.get_width() / 2, 
                         HINT_BUTTON_Y + HINT_BUTTON_HEIGHT / 2 - hint_text.get_height() / 2))

    # draw lives
    lives_text = LETTER_FONT.render(f"Lives: {lives}", 1, BLACK)
    win.blit(lives_text, (20, 20))  # Display lives at the top-left corner

    pygame.display.update()



def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global hangman_status, hint_used, lives

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()

                # Check if a letter is clicked
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
                                lives -= 1  # Decrease lives for incorrect guess

                # Check if hint button is clicked
                if (HINT_BUTTON_X <= m_x <= HINT_BUTTON_X + HINT_BUTTON_WIDTH and 
                    HINT_BUTTON_Y <= m_y <= HINT_BUTTON_Y + HINT_BUTTON_HEIGHT):
                    if not hint_used:
                        hint_used = True
                        available_letters = [ltr for ltr in word if ltr not in guessed]
                        if available_letters:
                            guessed.append(random.choice(available_letters))
        
        draw()

        # Check for win/loss conditions
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        
        if won:
            display_message("You WON!")
            break

        if hangman_status == 6 or lives == 0:  # Update loss condition
            display_message("You LOST!")
            break
    
    return run


while True:
    game_running = main()
    if not game_running:  # Exit the loop if the user closes the game window
        break
    
    main()
pygame.quit()