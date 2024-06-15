# To optimize and improve the readability and maintainability of the given code, 
# I have refactored it by breaking down large functions into smaller, more manageable ones, 
# removing redundancy, and leveraging Python's features effectively. 
# Here’s my optimized version:

import maya.cmds as cmd
import functools as func
import random as r


class TileGenerator:
    def __init__(self):
        self.initialize_defaults()
        self.generatedTiles = []

    def initialize_defaults(self):
        self.tileX = 10
        self.tileY = 5
        self.tileSizeX = 2
        self.tileSizeY = 2
        self.tileSizeZ = 0.5
        self.gapX = 0.1
        self.gapY = 0.3
        self.maxRotationX = 5
        self.maxRotationY = 5
        self.maxRotationZ = 5
        self.heightVariation = 0.5
        self.rotationXMin, self.rotationXMax = -8, 5
        self.rotationYMin, self.rotationYMax = -10, 8
        self.rotationZMin, self.rotationZMax = -10, 15
        self.heightVariationMin, self.heightVariationMax = -0.5, 0.2
        self.gapYmin, self.gapYmax = 0.2, 0.8
        self.gapXmin, self.gapXmax = 0.23, 0.55
        self.tileSizeXMin, self.tileSizeXMax = 2.0, 2.5
        self.tileSizeYMin, self.tileSizeYMax = 2, 3
        self.tileSizeZMin, self.tileSizeZMax = 0.2, 0.5
        self.clear = True
        self.keepHeight = False
        self.keepSizeX = False
        self.keepSizeY = False
        self.keepSizeZ = False
        self.keepRotX = False
        self.keepRotY = False
        self.keepRotZ = False

    def generate_tiles(self, UI, *args):
        self.update_values(UI)
        if self.clear:
            self.clear_tiles()
        self.generatedTiles = []
        offsetX, gapsX = 0.0, 0.0

        for i in range(self.tileX):
            offsetY, gapsY = 0.0, 0.0
            gapX = r.uniform(self.gapXmin, self.gapXmax)
            sizeX = r.uniform(self.tileSizeXMin, self.tileSizeXMax)
            offsetX += sizeX / 2 + gapX

            for j in range(self.tileY):
                sizeY = r.uniform(self.tileSizeYMin, self.tileSizeYMax)
                sizeZ = r.uniform(self.tileSizeZMin, self.tileSizeZMax)
                offsetY += sizeY / 2 + (r.uniform(self.gapYmin, self.gapYmax) if j != 0 else 0)

                heightOffset = r.uniform(self.heightVariationMin, self.heightVariationMax)
                rotX = r.uniform(self.rotationXMin, self.rotationXMax)
                rotY = r.uniform(self.rotationYMin, self.rotationYMax)
                rotZ = r.uniform(self.rotationZMin, self.rotationZMax)

                tile = cmd.polyCube(d=sizeY, w=sizeX, h=sizeZ)[0]
                cmd.move(offsetX + gapsX, heightOffset, offsetY + gapsY, tile)
                cmd.rotate(rotX, rotY, rotZ, tile)
                self.generatedTiles.append(tile)

    def clear_tiles(self, *args):
        for tile in self.generatedTiles:
            if cmd.objExists(tile):
                cmd.delete(tile)

    def update_values(self, UI, *args):
        self.clear = cmd.checkBox(UI.clearScene, q=True, v=True)
        self.keepSizeX = cmd.checkBoxGrp(UI.reGenSettings, q=True, v2=True)
        self.keepSizeY = cmd.checkBoxGrp(UI.reGenSettings, q=True, v3=True)
        self.keepSizeZ = cmd.checkBoxGrp(UI.reGenSettings, q=True, v4=True)
        self.keepHeight = cmd.checkBoxGrp(UI.reGenSettings2, q=True, v1=True)
        self.keepRotX = cmd.checkBoxGrp(UI.reGenSettings2, q=True, v2=True)
        self.keepRotY = cmd.checkBoxGrp(UI.reGenSettings2, q=True, v3=True)
        self.keepRotZ = cmd.checkBoxGrp(UI.reGenSettings2, q=True, v4=True)

        self.tileX, self.tileY = cmd.intFieldGrp(UI.tiles, q=True, v=True)

        tileIsSimple = cmd.radioButtonGrp(UI.selectorTileSize, q=True, sl=True)
        gapsIsSimple = cmd.radioButtonGrp(UI.selectorGaps, q=True, sl=True)
        heightIsSimple = cmd.radioButtonGrp(UI.selectorHeight, q=True, sl=True)
        rotationIsSimple = cmd.radioButtonGrp(UI.selectorMaxRotation, q=True, sl=True)

        if tileIsSimple == 1:
            temp = cmd.floatFieldGrp(UI.tileSize, q=True, v=True)
            self.set_tile_size(temp, temp, temp)
        elif tileIsSimple == 2:
            tempMin = cmd.floatFieldGrp(UI.tileSizeMin, q=True, v=True)
            tempMax = cmd.floatFieldGrp(UI.tileSizeMax, q=True, v=True)
            self.set_tile_size(tempMin, tempMax)

        if gapsIsSimple == 1:
            temp = cmd.floatFieldGrp(UI.gaps, q=True, v=True)
            self.set_gaps(temp, temp)
        elif gapsIsSimple == 2:
            tempMin = cmd.floatFieldGrp(UI.gapsMin, q=True, v=True)
            tempMax = cmd.floatFieldGrp(UI.gapsMax, q=True, v=True)
            self.set_gaps(tempMin, tempMax)

        if heightIsSimple == 1:
            temp = cmd.floatFieldGrp(UI.heightVariation, q=True, v=True)
            self.heightVariationMax = temp[0]
            self.heightVariationMin = 0
        elif heightIsSimple == 2:
            temp = cmd.floatFieldGrp(UI.heightVariationMinMax, q=True, v=True)
            self.heightVariationMin, self.heightVariationMax = temp

        if rotationIsSimple == 1:
            temp = cmd.floatFieldGrp(UI.maxRotation, q=True, v=True)
            self.set_rotation(temp, (0, 0, 0))
        elif rotationIsSimple == 2:
            tempMin = cmd.floatFieldGrp(UI.rotationMin, q=True, v=True)
            tempMax = cmd.floatFieldGrp(UI.rotationMax, q=True, v=True)
            self.set_rotation(tempMax, tempMin)

    def set_tile_size(self, min_vals, max_vals):
        self.tileSizeXMin, self.tileSizeYMin, self.tileSizeZMin = min_vals
        self.tileSizeXMax, self.tileSizeYMax, self.tileSizeZMax = max_vals

    def set_gaps(self, min_vals, max_vals):
        self.gapXmin, self.gapYmin = min_vals
        self.gapXmax, self.gapYmax = max_vals

    def set_rotation(self, max_vals, min_vals):
        self.rotationXMax, self.rotationYMax, self.rotationZMax = max_vals
        self.rotationXMin, self.rotationYMin, self.rotationZMin = min_vals

    def regenerate(self, UI, *args):
        selected = cmd.ls(selection=True)
        self.update_values(UI)

        for item in selected:
            cubeAttr = cmd.listConnections(cmd.listRelatives(item))

            if not cubeAttr:
                continue

            sizeX = r.uniform(self.tileSizeXMin, self.tileSizeXMax)
            sizeY = r.uniform(self.tileSizeYMin, self.tileSizeYMax)
            sizeZ = r.uniform(self.tileSizeZMin, self.tileSizeZMax)
            heightOffset = r.uniform(self.heightVariationMin, self.heightVariationMax)
            rotX = r.uniform(self.rotationXMin, self.rotationXMax)
            rotY = r.uniform(self.rotationYMin, self.rotationYMax)
            rotZ = r.uniform(self.rotationZMin, self.rotationZMax)

            if not self.keepSizeX:
                cmd.setAttr(f"{cubeAttr[1]}.width", sizeX)
            if not self.keepSizeY:
                cmd.setAttr(f"{cubeAttr[1]}.height", sizeY)
            if not self.keepSizeZ:
                cmd.setAttr(f"{cubeAttr[1]}.depth", sizeZ)
            if not self.keepHeight:
                cmd.setAttr(f"{item}.translateY", heightOffset)
            if not self.keepRotX:
                cmd.setAttr(f"{item}.rotateX", rotX + 90)
            if not self.keepRotY:
                cmd.setAttr(f"{item}.rotateY", rotY + 90)
            if not self.keepRotZ:
                cmd.setAttr(f"{item}.rotateZ", rotZ)

        print("Finished re-generating values for the cubes.")


