""""
Autor: Andres Hurtado
Cedula: 29.626.410

REQUISITOS DEL JUEGO
    1)Intalar pygame => pip install pygame
    2)Intalar numpy => pip install numpy

COMO JUGAR
    -Al presionar cualquier tecla pausas y arracas el juegos
    -Con el click derecho revives un celula
    -Con el click izquierdo matas a una celula

COMO EJECUTAR EL JUEGO
    -Pulsando la tecla F1 si estas usando Visual Studio Code
    -Pulsando la tecla F5 si estas unsado el IDLE de Python

El juego sera ejecutado con 2 automatas, el automata Palo y el automata Movil
"""

import pygame;
import numpy as np;
import time;

# Screen of the game
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((height, width))

# Background Color
bg = 25, 25, 25
screen.fill(bg)

# Create the cells of the game
nxC, nyC = 50, 50
# Cells dimensions
dimCW = width / nxC
dimCH = height / nyC

# Cells's states: Live=1, Dead=0
gameState = np.zeros((nxC, nyC))

# Palo automata
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Movil automaa
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Pause control of the game
pauseExect = False

running = True

# Display the screen indefinitely
while running:
    # Create a copy of the game
    newGameState = np.copy(gameState)
    # Clean the screen for each iteration
    screen.fill(bg)
    # Time refresh
    time.sleep(0.1)
    # Detect if any key of the keyboard is clicked to stop the game
    ev =  pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            running = False 

        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExect:

                # Calculate the number of neighbors dead
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                        gameState[(x) % nxC, (y-1) % nyC] + \
                        gameState[(x+1) % nxC, (y-1) % nyC] + \
                        gameState[(x-1) % nxC, (y) % nyC] + \
                        gameState[(x+1) % nxC, (y) % nyC] + \
                        gameState[(x-1) % nxC, (y+1) % nyC] + \
                        gameState[(x) % nxC, (y+1) % nyC] + \
                        gameState[(x+1) % nxC, (y+1) % nyC]
                
                # Rule 1: A dead cell with exactly 3 living neighbors, "revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Rule 2: A living cell with less than 2 or more than 3 neighbors, "dies"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0
            
            # Points defining the polygon we're drawing
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]

            # Draw the cells for each x and y axis pair
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Update games state
    gameState = np.copy(newGameState)

    # Display and update the frame at each loop iteraction
    pygame.display.flip()

pygame.quit()

    