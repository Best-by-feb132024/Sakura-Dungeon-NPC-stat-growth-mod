#seems to mostly be mostly menu screens and scripts

label stats:
    python:
        for i in party:
            i.face_change()
        config.skipping=None
        _rollback=False
        current_actor = party[0]
        chosen_actor = None
        chosen_skill = None
        chosen_item = None
        active_actor = None
        passive_actor = None
        current_message = ""
        current_ex_message = ""
        current_item_focus =True
    play audio "Open_Menu"
    call screen stats
    return


label organize:
    python:
        for i in party+backup:
            i.face_change()
        config.skipping=None
        _rollback=False
        current_actor = party[0]
        chosen_actor = None
        chosen_skill = None
        chosen_item = None
        active_actor = None
        passive_actor = None
        current_message = ""
        current_mode = "Organize"
        renpy.retain_after_load()
    call screen stats
    return





screen stats():
    tag menu

    on "hide" action [Hide("alt_notify"), Hide("message_screen")]

    add Solid("#0006") at gui_dissolve

    add Transform(current_actor.objectname, anchor=(.5,.5)) at show_player(.85)

    if current_mode == "Organize":
        label _("Organize") style "large_label" xpos 10 ypos 10:
            at gui_dissolve_left
    else:
        label _("Statistics") style "large_label" xpos 10 ypos 10:
            at gui_dissolve_left

    frame xpos 10 ypos 75 xsize 160 style_group "nav_menu": #pause menu
        at nav_dissolve_left
        has vbox
        if current_mode == "Organize":
            textbutton _("Disband") default True:
                if not chosen_actor and not chosen_item and not chosen_skill:
                    action Show("alt_confirm", message=_("Do you wish to disband your current party?"), yes_action=Function(player.disband))
        else:
            textbutton _("Consumables") default True:
                if not chosen_actor and not chosen_item and not chosen_skill:
                    action [With(Dissolve(.25)),SelectedIf(current_mode=="Consumables"), SetVariable("current_mode", "Consumables")]
                if current_mode != "Full Map":
                    default True
            textbutton _("Valuables"):
                if not chosen_actor and not chosen_item and not chosen_skill:
                    action [With(Dissolve(.25)),SelectedIf(current_mode=="Valuables"), SetVariable("current_mode", "Valuables")]
            textbutton _("Full Map"):
                if not chosen_actor and not chosen_item and not chosen_skill and not isinstance(stand, str):
                    action [With(Dissolve(.25)),SelectedIf(current_mode=="Full Map"), SetVariable("current_mode", "Full Map")]
                if current_mode == "Full Map":
                    default True
            textbutton _("Back Log"):
                if not chosen_actor and not chosen_item and not chosen_skill:
                    action [SelectedIf(False), SetVariable("yvalue", 1.0), ShowMenu("text_history")] activate_sound None
            textbutton _("Save Game"):
                if not chosen_actor and not chosen_item and not chosen_skill:
                    action ShowMenu("save") activate_sound None
            textbutton _("Load Game"):
                if not chosen_actor and not chosen_item and not chosen_skill:
                    action ShowMenu("load") activate_sound None
            textbutton _("Options"):
                if not chosen_actor and not chosen_item and not chosen_skill:
                    action ShowMenu("preferences") activate_sound None






        textbutton _("Return"):
            if not chosen_actor and not chosen_item and not chosen_skill:
                action [Play("audio", "Closing_Menu"),Return()] activate_sound None

    if current_mode not in ["Organize", "Full Map"]:
        frame xpos 250 ypos 20 xpadding 10 background Frame("system/gui/miniframe.png", 12,12):
            at gui_dissolve_top
            has hbox
            text _("Mana shards") style "say_dialogue"
            text "[player.currency:>6]" text_align 1.0 min_width 100 style "say_dialogue"

    if current_mode == "Full Map" and not isinstance(stand, str): #rotates the minimap arrow for the direction you are facing
        add Tilemap(stand.level.map, mapped=stand.level.mapped) xpos 220 ypos 32 at gui_dissolve_top
        if stand.dy==-1:
            add Transform("system/gui/arrow.png", rotate =180, xpos = 220+stand.x*16, ypos = 32+stand.y*16) at gui_dissolve_top
        elif stand.dx==1:
            add Transform("system/gui/arrow.png", rotate = 270, xpos =220+stand.x*16, ypos = 32+stand.y*16) at gui_dissolve_top
        elif stand.dy==1:
            add Transform("system/gui/arrow.png", rotate = 0, xpos = 220+stand.x*16, ypos = 32+stand.y*16) at gui_dissolve_top
        else:
            add Transform("system/gui/arrow.png", rotate =90, xpos = 220+stand.x*16, ypos = 32+stand.y*16) at gui_dissolve_top
        vbox align (.75,.1) xsize 320: #select proiper sprite
            for i in [(mm_image[1],_("Wall")), #selects map sprite for mnini map from mm.png
                        (mm_image[2],_("Fake Wall")),
                        (mm_image[3],_("Door")),
                        (mm_image[4],_("Upstairs")),
                        (mm_image[5],_("Downstairs")),
                        (mm_image[6],_("Teleporter")),
                        (mm_image[7],_("Trap")),
                        (mm_image[8],_("Pitfall")),
                        (mm_image[9],_("Event")),
                        (mm_image[10],_("Battle")),
                        (mm_image[11],_("Boss"))]:
                hbox:
                    add i[0] yalign .5
                    null width 8
                    text i[1]
    else:
        if current_mode == "Organize":
            use backup_frame()
        else:
            use item_frame(current_actor)
        use attribute_frame(current_actor)

        window align (.35, .645) ysize 130:
            at gui_dissolve_top
            text current_message style "say_dialogue" size 20
            text current_ex_message outlines [(1,"#0009",1,1), (1,"#000d")] yoffset -4

    use status_frame(party[0], position=(5, -105), mode=current_mode)
    if len(party)>1:
        use status_frame(party[1], position=(295, -105), mode=current_mode)
    if len(party)>2:
        use status_frame(party[2], position=(585, -105), mode=current_mode)
    if len(party)>3:
        use status_frame(party[3], position=(5, -5), mode=current_mode)
    if len(party)>4:
        use status_frame(party[4], position=(295, -5), mode=current_mode)
    if len(party)>5:
        use status_frame(party[5], position=(585, -5), mode=current_mode)

    key "game_menu":
        if chosen_actor and chosen_item:
            action [Play("audio", "Cancel_Button"), SetVariable("chosen_actor", None), Show("message_screen", message=_("Select whom"))]
        elif chosen_skill != None:
            action [Play("audio", "Cancel_Button"), SetVariable("chosen_skill", None), Hide("message_screen")]
        elif chosen_actor != None:
            action [Play("audio", "Cancel_Button"), SetVariable("chosen_actor", None), Hide("message_screen")]
        elif chosen_item != None:
            action [Play("audio", "Cancel_Button"), SetVariable("chosen_item", None), Hide("message_screen")]
        else:
            action [Play("audio", "Closing_Menu"), Return()]


    key "K_TAB" action [Play("audio", "Closing_Menu"), Return()]
    key "hide_windows" action NullAction()





