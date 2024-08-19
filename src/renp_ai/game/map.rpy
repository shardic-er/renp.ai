# For maps/point and click scenes.

# Define button fade animation:
transform buttonfade(speed=0.3): # Change speed's number to change the animation's fade speed.
    alpha 0.0
    on idle:
        linear speed alpha 0.0
    on selected_idle:
        linear speed alpha 1.0
    on hover:
        linear speed alpha 1.0
    on selected_hover:
        linear speed alpha 1.0

screen map_screen_1():
    #tag menu # This ensures that any other menu screen is replaced.

    ## Ensure other screens do not get input while this screen is displayed.
    #modal True
    zorder -10 # Places screen in front of the textbox, health bars, etc.
    #zorder 200 # Places screen in front of the textbox, if you'd prefer that.

    style_prefix "map"

    add "images/map_ref.png"

    #Define the interactable items as imagebuttons:
    imagebutton:
        pos (350, 179) # Position of the image from the top-left of the screen.
        auto "images/shirt_%s.png" # auto replaces the % with "hover" and "idle" images.
                                  # Be sure to include hover and idle where the %s is
                                  # in the images' names.
        action Jump("map_1_shirt") # What clicking on it does.

    imagebutton:
        pos (400, 600)
        auto "images/orb_%s.png"
        action Jump("map_1_orb_1")

    imagebutton:
        pos (700, 650)
        auto "images/orb_%s.png"
        action Jump("map_1_orb_2")
        mouse "grab" # Changes cursor to a custom icon. These are defined in gui.rpy, at the bottom.

    imagebutton:
        align (0.0, 1.0)
        idle "images/map_south_hover.png"
        action Jump("done_map_1") # Return back to this label in the script.
        mouse "walk" # Changes cursor to the walk icon.
        at buttonfade

# You can add more map screens to use below:




# Styles #########################

style map_image_button:
    mouse "talk" #cursor changes when hovering over buttons
