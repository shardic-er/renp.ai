#This script lets you define different parts of the game.

# You can add in more as you see fit.

## CHARACTERS ########################################

# Declare characters used by this game.
#image kim = "images/character_ref.png" #Example

# Defines the narrator text as text that uses the nvl style textbox:
define narrator = nvl_narrator # When you don't want a portrait to appear.
# When you want character portraits to appear:
define a = Character(None, kind=nvl, image="pics")

# Define portraits below:
layeredimage side pics:
    always:
        "images/portrait_frame.png" # The portrait's frame. Feel free to replace.
    group face:
        attribute drop "images/portrait_drop.png"
        attribute moon "images/portrait_moon.png"
        attribute intellect "images/portrait_intellect.png"
        attribute psyche "images/portrait_psyche.png"
        attribute physique "images/portrait_physique.png"
        attribute motorics "images/portrait_motorics.png"
        # To add more:
        #attribute [NAME] "[IMAGE DIRECTORY]"


## TEXT COLOURS ########################################

#Below are the set colours for tags with the 4 abilities:
define intel = "#6cc6ce" #Why is it "intel" instead of "int"? Because the engine doesn't like "int". Gives a unicode error.
define psy = "#705cbb"
define fys = "#c6496b"
define mot = "#e4b934"

#Below are the set colours for darkened Skill types. In case you want to program in darked text:
define int2 = "#3e6b6f"
define psy2 = "#403666"
define fys2 = "#6b2d3e"
define mot2 = "#7a6522"

# Success/Fail skill check text colours:
define check = "#959891"
define check2 = "#595a55"

define youtext = "#737c87" # The player character's text
define npc = "#ffffff" # For character/place/item names. White.
# To define the colour of red choice text (and red menu text), go to gui.rpy and edit the hex colour on line 34.
define textnorm = "#d2d3cd" # Normal text, like characters and objects. Also for numbers in choices.
define textold = "#71726f" # Darkened normal texts. In case you want to program in darked text.

define greentext = "#95b586" # Text colour in the textbox for gaining XP, tasks, etc.

# Postitive and negative modifier text colours #For some reason, tooltip.rpy doesn't like using them, but I'll leave this here.
define modpos = "#bae625" #Green
#define modneg = "#fc4614" #Red


## SCREEN GRADIENTS ########################################

image black = "#000" # A black screen for when the player is knocked out. Or if you need a solid black screen.
image white = "#ffffff"# A solid white screen for check rolls.
#image red = "#ff0000" # The colour of the red screen for the health damage animation. Hidden now with "effects.png" replacing it.
image effects = "images/effects.png" # Red gradient for health and item effects.

#Overlays for animated success/fail rolls:
image success_roll = "images/success_gradient.png"
#image fail_roll = "images/fail_gradient.png"#In case you want to add a custom fail roll

## NOTIFICATION ########################################

# Symbols for the different notifications (money gained, item gained, etc.)

image notification_damage_health: # Health damage
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_damage.png"
    matrixcolor HueMatrix(+130) # Red
image notification_damage_morale: # Morale damage
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_damage.png"

image notification_heal_health: # Health healed
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_heal.png"
    matrixcolor HueMatrix(+130) # Red
image notification_heal_morale: # Morale healed
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_heal.png"

image notification_critical_health: # Critical health
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_critical.png"
    matrixcolor HueMatrix(+130) # Red
image notification_critical_morale: # Critical morale
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_critical.png"

# More notifications:
image notification_task: # New task, task complete
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_task.png"
image notification_xp: # Leveled up/Experience gained
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_xp.png"
image notification_skill: # Leveled up/Experience gained
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_skill.png"
image notification_item: # Item gained
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_item.png"
image notification_magnesium: # Health/Morale healing item gained
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_magnesium.png"
image notification_thought: # Thought gained
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_thought.png"
image notification_money: # Money gained
    xpos 0.41
    xanchor 0.5
    yalign 1.0
    "images/notification_money.png"