class UI:
    def __init__(self, id):
        self.generator = TileGenerator()
        self.setup_ui(id)

    def setup_ui(self, id):
        if cmd.window('window1', ex=True):
            cmd.deleteUI('window1', window=True)

        mainWindow = cmd.window(title=id, sizeable=False, resizeToFitChildren=True)
        cmd.rowColumnLayout(numberOfColumns=1, co=(1, 'both', 5), cw=(100, 500))
        self.setup_tile_count_ui()
        self.setup_tile_size_ui()
        self.setup_gaps_ui()
        self.setup_height_variation_ui()
        self.setup_rotation_ui()
        self.setup_regeneration_ui()
        self.setup_clear_and_generate_ui()
        cmd.showWindow(mainWindow)

    def setup_tile_count_ui(self):
        self.tiles = cmd.intFieldGrp(
            l="Tiles", v1=self.generator.tileX, v2=self.generator.tileY, 
            columnWidth=[(1, 100), (2, 100), (3, 100)], 
            numberOfFields=2
        )

    def setup_tile_size_ui(self):
        self.selectorTileSize = cmd.radioButtonGrp(
            nrb=2, l='Tile Size:', sl=1, la2=['Simple', 'Advanced'],
            cc1=lambda *args: self.update_tile_size_ui(1),
            cc2=lambda *args: self.update_tile_size_ui(2)
        )
        self.tileSize = cmd.floatFieldGrp(
            l="Tile Size", v1=self.generator.tileSizeX, 
            columnWidth=[(1, 100), (2, 100)], 
            pre=3
        )
        self.tileSizeMin = cmd.floatFieldGrp(
            l="Tile Size Min", v1=self.generator.tileSizeXMin,
            v2=self.generator.tileSizeYMin, v3=self.generator.tileSizeZMin,
            columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100)], 
            pre=3, en=False
        )
        self.tileSizeMax = cmd.floatFieldGrp(
            l="Tile Size Max", v1=self.generator.tileSizeXMax,
            v2=self.generator.tileSizeYMax, v3=self.generator.tileSizeZMax,
            columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100)], 
            pre=3, en=False
        )

    def setup_gaps_ui(self):
        self.selectorGaps = cmd.radioButtonGrp(
            nrb=2, l='Gaps:', sl=1, la2=['Simple', 'Advanced'],
            cc1=lambda *args: self.update_gaps_ui(1),
            cc2=lambda *args: self.update_gaps_ui(2)
        )
        self.gaps = cmd.floatFieldGrp(
            l="Gaps", v1=self.generator.gapX, 
            columnWidth=[(1, 100), (2, 100)], 
            pre=3
        )
        self.gapsMin = cmd.floatFieldGrp(
            l="Gaps Min", v1=self.generator.gapXmin,
            v2=self.generator.gapYmin,
            columnWidth=[(1, 100), (2, 100), (3, 100)], 
            pre=3, en=False
        )
        self.gapsMax = cmd.floatFieldGrp(
            l="Gaps Max", v1=self.generator.gapXmax,
            v2=self.generator.gapYmax,
            columnWidth=[(1, 100), (2, 100), (3, 100)], 
            pre=3, en=False
        )

    def setup_height_variation_ui(self):
        self.selectorHeight = cmd.radioButtonGrp(
            nrb=2, l='Height Variation:', sl=1, la2=['Simple', 'Advanced'],
            cc1=lambda *args: self.update_height_variation_ui(1),
            cc2=lambda *args: self.update_height_variation_ui(2)
        )
        self.heightVariation = cmd.floatFieldGrp(
            l="Height Variation", v1=self.generator.heightVariation, 
            columnWidth=[(1, 100), (2, 100)], 
            pre=3
        )
        self.heightVariationMinMax = cmd.floatFieldGrp(
            l="Height Variation Min/Max", v1=self.generator.heightVariationMin,
            v2=self.generator.heightVariationMax,
            columnWidth=[(1, 100), (2, 100), (3, 100)], 
            pre=3, en=False
        )

    def setup_rotation_ui(self):
        self.selectorMaxRotation = cmd.radioButtonGrp(
            nrb=2, l='Max Rotation:', sl=1, la2=['Simple', 'Advanced'],
            cc1=lambda *args: self.update_rotation_ui(1),
            cc2=lambda *args: self.update_rotation_ui(2)
        )
        self.maxRotation = cmd.floatFieldGrp(
            l="Max Rotation", v1=self.generator.maxRotationX, 
            columnWidth=[(1, 100), (2, 100)], 
            pre=3
        )
        self.rotationMin = cmd.floatFieldGrp(
            l="Rotation Min", v1=self.generator.rotationXMin,
            v2=self.generator.rotationYMin, v3=self.generator.rotationZMin,
            columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100)], 
            pre=3, en=False
        )
        self.rotationMax = cmd.floatFieldGrp(
            l="Rotation Max", v1=self.generator.rotationXMax,
            v2=self.generator.rotationYMax, v3=self.generator.rotationZMax,
            columnWidth=[(1, 100), (2, 100), (3, 100), (4, 100)], 
            pre=3, en=False
        )

    def setup_regeneration_ui(self):
        self.reGenSettings = cmd.checkBoxGrp(
            numberOfCheckBoxes=4,
            label='Keep these settings the same when re-generating values',
            labelArray4=['X Size', 'Y Size', 'Z Size', 'Height'],
            cw5=[35, 150, 60, 60, 60]
        )
        self.reGenSettings2 = cmd.checkBoxGrp(
            numberOfCheckBoxes=4,
            label='',
            labelArray4=['Height', 'X Rotation', 'Y Rotation', 'Z Rotation'],
            cw5=[35, 150, 60, 60, 60]
        )

    def setup_clear_and_generate_ui(self):
        self.clearScene = cmd.checkBox(
            label="Clear Scene", value=True
        )
        cmd.separator(h=10, style="none")
        cmd.button(
            label="Generate Tiles", 
            c=func.partial(self.generator.generate_tiles, self)
        )
        cmd.button(
            label="Re-generate selected", 
            c=func.partial(self.generator.regenerate, self)
        )

    def update_tile_size_ui(self, state):
        cmd.floatFieldGrp(self.tileSize, e=True, en=(state == 1))
        cmd.floatFieldGrp(self.tileSizeMin, e=True, en=(state == 2))
        cmd.floatFieldGrp(self.tileSizeMax, e=True, en=(state == 2))

    def update_gaps_ui(self, state):
        cmd.floatFieldGrp(self.gaps, e=True, en=(state == 1))
        cmd.floatFieldGrp(self.gapsMin, e=True, en=(state == 2))
        cmd.floatFieldGrp(self.gapsMax, e=True, en=(state == 2))

    def update_height_variation_ui(self, state):
        cmd.floatFieldGrp(self.heightVariation, e=True, en=(state == 1))
        cmd.floatFieldGrp(self.heightVariationMinMax, e=True, en=(state == 2))

    def update_rotation_ui(self, state):
        cmd.floatFieldGrp(self.maxRotation, e=True, en=(state == 1))
        cmd.floatFieldGrp(self.rotationMin, e=True, en=(state == 2))
        cmd.floatFieldGrp(self.rotationMax, e=True, en=(state == 2))

