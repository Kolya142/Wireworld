import pygame, sys, asyncio
from time import sleep
from os import walk
from src.settings import *
from src.support import exit, save, load, draw_text, Button
from src.debug import debug
from src.tile import Tile

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock.get_fps()

saveText = ''
moveX = 0
moveY = 0
speed = 20
inc = 0
targetState = 0
TILE_GRID_SIZE = 150
TILES = []


def generate(width, height, surf, tileSize):
    global TILES
    for y in range(width):
        row = []
        for x in range(height):
            newTile = Tile(x, y, surf, tileSize)
            row.append(newTile)
        TILES.append(row)


def process_state():
    global TILES
    newTiles = []
    for row in TILES:
        newRow = []
        for tile in row:
            if tile.state == 0:
                newRow.append(create_tile(tile, 0))
                continue
            charge = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (x == 0 and y == 0) or tile.y + y < 0 or tile.y + y > TILE_GRID_SIZE - 1 or \
                            tile.x + x < 0 or tile.x + x > TILE_GRID_SIZE - 1:
                        pass
                    else:
                        if TILES[tile.y + y][tile.x + x].state == 2:
                            charge += 1
            if tile.state == 1:
                if charge == 1 or charge == 2:
                    newRow.append(create_tile(tile, 2))
                else:
                    newRow.append(create_tile(tile, 1))

            elif tile.state == 2:
                newRow.append(create_tile(tile, 3))

            elif tile.state == 3:
                newRow.append(create_tile(tile, 1))

        newTiles.append(newRow)
    TILES = newTiles
    sleep(0.1)


def create_tile(tile, state):
    newTile = Tile(tile.x, tile.y, tile.displaySurf, tile.size)
    newTile.moveX, newTile.moveY = tile.moveX, tile.moveY
    newTile.state = state
    return newTile


