#!/usr/bin/python
import mcpi.minecraft as minecraft
import mcpi.block as block
        
from tkinter import *
import numpy as np

# Global variables and initialization
global active_colour, grid_distance, maze, mc

mc = minecraft.Minecraft.create()

canvas_width = 500
canvas_height = 500
grid_distance = 10
label_text = 'CoderDojo Dahlem @ Freie Universität Berlin'
python_green = "#476042"
python_white = "#fff"
python_black = "#000000"

active_colour = python_black

maze = np.zeros((int(canvas_width/grid_distance+1),int(canvas_height/grid_distance+1)), dtype=np.int)
print(maze.shape)

# Event handlers

def fill_box(event, maze):
    #global active_colour, grid_distance, maze
	
    x1, y1 = ( event.x - event.x%grid_distance +2), \
			 ( event.y - event.y%grid_distance +2)
			 
    x2, y2 = ( event.x - event.x%grid_distance + grid_distance -1), \
			 ( event.y - event.y%grid_distance +2)
			 
    x3, y3 = ( event.x - event.x%grid_distance + grid_distance -1), \
			 ( event.y - event.y%grid_distance + grid_distance -1)
			 
    x4, y4 = ( event.x - event.x%grid_distance +2), \
			 ( event.y - event.y%grid_distance + grid_distance -1)

    w.create_polygon( x1, y1, x2, y2, x3, y3, x4, y4, fill = active_colour )

    if active_colour == python_white:
        matrix_value = 0
    elif active_colour == python_black:
        matrix_value = 1
    
    maze[int(event.x/grid_distance),int(event.y/grid_distance)] = matrix_value
	
def checkered(canvas, line_distance):
    # vertical lines at an interval of "line_distance" pixel
    for x in range(line_distance,canvas_width,line_distance):
        canvas.create_line(x, 0, x, canvas_height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance,canvas_height,line_distance):
        canvas.create_line(0, y, canvas_width, y, fill="#476042")

def update_label(event):
   	label_text = 'x: ' + str(event.x) + ' - y: ' + str(event.y)

def button_erase_event():
    global active_colour
    active_colour = python_white
    print(active_colour)

def button_draw_event():
    global active_colour
    active_colour = python_black
    print(active_colour)

def button_reset_handler(w, maze, mc):

	# Clear the canvas
	w.create_polygon( 	1, 1, 
						1, canvas_height, 
						canvas_width, canvas_height, 
						canvas_width, 1, fill = python_white )
	checkered(w, grid_distance)

	# Clear Minecraft
	maze[:] = 0	
	button_MC_H_handler(maze,mc)
	
def button_close(): # TODO
    master.destroy()

def button_MC_H_handler(maze,mc):

    row, col = maze.shape

    #mc.player.setpos(0, 0, 0)
    for r in range(row):
        for c in range(col):
            if maze[(r,c)] == 1:
                mc.setBlock(r, 5, c, 1)
                print(r,c)
            else:
                mc.setBlock(r, 5, c, 0)
                
# Appearance of the screen	
master = Tk()
master.title( "Minecraft Maze Generator" )
myContainer = Frame(master)
myContainer.pack()

canvasFrame = Frame(myContainer)
canvasFrame.pack()
w = Canvas(canvasFrame, 
           width=canvas_width, 
           height=canvas_height,
    	   bg="white")
w.pack(expand = YES, fill = BOTH)

buttonsFrame = Frame(myContainer)
buttonsFrame.pack()

button_erase = Button(buttonsFrame, command=button_erase_event)
button_erase.configure(text="Erase", padx = 10)
button_erase.pack(side = LEFT, padx = 10)

button_draw = Button(buttonsFrame, command=button_draw_event)
button_draw.configure(text = 'Draw', padx = 10)
button_draw.pack(side = LEFT, padx = 10)

# Example of passing arguments taken from http://thinkingtkinter.sourceforge.net/tt078_py.txt
button_MC_H = Button(buttonsFrame, command=lambda arg1=maze, arg2=mc : button_MC_H_handler(arg1, arg2))
button_MC_H.configure(text = 'Minecraft H', padx = 10)
button_MC_H.pack(side = LEFT, padx = 10)

button_reset = Button(buttonsFrame, command=lambda arg1=w, arg2=maze, arg3=mc : button_reset_handler(arg1,arg2,arg3))
button_reset.configure(text = 'Reset', padx = 10)
button_reset.pack(side = LEFT, padx = 10)

checkered(w,grid_distance)

#w.bind( "<B1-Motion>", fill_box )
w.bind( "<B1-Motion>", lambda event, arg1=maze : fill_box(event, arg1) )

message = Label( master, text = label_text )
message.pack( side = BOTTOM )


    
mainloop()