screen status_frame(who, position, mode): #party member status screen

    button xysize (290, 100) style "slot_button" bottom_padding 0:
        if position[0]<0:
            xanchor 1.0
            pos (config.screen_width + position[0], position[1])
        elif position[1]<0:
            yanchor 1.0
            pos (position[0], config.screen_height + position[1])
        elif position[1]<0 and position[0]<0:
            yanchor 1.0 xanchor 1.0
            pos (config.screen_width + position[0], config.screen_height + position[1])
        else:
            pos position
        if position[1]<0:
            at gui_dissolve_bottom
        else:
            at gui_dissolve_top

        if mode in ["Consumables", "Valuables", "Stats", "Full Map"] and not chosen_skill:
            if chosen_item and chosen_actor:
                action SelectedIf(chosen_actor==who)
            elif chosen_item:
                action Function(chosen_item.use, who=player, target =who) activate_sound None
            elif active_actor != None and who.vp>0 and party.index(who)>2:
                action Show("alt_confirm", message=_("Switch party members?"), yes_action=[Function(who.member_change), Return("change")])
            elif active_actor == None:
                action [SelectedIf(chosen_actor==who), Function(who.order_change)]
            else:
                action Show("alt_notify", message=_("You can only switch party members in your backup line."))
            if not chosen_item or not chosen_actor:
                hovered [SetVariable("current_actor", who), SetVariable("current_message", who.info),SetVariable("current_ex_message", "")]
        elif mode=="Organize" and not chosen_skill:
            action [Function(who.pop)]
            hovered [SetVariable("current_actor", who), SetVariable("current_message", who.info),SetVariable("current_ex_message", "")]
        elif mode=="ally":
            if who in [active_actor, shown_actor]:
                background Fixed(Frame("system/gui/frame4.png", 12,12),
                    Transform(Frame("system/gui/frame4.png", 12,12), additive=.2), fit_first=True)
            else:
                background Frame("system/gui/frame4.png", 12,12)
        elif mode=="enemy":
            background None

        if who == nobody:
            text _("―― Empty ――") align (.5,.5) style "say_label"
        else:
            vbox spacing -4:
                hbox xfill True:
                    text "[who.name]" size 22 style "say_label" min_width 100
                    fixed xysize (50, 30):
                        hbox yalign 1.0:
                            if who.disrupt>0:
                                hbox:
                                    add "system/gui/disrupt.png"
                                    text "%d"%who.disrupt color "#9ff" yalign 1.0 size 18
                            if who.paralyze>0:
                                hbox:
                                    add "system/gui/paralyze.png"
                                    text "%d"%who.paralyze color "#ee3" yalign 1.0 size 18
                            if who.stripped > 0:
                                hbox:
                                    add "system/gui/torn.png"
                            if who.vp<1:
                                hbox:
                                    add "system/gui/dying.png"
                    if who.flow>0:
                        add "system/gui/flow.png"
                        text "%d"%who.flow color "#ff6" yalign 1.0 size 18
                    elif who.panic>0:
                        add "system/gui/panic.png"
                        text "%d"%who.panic color "#99f" yalign 1.0 size 18
                    else:
                        text "Cp%d"%who.cp yalign 1.0 size 16
                    text "Lv%2d"%(who.level) yalign 1.0 size 18
                vbox xalign .5:
                    null height 8
                    hbox:
                        text "VP" line_leading -4 size 20 min_width 30
                        fixed fit_first True:
                            add Transform(Frame("system/gui/bar_disabled.png", 12, 6), size=(230,18))
                            bar value AnimatedValue(who.vp, who.max_vp, 1.0)
                            bar value AnimatedValue(who.vp, who.max_vp, .3) left_bar Frame("system/gui/bar_green.png", 12, 6)
                            text "{:0>3}/{:0>3}".format(int(who.vp),int(who.max_vp)) line_leading -7 size 21 xalign .9
                    null height 6
                    hbox:
                        text "AP" line_leading -4 size 20 min_width 30
                        fixed fit_first True:
                            add Transform(Frame("system/gui/bar_disabled.png", 12, 6), size=(230,18))
                            bar value AnimatedValue(who.ap, who.max_ap, 1.0)
                            bar value AnimatedValue(who.ap, who.max_ap, .3) left_bar Frame("system/gui/bar_blue.png", 12, 6)
                            text "{:0>3}/{:0>3}".format(who.ap,who.max_ap) line_leading -7 size 21 xalign .9





