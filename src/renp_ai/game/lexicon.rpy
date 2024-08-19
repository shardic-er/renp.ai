# If you get a false positive (the lexicon hyperlink appearing in text you don't want linked) you could just add a {#tag} to force ignore:
# "Test phrases that should not make link... [[1]{#no-lex} {#no-lex}[[2]"

init python:

    lexicon = {
        #Modifiers: Feel free to edit and add more modifiers below.
        ('[[1]') : "{color=#fc4614}-1{/color} You're nervous.{p}{color=#bae625}+2{/color} But excited!",
        ('[[2]') : "{color=#fc4614}-1{/color} Programming is tricky.{p}{color=#bae625}+3{/color} You've got Tutorial Agent on your side.",
        ('[[3]') : "{color=#bae625}+5{/color} You're in love with Kim."
    }

    def hyperlink_lexicon( str_to_test ):
        for keys in lexicon:
            # add this bit
            if isinstance(keys, basestring):
                keys = [keys]

            for phrase in keys:
                # preceded by a space
                str_to_test = str_to_test.replace(
                    " {0}".format(phrase),
                    " {{a=lexicon:{phrase}}}{phrase}{{/a}}".format(
                        phrase = phrase ) )
                # followed by a space
                str_to_test = str_to_test.replace(
                    "{0} ".format(phrase),
                    "{{a=lexicon:{phrase}}}{phrase}{{/a}} ".format(
                        phrase = phrase ) )
        return str_to_test

    config.say_menu_text_filter = hyperlink_lexicon

    def hyperlink_styler(*args):
        return style.hyperlink_text

    def hyperlink_hovered(*args):
        if not args[0]:
            # tried renpy.hide_screen ... no joy
            #return
            # Ren'Py 7+ recent nightly only, see below
            renpy.hide_screen("lexicon_popup")
            return
        elif args[0][:8] == "lexicon:":
            renpy.show_screen( "lexicon_popup",
                               args[0][8:],
                               renpy.get_mouse_pos() )
        renpy.restart_interaction()
        return #added to solve link issue

    #def hyperlink_clicked(*args):
    #    # We could add a function for clicked here
    #    #return None

    #    if not args[0]:
    #        # tried renpy.hide_screen ... no joy
    #        return
    #    elif args[0][:8] == "lexicon:":
    #        renpy.show_screen( "lexicon_popup",
    #                           args[0][8:],
    #                           renpy.get_mouse_pos() )
    #    renpy.restart_interaction()
    def hyperlink_clicked(*args):

        #this section lets you click on links to bring up the popup:
        if not args[0]:
                # tried renpy.hide_screen ... no joy
                return
        elif args[0][:8] == "lexicon:":
            renpy.show_screen( "lexicon_popup",
                               args[0][8:],
                               renpy.get_mouse_pos() )
        renpy.restart_interaction()

        if args[0] and args[0][:8] != 'lexicon:':

            # adapted from common/00defaults.rpy
            if args[0].startswith("http:") or args[0].startswith("https:"):
                try:
                    import webbrowser
                    webbrowser.open(args[0])
                except:
                    renpy.notify("Failed to open browser")

            elif args[0].startswith("jump:"):
                renpy.jump( args[0][5:] )

            else:
                renpy.call_in_new_context(args[0][args[0].index(':')+1:])

            #    renpy.show_screen( "lexicon_popup",args[0][8:],
            #                       renpy.get_mouse_pos() )
            #renpy.restart_interaction()



    style.default.hyperlink_functions = ( hyperlink_styler,
                                          hyperlink_clicked,
                                          hyperlink_hovered )


screen lexicon_popup(phrase=None, pos=(100,100)):

    if phrase:

        python:
            # get description
            d = [ lexicon[k] for k in lexicon if phrase in k ]
            description = d[0] if len(d) else "No description found."
            description = " ".join( [ k for k in description.split()
                                      if k not in [" ", "\t"] ] )
            # move the ypos up by a bit
            pos = ( pos[0], pos[1] - 25 )

            # reformat phrase
            p = [ k for k in lexicon if phrase in k ]
            primary_phrase = p[0][0] if len(p) else phrase
            if primary_phrase != phrase:
                #phrase = "{0} ({1})".format(phrase, primary_phrase)
                phrase = "Modifiers".format(phrase, primary_phrase)

        frame:
            anchor (0.5, 1.0)
            pos pos
            xsize 240 #xsize 340
            background Solid("#171717") #Dark grey
            vbox:
                text "[phrase]" size 25 xpos 0.3 #Centres phrase text
                text "\n[description]\n" size 18

    # Hacky workaround as hyperlink_hovered does not seem to nicely hide this
    # Just hide after (2 words per second) guesstimate delay
    timer len(description.split()) / 2.0 action Hide("lexicon_popup") #4.0
    # --- Fixed in Ren'Py 7.0 nightlies of May 23rd onwards apparently
    #timer 2.0 action Hide("lexicon_popup")
