from main import *

# p = "0,0,0"
# p = p.split(",")
# p = tuple([int(i) for i in p])

# print(p)

# print(type((0,0,0)))

if __name__ == "__main__":
    pg.init()
    clock = pg.time.Clock()
    worldWidth, worldHeight = 1000, 1000
    running = True
    userText = ""
    win = pg.display.set_mode((worldWidth,worldHeight))
    onMenu = False
    saveMenu = SaveMenu("Save", WHITE, 200, 200, [])
    button = SaveButton("Save", RED, 150, 150, 800, 800, saveMenu)
    menuX, menuY = None, None

    while running:
        win.fill(BLACK)
        button.draw()
        cursorCoords = pg.mouse.get_pos()
        cursorCoordsRel = pg.mouse.get_rel()
        cursorClicks = pg.mouse.get_pressed(num_buttons=3)
        keyState = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if saveMenu.checkCursor(cursorCoords):
                        continue
                    if button.checkCursor(cursorCoords):
                        onMenu = True
                        menuX, menuY = cursorCoords[0]-saveMenu.width, cursorCoords[1]-saveMenu.height
                    else:
                        onMenu = False
        
        if onMenu:
            saveMenu.draw(menuX, menuY)

        if keyState[pg.K_ESCAPE]:
            print("exit")
            running = False
        if keyState[pg.K_w]: #debug
            print("gay", cursorCoords, cursorClicks, cursorCoordsRel, f"{clock.get_fps():.0f}")

        
        clock.tick(500)
        pg.display.update()
    
    pg.quit()