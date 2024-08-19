# The health and morale screen.

screen vitality_screen():
    image "images/health_hearts.png" xalign 0.0 yalign 1.0
    image "images/health_frame.png" xalign 0.0 yalign 1.0
    image "images/health_mc.png" xalign 0.0 yalign 1.0 # Player character's portrait art.

    if has_partner == True: # If set to True in script.rpy, this 2nd portrait appears:
        image "images/health_frame.png" xpos 174 yalign 1.0
        image "images/health_mc.png" xpos 174 yalign 1.0 # Partner's portrait art.

    hbox:
        yalign 1.0
        xpos 87
        xalign 0.5
        null height 274
        vbox:
            text "[health]" xalign 0.5 style "vitality_text"
            null height 7

            hbox:
                bar:
                    # To make this bar orange:
                    left_bar Frame("gui/bar/leftorange.png", gui.bar_borders, tile=gui.bar_tile)
                    xmaximum 65
                    value health
                    range healthmax
                    left_gutter 0
                    right_gutter 0
                    thumb None
                    thumb_shadow None
                #text "[health] / 5" size 16

        null width 5

        vbox:
            #text "Morale" size 22 xalign 0.5
            text "[morale]" xalign 0.5 style "vitality_text"
            null height 7

            hbox:
                bar:
                    xmaximum 65
                    value morale
                    range moralemax
                    left_gutter 0
                    right_gutter 0
                    thumb None
                    thumb_shadow None
                #text "[morale] / 5" size 16

    #text "test text title" xalign 0.5 yalign 0.05 size 30

style vitality_text:
    bold True
    size 25
    color "#ffffff" # White text
    font "DejaVuSans.ttf"
    
