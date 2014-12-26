# -*-coding: utf-8 -*-
__author__ = 'JacobWunder'


class Character(object):
    def __init__(self, name="Jacob", head="╓╖", body="╙╜", ):
        self.name = name
        self.head = head
        self.body = body
        self.pos = [50, 50]
        self.string = self.head + "\n" + self.body

        self.headLeft = self.head + " "
        self.headRight = " " + self.head

        self.bodyLeft = self.body + " "
        self.bodyRight = " " + self.body