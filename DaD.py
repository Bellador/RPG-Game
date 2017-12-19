# Text based Dungeons and Dragons game

# --------------ATTRIBUTE DEFINITION------------------------------------------------------------------------------------
# health: low 250 - 3500 high
# armour: (armour value regarding health point protection/ dmg mitigation) 0-100
# weapon: (weapon description) string -> maybe weapon specific attributes
# dmg: (damage per hit) will be a range and maybe light and heavy attacks (30% stronger but hight dodge chance for enemy)
# agility: (ability to dodge attacks/debuffs) in %
# charisma: (ability to convince and lead) 0 - 10
# --------------------- PERSONAS ---------------------------------------------------------------------------------------
# Narrator - provides verbal Feedback of the game progress, fight progression, environment etc.
# class names - provides verbal Feedback for it's own persona
# -------------------- ATTACKS -----------------------------------------------------------------------------------------
# light dmg: 2/3 of heavy
# heavy dmg: reference
# crit dmg: double

# ------------------- IMPORTS --------------------------------------
import random
import time
import turtle
import tkinter


# ------------------------------------------------------------------

# chance to break armour / mitigation in regards to attack type

def init_attack(hero, npc, pen_object):  # takes the object names

    #### INPUT listener -> key for light attack and so on
    print("--------------ENCOUNTER---------------")
    print(str(hero.name) + " VS " + str(npc.__class__.__name__))
    attacker_attacks = hero.attacks()
    defender_attacks = npc.attacks()
    init_hero_pos = hero.position()
    init_npc_pos = npc.position()
    pen_object_shape = pen_object.shape()
    hero.up()
    hero.setheading(0)
    npc.up()
    npc.setheading(180)
    pen_object.color("white")
    pen_object.up()


    dmg_pos = (0, 200)
    hit_pos = (0, 170)
    dodge_pos = (0, 140)
    crit_pos = (0, 110)
    pen_object.setpos(dmg_pos)

    order = [hero, npc]

    if npc.agility >= hero.agility:
        order = list(reversed(order))  # reverse provides a reversed iterator, not a reversed list! -> list()

    round_counter = 0
    while hero.health and npc.health > 0:
        round_counter += 1
        print("Round {}: {} attacks {}".format(round_counter, order[0].name, order[1].name))
        if order[0].__class__.__name__ in Setup.char_list: # check if it's the turn of the hero or the npc
            print("Narrator: Choose your action: ")
            for i, attack in enumerate(order[0].attacks()):
                print("{}. {}".format(int(i + 1), attack[0]))
            print("{}. Try to escape".format(i + 2))

            while True:
                action = input("Enter the chosen number: ")
                if action.isdigit() and int(action) in list(range(1, len(order[0].attacks())+1)):
                    break
                else:
                    print("Please enter a valid number")
            if int(action) != i + 2:
                result_tuple = order[1].getAttacked(order[0].attacks()[int(action) - 1], pen_object)
                print("-------------------------------")
            elif int(action) == i + 2:  # handling escape action
                pass

        else:
            action = random.randint(0, 1)
            result_tuple = order[1].getAttacked(order[0].attacks()[int(action)], pen_object)
            print("-------------------------------")
        # Attack movement
        order[0].fd(500)
        time.sleep(0.2)
        order[0].bk(500)

        if result_tuple[0] == False:
            pen_object.setpos(hit_pos)
            pen_object.write("MISS", font=("Arial", 30, "normal"))
        elif result_tuple[1] == True:
            pen_object.setpos(dodge_pos)
            pen_object.write("DODGED", font=("Arial", 30, "normal"))
        elif result_tuple[3] != None:
            pen_object.setpos(dmg_pos)
            pen_object.write(str(round(result_tuple[3])), font=("Arial", 30, "normal"))

        if result_tuple[2] == True:
            pen_object.color("red")
            pen_object.setpos(crit_pos)
            pen_object.write("CRITICAL HIT!", font=("Arial", 30, "normal"))
            pen_object.color("white")


        if result_tuple[4] == True: #set armour break symbol
            pen_object.ht()
            pen_object.setpos(order[1].position()[0], order[1].position()[1]+100)
            pen_object.st()
            pen_object.shape("armour_break_status.gif")
            pen_object.stamp()
            pen_object.ht()

        if hero.health <= 0:
            screen.done()
            pass

        time.sleep(2)
        pen_object.clear()
        pen_object.shape(pen_object_shape)
        order = list(reversed(order))

    if npc.health <= 0:
        for i in range(5):
            npc.ht()
            time.sleep(0.15)
            npc.st()
            time.sleep(0.15)
        npc.ht()
        Draw.redraw(object_handler.current_screens[0], False)
        object_handler.current_screens[0].bgcolor("green")
        hero.shape("classic")
        hero.setpos(Move.hero_pos_before_enc[0], Move.hero_pos_before_enc[1])
        Move.encounter = False

