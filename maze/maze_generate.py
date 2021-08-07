#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.cm as cm


#Pim's algorithm
def prim(size1,size2):

    # A matrix to represent maze. M[i,j] = [LEFT, UP, RIGHT, DOWN, CHECK_IF_VISITED]
    # initialize maze
    M = np.zeros((size1, size2, 5), dtype=np.uint8)

    # start row idx and start column idx
    start_r = 0
    start_c = 0

    # set history to empty
    history = list() # a list to hold all the nodes visited

    history.append((start_r,start_c))

    while len(history)!=0:

        r,c = random.choice(history)
        history.remove((r,c))
        # set current cell as visited
        M[r,c,4] = 1
        move = [] # set move list to empty

        if c>0:
            if M[r,c-1,4] == 1:
                move.append("Left")
            elif M[r,c-1,4] == 0:
                history.append((r,c-1))
                M[r,c-1,4] = 2 # have append in history but haven't been visited yet
        if r>0:
            if M[r-1,c,4] == 1:
                move.append("Up")
            elif M[r-1,c,4] == 0:
                history.append((r-1,c))
                M[r-1,c,4] = 2 # have append in history but haven't been visited yet
        if c<size2-1:
            if M[r,c+1,4] == 1:
                move.append("Right")
            elif M[r,c+1,4] == 0:
                history.append((r,c+1))
                M[r,c+1,4] = 2 # have append in history but haven't been visited yet
        if r<size1-1:
            if M[r+1, c , 4] == 1:
                move.append("Down")
            elif M[r+1, c, 4] == 0:
                history.append((r + 1, c))
                M[r+1, c , 4] = 2  # have append in history but haven't been visited yet

        if len(move)>0:
            chosen_move = random.choice(move)

            # remove left
            if chosen_move=='Left':
                # break the wall
                M[r,c,0] = 1
                M[r,c-1,2] = 1

            # remove right
            elif chosen_move=='Right':
                M[r, c, 2] = 1
                M[r, c +1, 0] = 1
            # remove up
            elif chosen_move=='Up':
                M[r-1, c, 3] = 1
                M[r, c , 1] = 1
            # remove down
            elif chosen_move=='Down':
                M[r+1, c, 1] = 1
                M[r, c , 3] = 1


    M[0, 0, 0] = 1
    M[size1 - 1, size2 - 1, 2] = 1

    return M


def random_first(size1,size2):


    # A matrix to represent maze. M[i,j] = [LEFT, UP, RIGHT, DOWN, CHECK_IF_VISITED]
    M = np.zeros((size1, size2, 5), dtype=np.uint8)

    # start row idx and start column idx
    r = 0
    c = 0

    # set hostory to empty
    history = list()  # a list to hold all the nodes visited
    history.append((r, c))
    while len(history) != 0:

        # print(r,c)
        M[r, c, 4] = 1

        move = list() # set move list to empty

        if c > 0:
            if M[r, c - 1, 4] == 0:
                move.append('Left')

        if r > 0:
            if M[r - 1, c, 4] == 0:
                move.append("Up")

        if c < size2 - 1:
            if M[r, c + 1, 4] == 0:
                move.append("Right")

        if r < size1 - 1:
            if M[r + 1, c, 4] == 0:
                move.append("Down")

        if len(move) > 0:
            history.append((r, c)) # break a wall in a random direction
            chosen_move = random.choice(move)
            if chosen_move == 'Left':
                # break the wall
                M[r, c, 0] = 1
                M[r, c - 1, 2] = 1
                c = c - 1
            elif chosen_move == 'Right':
                M[r, c, 2] = 1
                M[r, c + 1, 0] = 1
                c = c + 1
            elif chosen_move == 'Up':
                M[r - 1, c, 3] = 1
                M[r, c, 1] = 1
                r = r - 1
            elif chosen_move == 'Down':
                M[r + 1, c, 1] = 1
                M[r, c, 3] = 1
                r = r + 1
        else:
            r, c = history.pop()
    M[0, 0, 0] = 1
    M[size1 - 1, size2 - 1, 2] = 1

    return M

def sidewinder(size1,size2):
    # A matrix to represent maze. M[i,j] = [LEFT, UP, RIGHT, DOWN, CHECK_IF_VISITED]
    M = np.zeros((size1, size2, 5), dtype=np.uint8)

    current_cell = (0, 0)
    runset = list()
    col_idx = 0
    # iterate all rows
    for row_idx in range(size1):
        runset = list()
        # iterate all column
        for col_idx in range(size2):
            if row_idx == 0:
                if col_idx != size2 - 1:
                    M[row_idx, col_idx, 2] = 1
                    M[row_idx, col_idx + 1, 0] = 1
            # go north or west
            else:
                current_cell = (row_idx, col_idx)
                runset.append(current_cell)
                if col_idx != size2 - 1:
                    r = random.random()
                    if r < 0.5:  # go east
                        # break wall
                        M[row_idx, col_idx, 2] = 1
                        M[row_idx, col_idx + 1, 0] = 1

                    else:
                        # go north
                        cell = random.choice(runset)
                        cell_r, cell_c = cell[0], cell[1]
                        M[cell_r, cell_c, 1] = 1
                        M[cell_r - 1, cell_c, 3] = 1
                        runset.clear()
                else: #
                    cell = random.choice(runset)
                    cell_r, cell_c = cell[0], cell[1]
                    M[cell_r, cell_c, 1] = 1
                    M[cell_r - 1, cell_c, 3] = 1
                    runset.clear()

    M[0, 0, 0] = 1
    M[size1 - 1, size2 - 1, 2] = 1
    return M