# Notification text:
screen notice(title, subtitle):
    text title:
        xpos 0.41
        xanchor 0.5
        ypos 0.82
        yalign 1.0
        font "DejaVuSans.ttf"
        size 36
        text_align 0.5
        layout "subtitle"
    if subtitle:
        text subtitle:
            xpos 0.41
            xanchor 0.5
            ypos 0.82
            yalign 0.0
            font "DejaVuSans.ttf"
            size 24
            text_align 0.5
            layout "subtitle"


## ANIMATIONS ########################################

#define character sprite animation:
transform pulse_anim:
    alpha 0.0
    linear 0.5 alpha 1.0
    pause .1
    linear 0.5 alpha 0.0
    pause .1
    repeat


## BACKGROUNDS ########################################

#define images you plan on reusing a lot, such as backgrounds:
image bathroom = "images/bg_bathroom.png"

image map = "images/map_ref.png"

## DICE ########################################

# define blank dice image:
image dicebg:
    xpos 0.41
    ypos 0.7
    xanchor 0.5
    yanchor 0.5
    "images/dice_blank.png"

# Dice number result visual:
screen text_dicenumber():
    text _("[roll2d6]"):
        size 70
        xpos 0.41
        ypos 0.7
        xanchor 0.5
        yanchor 0.5

# Spinning dice animation:
transform dicespin:
    ease 1.3 rotate 360


## SOUND EFFECTS ########################################

# Define the sound effect used for skills:
define sfx_int = "audio/sfx_by_katy/sfx_intellect.mp3"
define sfx_psy = "audio/sfx_by_katy/sfx_psyche.mp3"
define sfx_mot = "audio/sfx_by_katy/sfx_motorics.mp3"
define sfx_fys = "audio/sfx_by_katy/sfx_physique.mp3"

# sfx for rolls:
define dice_rolling = "audio/sfx_by_katy/dice_rolling.mp3"
#Success and failure sfx are different in case you want them to be different sound files:
define dice_success = "audio/sfx_by_katy/dice_result.mp3"
define dice_failure = "audio/sfx_by_katy/dice_result.mp3"

# sfx for button clicks:
define click = "audio/sfx_by_katy/button_click.mp3"
#define inv_click = "audio/.mp3"
#define clock_tick = "audio/.mp3"
#define save_reel = "audio/.mp3"

#define health_damage = "audio/.mp3"
#define health_heal = "audio/.mp3"
#define morale_damage = "audio/.mp3"
#define morale_heal = "audio/.mp3" # Meds heal
#define morale_heal_2 = "audio/.mp3" # Non-meds heal
#define health_critical = "audio/.mp3" # For health and morale

#define int_raised = "audio/.mp3"
#define psy_raised = "audio/.mp3"
#define fys_raised = "audio/.mp3"
#define mot_raised = "audio/.mp3"

#define freeze = "audio/.mp3"
#define unfreeze = "audio/.mp3"
#define freeze_2 = "audio/.mp3"
#define unfreeze_2 = "audio/.mp3"

#define task_gained = "audio/.mp3"
#define task_updated = "audio/.mp3"
#define task_completed = "audio/.mp3"
#define task_completed_secret = "audio/.mp3" # For secret tasks

#define thought_gained = "audio/.mp3"
#define thought_imminent = "audio/.mp3"
#define thought_completed = "audio/.mp3"

#define item_shared = "audio/.mp3" # Item gained or lost
#define money_shared = "audio/.mp3" # Money gained or lost
#define item_shared_bottles = "audio/.mp3"
#define magnesium_gained = "audio/.mp3"
#define keys_shared = "audio/.mp3"

#define xp_gained = "audio/.mp3"
#define skill_point = "audio/.mp3"

#define orb_formed = "audio/.mp3"
#define orb_interact = "audio/.mp3"
