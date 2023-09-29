import pygame, sys
from src.settings import *
import struct


def exit():
    pygame.quit()
    sys.exit()


def draw_text(text, color, surf, x, y, font):
    textRender = font.render(text, 1, color)
    textRect = textRender.get_rect()
    textRect.topleft = (x, y)
    surf.blit(textRender, textRect)


def save(path, iterator):
    with open(path, 'wb') as file:
        for row in iterator:
            for tile in row:
                if tile.state == 0:
                    continue
                x = struct.pack("h", tile.x)
                y = struct.pack("h", tile.y)
                s = struct.pack("h", tile.state)
                file.write(x)
                file.write(y)
                file.write(s)


def load(path, tiles):
    with open(path, 'rb') as file:
        while True:
            d = file.read(2)
            if not d:
                break
            x_ = struct.unpack('h', d)[0]
            y_ = struct.unpack('h', file.read(2))[0]
            s = struct.unpack('h', file.read(2))[0]
            for y in range(len(tiles)):
                for x in range(len(tiles[y])):
                    if x == x_ and y == y_:
                        tiles[y][x].state = s


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        super().__init__()
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active = True

    def draw(self, surf, color: str, ofsX: int = 0, ofsY: int = 0, small: bool = False, outline=None, ):
        if not self.active:
            if outline:
                pygame.draw.rect(surf, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

            pygame.draw.rect(surf, COLORS[0], (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(surf, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            if not small:
                draw_text(self.text, color, surf, self.x + ofsX, self.y + ofsY, FONT)
            else:
                draw_text(self.text, color, surf, self.x + ofsX, self.y + ofsY, SMALL_FONT)

    def toggleActive(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def isActive(self):
        if self.active:
            return True
        else:
            return False

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