screen attribute_frame(who, xcoord=505): #actor display screen

    frame xysize (400, 365) pos (xcoord, 10) style_group "attributes" at gui_dissolve_top:
        has vbox
        hbox xfill True:
            text "[who.name]" font font_label size 42 min_width 200 #name
            text "Xp%02d"%(who.xp) size 22 yalign 1.0 #xp
            text "Lv%2d"%(who.level) size 26 yalign 1.0 #lvl

        label _("Attributes")

        hbox xfill True:
            vbox: #stats  hover text
                button action NullAction() activate_sound None:
                    text "VIT" size 16
                    hovered [SetVariable("current_message", _("For every point of Vitality, you gain 5 VP and 1 damage reduction against all types.")),
                        SetVariable("current_ex_message", "")]
                button action NullAction() activate_sound None:
                    text "AGI" size 16
                    hovered [SetVariable("current_message", _("For every point of Agility, you again 5 AP and an initiative bonus.")),
                        SetVariable("current_ex_message", "")]
                button action NullAction() activate_sound None:
                    text "MNT" size 16
                    hovered [SetVariable("current_message", _("For every point of Mentality, you gain 1 CP and bonuses to CP-related conditions. You also deal 1 more damage and take 1 less damage with elemental and magical attacks.")),
                        SetVariable("current_ex_message", "")]
                button action NullAction() activate_sound None:
                    text "STR" size 16
                    hovered [SetVariable("current_message", _("For every point of Strength, you deal 1 more damage and take 1 less damage with physical and melee attacks.")),
                        SetVariable("current_ex_message", "")]
                button action NullAction() activate_sound None:
                    text "DEX" size 16
                    hovered [SetVariable("current_message", _("For every point of Dexterity, you deal 1 more damage with ranged attacks. This also improves your hit chance by 5%, critical chance by 5%, and dodge chance by 3%.")),
                        SetVariable("current_ex_message", "")]
                button action NullAction() activate_sound None:
                    text "RES" size 16
                    hovered [SetVariable("current_message", _("For every point of Resilience, you gain 1 regeneration. This also makes you deal 1 more damage and take 1 less damage from poison attacks.")),
                        SetVariable("current_ex_message", "")]
            vbox:
                for i in ["vit", "agi", "mnt", "str", "dex", "res"]:
                    $ value1=getattr(who,i)

                    text "[value1:>2]" size 16 min_width 16
            vbox:
                for i in [_("{color=#3ff}Physical{/color}"),_("{color=#f0f}Poison{/color}"),_("{color=#6f6}Air{/color}"),_("{color=#f30}Fire{/color}"),_("{color=#99f}Ice{/color}"),_("{color=#ff0}Shock{/color}")]:
                    button action NullAction() activate_sound None:
                        text " [i!t]" size 16
                        hovered [SetVariable("current_message", _("Resistance reduces damage taken from attack types by a percentage. 0% means no damage reduction from this type, 100% is immunity to this type.")),
                            SetVariable("current_ex_message", "")]
            vbox:
                for i in ["physical", "poison", "air", "fire", "ice", "shock"]:
                    $ value1=get_icons(getattr(who,i))

                    text "[value1]" size 16 min_width 50

            vbox xsize 100:
                for i in who.abilities:
                    button style "attributes_button" action NullAction() activate_sound None:
                        text i size 16 min_width 70
                        hovered [SetVariable("current_message", ability_dict[i]), SetVariable("current_ex_message", "")]
                for j in xrange(6 - len(who.abilities)):
                    button style "attributes_button":
                        text "" size 16 min_width 70

        label _("Skills")

        grid 2 3 transpose False style_group "skill":
            for n,i in enumerate(who.skills):
                textbutton i.name:
                    if chosen_actor and chosen_item:
                        if n>0:
                            action [SetVariable("chosen_skill", i), Show("alt_confirm", message=_("There is already a skill there. Replace it?"), 
                                    yes_action=[Function(chosen_item.use, who=player, target=chosen_actor)], no_action=SetVariable("chosen_skill", None))]
                    elif not chosen_actor and not chosen_item:
                        activate_sound None
                        action [SelectedIf(chosen_skill==i), Function(i.order_change, who=current_actor)]
                    hovered [SetVariable("current_message",  i.get_info(who)), SetVariable("current_ex_message", i.get_ex_info(who))]

            for i in xrange(6-len(who.skills)):
                textbutton "":
                    if chosen_actor and chosen_item:
                        action [Show("alt_confirm", message=_("Learn this skill?"), 
                                yes_action=[Function(chosen_item.use, who=player, target=chosen_actor)])]

