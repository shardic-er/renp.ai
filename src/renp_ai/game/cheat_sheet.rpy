# Cheat sheets for quich reference as you're programming.


## SKILL CHECKS ##############################################

# A cheat sheet to skill checks:
#
# Trivial:      roll2d6>5
# Easy:         roll2d6>7
# Medium:       roll2d6>9
# Challenging:  roll2d6>11
# Formidable:   roll2d6>12
# Legendary:    roll2d6>13
# Heroic:       roll2d6>14
# Godly:        roll2d6>15
# Impossible:   roll2d6>17


## EFFECT COLOURS (HueMatric) ##############################################

# Cheat sheet for HueMatric colours for effects.png:
#
# matrixcolor HueMatrix(+70) * SaturationMatrix(+20) # Yellow (for Motorics Raised effects)
# matrixcolor HueMatrix(+60) # Orange (for Health healed)
# matrixcolor HueMatrix(-20) # Pink (for Physique Raised effects)
# matrixcolor HueMatrix(-80) # Purple (for Psyche Raised effects)
# matrixcolor HueMatrix(-160) # Teal (for Morale healed/Intelligence Raised effects)
# matrixcolor HueMatrix(-190) # Green (for level ups)

# Cheat sheet for HueMatric colours for fail_roll:
# matrixcolor HueMatrix(-120) # Orange


## GREEN TEXT MESSAGES ##############################################

# Cheat sheet for different green text messages:
#
#"{color=[greentext]}Item gained: Name of Item{/color}{nw}"
#"{color=[greentext]}Item lost: Name of Item{/color}{nw}"
#
#"{color=[greentext]}Thought gained: Name of Thought{/color}{nw}"
#
#"{color=[greentext]}New task: Name of task{/color}{nw}"
#"{color=[greentext]}Task complete: Name of task{/color}{nw}"
#"{color=[greentext]}Secret task complete: Name of task{/color}{nw}"
#
#"{color=[greentext]}+5 XP: gained experience{/color}{nw}"
#{color=[greentext]}Gained experience: +10{/color}{nw}"
#{color=[greentext]}Level up!{/color}{nw}"


## NOTIFICATION MESSAGES ##############################################

# Cheat sheet for different notification messages:
#
# show screen notice(_("CHECK SUCCESS"), ())
# show screen notice(_("CHECK FAILURE"), ())
#
# show screen notice(_("DAMAGED HEALTH"), _("-1"))
# show screen notice(_("DAMAGED MORALE"), _("-1"))
# show screen notice(_("HEALED HEALTH"), _("+1"))
# show screen notice(_("HEALED MORALE"), _("+1"))
# show screen notice(_("HEALTH CRITICAL!"), _("HEAL YOURSELF NOW!"))
# show screen notice(_("MORALE CRITICAL!"), _("HEAL YOURSELF NOW!"))
#
# show screen notice(_("MONEY GAINED:"), _("1.00 REÁL"))
# show screen notice(_("MONEY LOST:"), _("1.00 REÁL"))
#
# show screen notice(_("ITEM GAINED:"), _("NAME OF ITEM"))
# show screen notice(_("ITEM LOST:"), _("NAME OF ITEM"))
#
# show screen notice(_("THOUGHT GAINED:"), _("NAME OF THOUGHT"))
# show screen notice(_("BREAKTHROUGH IMMINENT"), _("NAME OF THOUGHT"))
#
# show screen notice(_("TASK GAINED:"), _("NAME OF TASK."))
# show screen notice(_("TASK UPDATED:"), _("NAME OF TASK."))
# show screen notice(_("TASK COMPLETE:"), _("NAME OF TASK. +10 EXPERIENCE"))
# show screen notice(_("SECRET TASK COMPLETE:"), _("NAME OF TASK. +10 EXPERIENCE"))
# show screen notice(_("GAINED EXPERIENCE"), _("+5XP"))
# show screen notice(_("NEW SKILL POINT!"), ())
#
# show screen notice(_("INTELLECT RAISED"), ())
# show screen notice(_("PSYCHE RAISED"), ())
# show screen notice(_("PHYSIQUE RAISED"), ())
# show screen notice(_("MOTORICS RAISED"), ())
#
