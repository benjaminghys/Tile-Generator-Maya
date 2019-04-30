import maya.cmds as cmd

cmd.select(all = True)
cmd.delete()

#variables
width = 2
depth = 2
height = 3.0
indentation = 1  #(gets converted to float) else it will round off when dividing 
wallLength = 5 #(get converted to int) range only takes int



indentation = float(indentation)
wallLength = int(wallLength)

i = 0
for i in range(wallLength):
    block = cmd.polyCube(w = width, d = depth, h = height) #big block
    cmd.move(width*(2*i),0,0)
    cmd.polyCube(w = width, d = depth, h = (height - indentation)) #small block
    smallBlock = cmd.move(width*(i*2+1),-indentation/2,0) #move the last created object