# --------------------------------------------------------------
class Draw:  # building of a 2D array (map) with every tile having specific attributes (enemies, forest, plain, etc.)

    pen = turtle.Turtle()  # turtle for drawing
    list_tree = []
    list_grass = []
    list_potions = {}  # stamp_id and print location
    kill_display_pos = (-320, 180)
    font_size = 40

    @staticmethod
    def tree(pen):
        circle_size = 40
        circle_color = "#32A962"
        pen.color("brown", "brown")
        pen.pensize(4)
        pen.fd(20)
        pen.up()
        pen.bk(10)
        pen.down()
        pen.left(90)
        pen.fd(65)
        pos = pen.position()

        pen.up()
        pen.setpos(int(pos[0]) - random.randint(2, 8), int(pos[1]) - random.randint(17, 23))
        pen.down()
        pen.dot(circle_size, circle_color)

        pen.up()
        pen.setpos(int(pos[0]) + random.randint(2, 8), int(pos[1]) - random.randint(17, 23))
        pen.down()
        pen.dot(circle_size, circle_color)

        pen.up()
        pen.setpos(int(pos[0]) - random.randint(-1, 6), int(pos[1]) + random.randint(-2, 2))
        pen.down()
        pen.dot(circle_size, circle_color)
        pen.up()

        pen.setpos(int(pos[0]) + random.randint(0, 6), int(pos[1]) + random.randint(-2, 2))
        pen.down()
        pen.dot(circle_size, circle_color)
        pen.up()

        pen.setpos(int(pos[0] + random.randint(-2, 2)), int(pos[1]) + random.randint(2, 8))
        pen.down()
        pen.dot(circle_size, circle_color)
        pen.up()

        pen.right(90)

    @staticmethod
    def grass(pen):
        start_pos = pen.position()
        pen.color("#8AFFB9", "#8AFFB9")
        pen.pensize(5)
        pen.setheading(90)
        pen.circle(10, 100)
        pen.up()
        pen.setpos(start_pos)
        pen.down()
        pen.setheading(90)
        pen.fd(15)
        pen.up()
        pen.setpos(start_pos)
        pen.down()
        pen.setheading(90)
        pen.circle(-10, 100)
        pen.setheading(0)

    @classmethod
    def potion(cls, pen):
        potion_location = pen.position()
        pen.pensize(15)
        pen.color("#980000", "#D44A4A")
        stamp_ID = pen.stamp()
        cls.list_potions[stamp_ID] = potion_location

        # print letters HP
        pen.up()
        pen.setpos(potion_location[0] - 5, potion_location[1] - 8)
        pen.down()
        text = "HP"
        pen.pencolor("white")
        pen.write(text)
        return cls.list_potions

    @classmethod
    def redraw(cls, canvas, encounter):
        print("Redrawing...")
        pen = cls.pen
        t = canvas.tracer()
        canvas.tracer(0, 0)  # turns off turtle animation
        pen.clear()

        if encounter == False:

            pen.up()
            pen.setpos(-350, -250)
            pen.down()
            pen.color("Black")
            for border in range(2):
                pen.fd(700)
                pen.left(90)
                pen.fd(500)
                pen.left(90)

            for grass in cls.list_grass:
                pen.up()
                pen.setpos(grass[0], grass[1])
                pen.down()
                cls.grass(pen)

            for tree in cls.list_tree:
                pen.up()
                pen.setpos(tree[0], tree[1])
                pen.down()
                cls.tree(pen)

            for key in list(cls.list_potions):
                pen.up()
                pos = cls.list_potions[key]
                pen.setpos(pos[0], pos[1])
                pen.down()
                cls.potion(pen)
                del cls.list_potions[key]
            cls.kill_display()
            canvas.update()
            canvas.tracer(t, 0)

        else:
            cls.encounter(encounter, canvas, t)

    @classmethod
    def environment(cls, canvas):  # canvas is passed screen object, draws map
        print("Draw environment")
        cls.list_tree = []
        cls.list_grass = []
        cls.list_potions = {}
        pen = cls.pen
        # pen = object_handler.current_heros[0] <- actual code
        pen.speed(0)  # highest speed
        t = canvas.tracer()
        canvas.tracer(0, 0)  # turns off turtle animation
        pen.shape("circle")
        pen.pensize(10)
        pen.up()
        pen.setpos(-350, -250)
        pen.down()

        for border in range(2):
            pen.fd(700)
            pen.left(90)
            pen.fd(500)
            pen.left(90)

        for grass in range(random.randint(90, 120)):
            # print("Printing grass")
            pen.up()
            grass_pos = (random.uniform(-325, 325), random.uniform(-240, 232))
            cls.list_grass.append(grass_pos)
            pen.setpos(grass_pos[0], grass_pos[1])
            pen.down()
            Draw.grass(pen)

        for tree in range(random.randint(10, 15)):
            # print("Printing trees")
            pen.up()
            tree_pos = (random.uniform(-325, 325), random.uniform(-240, 232))
            cls.list_tree.append(tree_pos)
            pen.setpos(tree_pos[0], tree_pos[1])
            pen.down()
            Draw.tree(pen)

        for potion in range(3):
            pen.up()
            pen.setpos(random.uniform(-325, 325), random.uniform(-240, 232))
            pen.down()
            cls.list_potions = cls.potion(pen)
        print(str(cls.list_potions))

        pen.ht()

        cls.kill_display()

        canvas.update()  # refreshes while tracer (animation turned off) was active
        canvas.tracer(t, 0) # back to original refresh rate

    @classmethod
    def encounter(cls, encounter, canvas, original_tracer):
        pen = cls.pen
        hero_startPos = (-300, -197)
        goblin_startPos = (300, -142)

        hero = object_handler.current_heros[0]
        hero.shape("pixel_knight.gif")
        hero.up()
        hero.setpos(hero_startPos)

        goblin = Goblin()
        goblin.shape("pixel_goblin.gif")
        goblin.up()
        goblin.setpos(goblin_startPos)

        pen.up()
        pen.setpos(-190, 0)
        pen.down()

        canvas.update()
        canvas.tracer(original_tracer, 0)
        # inital encounter drawing
        for flicker in range(5):
            canvas.bgcolor("White")
            pen.write("ENCOUNTER", font=("Arial", cls.font_size, "normal"))
            time.sleep(0.1)
            canvas.bgcolor("Black")
            pen.write("ENCOUNTER", font=("Arial", cls.font_size, "normal"))
            time.sleep(0.1)

        while encounter == True:
            pen.clear()
            canvas.bgcolor("Black")
            init_attack(hero, goblin, pen)

            time.sleep(2)  # sets frame refresh speed - at least that's the idea
            break

    @classmethod
    def kill_display(cls):
        kills = int(object_handler.get_kills())
        pen = cls.pen
        pen.up()
        pen.setpos(cls.kill_display_pos[0], cls.kill_display_pos[1])
        pen.write("Kills: {}".format(kills), font=("Arial", cls.font_size, "normal"))
        pen.down()