async def save_menu():
    global saveText
    running = True
    clicking = False
    active = False

    while running:

        screen.fill('blue')
        mousePos = pygame.mouse.get_pos()

        box = pygame.Rect(int(WIDTH / 2) - 150, int(HEIGHT / 2) - 115, 200, 130)
        inputBox = pygame.Rect(int(WIDTH / 2) - 125, int(HEIGHT / 2) - 80, 151, 31)
        button0 = Button('red', int(WIDTH / 2) - 115, int(HEIGHT / 2) - 40, 130, 30, 'Save File')

        textRender = FONT.render(saveText, 1, 'white')

        if button0.isOver(mousePos) and clicking and len(saveText) != 0:
            save('src/saves/' + saveText + '.sav', TILES)
            saveText = ''
            running = False
            sleep(0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        saveText = saveText[:-1]
                    else:
                        saveText += event.unicode

                if event.key == pygame.K_ESCAPE:
                    saveText = ''
                    running = False
                    sleep(0.1)

            clicking = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inputBox.collidepoint(event.pos):
                    active = True

                if event.button == 1:
                    clicking = True

        if active:
            if len(saveText) > 7:
                active = False

        pygame.draw.rect(screen, 'cyan', box)
        pygame.draw.rect(screen, 'black', inputBox, 2)
        screen.blit(textRender, (inputBox.x + 5, inputBox.y + 5))
        button0.draw(screen, 'white', 5, 5)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


async def load_menu():
    running = True
    clicking = False

    while running:
        screen.fill('black')
        mousePos = pygame.mouse.get_pos()

        saveBox = pygame.Rect(int(WIDTH / 2), int(HEIGHT / 2) - 115, 200, 200)
        templateBox = pygame.Rect(int(WIDTH / 2) - 400, int(HEIGHT / 2) - 115, 250, 330)

        pygame.draw.rect(screen, 'cyan', saveBox)
        pygame.draw.rect(screen, 'cyan', templateBox)

        for _, __, files in walk('src/references'):
            incrementY = 20
            incrementYW = incrementY
            incrementX = 0
            for fileIndex, file in enumerate(files):
                if fileIndex < 10:
                    text = str(file)
                    newText = text.split('.sav')
                    button = Button('red', ((templateBox.x + 20) + incrementX), templateBox.y + incrementY, 100, 20,
                                    newText[0].title())
                    incrementY += 30
                    if button.isOver(mousePos) and clicking:
                        load('src/references/' + file, TILES)
                        running = False
                        sleep(0.1)
                    button.draw(screen, 'white', 5, 5, small=True)

                elif fileIndex >= 10:
                    incrementX = 125
                    text = str(file)
                    newText = text.split('.txt')
                    button = Button('red', templateBox.x + incrementX, templateBox.y + incrementYW, 100, 20,
                                    newText[0].title())
                    incrementYW += 30
                    if button.isOver(mousePos) and clicking:
                        load('src/references/' + file, TILES)
                        running = False
                        sleep(0.1)
                    button.draw(screen, 'white', 5, 5, small=True)

        for _, __, files in walk('src/saves'):
            increment = 20
            for file in files:
                button = Button('red', saveBox.x + 50, saveBox.y + increment, 100, 20, file)
                increment += 30
                if button.isOver(mousePos) and clicking:
                    load('src/saves/' + file, TILES)
                    running = False
                    sleep(0.1)
                button.draw(screen, 'white', 5, 5, small=True)

        clicking = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sleep(0.1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicking = True

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


async def options():
    global TILE_GRID_SIZE, TILES
    running = True
    clicking = False

    while running:
        screen.fill('black')
        mousePos = pygame.mouse.get_pos()

        box = pygame.Rect(int(WIDTH / 2) - 150, int(HEIGHT / 2) - 115, 200, 260)
        button0 = Button('red', int(WIDTH / 2) - 100, int(HEIGHT / 2) - 100, 100, 50, 'save')
        button1 = Button('red', int(WIDTH / 2) - 100, int(HEIGHT / 2) - 40, 100, 50, 'load')
        button2 = Button('red', int(WIDTH / 2) - 100, int(HEIGHT / 2) + 20, 100, 50, 'exit')
        button3 = Button('red', int(WIDTH / 2) - 100, int(HEIGHT / 2) + 80, 100, 50, 'rest')

        if button0.isOver(mousePos) and clicking:
            sleep(0.1)
            await save_menu()
            running = False

        if button1.isOver(mousePos) and clicking:
            sleep(0.1)
            await load_menu()
            running = False

        if button2.isOver(mousePos) and clicking:
            exit()

        if button3.isOver(mousePos) and clicking:
            sleep(0.1)
            TILES = []
            generate(TILE_GRID_SIZE, TILE_GRID_SIZE, screen, TILE_SIZE)
            running = False


        clicking = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sleep(0.1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicking = True

        pygame.draw.rect(screen, 'cyan', box)
        button0.draw(screen, 'white', 15, 15)
        button1.draw(screen, 'white', 15, 15)
        button2.draw(screen, 'white', 15, 15)
        button3.draw(screen, 'white', 15, 15)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


async def main():
    global targetState, moveX, moveY, speed, screen, clock, TILE_GRID_SIZE, inc

    generate(TILE_GRID_SIZE, TILE_GRID_SIZE, screen, TILE_SIZE)

    while True:

        mouseX, mouseY = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for row in TILES:
                        for tile in row:
                            if pygame.Rect((tile.x * tile.size + moveX,
                                            tile.y * tile.size + tile.moveY),
                                           (tile.size, tile.size)).collidepoint(pygame.mouse.get_pos()):
                                tile.state = targetState

                if pygame.mouse.get_pressed()[2]:
                    for row in TILES:
                        for tile in row:
                            if pygame.Rect((tile.x * tile.size + moveX,
                                            tile.y * tile.size + tile.moveY),
                                           (tile.size, tile.size)).collidepoint(pygame.mouse.get_pos()):
                                tile.state = 0

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    for row in TILES:
                        for tile in row:
                            if pygame.Rect((tile.x * tile.size + moveX,
                                            tile.y * tile.size + tile.moveY),
                                           (tile.size, tile.size)).collidepoint(pygame.mouse.get_pos()):
                                tile.state = targetState

                if pygame.mouse.get_pressed()[2]:
                    for row in TILES:
                        for tile in row:
                            if pygame.Rect((tile.x * tile.size + moveX,
                                            tile.y * tile.size + tile.moveY),
                                           (tile.size, tile.size)).collidepoint(pygame.mouse.get_pos()):
                                tile.state = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    for row in TILES:
                        for tile in row:
                            if tile.size > 10:
                                tile.size -= speed / 10

                if event.button == 5:
                    for row in TILES:
                        for tile in row:
                            if tile.size < 100:
                                tile.size += speed / 10

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            process_state()
            inc += 1

        screen.fill('black')
        textFps = FONT.render(f'{round(clock.get_fps(), 2)}', 1, 'green')
        if keys[pygame.K_1]:
            targetState = 1
        if keys[pygame.K_2]:
            targetState = 2
        if keys[pygame.K_3]:
            targetState = 3
        # if keys[pygame.K_z]: save('src/references/basic elements.txt', TILES)
        if keys[pygame.K_ESCAPE]:
            await options()
        if keys[pygame.K_w]:
            moveY += speed
        if keys[pygame.K_a]:
            moveX += speed
        if keys[pygame.K_s]:
            moveY -= speed
        if keys[pygame.K_d]:
            moveX -= speed
        if keys[pygame.K_r]:
            for row in TILES:
                for tile in row:
                    tile.state = 0

        for row in TILES:
            for tile in row:
                tile.draw(moveX, moveY)

        for rowIndex, row in enumerate(TILES):
            for colIndex, tile in enumerate(row):
                if pygame.Rect((tile.x * tile.size + moveX,
                                tile.y * tile.size + tile.moveY),
                               (tile.size, tile.size)).collidepoint(pygame.mouse.get_pos()):
                    draw_text(f'{tile.x, tile.y}', 'green', screen, 1165, 690, FONT)

        if targetState == 0:
            pygame.draw.circle(screen, 'white', (40, HEIGHT - 40), 30)
        else:
            pygame.draw.circle(screen, COLORS[targetState], (40, HEIGHT - 40), 30)

        screen.blit(textFps, (10, 10))
        # debug(f'{clock}')
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())
