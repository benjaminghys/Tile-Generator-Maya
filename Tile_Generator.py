import maya.cmds as cmd
# import TileGenerator
import functools as func
import random as r


class UI:
    def __init__(self, id):
        self.tileX = 10
        self.tileY = 5

        self.tileSizeX = 2
        self.tileSizeY = 2
        self.tileSizeZ = .5

        self.gapX = .1
        self.gapY = .3

        self.maxRotationX = 5  # degrees
        self.maxRotationY = 5  # degrees
        self.maxRotationZ = 5  # degrees

        self.heightVariation = .5

        self.rotationXMin = -8
        self.rotationXMax = 5

        self.rotationYMin = -10
        self.rotationYMax = 8

        self.rotationZMin = -10
        self.rotationZMax = 15

        self.heightVariationMin = -.5
        self.heightVariationMax = .2

        self.gapYmin = .2
        self.gapYmax = .8

        self.gapXmin = .23
        self.gapXmax = .55

        self.tileSizeXMin = 2.0
        self.tileSizeXMax = 2.5

        self.tileSizeYMin = 2
        self.tileSizeYMax = 3

        self.tileSizeZMin = .2
        self.tileSizeZMax = 0.5

        self.clear = True
        self.keepHeight = False
        self.keepSizeX = False
        self.keepSizeY = False
        self.keepSizeZ = False
        self.keepRotX = False
        self.keepRotY = False
        self.keepRotZ = False


        self.createUI(id)

    def createUI(self, windowId="newWindow"):

        self.venster = cmd.window(title=windowId, sizeable=False, resizeToFitChildren=True)  # create new window
        cmd.rowColumnLayout(numberOfColumns=1, co=(1,"both",15))

        cmd.text(label="Tile Generator", al="center", h=45)
        cmd.separator(h=5)

        # inputs
        # simple
        self.tiles = cmd.intFieldGrp(numberOfFields=2, value1=self.tileX, value2=self.tileY, label="tiles in X / Y direction",
                                     cal=(1, "left"))

        cmd.separator(h=5)
        cmd.separator(h=5)  # double separator line
        # simple
        self.tileSize = cmd.floatFieldGrp(numberOfFields=3, value1=self.tileSizeX, value2=self.tileSizeY, value3=self.tileSizeZ,
                                          label="tile size X / Y / Z direction", cal=(1, "left"))
        cmd.separator(h=5, style="none")
        # complex
        self.tileSizeMin = cmd.floatFieldGrp(numberOfFields=3, value1=self.tileSizeXMin, value2=self.tileSizeYMin, value3=self.tileSizeZMin,
                                             label="tile size X / Y / Z minimum", cal=(1, "left"), en=False)
        self.tileSizeMax = cmd.floatFieldGrp(numberOfFields=3, value1=self.tileSizeXMax, value2=self.tileSizeYMax, value3=self.tileSizeZMax,
                                             label="tile size X / Y / Z maximum", cal=(1, "left"), en=False)
        # selector (radiobutton)
        self.selectorTileSize = cmd.radioButtonGrp(label1="Simple", label2="Godmode", sl=1, nrb=2, adj=1, h=30,
                                                   of1=func.partial(self.turnOff, self.tileSize),
                                                   of2=func.partial(self.turnOff, self.tileSizeMin, self.tileSizeMax),
                                                   on2=func.partial(self.turnOn, self.tileSizeMin, self.tileSizeMax),
                                                   on1=func.partial(self.turnOn, self.tileSize))
        # sends a reference to to turnOn or turnOff so it can enable or disable, (same for the other radioButtons)

        cmd.separator(h=5)
        cmd.separator(h=5)  # double separator line
        # simple
        self.gaps = cmd.floatFieldGrp(numberOfFields=2, value1=self.gapX, value2=self.gapY, label="gaps between tiles X / Y",
                                      cal=(1, "left"), ann="no random gap amount, will always be the same")
        cmd.separator(h=5, style="none")
        # complex
        self.gapsMin = cmd.floatFieldGrp(numberOfFields=2, value1=self.gapXmin, value2=self.gapYmin, label="gaps tiles X / Y minimum",
                                         cal=(1, "left"), en=False)
        self.gapsMax = cmd.floatFieldGrp(numberOfFields=2, value1=self.gapXmax, value2=self.gapYmax, label="gaps tiles X / Y maximum",
                                         cal=(1, "left"), en=False)
        # selector (radiobutton)
        self.selectorGaps = cmd.radioButtonGrp(label1="Simple", label2="Godmode", sl=1, nrb=2, adj=1, h=30,
                                               of1=func.partial(self.turnOff, self.gaps),
                                               of2=func.partial(self.turnOff, self.gapsMin, self.gapsMax),
                                               on2=func.partial(self.turnOn, self.gapsMin, self.gapsMax),
                                               on1=func.partial(self.turnOn, self.gaps))

        cmd.separator(h=5)
        cmd.separator(h=5)  # double separator line
        # simple
        self.maxRotation = cmd.floatFieldGrp(numberOfFields=3, value1=self.maxRotationX, value2=self.maxRotationY, value3=self.maxRotationZ,
                                             label="max rotation in X / Y / Z axis", cal=(1, "left"), ann="variation in rotation starting from 0")
        cmd.separator(h=5, style="none")
        # complex
        self.rotationMin = cmd.floatFieldGrp(numberOfFields=3, value1=self.rotationXMin, value2=self.rotationYMin, value3=self.rotationZMin,
                                             label="min rotation in X / Y / Z axis", cal=(1, "left"), en=False)
        self.rotationMax = cmd.floatFieldGrp(numberOfFields=3, value1=self.rotationXMax, value2=self.rotationYMax, value3=self.rotationZMax,
                                             label="max rotation in X / Y / Z axis", cal=(1, "left"), en=False)
        # selector (radiobutton)
        self.selectorMaxRotation = cmd.radioButtonGrp(label1="Simple", label2="Godmode", sl=1, nrb=2, adj=1, h=30,
                                                      of1=func.partial(self.turnOff, self.maxRotation),
                                                      of2=func.partial(self.turnOff, self.rotationMin,
                                                                       self.rotationMax),
                                                      on2=func.partial(self.turnOn, self.rotationMin, self.rotationMax),
                                                      on1=func.partial(self.turnOn, self.maxRotation))

        cmd.separator(h=5)
        cmd.separator(h=5)  # double separator line

        # simple
        self.heightVariation = cmd.floatFieldGrp(numberOfFields=1, value1=self.heightVariation, label="max variation in height",
                                                 cal=(1, "left"), ann="variation in height starting from 0")
        cmd.separator(h=5, style="none")
        # complex
        self.heightVariationMinMax = cmd.floatFieldGrp(numberOfFields=2, value1=self.heightVariationMin, value2=self.heightVariationMax,
                                                       label="min/max variation in height", cal=(1, "left"), en=False)
        # selector (radiobutton)
        self.selectorHeight = cmd.radioButtonGrp(label1="Simple", label2="Godmode", sl=1, nrb=2, adj=1, h=30,
                                                 of1=func.partial(self.turnOff, self.heightVariation),
                                                 of2=func.partial(self.turnOff, self.heightVariationMinMax),
                                                 on2=func.partial(self.turnOn, self.heightVariationMinMax),
                                                 on1=func.partial(self.turnOn, self.heightVariation))

        cmd.separator(h=5)
        cmd.separator(h=5)  # double separator line
        cmd.separator(h=5, style="none")  # small offset

        space = (cmd.window(self.venster, q=True, w=True) / 6)  # value to keep nice indentations

        cmd.rowLayout(numberOfColumns=5)
        cmd.separator(h=5, style="none", w=space/2)  # indentation
        self.clearScene = cmd.checkBox(l="clear entire scene", v=self.clear)
        cmd.separator(h=5, style="none", w=10)  # indentation
        self.reGenSettings = cmd.checkBoxGrp(vr=True, ncb=4, la4=["to not ReGen","tile width","tile height","tile depth"], en1=False, w=100, v1=True, co2=(250,120), ann="boxes that are checked will not be regenerated")
        self.reGenSettings2 = cmd.checkBoxGrp(vr=True, ncb=4, la4=["variation in height","rotation in X","rotation in Y","rotation in Z"], ann="boxes that are checked will not be regenerated")
        cmd.setParent("..")  # back to default columns
        cmd.separator(h=5, style="none")  # small offset

        cmd.rowLayout(nc=5)
        cmd.separator(h=5, w=space/2, style="none")
        cmd.button(label="Generate", command=self.generateTiles, w=space)
        cmd.separator(h=5, w=space/2, style="none")
        cmd.button(label="Re-Gen Selection", command=self.reGenerate, w=space)
        cmd.setParent("..")
        cmd.separator(h=10, style="none")

        # clear scene button
        cmd.rowLayout(nc=2)
        cmd.separator(h=5, style="none", w=space/2)
        cmd.button(label="clear entire scene", c=clearScene, w=2.55*space)

        cmd.setParent("..")
        cmd.separator(h=10, style="none")


        cmd.showWindow(self.venster)

    def generateTiles(self, *args):
        self.updateValues()

        if self.clear:
            clearScene()

        offsetX = .0
        gapsX = .0
        for i in range(self.tileX):  # generates the X direction of the tiles
            offsetY = 0.0  # reset offset
            gapsY = 0.0  # reset gaps
            gapX = r.uniform(self.gapXmin, self.gapXmax)  # variation in the x axis

            sizeX = r.uniform(self.tileSizeXMin, self.tileSizeXMax)
            offsetX += sizeX / 2
            gapsX += gapX

            if i != 0:  # increment offset
                offsetX += sizeX / 2

            for j in range(self.tileY):  # generates the Y direction of the tiles
                sizeY = r.uniform(self.tileSizeYMin, self.tileSizeYMax)
                offsetY += sizeY / 2
                sizeZ = r.uniform(self.tileSizeZMin, self.tileSizeZMax)

                if j != 0:  # gap y direction
                    gapsY += r.uniform(self.gapYmin, self.gapYmax)

                heightOffset = r.uniform(self.heightVariationMin, self.heightVariationMax)
                rotX = r.uniform(self.rotationXMin, self.rotationXMax)
                rotY = r.uniform(self.rotationYMin, self.rotationYMax)
                rotZ = r.uniform(self.rotationZMin, self.rotationZMax)

                if j != 0:  # increment offset
                    offsetY += sizeY / 2

                # spawn polyCube with the generated variables
                cmd.polyCube(d=sizeY, w=sizeX, h=sizeZ)
                cmd.move(offsetX + gapsX, heightOffset, offsetY + gapsY)
                cmd.rotate(rotX, rotY, rotZ)

        print("finished generating cubes")

    def updateValues(self, *args):
        tileIsSimple = cmd.radioButtonGrp(self.selectorTileSize, q=True, sl=True)
        gapsIsSimple = cmd.radioButtonGrp(self.selectorGaps, q=True, sl=True)
        heightIsSimple = cmd.radioButtonGrp(self.selectorHeight, q=True, sl=True)
        rotationIsSimple = cmd.radioButtonGrp(self.selectorMaxRotation, q=True, sl=True)

        self.clear = cmd.checkBox(self.clearScene, q=True, v=True)

        self.keepSizeX = cmd.checkBoxGrp(self.reGenSettings, q=True, v2=True)
        self.keepSizeY = cmd.checkBoxGrp(self.reGenSettings, q=True, v3=True)
        self.keepSizeZ = cmd.checkBoxGrp(self.reGenSettings, q=True, v4=True)

        self.keepHeight = cmd.checkBoxGrp(self.reGenSettings2, q=True, v1=True)
        self.keepRotX = cmd.checkBoxGrp(self.reGenSettings2, q=True, v2=True)
        self.keepRotY = cmd.checkBoxGrp(self.reGenSettings2, q=True, v3=True)
        self.keepRotZ = cmd.checkBoxGrp(self.reGenSettings2, q=True, v4=True)

        temp = cmd.intFieldGrp(self.tiles, q=True, v=True)
        self.tileX = temp[0]
        self.tileY = temp[1]

        if tileIsSimple == 1:
            temp = cmd.floatFieldGrp(self.tileSize, q=True, v=True)
            self.tileSizeXMax = temp[0]
            self.tileSizeXMin = temp[0]  # should be no variation since simple was chosen in the radio button
            self.tileSizeYMax = temp[1]
            self.tileSizeYMin = temp[1]
            self.tileSizeZMax = temp[2]
            self.tileSizeZMin = temp[2]

        elif tileIsSimple == 2:
            tempMin = cmd.floatFieldGrp(self.tileSizeMin, q=True, v=True)
            tempMax = cmd.floatFieldGrp(self.tileSizeMax, q=True, v=True)
            self.tileSizeXMax = tempMax[0]  # godmode aka min/max has been chosen, so the values get updated
            self.tileSizeXMin = tempMin[0]
            self.tileSizeYMax = tempMax[1]
            self.tileSizeYMin = tempMin[1]

        if gapsIsSimple == 1:
            temp = cmd.floatFieldGrp(self.gaps, q=True, v=True)
            self.gapXmax = temp[0]  # simple mode, if min and max are the same the result = min or max
            self.gapXmin = temp[0]
            self.gapYmax = temp[1]
            self.gapYmin = temp[1]

        elif gapsIsSimple == 2:
            tempMin = cmd.floatFieldGrp(self.gapsMin, q=True, v=True)
            tempMax = cmd.floatFieldGrp(self.gapsMax, q=True, v=True)
            self.gapXmax = tempMax[0]  # complex, required 2 values to get the min and max
            self.gapXmin = tempMin[0]
            self.gapYmax = tempMax[1]
            self.gapYmin = tempMin[1]

        if heightIsSimple == 1:
            temp = cmd.floatFieldGrp(self.heightVariation, q=True, v=True)
            self.heightVariationMax = temp[0]
            self.heightVariationMin = 0  # variation in height starting from 0

        elif heightIsSimple == 2:
            temp = cmd.floatFieldGrp(self.heightVariationMinMax, q=True, v=True)
            self.heightVariationMin = temp[0]
            self.heightVariationMax = temp[1]

        if rotationIsSimple == 1:
            temp = cmd.floatFieldGrp(self.maxRotation, q=True, v=True)
            self.rotationXMax = temp[0]
            self.rotationXMin = 0
            self.rotationYMax = temp[1]
            self.rotationYMin = 0
            self.rotationZMax = temp[2]
            self.rotationZMin = 0

        elif rotationIsSimple == 2:
            tempMin = cmd.floatFieldGrp(self.rotationMin, q=True, v=True)
            tempMax = cmd.floatFieldGrp(self.rotationMax, q=True, v=True)
            self.rotationXMax = tempMax[0]
            self.rotationXMin = tempMin[0]
            self.rotationYMax = tempMax[1]
            self.rotationYMin = tempMin[1]
            self.rotationZMax = tempMax[2]
            self.rotationZMin = tempMin[2]

        print("updated all values")



    @staticmethod
    def turnOff(group, group2, *args):
        isFloatGroup = cmd.floatFieldGrp(group, q=True, ex=True)
        isIntGroup = cmd.intFieldGrp(group, q=True, ex=True)

        if (isFloatGroup):
            cmd.floatFieldGrp(group, e=True, en=False)
            grp2Exist = cmd.floatFieldGrp(group2, q=True, ex=True)
            if (grp2Exist):
                cmd.floatFieldGrp(group2, e=True, en=False)
        elif (isIntGroup):
            cmd.intFieldGrp(group, e=True, en=False)
            grp2Exist = cmd.intFieldGrp(group2, q=True, ex=True)
            if (grp2Exist):
                cmd.intFieldGrp(group2, e=True, en=False)

    @staticmethod
    def turnOn(group, group2, *args):
        isFloatGroup = cmd.floatFieldGrp(group, q=True, ex=True)
        isIntGroup = cmd.intFieldGrp(group, q=True, ex=True)

        if (isFloatGroup):
            cmd.floatFieldGrp(group, e=True, en=True)
            grp2Exist = cmd.floatFieldGrp(group2, q=True, ex=True)
            if (grp2Exist):
                cmd.floatFieldGrp(group2, e=True, en=True)
        elif (isIntGroup):
            cmd.intFieldGrp(group, e=True, en=True)
            grp2Exist = cmd.intFieldGrp(group2, q=True, ex=True)
            if (grp2Exist):
                cmd.intFieldGrp(group2, e=True, en=True)

    def reGenerate(self, *args):
        selected = cmd.ls(selection=True)
        self.updateValues()

        for item in selected:
            cubeAttr = cmd.listConnections(cmd.listRelatives(item))

            heightOffset = r.uniform(self.heightVariationMin, self.heightVariationMax)
            rotX = r.uniform(self.rotationXMin, self.rotationXMax)
            rotY = r.uniform(self.rotationYMin, self.rotationYMax)
            rotZ = r.uniform(self.rotationZMin, self.rotationZMax)
            sizeX = r.uniform(self.tileSizeXMin, self.tileSizeXMax)
            sizeY = r.uniform(self.tileSizeYMin, self.tileSizeYMax)
            sizeZ = r.uniform(self.tileSizeZMin, self.tileSizeZMax)

            if not self.keepSizeX:
                cmd.setAttr("{cube}.width".format(cube=cubeAttr[1]), sizeX)
            if not self.keepSizeY:
                cmd.setAttr("{cube}.height".format(cube=cubeAttr[1]), sizeY)
            if not self.keepSizeZ:
                cmd.setAttr("{cube}.depth".format(cube=cubeAttr[1]), sizeZ)
            if not self.keepHeight:
                cmd.setAttr("{cube}.translateY".format(cube=item), heightOffset)
            if not self.keepRotX:
                cmd.setAttr("{cube}.rotateX".format(cube=item), rotX+90)
            if not self.keepRotY:
                cmd.setAttr("{cube}.rotateY".format(cube=item), rotY+90)
            if not self.keepRotZ:
                cmd.setAttr("{cube}.rotateZ".format(cube=item), rotZ)

        print("finished re-generating values for the cubes")


def clearScene(*args):
    cmd.select(all=True)
    cmd.delete()


em = u"\U0001F4A6"
lit = u"\U0001F525"
logo = u"\u24B8"

win = UI("Tile generator  " + logo + "BB" + lit + em)