class Character(turtle.Turtle):  # character as a subclass of Turtle object  mother-class

    armour_break_light = 100 #10
    armour_break_heavy = 100 #20
    armour_break_crit = 100 #50

    # critical hit adds 50% to the persistent chance

    def setWeapon(self):
        print("These are the possible weapons: ")
        for k, item in enumerate(self.weapons):
            print(("{}. " + item).format(k + 1))
        print("Enter the number of your choice")

        while True:
            self.choice = input()
            try:
                self.choice.isdigit()
                (int(self.choice) - 1) in list(range(0, len(self.weapons)))
                break

            except:
                print("Enter valid number")

        return self.choice

    def takePotion(self):
        self.health += 500
        print("Health increased by 500 to a total of {}".format(self.health))

    def getAttacked(self, dmg_prop, pen_object):
        # dmg_prop is a tupel (type, lower_ranger, upper_range,
        # hit_chance, crit_rate, weapon), hit_chance is the hit probability of the enemy attack
        # determining hit by hit chance of enemy attack
        hit = False
        dodge = False
        crit = False
        t_dmg = None
        armour_break = False

        if random.randint(0, 100) > dmg_prop[3]:  # it is hit chance therefore '>'
            print("Narrator: Attack missed!")
            print()
            hit = False
        else:
            print("Narrator: Attack about to hit...", end=" ")
            time.sleep(1)
            # determining ability to dodge of this char
            if random.randint(0, 100) <= self.agility:
                print("but got dodged!")
                dodge = True
                hit = False

            else:
                print("and was not dodged!")
                dodge = False
                hit = True

        if hit == True and dodge == False:

            # determining a critical hit           
            rand = random.randint(0, 100)
            print("Random number for crit: {}".format(rand))
            print("Dmg_prop[0]: {}".format(dmg_prop[0]))
            print("Dmg_prop[1]: {}".format(dmg_prop[1]))
            print("Dmg_prop[2]: {}".format(dmg_prop[2]))
            print("Dmg_prop[3]: {}".format(dmg_prop[3]))
            print("Dmg_prop[4]: {}".format(dmg_prop[4]))

            if rand <= dmg_prop[4]:
                crit = True
                print("Narrator: Critical hit!")
            else:
                print("Narrator: No critical hit.")

            # determining armour break
            print("dmg_prop[0]: {}".format(dmg_prop[0]))
            if dmg_prop[0] == "light":
                if random.randint(0, 100) <= Character.armour_break_light:
                    armour_break = True
                    print("Narrator: Light attack broke the armour")
                    self.armour = self.armour * 0.75
            elif dmg_prop[0] == "heavy":
                if random.randint(0, 100) <= Character.armour_break_heavy:
                    armour_break = True
                    print("Narrator: Heavy attack broke the armour")
                    self.armour = self.armour * 0.75
            elif crit == True:
                if random.randint(0, 100) <= Character.armour_break_crit:
                    armour_break = True
                    print("Narrator: Critical {} attack broke the armour".format(dmg_prop[0]))
                    self.armour = self.armour * 0.75

