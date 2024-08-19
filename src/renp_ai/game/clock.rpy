# In-Game Clock #########################

screen clock_icon():
    vbox:
        xpos 22
        yalign 0.73
        text "Time: [time]" text_align 0.5
        # If you want it to use a : instead of a period, you can define hours
        # and minutes individually, like this:
        #text "Time: [hour]:[minute]" text_align 0.5
        # However, this method will make it harder to turn minutes into hours if
        # your game has a lot of choices and route to track.
        
