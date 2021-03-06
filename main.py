# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color

from random import randint, choice
from character import Character
import copy

"""░ ▒ ▓ │ ┤ ╡ ╢ ╖ ╕ ╣ ║ ╗ ╝ ╜ ╛ ┐ └ ┴ ┬ ├ ─ ┼ ╞ ╟ ╚ ╔ ╩ ╦ ╠ ═ ╬ ╧ ╨ ╤
╥ ╙ ╘ ╒ ╓ ╫ ╪ ┘ ┌ █ ▄ ▌ ▐  ▀ ■ ⌂ ☼ § ∟ ▲ ▼ ♂ ♀ ☺ ☻ ♥ ♦ ♣ ♠ • ○ ◘ ♪ ♫
↑ ↓ → ← ↔"""

LENGTH = 100
upperWall = "▄▄"
floor = "▀▀"
leftWall = "▌ "
rightWall = " ▐"
space = "  "
lightShading = "░░"
medShading = "▒▒"
darkShading = "▓▓"
stones = "▒▒"
flooring1 = "▞▞"
flooring2 = "▚▚"
RIGHTKEY = 124
UPKEY = 126
LEFTKEY = 123
DOWNKEY = 125


class TextAdventureGame(FloatLayout):
    def __init__(self):
        super(TextAdventureGame, self).__init__()
        self.backgroundWidget = Widget()
        with self.backgroundWidget.canvas.before:
            pass
            # Color(76. / 256., 230. / 256., 0., .5)
            # Rectangle(pos=(0, 0), size=Window.size)

        self.char = Character()
        self.world = self.createLandscape()
        self.world = self.generateTerrain(self.world)
        for i in range(randint(3, 6)):
            self.createRoom(self.world)
        self.worldWithCharacter = list(self.world)
        self.worldWithCharacter = self.placeChar(self.worldWithCharacter, self.char)
        self.worldLabel = Label(
            color=(76. / 256., 146. / 256., 0., 1.),
            text=self.joinRoom(self.world),
            markup=True,
            center_x=Window.width / 2,
            center_y=Window.height / 2,
            font_name="assets/fonts/DejaVuSansMono.ttf",
            font_size="20sp"
        )
        self.worldLabel.size = self.worldLabel.texture_size
        with self.worldLabel.canvas:
            Color(146. / 256., 76. / 256., 0., 1.)
            Rectangle(pos=self.worldLabel.pos, size=self.worldLabel.size)
        self.add_widget(self.backgroundWidget)
        self.add_widget(self.worldLabel)
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, *args):
        ##MOVE UP
        if args[2] == UPKEY:
            self.worldLabel.center_y -= 25
            if self.char.pos[1] - 1 > 0:
                self.char.pos[1] -= 1
        ## MOVE DOWN
        elif args[2] == DOWNKEY:
            self.worldLabel.center_y += 20
            if self.char.pos[1] + 3 < LENGTH:
                self.char.pos[1] += 1
        ## MOVE LEFT
        elif args[2] == LEFTKEY:
            self.worldLabel.center_x += 20
            if self.char.pos[0] - 1 > 0:
                self.char.pos[0] -= 1
        ## MOVE RIGHT
        elif args[2] == RIGHTKEY:
            self.worldLabel.center_x -= 25
            if self.char.pos[0] + 2 < LENGTH:
                self.char.pos[0] += 1

        # print(self.char.pos)
        self.worldWithCharacter = self.world[:]
        self.worldWithCharacter = self.placeChar(self.worldWithCharacter, self.char)
        self.worldLabel.text = self.joinRoom(self.world)
        self.worldLabel.texture_update()

    def placeChar(self, room, char):
        newRoom = room[:]
        newRoom[char.pos[1]][char.pos[0]] = char.head
        newRoom[char.pos[1] + 1][char.pos[0]] = char.body
        return newRoom

    def joinRoom(self, room):
        finalRoom = ""
        for r, row in enumerate(room):
            if r > 0:
                finalRoom += "\n"
            for slot in row:
                finalRoom += slot
        return finalRoom

    def createRoom(self, room):
        pos = (randint(3, LENGTH - int(LENGTH / 10) - 3),
               randint(3, LENGTH - int(LENGTH / 10) - 3))
        smallRoom = [[flooring1 for i in range(LENGTH / 10)] for j in range(LENGTH / 10)]
        for r, row in enumerate(smallRoom):
            row[0] = leftWall
            row[-1] = rightWall
        smallRoom[0] = [upperWall for i in range(LENGTH / 10)]
        smallRoom[-1] = [floor for i in range(LENGTH / 10)]
        for i in range(LENGTH / 10):
            for j in range(LENGTH / 10):
                room[pos[1] + i][pos[0] + j] = smallRoom[i][j]

    def createLandscape(self):
        landscape = [[lightShading for i in range(LENGTH)] for j in range(LENGTH)]
        border = [darkShading for i in range(LENGTH)]
        landscape[0] = border
        landscape[-1] = border
        for row in landscape:
            row[0] = darkShading
            row[-1] = darkShading
        return landscape

    def generateTerrain(self, room):
        roomWithTerrain = room[:]
        numbers = [-1, -1, 1, 1, 2]
        for i in range(randint(LENGTH / 10, LENGTH / 2)):
            stonesCoord = [randint(3, LENGTH - 3), randint(3, LENGTH - 3)]
            roomWithTerrain[stonesCoord[1]][stonesCoord[0]] = stones
            for j in range(randint(5, 10)):
                try:
                    roomWithTerrain[stonesCoord[1] + choice(numbers)][stonesCoord[0] + choice(numbers)] = stones
                except IndexError:
                    pass
        border = [darkShading for i in range(LENGTH)]
        roomWithTerrain[0] = border
        roomWithTerrain[-1] = border
        for row in roomWithTerrain:
            row[0] = darkShading
            row[-1] = darkShading
        return roomWithTerrain


class TextAdventureApp(App):
    def build(self):
        game = TextAdventureGame()
        return game

if __name__ == "__main__":
    TextAdventureApp().run()