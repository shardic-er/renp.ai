# The journal screen.

# Accessing the Journal #########################
# An overlay button so players can access the journal while playing:

screen journal_icon():
    vbox:
        xalign 0.0 yalign 0.0
        imagebutton auto "images/journal_icon_%s.png" action ShowMenu('journal_index') activate_sound click #sound when pressed

# Index ##################################

screen journal_index():

    tag menu

    use game_menu(_("Journal"), scroll="viewport"):

        style_prefix "journal"

        vbox:
            style "journal_button_text"
            text _p("""
                Money: [money]  |  Good/Bad Points: [goodbad]
                """) # Feel free to add more point systems. Be sure to define them.
                     # Example: To add an experience point counter: | XP: [exp]
            null height 20
            text _p("""
                Attributes: {color=[intel]}Intellect: [intellect]{/color}  |  {color=[psy]}Psyche: [psyche]{/color}  |  {color=[fys]}Physique: [physique]{/color}  |  {color=[mot]}Motorics: [motorics]{/color}
                """)
            null height 20
            #vbox: # To make this text wider.
            #style "journal_skill_text"
            text _p("""
                Skills: {color=[intel]}Logic: [logic]  |  Encyclopedia: [encyclopedia]  |  Rhetoric: [rhetoric]  |  Drama: [drama]  |  Conceptualization: [conceptualization]  |  Visual Calculus: [visual_calculus]{/color}
                {p}{color=[psy]}Volition: [volition]  |  Inland Empire: [inland_empire]  |  Empathy: [empathy]  |  Authority: [authority]  |  Esprit De Corps: [esprit_de_corps]  |  Suggestion: [suggestion]{/color}
                {p}{color=[fys]}Endurance: [endurance]  |  Pain Threshold: [pain_threshold]  |  Physical Instr: [physical_instrument]  |  Electrochemistry: [electrochemistry]  |  Shivers: [shivers]  |  Half Light: [half_light]{/color}
                {p}{color=[mot]}Hand/Eye Co: [hand_eye_coordination]  |  Perception: [perception]  |  Reaction Speed: [reaction_speed]  |  Savoir Faire: [savoir_faire]  |  Interfacing: [interfacing]  |  Composure: [composure]{/color}
                """) xsize 1600 # Makes this text max width wider.

            null height 50

            label "Tasks"

            null height 20

            # List your tasks:
            if task_go_on_a_date >= 1: # If the task is set to 1 or higher, it appears.
                hbox:
                    textbutton _("Go on a date") action ShowMenu('task_go_on_a_date')
                    if task_go_on_a_date == 4: # If the task is set to 4, it appears as done.
                                               # The higher the number, the more steps the task has.
                        textbutton _("(DONE)")
            if task_brush_teeth >= 1: # "If the task is set to 1 or higher."
                hbox:
                    textbutton _("Brush your teeth") action ShowMenu('task_brush_teeth')
                    if task_brush_teeth == 2: # "If the task is set to 2."
                        textbutton _("(DONE)")
            if task_buy_hat >= 1: # "If the task is set to 1 or higher."
                hbox:
                    textbutton _("Buy a new hat") action ShowMenu('task_buy_hat')
                    if task_buy_hat == 2: # "If the task is set to 2."
                        textbutton _("(DONE)")
            # Feel free to add more tasks.

            null height 50

            label "Thought Cabinet"

            null height 20

            # List your thoughts:
            if thought_this_feeling >= 1: # If the task is set to 1 or higher, it appears.
                textbutton _("This Feeling") action ShowMenu('thought_this_feeling')
            # Feel free to add more thoughts.

            null height 50

            label "Inventory"

            null height 20

            # List your thoughts:
            if silly_shoes == True: # If the task is set True, it appears.
                textbutton _("Silly Shoes") action ShowMenu('silly_shoes')
            # Feel free to add more items.

# Task Pages ########################
# Of course, a single screen won't do us much good - A blank journal. So here are
# the rest of the screens in our little journal:

screen task_go_on_a_date():

    tag menu

    use game_menu(_("Journal"), scroll="viewport"):

        style_prefix "journal"

        vbox:
            label "GO ON A DATE"

            null height 50

            text _p("""
                It's been a while, hasn't it? You're not out of practice, but
                you're certainly not *in practice* at the moment. It's time to
                take a deep breath, take the pluge... and ask someone out on a
                date.
                """)

            null height 30

            if task_go_on_a_date == 1: # "If the task is set to 1, show this"
                text "• Ask Kim out on a date."
            elif task_go_on_a_date == 2: # Update the task to this number to see this.
                text "• Ask Kim out on a date." style "journal_text_done" #Style crosses out text.
                text "• Buy flowers or chocolates."
            elif task_go_on_a_date == 3:
                text "• Ask Kim out on a date." style "journal_text_done"
                text "• Buy flowers or chocolates." style "journal_text_done"
                text "• Find a nice place to go to for the date."
            elif task_go_on_a_date == 4: # Task completed. Everything on the list crossed out.
                text "• Ask Kim out on a date." style "journal_text_done"
                text "• Buy flowers or chocolates." style "journal_text_done"
                text "• Find a nice place to go to for the date." style "journal_text_done"

            null height 50

            textbutton _("Back to Index") action ShowMenu('journal_index')

