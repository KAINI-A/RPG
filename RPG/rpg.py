#Importing the necessary libraries
import random #for random choice
import pygame #for game functionality

# Initializing pygame mixer for sound playback
pygame.init()
pygame.mixer.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("World of Adventures")

# Loading the sound files.
try:
    intro_sound = pygame.mixer.Sound('gameintro.mp3')
    coin_sound = pygame.mixer.Sound('coins.wav')
    defeated_sound = pygame.mixer.Sound('defeated.wav')
    gamewon_sound = pygame.mixer.Sound('gamewon.wav')
    levelup_sound = pygame.mixer.Sound('Levelup.wav')
    monsterkilled_sound = pygame.mixer.Sound('monsterkilled.wav')
    healingpotion_sound = pygame.mixer.Sound('healingpotion.wav')
    armor_sound = pygame.mixer.Sound('armor.wav')
    encounter_sound = pygame.mixer.Sound('encounter.wav')
    print("All sounds loaded successfully.")
except pygame.error as e:
    print(f"Error loading the sound: {e}")
    pygame.quit()
    exit()

try:
    # Loading the images
    background_image = pygame.image.load('background.jpg')
    rabbit_image = pygame.image.load('rabbit.png')
    rat_image = pygame.image.load('rat.png')
    wolf_image = pygame.image.load('wolf.png')
    monster_image = pygame.image.load('monster.png')
    dragon_image = pygame.image.load('dragon.gif')
    giant_image = pygame.image.load('giant.png')
    print("All images loaded successfully.")
except pygame.error as e:
    print(f"Error loading the image: {e}")
    pygame.quit()
    exit()

background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
print("Background image scaled successfully.")

#color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Creatures are assigned to different levels.
LEVELS = {1: ["rabbit", "rat"], 2: ["monster", "wolf"], 3: ["dragon", "giant"]}

# Creatures health and attack is defined
CREATURE_STATS = {"rabbit": {"health": 5, "attack": 1}, "rat": {"health": 7, "attack": 3}, "monster": {"health": 15, "attack": 7}, "wolf": {"health": 20, "attack": 10}, "giant": {"health": 25, "attack": 12}, "dragon": {"health": 30, "attack": 15}}

# Declared the constants
ITEMS = ["helmet", "shield", "boots", "chest plate", "gauntlets"]
OTHER_THINGS = ["rock", "bush", "big tree", "healing potion"]

# function to display text on a pygame screen
def text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)  # renders the text with given font and color
    text_rect = text_obj.get_rect()  # creates a rect for the rendered text obj
    text_rect.topleft = (x, y)  # sets the top left corner of rect to (x,y) coordinates
    surface.blit(text_obj, text_rect)  # draws the text obj