#--------------------final dmg calculation------------------------------------------

            if crit == True and hit == True:
                t_dmg = random.randint(dmg_prop[1], dmg_prop[2]) * ((100 - self.armour) / 100) * 2  # double crit dmg + deduct the armour mitigation value
            elif crit == False and hit == True:
                t_dmg = random.randint(dmg_prop[1], dmg_prop[2]) * ((100 - self.armour) / 100)

            print("Narrator: Damage inflicted: " + str(int(t_dmg)))
            self.health -= t_dmg
            if self.health > 0:
                print(
                    "Narrator: Remaining health of " + str(self.__class__.__name__) + " " + str(self.name) + ": " + str(
                        int(self.health)))
                print(
                    "Narrator: Remaining armour of " + str(self.__class__.__name__) + " " + str(self.name) + ": " + str(
                        int(self.armour)))
                print(str(__class__.__name__) + " " + str(self.name) + ": " + self.phrases[
                    random.randint(0, len(self.phrases) - 1)])
            else:
                print("{} received fatal damage!!!".format(self.name))
                object_handler.kill_counter(self.__class__.__name__)

        return (hit, dodge, crit, t_dmg, armour_break) # t_dmg = total resulting damage


class Knight(Character):
    health = 2000
    armour = 50
    agility = 15
    charisma = 8
    dmg = 10  # setWeapon defines dmg according to weapon chosen
    hit_c = 30  # setWeapon defines hit chance according to weapon chosen
    crit_c = 30  # 5 setWeapon defines critical hit chance according to weapon chosen

    weapons = ("longsword", "shield and sword")
    phrases = ("Deus Vult!", "Come here you infidel!", "Let me bring you justice!", "For the holy land",
               "God be my witness as I slay this abstorsity!")

    # possible weapons: longsword, shield and one-handed sword

    def __init__(self, name="Holy Crusader", *args, **kwargs):
        self.name = name
        self.setWeapon()
        super(Knight, self).__init__(*args,
                                     **kwargs)  # executes the turtle __init__ and makes the knight object able to do everyting turtle does :DD

    # ---------------------------- ACTIONS ------------------------------------------------------------
    def setWeapon(self):
        self.choice = super(Knight, self).setWeapon()

        if self.choice == "1":
            self.weapon = "longsword"
            self.dmg = (500, 750)
            self.agility -= 5
            self.hit_c = 100 #85
            self.crit_c = 100 #30

        elif self.choice == "2":
            self.weapon = "shield and sword"
            self.dmg = (300, 450)
            self.armour += 10
            self.hit_c = 100 #90
            self.crit_c = 100 #25
        else:
            print("no weapon set")

        print(("{} successfully equiped").format(self.weapon))

    def attacks(self):
        light = ("light", self.dmg[0], int(((self.dmg[1] - self.dmg[0]) / 2) + self.dmg[0]), self.hit_c, self.crit_c,
                 self.weapon)
        heavy = ("heavy", int(((self.dmg[1] - self.dmg[0]) / 2) + self.dmg[0]), self.dmg[1], self.hit_c, self.crit_c,
                 self.weapon)

        return (light, heavy)


