




init python:
    # new import random library for capacity-2
    import random
    class Actor(object): #initialize / variables to initialize an actor object

        def __init__(self, objectname="", name="", level=0, currency=0, vit=0, agi=0, mnt=0, str=0, dex=0, res=0,
            physical=0, poison=0, air=0, fire=0, ice=0, shock=0, type="", skills=None, abilities=None, hitface="", sufferface="", info = "", number=0):
            #initialize, but have defaults of zero/empty in case smth goes wrong

            #a lot of these actor class variables can be set on the actors.tsv sheet
            self.objectname = objectname
            self.original_name = objectname.capitalize().replace("_", " ")
            self.name=name
            self.level=int(level)
            self.base_level=int(level)
            self.currency = int(currency)

            #stats
            self.vit=int(vit) #stats
            self.agi=int(agi)
            self.mnt=int(mnt)
            self.str=int(str)
            self.dex=int(dex)
            self.res=int(res)

            #resists
            self.physical=int(physical)
            self.poison=int(poison)
            self.air=int(air)
            self.fire=int(fire)
            self.ice=int(ice)
            self.shock=int(shock)

            self.type=type #type of actor. Can be either magic, melee, or ranged

            #add skills and abilities to an actor
            #references skills.tsv
            if skills not in [None, [""]]: #is the actor's skills not null? aka do they have at least one skill
                self.skills = [getattr(store, x) for x in skills]
            else: #if an actor has no skills its empty
                self.skills=[]
            #abilities works similarly but I need to find the script it references as it doesnt use a tsv like skills.
            #my guess is battle.rpy might have the code tho
            if abilities not in [None, [""]]:
                self.abilities=abilities
            else: #if empty
                self.abilities=[]

            #facial expressions. String variable, and refers to the face png of an actor in their respective /actors/ sub folder
            #should be the image file name but without the .png extension
            #eg: hit1 would refer to hit1.png
            self.hitface=hitface
            self.sufferface=sufferface

            #info text displayed for a character's summary
            #corresponds to the column of the same name in actors.tsv
            self.info=info

            #idk I think this is for checking certain character states?
            self.number=int(number)

            self.items = [] #initialize empty list for items
            self.valuables = [] #initialize empty list for valuable items

            #other stats
            self.max_vp = self.vit*5+50 #calculate an actor / characters max HP. basically just 50 + 5*VIT
            self.vp= float(self.max_vp)
            self.dp=self.vp
            self.max_ap= self.agi*5+50 #calculate an actor / characters max AP. basically just 50 + 5*VIT
            self.ap=self.max_ap
            self.cp=self.mnt
            self.xp=0.0 #starting XP when recruited, can range from 0 to 100 (values over 100 get rounded down to 100)

            #statuses. 0 = dont have the status, 1 = has the status I think
            self.flow=0
            self.panic=0
            self.paralyze=0
            self.disrupt=0
            self.stun = 0

            #skills extra stuff
            if len(self.skills)>0:
                self.skill=self.skills[0]
            else:
                self.skill=None

            self.target=None
            #sprite stuff
            self.xposition = .85
            self.pose="default"
            self.dresses=[]
            self.dress = "default"
            self.stripped = 0 #0 = clothed
            if objectname in ["fox","knight","dark_elf"]: #references png names in actors folder. main char
                self.face_list=["normal","hit1","hit2","hit3","embarrassed","happy","angry","joking","laughing","neutral","scared","shocked","shy","smiling"] #eg: hit.png
            elif objectname in ["shopgirl","innkeeper"]: #shop owners
                self.face_list=["normal","hit1","hit2","hit3","embarrassed", "happy","angry","sad"]
            else: #monsters
                self.face_list=["normal","hit1","hit2","hit3","embarrassed"]
            self.face="normal"
            self.order=0
            self.defeat_count=0
            self.defeated_count=0
            self.soulraise = 0
            self.guardtype = None #seems to be for E-skin ability? boosts resists to a given element temporarily it seems
            if objectname in ["fox"]: #yumis clothes, fox is folder name for sprites
                self.dress_list=["default","bikini","bikini_black","schoolswim","bunnysuit","swimsuit","tribal","tiger","maid","chocolate","wedding","bondage","ribbon","demon","talisman","scifi"]
            elif objectname in ["knight"]: #Ceri clothes
                self.dress_list=["default","bikini","bikini_blue","dancer","schoolswim","bunnysuit","leaf","maid","tribal","lingerie","lingerie_black","chocolate","wedding","bondage","ribbon","ribbon_black","jewelry","scifi"]
            else: #everyone else
                self.dress_list=["default"]


        def face_change(self, hit=False):
            self.pose="default"
            if in_battle and config.skipping and config.skip_delay <= 5:
                return
            if hit or self.vp < 1 or self.panic:
                self.face=self.hitface
            elif self.flow: #flow state, default face
                self.face="normal"
            elif self.stripped > 0:
                if self==fox:
                    self.face="shy"
                else:
                    self.face="embarrassed"
            elif self.paralyze or self.disrupt:
                self.face=self.sufferface
            else:
                self.face="normal"
            return

        def order_change(self):



            if self.vp < 1:
                renpy.music.play("Click_Disabled_Button", channel="audio")
                renpy.hide_screen("message_screen")
                renpy.show_screen("alt_notify", message=_("Can't change the order of VP zero character."))
                store.chosen_actor=None
            else:
                if chosen_actor == None:
                    store.chosen_actor = self
                    renpy.show_screen("message_screen", message=_("Select a slot which will be replaced."))
                else:
                    for i in xrange(len(party)):
                        if party[i] == self:
                            store.party[i] = chosen_actor
                        elif party[i] == chosen_actor:
                            store.party[i]= self
                    store.chosen_actor = None
                    renpy.hide_screen("message_screen")
                    renpy.show_screen("alt_notify", message=_("Replaced the order."))


        def member_change(self):



            renpy.hide(active_actor.objectname, layer="fg")
            active_actor.ap=active_actor.max_ap/5
            self.order = active_actor.order
            for i in xrange(len(party)):
                if party[i] == self:
                    store.party[i] = active_actor
                elif party[i] == active_actor:
                    store.party[i]= self
            store.active_actor = self
            renpy.show(active_actor.objectname, at_list=[show_player(active_actor.xposition)], layer="fg")


        def add(self): #adding party members from jail / town



            if len(party)<6:
                store.backup.remove(self)
                store.party.append(self)
                renpy.hide_screen("message_screen")
                renpy.show_screen("alt_notify", message=_("Added into party."))
            else:
                renpy.hide_screen("message_screen")
                renpy.show_screen("alt_notify", message=_("Party is full."))


        def pop(self):



            if self not in [knight]: #check if you are trying to remove Ceri
                store.party.remove(self)
                store.backup.append(self)
                renpy.hide_screen("message_screen")
                renpy.show_screen("alt_notify", message=_("Removed from party."))
            else: #throw error if trying to remove ceri
                renpy.hide_screen("message_screen")
                renpy.show_screen("alt_notify", message=_("Can't remove her from party."))


        def disband(self): #disband/remove/release party member stat



            for i in copy(party):
                if i not in [knight]:
                    store.party.remove(i)
                    store.backup.append(i)
            renpy.hide_screen("message_screen")
            renpy.show_screen("alt_notify", message=_("Disbanded."))


        def sort(self, level=False): #sorting baraks members



            if level:
                store.backup.sort(key=attrgetter("level"), reverse=True)
            else:
                store.backup.sort(key=attrgetter("number"), reverse=False)
            renpy.hide_screen("message_screen")
            renpy.show_screen("alt_notify", _("Sorted"))


        def item_sort(self):



            self.items.sort(key=attrgetter("number"), reverse=False)
            renpy.music.play("click_button", channel="audio")
            renpy.hide_screen("message_screen")
            renpy.show_screen("alt_notify", _("Sorted"))

        def valuable_sort(self):



            self.valuables.sort(key=attrgetter("number"), reverse=False)
            fox.dresses.sort(key=attrgetter("number"), reverse=False)
            knight.dresses.sort(key=attrgetter("number"), reverse=False)
            renpy.music.play("click_button", channel="audio")
            renpy.hide_screen("message_screen")
            renpy.show_screen("alt_notify", _("Sorted"))

        def has(self, item):
            return item.objectname in [x.objectname for x in self.valuables+self.dresses+self.items+self.skills]


        def remove(self, item):
            for i in self.valuables[:]:
                if i.objectname == item.objectname:
                    self.valuables.remove(i)
            for i in self.items[:]:
                if i.objectname == item.objectname:
                    self.items.remove(i)
            for i in self.skills[:]:
                if i.objectname == item.objectname:
                    self.skills.remove(i)


        def don(self, item):
            self.dress = item.objectname.replace("fox_", "").replace("knight_", "").replace("dark_elf_", "")

        def raise_stats(self, point):  #raise all stats by a given #
        #eg: sylvi shyness dialogue from level0_chat calls this method
        #see if there's a damage reduction increase function similar to this?
            self.max_vp += 5*point
            self.max_ap += 5*point
            self.vit += point
            self.agi += point
            self.mnt += point
            self.str += point
            self.dex += point
            self.res += point

        #NEW BASIC METHOD to increase resists
        #basically same as raise_stats. Really broken so use sparingly
        #IN: self is the actor to increase states for, point is how many points you want to raise by
        def raise_resists(self, point):
            self.physical += point
            self.poison += point
            self.air += point
            self.fire += point
            self.ice += point
            self.shock += point
            #note due to how dmg is calced even if a resist goes above 4 / 100% it basically is the same functionally
            #unless there are skills which lower a user's resit?


        def xpchange(self, level): #how much earned XP?


            # do these compare to dungeon level or to enemy level?
            if  self.level+4 < level:
                val = 2.0 #more than 4 lvls lower than foe give x2 xp?
            elif self.level+4 == level:
                val = 1.0/3*5 #5/3 xp if enemy is 4 lvls above
            elif self.level+4 == level:
                val = 1.0/3*4
            elif self.level+3 == level:
                val = 1.0
            elif self.level+2 == level:
                val = 1.0/6*5
            elif self.level+1 == level:
                val = 1.0/6*4
            elif self.level  == level:
                val = 1.0/2
            elif self.level-1 == level:
                val = 1.0/3
            elif self.level-2  == level:
                val = 1.0/5
            elif self.level-3  == level:
                val = 1.0/8
            elif self.level-4  == level:
                val = 1.0/12
            elif self.level-5  == level:
                val = 1.0/16
            else:
                val = 1.0/20
            # change base XP given based on users level
            # higher lvls have lower base XP
            if self.level==1:
                val= val*12
            elif self.level==2:
                val=val*10
            elif self.level==3:
                val=val*9
            elif self.level==4:
                val=val*8
            elif self.level==5:
                val=val*7
            elif self.level==6:
                val=val*6.4
            elif self.level==7:
                val=val*6
            elif self.level==8:
                val=val*5.6
            elif self.level==9:
                val=val*5.3
            elif self.level==10:
                val=val*5
            elif self.level==11:
                val=val*4.8
            elif self.level==12:
                val=val*4.6
            elif self.level==13:
                val=val*4.4
            elif self.level==14:
                val=val*4.2
            else:
                val = val*4
            # NEW
            # debug XP boost ability
            if "XP-Debug" in self.abilities:
                val = val*100 #multiply by 100 so every encounter basically levels you up

            self.xp += val*persistent.xp/2.0
            if self.xp>=100:
                if self in party[:3]:
                    slot_y = .95
                    if self == party[0]:
                        slot_x = .12
                    elif self == party[1]:
                        slot_x = .35
                    elif self == party[2]:
                        slot_x = .58
                    renpy.music.play("level_up", channel="audio")
                    renpy.show("levelup", at_list=[show_state(slot_x, slot_y)], layer="screens", what=Text(_("Level Up"), style="effect_text", color="ff9"))
                if "Capacity" in self.abilities: #capacity for ceri stat growth
                    self.stats_check(self.level, self.level+1)

                # NEW
                # NPC growth / capacity 2 call
                elif "Capacity-2" in self.abilities:
                    self.npc_growth(self.level+1)

                self.level+=1 #lvl up
                self.xp=0.0


        def stats_check(self, old, new): #dictates lvl up stats for Capacity
            for i in xrange(old+1, new+1): #old = prior level, new = newly hit level
                if i>=66: #stop stat growth at lvl 66?
                    return
                if i ==3:
                    self.str += 1
                if i ==5:
                    self.vit += 1
                    self.max_vp += 5
                if i==7:
                    self.mnt += 1
                if i ==9:
                    self.dex += 1
                if i ==11:
                    self.agi += 1
                    self.max_ap += 5
                if i ==13:
                    self.str += 1
                if i in [15+x*12 for x in xrange(10)]:
                    self.vit += 1
                    self.max_vp += 5
                if i in [17+x*12 for x in xrange(10)]:
                    self.dex += 1
                if i in [19+x*12 for x in xrange(10)]:
                    self.agi += 1
                    self.max_ap += 5
                if i in [21+x*12 for x in xrange(10)]:
                    self.mnt += 1
                if i in [23+x*12 for x in xrange(10)]:
                    self.res += 1
                if i in [25+x*12 for x in xrange(10)]:
                    self.str += 1
            return

        # NEW
        # stats growth for non MCs
        # slower growth rate compared to capacity
        # lvls ending in 5 you gain +1 vit
        # lvls ending in 0 you gain +1 agi
        # lvls ending in 3, you gain either +1 mnt or str (random)
        # lvls ending in 7, you gain either +1 dex or res (random)
        # requires the library random which was imported in script
        def npc_growth(self,lvl):
            if ( (lvl-5) %10)==0: #W5,15,25 etc
                # VIT boost
                self.vit += 1
                self.max_vp += 5

            if (lvl%10)==0:
                # AGI boost
                self.agi += 1
                self.max_ap += 5

            if (lvl-3)%10==0:
                #MNT or STR
                ran_num = random.choice([1, 2])
                if ran_num == 1:
                    #MNT
                    self.mnt += 1
                else:
                    #STR
                    self.str += 1

            if (lvl-7)%10==0:
                #DEX or RES
                ran_num = random.choice([1, 2])
                if ran_num == 1:
                    #DEX
                    self.dex += 1
                else:
                    #RES
                    self.res += 1
            #end of npc growth method capacity 2 code
            return

        def reset_cp(self, param=.7):
            self.flow=0
            self.panic=0
            self.cp=1
            if "Prudent" in self.abilities:
                if param < .7:
                    param += .1
                else:
                    param += .15
            for i in xrange(self.mnt):
                if renpy.random.random()<param:
                    self.cp += 1
            if param < .7:
                if self.cp > 5:
                    self.cp = 5
            else:
                if self.cp > 8:
                    self.cp = 8


        def cp_change(self, value, force=False):



            if self in enemy:
                slot_x = self.xposition
                slot_y = .05
            else:
                slot_y = .95
                if self == party[0]:
                    slot_x = .12
                elif self == party[1]:
                    slot_x = .35
                elif self == party[2]:
                    slot_x = .58

            if value == -10:
                self.reset_cp(.4)
            elif force or (value !=0 and self.panic == 0 and self.flow == 0):
                self.cp += value
                if self in party:
                    renpy.show("cp", at_list=[show_state(slot_x, slot_y - .05)], layer="screens", what=Text("{:+}".format(value), style="effect_text"))
                else:
                    renpy.show("cp2", at_list=[show_state(slot_x, slot_y - .05)], layer="screens", what=Text("{:+}".format(value), style="effect_text"))
                if self.cp <= 0 and (self.panic==0 or force):
                    self.cp=0
                    self.flow = 0
                    self.panic = 9
                    for i in xrange(self.mnt):
                        if renpy.random.random()<.7:
                            self.panic -= 1
                    if self.panic < 2:
                        self.panic=2
                    self.ap=0
                    self.face_change()
                    renpy.music.play("Poisoned_2", channel="audio")
                    renpy.show("panic", at_list=[show_state(slot_x, slot_y)], layer="screens", what=Text(_("Panicked"), style="effect_text", color="#99f"))
                    return True
                if self.cp >= 10 and (self.flow==0 or force):
                    self.cp = 10
                    self.panic = 0
                    self.flow = 1
                    for i in xrange(self.mnt):
                        if renpy.random.random()<.7:
                            self.flow += 1
                    if self.flow < 2:
                        self.flow = 2
                    self.ap=self.max_ap
                    self.stun = 0
                    self.paralyze = 0
                    self.disrupt = 0
                    self.face_change()
                    if persistent.skip_inserts == None:
                        config.allow_skipping = False
                    elif persistent.skip_inserts == False:
                        config.skipping = None


                    config.allow_skipping = True
                    renpy.music.play("raged", channel="audio")
                    renpy.show("flow",at_list=[show_state(slot_x, slot_y)], layer="screens", what=Text(_("Flow"), style="effect_text", color="ff9"))
                    return True
            return


        def heal_walk(self):
            if self.vp>=1:
                reg=self.res/2.0
                if self.stripped>0:
                    reg /= 2.0
                self.vp += reg
                if self.vp > self.max_vp:
                    self.vp = self.max_vp

        def turn_reset(self):



            if self.vp>=1:
                self.ap += self.max_ap/5 #regenerate 20% of max AP every turn
                if "Recovery" in self.abilities:
                    self.ap += self.agi + 5
                if self.ap > self.max_ap:
                    self.ap = self.max_ap
                #set base amount of health regenerated
                reg=self.res

                #status condition checkers. if an actor has these status's de-increment their value by 1 until you hti 0
                if self.stun>0:
                    self.stun -= 1
                if self.paralyze>0:
                    self.paralyze -= 1
                if self.disrupt>0:
                    self.disrupt -=1
                if self.panic>0:
                    self.panic -= 1
                    reg = 0
                    if self.panic==0:
                        self.reset_cp()
                if self.flow>0: #if flow state
                    self.flow -= 1
                    reg += reg
                    if self.flow==0:
                        self.reset_cp(.4)
                if self.stripped>0:
                    reg /= 2.0 #if clothes are ripped recover only half as much healrt

                self.vp += reg #regenerate health based on REG stat

                if self.vp > self.max_vp: #if you'd go over your max VP set value to max VP
                    self.vp = self.max_vp
            self.face_change()


        def full_reset(self, heal_vp=False, repair_dress=False, level_reset=False):


            #reset/remove status conditions
            self.stun=0
            self.panic=0
            self.flow=0
            self.paralyze=0
            self.disrupt=0
            self.stun=0
            self.guardtype=None
            self.xposition = .85


            if heal_vp:
                self.vp=self.max_vp
                self.soulraise = 0
            self.ap=self.max_ap
            self.cp=self.mnt
            if self.cp>9: self.cp=9
            if repair_dress:
                self.stripped=0
            if level_reset:
                self.level = self.base_level


        def skill_auto(self, target): #auto battle?
            choice_list = self.skills[1:]
            choice_list.sort(key=attrgetter("ap"))
            for i in self.skills[1:]:
                if -i.ap >= self.ap:
                    choice_list.remove(i)
                elif  i.cp < 0 and -i.cp >= self.cp:
                    choice_list.remove(i)
                elif i.type == "magic" and self.disrupt > 0:
                    choice_list.remove(i)
                elif i.type == "heal" and (self.flow or (self.type != "heal" and self.panic == 0 and self.disrupt == 0 and self.paralyze == 0)):
                    choice_list.remove(i)
                elif i.attr == "capture":
                    choice_list.remove(i)
                elif i.attr == "disrupt" and ("Serenity" in target.abilities or target.vp <= target.max_vp*3/5 or self.level+2 < target.level or target.type != "magic" or target.disrupt):
                    choice_list.remove(i)
                elif i.attr == "terror" and ("Serenity" in target.abilities or target.vp <= target.max_vp*3/5 or self.level+2 < target.level or target.panic or self.flow):
                    choice_list.remove(i)
                elif i.type == "melee" and "Floating" in target.abilities and target.ap >= target.max_ap*3/4 and not self.flow and not target.panic:
                    choice_list.remove(i)
                elif i.type == "magic" and "D-Shield" in target.abilities and target.ap >= target.max_ap*3/4 and not self.flow and not target.panic:
                    choice_list.remove(i)
                elif i.type in ["melee", "ranged"] and self.paralyze > 0 and target.ap >= target.max_ap*3/4 and not self.flow and not target.panic:
                    choice_list.remove(i)
            if len(choice_list) == 0:
                return self.skills[0]
            elif target.ap <= target.max_ap*2/5 and target.vp <= choice_list[0].power and renpy.random.random() < .5:
                return choice_list[0]
            elif (self.panic > 0 or target.flow >0) and self.ap <= self.max_ap*2/5 and target.ap >= self.max_ap*4/5 and self.flow < 1 and target.panic < 1:
                return self.skills[0]
            elif self.ap <= self.max_ap*2/5 and self.type=="magic" and renpy.random.random() <.25:
                return self.skills[0]
            elif self.ap <= self.max_ap*2/5 and renpy.random.random() <.2:
                return self.skills[0]
            elif self.ap <= self.max_ap*3/5 and renpy.random.random()<.1 and self.flow < 1 and target.panic < 1:
                return self.skills[0]
            elif self.ap <= self.max_ap*4/5 and renpy.random.random()<.05 and self.flow < 1 and not target.panic <1:
                return self.skills[0]
            else:
                if (self.flow > 0 or target.panic > 0 or target.ap <= target.max_ap*2/5) and target.vp >= target.max_vp/5:
                    choice_list.sort(key=attrgetter("ap"), reverse=True)
                while True:
                    for i in choice_list:
                        if  self.flow and i.attr in ["astral"] and renpy.random.random() < .1:
                            return i
                        if self.type == i.type and i.attr in ["physical", "poison", "air", "fire", "ice", "shock"] and getattr(target, i.attr) == 0 and i.attr != target.guardtype and renpy.random.random() < .1:
                            return i
                        if self.type == i.type and i.attr in ["physical", "poison", "air", "fire", "ice", "shock"] and getattr(target, i.attr) <= 1 and renpy.random.random() < .1:
                            return i
                        if renpy.random.random() < .1:
                            return i


        def defence(self, user, aoe=False):

            #defending calcs for non AoE attacks

            undress_flag=False
            defeat_flag=False
            damage_flag=False
            critical_flag=False
            paralyze_flag=False
            disrupt_flag=False
            terror_flag=False
            stun_flag=False

            #sprite location
            if self in enemy:
                slot_x = self.xposition
                slot_y = .05
            else:
                slot_y = .95
                if self == party[0]:
                    slot_x = .12
                elif self == party[1]:
                    slot_x = .35
                elif self == party[2]:
                    slot_x = .58

            if self in party:
                self.xpchange(user.level)

            #calc hit rate
            #note: user is the attacker
            #self is defender
            hitrate = user.skill.hit + user.dex*5 + user.level*5 - self.ap - self.dex*3 - self.level*5
            #also references the levels of user and self to make weaker actors have a much harder time against stronger actors

            if self in party: #if the defender is you or an ally
                hitrate += difficulty*5 #calc enemy hitrate
                #game difficulty is (-2,0,2) from easist to hardest
                #so on abyssal difficulty enemies have an extra 10% hitrate

                hitrate -= max(0, 3-len(party))*10 #subtract hitrate based on party count it seems
                #so if your party is smaller enemies have less chance of hitting attacks?

            else: #if the defender is an enemy
                hitrate -= difficulty*5 #same as above but reversed. So max difficulty means your attacks are 10% less accurate
                hitrate += max(0, 3-len(party))*10

            #status checks
            if self.flow>0: #if defender has flow state decrease hitrate by 25%
                hitrate -=25
            elif self.panic>0:
                hitrate += 25
            if user.flow>0: #if enemy
                hitrate += 25
            elif user.panic>0:
                hitrate -= 25
            if user.paralyze>0 and user.skill.type in ["melee", "ranged"]:
                hitrate -=50

            #ability checks to do one last modification to hitrate
            if "Floating" in self.abilities and user.skill.type == "melee" and not "Floating" in user.abilities:
                hitrate -= int(self.ap/2)
            if "Parry" in self.abilities and user.skill.type == "melee":
                hitrate -= int(self.ap/4)
            if "S-Field" in self.abilities and user.skill.type in ["magic","ranged"]:
                hitrate -= int(self.ap/4)
            if "D-Shield" in self.abilities and user.skill.type == "magic":
                hitrate -= int(self.ap/2)
            if "Acrobat" in self.abilities:
                hitrate -= self.cp*3

            #Crit chance calulation
            criticalrate= hitrate - user.skill.hit + user.skill.critical
            #ability checks
            if "Grappler" in user.abilities and user.skill.type == "melee":
                criticalrate += user.cp*3
            if "Hunter" in user.abilities and user.skill.type == "ranged":
                criticalrate += user.cp*3
            if "Conjurer" in user.abilities and user.skill.type == "magic":
                criticalrate += user.cp*3


            #this if statement is if a hit LANDS
            if hitrate >= renpy.random.randint(1,100) or self.ap < 1 or (self.ap < 5 and "Reflexes" not in self.abilities):
                #set initial damage before any reductions or bonuses
                if user.skill.type == "melee":
                    damage = (user.skill.power+user.str)
                elif user.skill.type == "ranged":
                    damage = (user.skill.power+user.dex)
                else:
                    damage = (user.skill.power+user.mnt)

                #calcs dmg reduced from a defender/self's stats i think
                if user.skill.attr == "physical":
                    damage += user.str - (self.vit+self.str)/2.0
                if user.skill.attr == "poison":
                    damage += user.res - (self.vit+self.res)/2.0
                else:
                    damage += user.mnt - (self.vit+self.mnt)/2.0


                if self.level<=10:
                    damage = damage*(1.0+user.level*0.04-self.level*0.06)
                elif self.level<=30:
                    damage = damage*(.9+user.level*0.04-self.level*0.05)
                else:
                    damage = damage*(.6+user.level*0.04-self.level*0.04)

                #increase or decrease damage depending on difficulty
                if self in party:
                    damage *= (1+difficulty*0.04 - max(0, 3-len(party))*0.1)
                else:
                    damage *= (1-difficulty*0.04 + max(0, 3-len(party))*0.1)

                #Resists reduction
                #can probably change to allow user resists to not be by 25% intervals
                #and have like resists be on a much more flexible scale (eg: 10% increments)
                for i in [("physical",self.physical),("poison",self.poison),("air",self.air),("fire",self.fire),("ice",self.ice),("shock",self.shock)]:
                    if user.skill.attr == i[0]:
                        if i[1]>=4: #100% resistance causes attack to deal zero dmg
                            damage=0
                            renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("Immune"), style="ability_text"))
                        elif self.guardtype == i[0]: #Eskin ability. reduce dmg by 75%
                            damage= damage/4.0
                            renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("E-Skin"), style="ability_text"))
                        elif i[1]==3: #75%
                            damage= damage/4.0
                            renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("High Resist"), style="ability_text"))
                        elif i[1]==2: #50%
                            damage= damage/2.0
                            renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("High Resist"), style="ability_text"))
                        elif i[1]==1: #25% resistance
                            damage = damage*3/4.0
                            renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("Resist"), style="ability_text"))
                if "E-Skin" in self.abilities and user.skill.attr in ["poison","air","fire","ice","shock"]: #E-skin check, and also boost resist
                    self.guardtype = user.skill.attr
                if "Serenity" in self.abilities and user.skill.attr in ["disrupt","terror"]:
                    renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("Immune"), style="ability_text"))
                if aoe:
                    damage /= 2.0 #AoE attacks do 1/2 dmg?
                if damage<1 or user.skill.power==0: #if you do zero dmg
                    damage=0



                if criticalrate > renpy.random.randint(0,100):  #crit RNG calc
                    #basically if the character/actors crit chance is higher than the randomly genereated number 0-100 you crit
                    renpy.music.play("critical_hit", channel="audio")
                    renpy.pause(.05)
                    damage = int(damage*(1.0+renpy.random.random()*1/5)*1.5) #crit dmg calc
                    #dmg is attacks damage * (1 + (a random floating pt number between 0 and 1 divided by 5)) and then multiply by 1.5
                    #so range seems to be 1.5 to 1.7x damage?
                    critical_flag=True
                    renpy.show("critical", at_list=[show_damage(self.xposition, .35)], layer="screens", what=Text(_("Critical"), style="effect_text", size=80,color= "#ee6"))
                    renpy.show("damage", at_list=[show_damage(self.xposition,.5)], layer="screens", what=Text("%s"%damage, style="damage_text", size=150, color= "#f66"))
                else: #non crit attack
                    renpy.music.play("hit", channel="audio")
                    renpy.pause(.05)
                    damage = int(damage*(1.0+renpy.random.random()*1/5))
                    renpy.show("damage", at_list=[show_damage(self.xposition,.5)], layer="screens", what=Text("%s"%damage, style="damage_text", size=100, color= "#ee6"))

                #damage check
                if damage >= 1: #if you do at least one damage
                    damage_flag=True
                    self.vp -= damage #lower health / do damage
                    if "Endurance" in self.abilities: #Endurance skill, drain AP half speed
                        self.ap -= int(damage/8)
                    else: #no Endurance skill drain AP normally
                        self.ap -= int(damage/4)
                    if self.ap< 1: self.ap=0
                    if self.vp< 1: self.vp=0


                #turn order? Is dependent on game difficulty
                change = 0.5
                if self in party:
                    change += difficulty/2.0
                else:
                    change -= difficulty/2.0

                #Status conditions

                #Disruption status
                if user.skill.attr=="disrupt" and "Serenity" not in self.abilities:
                    change += renpy.random.random()*3+(user.mnt-self.mnt)*2+(user.level-self.level)
                    if critical_flag:
                        change=change*3/2.0
                    if change >= 2.0:
                        disrupt_flag=True
                        self.disrupt += int(change)
                        if self.disrupt>9:self.disrupt=9
                        renpy.music.play("magic_sealed", channel="audio")
                        renpy.show("status", at_list=[show_state(slot_x, slot_y)], layer="screens", what=Text(_("Disrupted"),  style="effect_text", color="f99"))

                #Paralyze / Poison status
                if user.skill.attr=="poison" and self.poison != 3:
                    change += renpy.random.random()*3+(user.res-self.res)*2+(user.level-self.level)
                    if critical_flag:
                        change=change*3/2.0
                    if self.poison>0:
                        change=change*(4-self.poison)/4.0
                    if change >= 2.0:
                        paralyze_flag=True
                        self.paralyze += int(change)
                        if self.paralyze>9:self.paralyze=9
                        renpy.music.play("poisoned", channel="audio")
                        renpy.show("status", at_list=[show_state(slot_x, slot_y)], layer="screens", what=Text(_("Paralyzed"),  style="effect_text", color="f9f"))

                #terror status
                if user.skill.attr=="terror" and "Serenity" not in self.abilities:
                    change = renpy.random.random()*3+(user.mnt-self.mnt)*2+(user.level-self.level)
                    change = change/2.0
                    if critical_flag:
                        change=change*3/2.0
                    if change >= 1.0:
                        terror_flag=True
                        self.cp_change(-int(change))
                elif user.skill.attr != "terror":
                    if critical_flag:
                        if self.stripped > 0 and "Patient" not in self.abilities:
                            self.cp_change(-2)
                        elif self.stripped > 0 or "Patient" not in self.abilities:
                            self.cp_change(-1)


                if paralyze_flag or disrupt_flag or damage >= self.max_vp/5:
                    self.face_change(hit=True)
                else:
                    self.face_change(hit=False)
                if self in party:
                    renpy.show(self.objectname, at_list=[shake, hide_out], layer="fg")
                else:
                    renpy.show(self.objectname, at_list=[smallshake])
                renpy.pause(0.75*persistent.battlespeed)


                if critical_flag and self.vp <= self.max_vp*.5 and self.stripped < 2 and damage_flag:
                    if  self.stripped == 0 or persistent.adult:
                        if persistent.inserts:
                            slow_skip = False
                            if persistent.while_inserts == "slow" and config.skipping:
                                slow_skip = True
                                config.skipping=False
                            elif persistent.while_inserts == "stop":
                                config.skipping=False
                            if not config.skipping:
                                renpy.call_in_new_context("tearing", actor=self)
                                if persistent.while_inserts == "slow" and slow_skip:
                                    config.skipping="slow"
                            else:
                                renpy.music.play("tearing", channel="audio")
                                self.stripped += 1
                                self.face_change()
                                renpy.pause(.25)


                if self.vp < 1 and self.soulraise==0 and "Dual-Soul" in self.abilities:
                    if False:
                        slow_skip = True if persistent.while_inserts == "slow" and config.skipping else False
                        if persistent.while_inserts != "skip":
                            config.skipping=False
                        renpy.call_in_new_context("dualsoul", actor=self)
                        if persistent.while_inserts == "slow" and slow_skip:
                            config.skipping="slow"

                    renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("Dual-Soul"), style="ability_text"))
                    self.soulraise = 1
                    self.vp= self.max_vp*2/5
                    self.flow==0
                    self.cp_change(10, force=True)
                    self.face_change()
                    renpy.pause (.5)


                elif self.vp < 1:
                    defeat_flag=True
                    if self in enemy:
                        getattr(store, self.objectname.replace("_1","").replace("_2","").replace("_3","")).defeated_count +=1
                        user.defeat_count+=1
                    if self not in party:
                        store.enemy_alive -= 1
                        for i in party:
                            if "Master" in i.abilities:
                                i.xpchange(self.level+4)
                            elif i.vp >= 1:
                                i.xpchange(self.level+2)
                            else:
                                i.xpchange(self.level+1)
                        for i in backup:
                            if "Master" in i.abilities:
                                i.xpchange(self.level+4)
                            else:
                                i.xpchange(self.level+1)
                    if user.skill.attr=="capture":
                        if self.level <= user.level and allow_capture:
                            renpy.music.play("Get_Item_2", channel="audio")
                            renpy.show("finish", at_list=[show_finish(self.xposition)], layer="screens", what=Text(_("Captured"), style="finish_text"))
                            captured.append(getattr(store, self.objectname.replace("_1","").replace("_2","").replace("_3","")))
                            current_captured.append(getattr(store, self.objectname.replace("_1","").replace("_2","").replace("_3","")))
                        else:
                            renpy.music.play("Knockdown_Hard", channel="audio")
                            renpy.show("finish", at_list=[show_finish(self.xposition)], layer="screens", what=Text(_("Capturing Failed"), style="finish_text"))
                    else:
                        renpy.music.play("Knockdown_Hard", channel="audio")
                        renpy.show("finish", at_list=[show_finish(self.xposition)], layer="screens", what=Text(_("Defeated"), style="finish_text"))
                    if self in party:
                        renpy.transition(wipedown, layer="fg", always=True)
                        renpy.hide(self.objectname, layer="fg")
                        store.passive_actor = None
                    else:
                        renpy.transition(wipedown, layer="master", always=True)
                        renpy.hide(self.objectname, layer="master")
                    renpy.pause(1.0*persistent.battlespeed)
                    renpy.hide("finish", layer="screens")


                    if self in party:
                        for i in party[3:]:
                            if i.vp >=1:
                                store.party.remove(i)
                                store.party.remove(self)
                                store.party.insert(2,i)
                                store.party.append(self)
                                user.target=i
                                i.order = battleturn + renpy.random.randint(10, 20) - i.agi
                                break
                    elif self in enemy:
                        for i in xrange(len(enemy)):
                            if partytarget.vp>=1: break
                            store.partytarget=enemy[0+i]
                        for n,i in enumerate(enemy[3:]):
                            if i.vp >=1:
                                store.enemy.remove(i)
                                if self == enemy[0]:
                                    store.enemy.insert(0,i)
                                    enemy[0].xposition = self.xposition
                                    renpy.show(enemy[0].objectname, at_list=[show_enemy(enemy[0].xposition)])
                                elif self == enemy[1]:
                                    store.enemy.insert(1,i)
                                    enemy[1].xposition = self.xposition
                                    renpy.show(enemy[1].objectname, at_list=[show_enemy(enemy[1].xposition)])
                                elif self == enemy[2]:
                                    store.enemy.insert(2,i)
                                    enemy[2].xposition = self.xposition
                                    renpy.show(enemy[2].objectname, at_list=[show_enemy(enemy[2].xposition)])
                                store.enemy.remove(self)
                                store.enemy.append(self)
                                user.target=i
                                i.order = battleturn + renpy.random.randint(10, 20) - i.agi
                                renpy.pause(0.5*persistent.battlespeed)
                                break



                if not aoe:
                    if user.skill.cp == -10:
                        user.cp_change(user.skill.cp)
                    elif user.skill.cp == 0:
                        if defeat_flag and (critical_flag and "Brutal" in self.abilities):
                            user.cp_change(3)
                        elif defeat_flag or (critical_flag and "Brutal" in self.abilities):
                            user.cp_change(2)
                        else:
                            user.cp_change(1)
                    elif user.skill.cp < 0:
                        if user.skill.cp == -2 and "Spiritual" in user.abilities:
                            user.cp_change(-1)
                        elif "Spiritual" not in user.abilities:
                            user.cp_change(user.skill.cp)



            else: #attack misses
                if "Reflexes" in self.abilities:
                    self.ap -= 1
                else:
                    self.ap -= 5
                if "S-Field" in self.abilities and user.skill.type in ["magic", "ranged"]:
                    renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("S-Field"), style="ability_text"))
                    renpy.music.play("Dodge_sound", channel="audio")

                    if self in party:
                        renpy.show(self.objectname, at_list=[stealth_r, hide_out], layer="fg")
                        renpy.show(self.objectname, tag="hide", at_list=[stealth_player(self.xposition)], layer="fg")
                    else:
                        renpy.show(self.objectname, at_list=[stealth_l])
                        renpy.show(self.objectname, tag="hide", at_list=[stealth_enemy(self.xposition)])
                    renpy.pause(0.5*persistent.battlespeed)
                    renpy.hide("hide")
                    renpy.hide("hide", layer="fg")
                elif "D-Shield" in self.abilities and user.skill.type == "magic":
                    renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("D-Shield"), style="ability_text"))
                    renpy.music.play("shield", channel="audio")
                    renpy.show("magic_2", at_list=[spellout(self.xposition)], layer="screens")
                    renpy.pause(0.5*persistent.battlespeed)
                    renpy.hide("magic_2", layer="screens")
                elif "Parry" in self.abilities and user.skill.type == "melee":
                    renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("Parry"), style="ability_text"))
                    renpy.music.play("Hit_Slashed_Sword_1", channel="audio")
                    if self in party:
                        renpy.show("cross_slashes", at_list=[effect_player(self.xposition)], layer="screens")
                    else:
                        renpy.show("cross_slashes", at_list=[effect_enemy(self.xposition)], layer="screens")
                    renpy.pause(0.5*persistent.battlespeed)
                else:
                    if "Floating" in self.abilities and user.skill.type == "melee" and not "floating" in user.abilities:
                        renpy.show("defence", at_list=[show_ability(self.xposition)], layer="screens", what=Text(_("Floating"), style="ability_text"))
                    renpy.music.play("Dodge_sound", channel="audio")

                    if self in party:
                        renpy.show(self.objectname, at_list=[sway_r, hide_out], layer="fg")
                    else:
                        renpy.show(self.objectname, at_list=[sway_l])
                    renpy.pause(0.5*persistent.battlespeed)

                if "Adaptive" in self.abilities:
                    self.cp_change(1)

                if not aoe:
                    if user.skill.cp < 0:
                        user.cp_change(user.skill.cp)


            self.face_change()
            renpy.hide("defence", layer="screens")
            renpy.hide("damage", layer="screens")
            renpy.hide("critical", layer="screens")
            return






    def read_actor(filename,duplicate=True):




        actor_list=[]

        f = renpy.file(filename)
        for n,l in enumerate(f):
            l = l.decode("utf-8")
            if filename.endswith(".csv"):
                a = l.rstrip().split(",")
            else:
                a = l.rstrip().split("\t")
            if not a[0] == "":
                for i in xrange(21-len(a)):
                    a.append("")
                setattr(store, a[0], Actor(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14], a[15], a[16],
                    a[17].split(","), a[18].split(","), a[19], a[20], a[21], number=n))
                if duplicate:
                    setattr(store, a[0]+"_1", Actor(a[0]+"_1", a[1]+" 1", a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14], a[15], a[16],
                        a[17].split(","), a[18].split(","), a[19], a[20], a[21], number=n))
                    setattr(store, a[0]+"_2", Actor(a[0]+"_2", a[1]+" 2", a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14], a[15], a[16],
                        a[17].split(","), a[18].split(","), a[19], a[20], a[21], number=n))
                    setattr(store, a[0]+"_3", Actor(a[0]+"_3", a[1]+" 3", a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14], a[15], a[16],
                        a[17].split(","), a[18].split(","), a[19], a[20], a[21], number=n))
                actor_list.append(globals()[a[0]])


                for i in globals()[a[0]].abilities:
                    if i not in ability_dict.keys():
                        raise NameError(a[0] + ':' + i + ' is not ability')

        f.close()

        return actor_list






    def register_actor_image(filename, duplicate=True):



        f = renpy.file(filename)
        for l in f:
            l = l.decode("utf-8")
            if filename.endswith(".csv"):
                a = l.rstrip().split(",")
            else:
                a = l.rstrip().split("\t")
            if not a[0] == "":
                for file in renpy.list_files():
                    if file.startswith('actors/{}/'.format(a[0])) and file.endswith('/default.png'):
                        renpy.image(a[0], DynamicDisplayable(render_actor, a[0]))
                        renpy.image(a[0]+"_l", DynamicDisplayable(render_actor, a[0], large=True))
                        if duplicate:
                            renpy.image(a[0]+"_1", DynamicDisplayable(render_actor, a[0]+"_1"))
                            renpy.image(a[0]+"_2", DynamicDisplayable(render_actor, a[0]+"_2"))
                            renpy.image(a[0]+"_3", DynamicDisplayable(render_actor, a[0]+"_3"))
                            renpy.image(a[0]+"_1_l", DynamicDisplayable(render_actor, a[0]+"_1", large=True))
                            renpy.image(a[0]+"_2_l", DynamicDisplayable(render_actor, a[0]+"_2", large=True))
                            renpy.image(a[0]+"_3_l", DynamicDisplayable(render_actor, a[0]+"_3", large=True))
                        break
                else:
                    renpy.image(a[0], Placeholder("girl"))
        f.close()


    def render_actor(st, at, actor_name, large=False):




        actor = globals()[actor_name]
        if large:
            actor_path = "actors_l/{}/{}/".format(actor_name.replace("_1","").replace("_2","").replace("_3",""), actor.pose)
        else:
            actor_path = "actors/{}/{}/".format(actor_name.replace("_1","").replace("_2","").replace("_3",""), actor.pose)
        if actor.stripped > 0 and renpy.loadable(actor_path+"{}{}.png".format(actor.dress, actor.stripped)):
            layers=[actor_path+"{}{}.png".format(actor.dress, actor.stripped)]
        elif actor.stripped > 1 and renpy.loadable(actor_path+"base.png"):
            layers=[actor_path+"base.png"]
        elif renpy.loadable(actor_path+"{}.png".format(actor.dress)):
            layers=[actor_path+"{}.png".format(actor.dress)]
        else:
            layers=[actor_path+"default.png"]

        if actor.flow > 0:
            if renpy.loadable(actor_path+"{}{}.png".format(actor.dress, actor.stripped)):
                layers.insert(1, Transform(zoomshining(actor_path+"{}{}.png".format(actor.dress, actor.stripped))))
            else:
                layers.insert(1, Transform(zoomshining(actor_path+"default.png")))

        if actor.face != None:
            if renpy.loadable(actor_path+"face/{}.png".format(actor.face)):
                layers.append(actor_path+"face/{}.png".format(actor.face))
            elif renpy.loadable(actor_path+"face/normal.png"):
                layers.append(actor_path+"face/normal.png")

        if large:
            return Fixed(*layers, fit_first=True, anchor=(.5,.4)), None
        else:
            return Fixed(*layers, fit_first=True, anchor=(.5,.5)), None
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
