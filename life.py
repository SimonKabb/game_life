import sys

import pygame
from pygame.locals import *

# Константы
BLACK = (85, 72, 63)
WHITE = (100, 153, 145)
HEIGHT = 1000
WIDTH = 1000
FPS = 30
NEIGHBOURS = ([-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1])
RUN = True


# Создаем окно
root = pygame.display.set_mode((WIDTH , HEIGHT))
clock = pygame.time.Clock()

# ищем положение квадрата
def find_square(position):
    pos_x = position[0] // 10 * 10
    if pos_x % 20 != 0:
        pos_x -= 10
    pos_y = position[1] // 10 * 10
    if pos_y %20 !=0:
        pos_y -=10
    return (pos_x, pos_y)


# поиск соседей
def find_neighbors(cells, position):
    count =0
    for neighbour in NEIGHBOURS:
        try:
            if cells[position[0]+ neighbour[0]][position[1]+neighbour[1]] == 1:
                count +=1
        except IndexError:
            pass
    return count
    
# Рисуем сетку
root.fill(WHITE)
for i in range(0 , root.get_height() // 20):
    pygame.draw.line(root , BLACK , (0 , i * 20) , (root.get_width() , i * 20))
for j in range(0 , root.get_width() // 20):
    pygame.draw.line(root , BLACK , (j * 20 , 0) , (j * 20 , root.get_height()))

# Создаем массив 
cells=[ [0 for j in range(root.get_height()//20)] for i in range(root.get_width()//20)]


while RUN:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==	QUIT:
            sys.exit()

        px, py = pygame.mouse.get_pos()
        position_x, position_y = find_square((px,py))
        if pygame.mouse.get_pressed() == (1,0,0):
            pygame.draw.rect(root, BLACK, (position_x, position_y, 20, 20))
            cells[position_x//20][position_y//20] = 1 
        elif pygame.mouse.get_pressed() == (0,0,1):
            pygame.draw.rect(root, WHITE, (position_x+1, position_y+1, 19, 19))
            cells[position_x//20][position_y//20] = 0



        # clear screen                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                for cell in range(0, len(cells)):
                    for one in range(0, len(cells[cell])):
                        if cells[cell][one] == 1:
                            cells[cell][one]=0
                            pygame.draw.rect(root, WHITE, (cell*20 +1, one*20+1, 19, 19))
        # cycle
        elif pygame.key.get_pressed()[K_SPACE]:
            for cell in range(0, len(cells)):
                        for one in range(0, len(cells[cell])):
                            if cells[cell][one] == 1:
                                pygame.draw.rect(root, BLACK, (cell*20 +1, one*20+1, 19, 19))
                            else:
                                pygame.draw.rect(root, WHITE, (cell*20 +1, one*20+1, 19, 19))
            pygame.display.update()
            cells_new = [[0 for j in range(len(cells[0]))] for i in range(len(cells))]
            for cell in range(0, len(cells)):
                for one in range(0, len(cells[cell])):
                    if cells[cell][one]:
                        if find_neighbors(cells, [cell,one]) not in (2,3):
                            cells_new[cell][one] = 0
                            continue
                        cells_new[cell][one] = 1
                        continue
                    elif cells[cell][one] == 0 and find_neighbors(cells, [cell,one]) == 3:
                        cells_new[cell][one] =1 
                        continue
            cells = cells_new
    pygame.display.update()