class Goblin(Character):
    health = 1250
    armour = 10
    agility = 0 #20-30
    charisma = 1
    dmg = 10  # setWeapon defines dmg according to weapon chosen
    hit_c = 10  # setWeapon defines hit chance according to weapon chosen
    crit_c = 5  # setWeapon defines critical hit chance according to weapon chosen

    weapons = ("dual dagger")
    phrases = ("Arrrrrgg!", "Brains and flesh!", "Lemme smash!")

    def __init__(self, name="Filth"):
        self.name = name
        self.setWeapon()
        super(Goblin,
              self).__init__()  # executes the turtle __init__ and makes the knight object able to do everyting turtle does :DD

    # ---------------------------- ACTIONS ------------------------------------------------------------
    def setWeapon(self):
        self.weapon = "dual daggers"
        self.dmg = (250, 500)
        self.hit_c = 70
        self.crit_c = 40

    def attacks(self):
        light = ("light", self.dmg[0], int(((self.dmg[1] - self.dmg[0]) / 2) + self.dmg[0]), self.hit_c, self.crit_c,
                 self.weapon)
        heavy = ("heavy", int(((self.dmg[1] - self.dmg[0]) / 2) + self.dmg[0]), self.dmg[1], self.hit_c, self.crit_c,
                 self.weapon)

        return (light, heavy)


# ----------------------------------------Initionation and Object handling-----------------------------------------------
class object_handler:  # nicht zu instansierende Klasse, keine (self)
    current_heros = []
    current_NPC = []
    current_screens = []
    total_kills = 0
    goblin_kills = 0
    # here add new npc's to distinguish kills

    @classmethod
    def get_kills(cls):
        return cls.total_kills

    @classmethod
    def kill_counter(cls, kill_type): #kill_tpye will be class.__name__ of killed object
        if kill_type == Goblin.__class__.__name__:
            cls.goblin_kills += 1

        cls.total_kills += 1

    @staticmethod
    def get_object_list():
        return (object_handler.current_heros, object_handler.current_NPC, object_handler.current_screens)

    # Frage: self in jeder methode einer classe? wenn eigentlich nicht umbedingt object instancen erstellt werden müssen? Wie importiert man Classen richtig in andere und verwendet so übergreifend module?
    def add_hero(new_hero):
        object_handler.current_heros.append(new_hero)
        # print(object_handler.current_heros[0].dmg)

    def add_NPC(new_NPC):
        object_handler.current_NPC.append(new_NPC)

    def add_screen(new_screen):
        object_handler.current_screens.append(new_screen)


# ------------------------SETUP-----------------------

class Setup:
    char_list = ["Knight", "Rouge", "Mage"]

    def __init__(self):
        self.welcome()
        self.selectChar()
        # self.createNPC(10) easier to handle when created during encounter...

    def welcome(self):
        print("Welcome to 'Goblin Unslaught'")
        # time.sleep(1)

    def selectChar(self):
        print("Please select one char with the corresponding number")
        for counter, hero in enumerate(Setup.char_list):
            print("{}. {}".format(counter + 1, hero))
        print("-------------------------------")
        while True:
            self.selected_char = input()

            try:
                self.selected_char.isdigit()
                (int(self.selected_char) - 1) in list(range(0, len(Setup.char_list)))
                break
            except:
                print("Please enter a valid number")

        while True:

            char_name = str(input("Choose a name for your hero: "))
            print("-------------------------------")
            try:
                len(char_name) > 0
                break

            except:
                print("Try again..")
                pass

        if self.selected_char == "1":
            object_handler.add_hero(Knight(char_name))
        elif self.selected_char == "2":
            object_handler.add_hero(rouge(char_name))
        elif self.selected_char == "3":
            object_handler.add_hero(mage(char_name))

    def createNPC(self, amount): #for now the same Goblin spawns over and over. No need specifically to create multiple objects (same starting health?) but necessary when different NPC's are precent -> new handler for each obejct then
        self.amount = amount
        for npc in range(amount):
            object_handler.add_NPC(Goblin())
        print("Narrator: Be wary traveler, {} goblins spawned nearby!".format(amount))
        return amount