screen task_brush_teeth():

    tag menu

    use game_menu(_("Journal"), scroll="viewport"):

        style_prefix "journal"

        vbox:
            label "BRUSH YOUR TEETH"

            null height 50

            text _p("""
                Did you brush your teeth yet? No?? Then for god's sake, *why*
                didn't you? Go and brush your teeth before someone smells your
                rancid breath.
                """)

            null height 30

            text "• Go home or go to your office bathroom and brush yourself."

            null height 50

            textbutton _("Back to Index") action ShowMenu('journal_index')

screen task_buy_hat():

    tag menu

    use game_menu(_("Journal"), scroll="viewport"):

        style_prefix "journal"

        vbox:
            label "BUY A NEW HAT"

            null height 50

            text _p("""
                You lost your favourite hat and need to buy another one, pronto.
                Something detective-y, that makes people turn to look at you and
                go, \"Wow, now *there's* a detective\". Maybe you can find one in
                a nearby shop.
                """)

            null height 30

            text "• Find a shop that sells hats."

            null height 50

            textbutton _("Back to Index") action ShowMenu('journal_index')


# Thought Cabinet Pages ########################

screen thought_this_feeling():

    tag menu

    use game_menu(_("Thought Cabinet"), scroll="viewport"):

        style_prefix "journal"

        vbox:
            label "THIS FEELING"

            null height 50

            if thought_this_feeling == 1: # "If the task is set to 1, show this"
                text _p("""
                    Temporary research bonuses:{p}-1 {color=[intel]}Logic{/color}: This
                    doesn't make any sense!{p}+1 {color=[psy]}Empathy{/color}: Need
                    to look inside youself...{p}Research time: 1h
                    """)
            else: # For when the thought is completed:
                text _p("""
                    Bonuses from the thought:{p}+3 {color=[psy]}Suggestion{/color}: Attuned
                    to Kim on a whole other level.{p}-1 {color=[mot]}Composure{/color}: Oh
                    god, this feeling in your chest. What if someone finds out?{p}
                    -2 {color=[fys]}Pain Threshold{/color}: Probably doesn't love
                    you back...
                    """)

            null height 50

            text "PROBLEM"

            null height 20

            text _p("""
                What is this feeling? This tightness in your chest? You need to
                look inside yourself to figure out what this feeling is about. Give
                it about an hour.
                """)

            if thought_this_feeling == 2: # For when the thought is completed:
                null height 30

                text "SOLUTION"

                null height 20

                text _p("""
                    Oh. *Oh.* It looks like you have a crush on a certain someone.
                    And, even worse, that person probably doesn't return that love.
                    At least you know why your lungs feel like they're glowing.
                    """)

            null height 50

            textbutton _("Back to Index") action ShowMenu('journal_index')

# Inventory Pages ########################

screen silly_shoes():

    tag menu

    use game_menu(_("Inventory"), scroll="viewport"):

        style_prefix "journal"

        vbox:
            #Add an image:
            image "images/item_pen.png"

            null height 20

            label "SILLY SHOES"

            null height 20

            # Item effects:
            text _p("""
                -1 {color=[mot]}Composure{/color}: These really are a silly pair
                of shoes{p}+1 {color=[mot]}Savoir Faire{/color}: But they *are*
                comfortable
                """)

            null height 20

            # Item description:
            text _p("""
                These are the shoes of a silly person. There's a specific children's
                book character who wears these shoes, but you can't recall the name
                of this character, nor what they looked like. Probably, they looked
                like someone silly enough to take on these shoes like a mantle.
                """)

            null height 50

            textbutton _("Back to Index") action ShowMenu('journal_index')


# Styles ########################

style journal_label:
    size gui.label_text_size #36

style journal_label_text:
    size gui.label_text_size
    color gui.text_color

style journal_text:
    size gui.text_size #24
    xsize 1000 # Change this to a larger number if the journal text needs more room.

style journal_button_text:
    size gui.text_size +4 #28
    idle_color gui.accent_color

# For when the task is completed:
style journal_text_done is journal_text
style journal_text_done:
    strikethrough True