# MAIN BODY
def game():
    # Player Stats
    player_health = 20
    coins = 0
    inventory = []
    armor_items = 0
    player_attack_damage = 5
    level = 1

    #plays intro sound
    intro_sound.play()

    font = pygame.font.Font(None, 36)

    # Display game title
    screen.fill(BLACK)
    text("World of Adventures", font, WHITE, screen, screen_width // 2 - 100, screen_height // 2 - 20)
    pygame.display.update()
    pygame.time.delay(3000)

    running = True
    encounter = False
    fight = False
    fight_choice = None

    while running:
        screen.fill(BLACK)  # fill the entire screen with single surface color black
        screen.blit(background_image, (0, 0)) #display background

        # display the player stats
        text(f"Health: {player_health}", font, WHITE, screen, 20, 20)
        text(f"Attack Damage: {player_attack_damage}", font, WHITE, screen, 20, 50)
        text(f"Coins: {coins}", font, WHITE, screen, 20, 80)

        # CRITERIA FOR DIFFERENT LEVELS IS SET.
        previous_level = level
        if coins >= 30 and coins < 60:
            level = 2
        elif coins >= 60:
            level = 3

        if level != previous_level:
            levelup_sound.play()

        # Creatures appear according to the level.
        if level in LEVELS:
            creatures = LEVELS[level]
        else:
            creatures = LEVELS[3]

        # Game starts.
        ALL_THINGS = creatures + ITEMS + OTHER_THINGS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and encounter and not fight:
                if encounter and not fight:
                    if event.key == pygame.K_y:
                        fight_choice = True
                    elif event.key == pygame.K_n:
                        fight_choice = False

        if not encounter:
            thing = random.choice(ALL_THINGS)
            # display encounter text
            text(f"You have encountered a {thing}!", font, BLACK, screen, 20, 110)
            pygame.display.update()
            pygame.time.delay(1000)

            # If healing potion is found.
            if thing == "healing potion":
                heal_amount = random.randint(5, 10)
                player_health += heal_amount
                healingpotion_sound.play()
                text(f"Your health increased by {heal_amount}!", font, (255, 255, 0), screen, 20, 130)
                pygame.display.update()
                pygame.time.delay(1000)
                encounter = False

            # If other thing except for healing potions and creatures is found.
            elif thing in ITEMS and thing not in inventory:
                inventory.append(thing)
                armor_items += 1
                armor_sound.play()
                encounter = False

            # Creatures appear
            elif thing in creatures:
                # Creature stats is set according to the name.
                creature_health = CREATURE_STATS[thing]["health"]
                creature_damage = CREATURE_STATS[thing]["attack"]
                encounter_sound.play()

                creature_image = globals().get(f'{thing}_image')
                if creature_image:
                    screen.blit(creature_image, (screen_width // 2 - creature_image.get_width() // 2, 200))
                    pygame.display.update()
                    pygame.time.delay(2000)

                # Display creature stats
                text(f"{thing.capitalize()} Health: {creature_health}", font, WHITE, screen, 20, 140)
                text(f"{thing.capitalize()} Attack: {creature_damage}", font, WHITE, screen, 20, 170)
                pygame.display.update()

                # Player makes a fight choice.
                fight_choice = None
                text("Do you want to fight? (Y/N)", font, WHITE, screen, 20, 200)
                pygame.display.update()
                while fight_choice is None:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:
                                fight_choice = True
                            elif event.key == pygame.K_n:
                                fight_choice = False

                # Clear the fight choice text
                pygame.draw.rect(screen, BLACK, (20, 200, screen_width, 30))
                pygame.display.update()

                # If the player decides to run away
                if not fight_choice:
                    encounter = False
                    continue

                # Player and creatures fight.
                while creature_health > 0 and player_health > 0:
                    # Player attacks
                    attack_damage = random.randint(4, 7)
                    creature_health -= attack_damage

                    # If the creature is alive, it attacks back.
                    if creature_health > 0:
                        # Damage is calculated while keeping the armor items in check.
                        damage = creature_damage - armor_items
                        if damage < 0:
                            damage = 0
                        player_health -= damage

                        # Player gets a choice
                        if player_health > 0 and creature_health > 0:
                            choice = None
                            text("Do you want to keep fighting? (Y/N)", font, WHITE, screen, 20, 200)
                            pygame.display.update()
                            while choice is None:
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN: 
                                        #Player fights if the key Y is pressed
                                        if event.key == pygame.K_y:
                                            choice = True
                                        #No fight if the key N is pressed
                                        elif event.key == pygame.K_n:
                                            choice = False
                            # Player runs away from the fight
                            if not choice:
                                break

                    # If the player dies
                    if player_health <= 0:
                        defeated_sound.play()
                        # Display death message
                        screen.fill(BLACK)
                        #aligning the text properly; 
                        text("You DIED!", font, WHITE, screen, screen_width // 2 - 50, screen_height // 2 - 20)
                        pygame.display.update()
                        pygame.time.delay(3000)
                        # Coins earned and the result is sent.
                        return coins, False

                # If the player defeats the creatures
                if player_health > 0 and creature_health <= 0:
                    monsterkilled_sound.play()
                    # Coins earned according to the creatures type.
                    if thing in ["monster", "wolf", "dragon", "giant"]:
                        coins += random.randint(10, 15)
                        coin_sound.play()

                        # Monsters drop healing and attack potions
                        if random.random() < 0.2:
                            attack_boost = random.randint(2, 4)
                            player_attack_damage += attack_boost
                            text(f"Your attack damage increased by {attack_boost}!", font, (255, 255, 0), screen, 20, 130)
                            pygame.display.update()
                            pygame.time.delay(1000)

                        elif random.random() < 0.5:
                            heal_amount = random.randint(5, 10)
                            player_health += heal_amount
                            healingpotion_sound.play()
                            text(f"Your health increased by {heal_amount}!", font, (255, 255, 0), screen, 20, 130)
                            pygame.display.update()
                            pygame.time.delay(1000)

                    elif thing == "rat":
                        coins += 4
                        coin_sound.play()
                    else:
                        coins += 2
                        coin_sound.play()

        # Player wins the game
        if coins >= 100:
            gamewon_sound.play()
            # Display win message
            screen.fill(BLACK)
            text("You WIN!", font, WHITE, screen, screen_width // 2 - 50, screen_height // 2 - 20)
            pygame.display.update()
            pygame.time.delay(3000)
            return coins, True

        # Player dies
        if player_health <= 0:
            defeated_sound.play()
            # Display death message
            screen.fill(BLACK)
            text("You DIED!", font, WHITE, screen, screen_width // 2 - 50, screen_height // 2 - 20)
            pygame.display.update()
            pygame.time.delay(3000)
            return coins, False

        encounter = False  # Reset encounter flag

        # Wait for the player to press ENTER to keep walking
        waiting_for_enter = True
        while waiting_for_enter:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting_for_enter = False

# game() is called and coins and result is noted.
coins, result = game()
if result:
    print(f"You WIN. You earned {coins} coins.")
else:
    print(f"TRY AGAIN! You earned {coins} coins.")

pygame.quit()