class Move:
    step = 60 #40
    encounter = False
    hero_pos_before_enc = 0

    # classen methoden sind statisch und können ähnlich wie instancen mit self, durch cls auf klassen
    # level ansprechen -> step auf classen level hätte auch mit Move.step angesprochen werden können, aber es ist
    # sauberer es mit dem decorator @classmethod zu machen, da es so wirklich die direkte classe anspricht und
    # falschverweise ausschliesst.
    @classmethod
    def checkBorder(cls, hero):
        print("Checking border")
        hero_pos = hero.position()
        if hero.heading() == 0:
            if hero_pos[0] + cls.step >= 345:
                hero.ht()
                Draw.environment(object_handler.current_screens[0])
                hero.setpos(-hero_pos[0], hero_pos[1])
                hero.st()

            else:
                hero.fd(cls.step)

        elif hero.heading() == 90:
            if hero_pos[1] + cls.step >= 245:
                hero.ht()
                Draw.environment(object_handler.current_screens[0])
                hero.setpos(hero_pos[0], -hero_pos[1])
                hero.st()

            else:
                hero.fd(cls.step)

        elif hero.heading() == 180:
            if hero_pos[0] - cls.step <= -345:
                hero.ht()
                Draw.environment(object_handler.current_screens[0])
                hero.setpos(abs(hero_pos[0]), hero_pos[1])
                hero.st()
            else:
                hero.fd(cls.step)

        elif hero.heading() == 270:
            if hero_pos[1] - cls.step <= -245:
                hero.ht()
                Draw.environment(object_handler.current_screens[0])
                hero.setpos(hero_pos[0], abs(hero_pos[1]))
                hero.st()
            else:
                hero.fd(cls.step)

    def checkPotion(hero):
        potions = Draw.list_potions
        print("Potions" + str(potions))
        hit_potion = False
        for key in list(potions):
            if hero.distance(potions[key]) <= 25:
                print("Collission")
                hit_potion = True
                # Draw.redraw(hit_potion, key)
                del potions[key]
                print("after del: " + str(potions))
                object_handler.current_heros[0].takePotion()

    @classmethod
    def checkEncounter(cls):
        encounter_chance = 100
        if random.randint(0, 100) <= encounter_chance:
            cls.encounter = True
            cls.hero_pos_before_enc = object_handler.current_heros[0].position()

    @classmethod
    def basicMoveEvent(cls, hero, canvas):
        time.sleep(0.25)
        if cls.encounter == False:
            Move.checkBorder(hero)
            time.sleep(0.1)
            Move.checkPotion(hero)
            Move.checkEncounter()
            Draw.redraw(canvas, cls.encounter)
        else:
            # here goes move list while in incounter
            pass

    @classmethod
    def left(cls, hero, canvas):
        hero.setheading(180)
        cls.basicMoveEvent(hero, canvas)

    @classmethod
    def right(cls, hero, canvas):
        hero.setheading(0)
        cls.basicMoveEvent(hero, canvas)

    @classmethod
    def up(cls, hero, canvas):
        hero.setheading(90)
        cls.basicMoveEvent(hero, canvas)

    @classmethod
    def down(cls, hero, canvas):
        hero.setheading(270)
        cls.basicMoveEvent(hero, canvas)


def main():
    Setup()
    hero = object_handler.current_heros[0]
    hero.up()
    hero.setheading(90)
    hero.setpos(0, -150)
    screen = turtle.Screen()
    screen.screensize(700, 500)
    screen.setup(720, 520, 0, 0)
    screen.bgcolor("green")

    shapes = ["pixel_goblin.gif", "pixel_knight.gif", "armour_break_status.gif"]

    for shape in shapes:
        print("{} {}".format(shape, type(shape)))
        screen.register_shape(shape)
    # screen.register_shape("pixel_goblin.gif")
    # screen.register_shape("pixel_knight.gif")
    #screen.register_shape("armour_break_status.png")
    # while True: #main loop
    # encounter = False
    Draw.environment(screen)

    # --------------Events--------------------------
    screen.onkey(lambda arg=hero, obj=screen: Move.up(arg, obj), "Up")
    screen.onkey(lambda arg=hero, obj=screen: Move.down(arg, obj), "Down")
    screen.onkey(lambda arg=hero, obj=screen: Move.left(arg, obj), "Left")
    screen.onkey(lambda arg=hero, obj=screen: Move.right(arg, obj), "Right")

    # if encounter == True:
    #  Draw.encounter(screen)

    object_handler.add_screen(screen)

    screen.listen()
    screen.mainloop()


    # init_attack(object_handler.current_heros[0], object_handler.current_NPC[0])


if __name__ == "__main__":
    main()