def generate_loop(maze,loop_num):
    u_list = []
    size1 = maze.shape[0]
    size2 = maze.shape[1]

    tmp = loop_num
    idx = 0
    # dead_num = None
    while tmp>0:

        u_list = list()

        for i in range(size1):
            for j in range(size2):
                # print(np.sum(maze[i,j],keepdims=False))
                if i!=0 and j!=0 and i!=size1-1 and j!=size2-1:
                    if np.sum(maze[i,j,:4],keepdims=False)==1:
                        idx = np.argmax(maze[i,j,:4])
                        u_list.append((i,j,idx))


        if len(u_list)==0:
            break
        choice = random.choices(u_list,k=1)

        # print("choice is ",choice)
        tmp = tmp-1
        # idx+=1
        for c in choice:
            dir = c[2]


            if dir==0: # left
                maze[c[0],c[1],2] = 1 # right
                maze[c[0],c[1]+1,0] = 1
            elif dir==1: # up
                maze[c[0],c[1],3] = 1 # down
                maze[c[0]+ 1, c[1] , 1] = 1
            elif dir==2:
                maze[c[0],c[1],0] = 1
                maze[c[0], c[1]-1, 2] = 1
            elif dir==3:
                maze[c[0],c[1],1] = 1
                maze[c[0] - 1, c[1], 3] = 1
    return maze


def get_dead_num_old(maze):
    u_list = list() # count U-shaped wall
    size1 = maze.shape[0]
    size2 = maze.shape[1]

    # iterate all column
    for i in range(size1):
        for j in range(size2):
            # print(np.sum(maze[i,j],keepdims=False))
            if i != 0 and j != 0 and i != size1 - 1 and j != size2 - 1:
                if np.sum(maze[i, j, :4], keepdims=False) == 1:
                    # idx = np.argmax(maze[i, j, :4])
                    u_list.append((i, j))

    return len(u_list)


def get_dead_num(maze):
    u_list = list()
    size1 = maze.shape[0]
    size2 = maze.shape[1]

    # iterate all column
    for i in range(size1):
        for j in range(size2):
            # print(np.sum(maze[i,j],keepdims=False))
            # if i != 0 and j != 0 and i != size1 - 1 and j != size2 - 1:
            if np.sum(maze[i, j, :4], keepdims=False) == 1:
                # idx = np.argmax(maze[i, j, :4])
                u_list.append((i, j))

    return len(u_list)



def get_road_num(maze):
    u_list = list()
    size1 = maze.shape[0]
    size2 = maze.shape[1]

    for i in range(size1):
        for j in range(size2):
            # print(np.sum(maze[i,j],keepdims=False))
            # if i != 0 and j != 0 and i != size1 - 1 and j != size2 - 1:
            if np.sum(maze[i, j, :4], keepdims=False) >2:
                # idx = np.argmax(maze[i, j, :4])
                u_list.append((i, j))

    return len(u_list) # 返回计数



def generate_image(M):
    size1,size2 = M.shape[0],M.shape[1]
    # The array image is going to be the output image to display
    image = np.zeros((size1 * 10, size2 * 10), dtype=np.uint8)
    # Generate the image for display
    for row in range(0, size1):
        for col in range(0, size2):
            cell_data = M[row, col]
            for i in range(10 * row + 2, 10 * row + 8):
                image[i, range(10 * col + 2, 10 * col + 8)] = 255
            if cell_data[0] == 1:
                image[range(10 * row + 2, 10 * row + 8), 10 * col] = 255
                image[range(10 * row + 2, 10 * row + 8), 10 * col + 1] = 255
            if cell_data[1] == 1:
                image[10 * row, range(10 * col + 2, 10 * col + 8)] = 255
                image[10 * row + 1, range(10 * col + 2, 10 * col + 8)] = 255
            if cell_data[2] == 1:
                image[range(10 * row + 2, 10 * row + 8), 10 * col + 9] = 255
                image[range(10 * row + 2, 10 * row + 8), 10 * col + 8] = 255
            if cell_data[3] == 1:
                image[10 * row + 9, range(10 * col + 2, 10 * col + 8)] = 255
                image[10 * row + 8, range(10 * col + 2, 10 * col + 8)] = 255
    return image
    # Display the image

    # plt.imshow(image,cmap=cm.Greys_r)
    # plt.xticks(np.arange(0,size * 10+1,step=10),np.arange(size+1))
    # plt.yticks(np.arange(0,size * 10+1,step=10),np.arange(size+1))
    # plt.show()



if __name__ == "__main__":
    m = prim(6,6)
    image = generate_image(m)
    plt.clf()
    plt.xticks([])
    plt.yticks([])
    plt.imshow(image)
    plt.show()
    m1 = generate_loop(m,4)

    image =  generate_image(m1)
    plt.clf()
    plt.xticks([])
    plt.yticks([])
    plt.imshow(image)
    plt.show()