init python:
    #ability descriptions. this table is referenced by the stats screen in stats.rpy
    ability_dict = {"Brutal":_("If this character makes a critical hit, she gains 1 bonus CP."),
        "Patient":_("If this character takes a critical hit, she does not lose CP."),
        "Adaptive":_("If this character dodges, she gains 1CP."),
        "Spiritual":_("If this character makes a hit, the CP cost for this skill is reduced by 1."),
        "Prudent":_("This character starts with higher CP when entering combat, or when Flow/Panic ends."),
        "Fortitude":_("If this character is under 50% VP, she gains 1 CP on her turn."),
        "Masochist":_("If this character is under 50% VP, she does 20% more damage"), #WIP
        "Horny":_("When this character's clothes are torn, she gains 75% resistance to fire and physical damage until her clothes are repaired."), #WIP
        "Acrobat":_("This character gains a dodge bonus equal to 3x her CP."), 
        "Grappler":_("This character gains a melee critical bonus equal to 3x her CP."),
        "Hunter":_("This character gains a ranged critical bonus equal to 3x her CP."),
        "Conjurer":_("This character gains a magic critical bonus equal to 3x her CP."),
        "Serenity":_("This character is immune to disrupting attacks and the panic state."),
        "Sneaking":_("This character starts with a 20% AP bonus at the start of combat. She also increases your escape chance by 20%."),
        "Recovery":_("This character recovers AP equal to her agility stat + 5."),
        "Endurance":_("This character's AP drains 50% slower."),
        "Reflexes":_("This character only loses 1 AP when dodging."),
        "Parry":_("This character has a chance to parry melee attacks. When attacked, the attacker loses hit rate equal to 25% of her current AP."),
        "Floating":_("This character has a chance to dodge melee attacks. When attacked, the attacker loses hit rate equal to 50% of her current AP. This also makes her avoid spear trap damage."),
        "S-Field":_("Stealth-Field. When a character is targeted by a ranged or magic attack, the attacker loses hit rate equal to 25% of her current AP."),
        "D-Shield":_("Dispel-Shield. When a character is targeted by a magic attack, the attacker loses hit rate equal to 50% of her current AP."),
        "E-Skin":_("Elemental-Skin. When this character takes elemental damage, she temporarily gains 75% resistance to that damage type."),
        "Capacity":_("This character gains 1 attribute point for every odd level she earns."),
        "Capacity-2":_("NPC Capacity. Gain 1 VIT when reaching levels 5, 15, 25, etc. 1 AGI levels 10, 20, 30, etc. 1 MNT, STR, DEX, or RES levels 3, 7, 13, 17, etc."), #NEW
        "Dual-Soul":_("When a character's VP reaches 0, she will be revived with 40% VP. This skill will only activate once in-between town visits."),
        "XP-Debug":_("Hyper inflates XP gain for debugging."),
        "Master":_("As master of her subordinates, Yomi gains XP every time they defeat a monster.")}




