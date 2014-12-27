# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color

from character import Character

"""░ ▒ ▓ │ ┤ ╡ ╢ ╖ ╕ ╣ ║ ╗ ╝ ╜ ╛ ┐ └ ┴ ┬ ├ ─ ┼ ╞ ╟ ╚ ╔ ╩ ╦ ╠ ═ ╬ ╧ ╨ ╤
╥ ╙ ╘ ╒ ╓ ╫ ╪ ┘ ┌ █ ▄ ▌ ▐  ▀ ■ ⌂ ☼ § ∟ ▲ ▼ ♂ ♀ ☺ ☻ ♥ ♦ ♣ ♠ • ○ ◘ ♪ ♫
↑ ↓ → ← ↔"""

LENGTH = 20
upperWall = "▄▄"
floor = "▀▀"
leftWall = "▌ "
rightWall = " ▐"
space = "  "
lightShading = "░░"
medShading = "▒▒"
darkShading = "▓▓"
RIGHTKEY = 124
UPKEY = 126
LEFTKEY = 123
DOWNKEY = 125


class TextAdventureGame(FloatLayout):
    def __init__(self):
        super(TextAdventureGame, self).__init__()
        self.backgroundWidget = Widget()
        with self.backgroundWidget.canvas.before:
            # Color(146. / 256., 76. / 256., 0., .5)
            Rectangle(pos=(0, 0), size=Window.size)

        self.char = Character()
        self.world = self.createLandscape()
        self.worldWithCharacter = self.placeChar(self.world, self.char)
        self.worldLabel = Label(
            color=(76. / 256., 146. / 256., 0., 1.),
            text=self.joinRoom(self.worldWithCharacter),
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
        self.worldWithCharacter = self.placeChar(self.world, self.char)
        self.worldLabel.text = self.joinRoom(self.world)
        self.worldLabel.texture_update()

    def placeChar(self, room, char):
        newRoom = list(room)
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

    def createRoom(self):
        row_template = [space] * LENGTH
        room = [row_template] * LENGTH
        for r, row in enumerate(room):
            row[0] = leftWall
            row[-1] = rightWall
        room[0] = [upperWall] * LENGTH
        room[-1] = [floor] * LENGTH
        return room

    def createLandscape(self):
        landscape = [[lightShading for i in range(LENGTH)] for j in range(LENGTH)]
        border = [darkShading for i in range(LENGTH)]
        landscape[0] = border
        landscape[-1] = border
        for row in landscape:
            row[0] = darkShading
            row[-1] = darkShading
        return landscape

    def generateTerrain(self):
        pass


class TextAdventureApp(App):
    def build(self):
        game = TextAdventureGame()
        return game

if __name__ == "__main__":
    TextAdventureApp().run()