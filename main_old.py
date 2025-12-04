import numpy as np
import random

N_Dwarfs = 1 # Number of Dwarfs
N_Giants = 1 # Number of Giants (AGENTS)
BOARD_SIZE = (20,10) # NXM matrix
BORDER = int(BOARD_SIZE[1]/2)

def create_board():
    board =[['_' for _ in range(BOARD_SIZE[1])] for _ in range(BOARD_SIZE[0])]
    board = np.array(board, dtype='<U3')
    # board[:,1] = [-1 for _  in range(BOARD_SIZE[1])]
    board[:, BORDER] = ['N' for _  in range(BOARD_SIZE[0])]
    return np.array(board)

def dwarf_directions(dwarfs_locations):
    dwarfs_directions = []
    needed_gap = BOARD_SIZE[1]-int(BOARD_SIZE[1]/2)-1
    for dwarf_id, dwarf_loc in enumerate(dwarfs_locations):
        possible_angels = [0]  # 0 means no degree
        if dwarf_loc[0] >= needed_gap:
            possible_angels.append(1)  # 1 means positive degree
        if dwarf_loc[0] < BOARD_SIZE[0] - needed_gap:
            possible_angels.append(2)  # 2 means negative degree
        dwarf_degree = random.choice(possible_angels)
        dwarfs_directions.append((dwarf_id, dwarf_loc, dwarf_degree))
    return dwarfs_directions

def init_dwarf(dwarfs):
    dwarfs_locations = []
    for dwarf in range(dwarfs):
        spawn_i = random.randint(0,BOARD_SIZE[0]-1)
        dwarfs_locations.append((spawn_i, BOARD_SIZE[1]-1))
    return dwarfs_locations

def update_future_board(dwarfs_directions, board):
    future_board = board
    for dwarf_id, dwarf_loc, dwarf_direction in dwarfs_directions:
        if dwarf_direction == 0:
            for index, j in enumerate(range(BOARD_SIZE[1]-2, BORDER, -1)):
                future_board[dwarf_loc[0],j] = str(dwarf_id) + "_" + str(index+1)
        if dwarf_direction == 1:
            for index, j in enumerate(range(BOARD_SIZE[1]-2, BORDER, -1)):
                future_board[dwarf_loc[0]-index-1,j] = str(dwarf_id) + "_" + str(index+1)
        if dwarf_direction == 2:
            for index, j in enumerate(range(BOARD_SIZE[1]-2, BORDER, -1)):
                future_board[dwarf_loc[0]+index+1,j] = str(dwarf_id) + "_" + str(index+1)
    return future_board

def init_settings():
    board = create_board()
    dwarfs_locations = init_dwarf(N_Dwarfs)
    for dwarf_id, dwarf_loc in enumerate(dwarfs_locations):
        board[dwarf_loc] = str(dwarf_id) + '_0'  # the form x_y represents the location of dwarf 'x' in time 'y'
    dwarfs_directions = dwarf_directions(dwarfs_locations)
    future_board = update_future_board(dwarfs_directions, board.copy())
    print(future_board)
    return board

boared = init_settings()
#print(boared)