screen item_frame(who):
    #items inventory
    python:
        adj = ui.adjustment(1.0, step=100, changed = store_yvalue)
        if current_mode=="Consumables":
            listitem = player.items
        else:
            listitem = player.valuables

    frame xpos 180 ypos 75 xysize (300, 300):
        at gui_dissolve_top
        has vbox
        hbox xfill True:
            label current_mode
            textbutton _("Sort") style "small_button" xalign 1.0 yalign .5:
                if not chosen_actor and not chosen_skill and not chosen_item:
                    if current_mode == "Consumables":
                        action Show("alt_confirm", message= _("Sort all items by default order?"), yes_action=Function(player.item_sort))
                    else:
                        action Show("alt_confirm", message= _("Sort all items by default order?"), yes_action=Function(player.valuable_sort))

        hbox:
            viewport yadjustment adj: #item inventory
                has vbox
                for i in listitem:
                    hbox xfill True:
                        python:
                            itemname=i.name
                        textbutton itemname style "item_button":
                            if not chosen_actor and not chosen_skill:
                                if chosen_item:
                                    action [SelectedIf(chosen_item==i)]
                                elif i.type in ["sell","valuable", "fox", "knight"]:
                                    activate_sound None
                                    action [Play("audio", "Click_Disabled_Button"), Show("alt_notify", message=_("You cannot use that right now."))]
                                    hovered [SetVariable("current_message", i.info), SetVariable("current_ex_message", "")]
                                elif i.type in ["allheal", "return", "lurk", "allure"]:
                                    action [SetVariable("chosen_item", i), Show("alt_confirm", message=_("Use this item?"), 
                                                yes_action=Function(i.use, who=player), no_action=SetVariable("chosen_item", None))]
                                    hovered [SetVariable("current_message", i.info),SetVariable("current_ex_message", "")]
                                else:
                                    action [SetVariable("chosen_item", i), Show("message_screen", message=_("Select party member"))]
                                    hovered [SetVariable("current_message", i.info),SetVariable("current_ex_message", "")]
            null width 4
            fixed yalign .5 xysize (10, 250):
                add Frame("system/gui/vscrollbar.png", 12,6)

                bar style "vscrollbar" adjustment adj

    key "rollback" action ReadbackScrollUp(adj)
    key "rollforward" action ReadbackScrollDown(adj)





screen backup_frame():

    $ adj = ui.adjustment(1.0, step=105, changed = store_yvalue) #sorting party / backup

    frame xpos 180 ypos 75 xysize (300, 300):
        at gui_dissolve_top
        has vbox
        hbox xfill True:
            label _("Backup")
            textbutton _("Sort") style "small_button" xalign 1.0 yalign .5:
                if not chosen_actor and not chosen_skill and not chosen_item:
                    action Show("alt_confirm", message= _("Sort backup members by default order?"), yes_action=Function(player.sort))
        hbox:
            vpgrid cols 4 yadjustment adj:
                for i in backup:
                    fixed xysize (70, 70):
                        if renpy.loadable("actors/{}/chip.png".format(i.objectname)):
                            add "actors/{}/chip.png".format(i.objectname) pos (1,1)
                        button style "face_button":
                            if not chosen_skill:
                                action [Function(i.add)]
                            hovered [SetVariable("current_actor", i), SetVariable("current_message", i.info), SetVariable("current_ex_message", "")]
            null width 4
            fixed yalign .5 xysize (10, 250):
                add Frame("system/gui/vscrollbar.png", 12,6)

                bar style "vscrollbar" adjustment adj

    key "rollback" action ReadbackScrollUp(adj)
    key "rollforward" action ReadbackScrollDown(adj)
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
