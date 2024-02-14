"""
Create a x, y, z coordinate on canvas
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from Point import Point
import ColorType
from DisplayableCube import DisplayableCube


class ModelAxes(Component):
    """
    Define our linkage model
    """

    components = None
    shaderProg = None

    def __init__(self, shaderProg, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.shaderProg = shaderProg

        xAxes = Component(Point((1, 0, 0)), DisplayableCube(self.shaderProg, 0.05, 0.05, 2, ColorType.SOFTRED))
        xAxes.setDefaultAngle(90, xAxes.vAxis)
        xAxes.renderingRouting = "vertex"
        yAxes = Component(Point((0, 1, 0)), DisplayableCube(self.shaderProg, 0.05, 0.05, 2, ColorType.SOFTGREEN))
        yAxes.setDefaultAngle(-90, yAxes.uAxis)
        yAxes.renderingRouting = "vertex"
        zAxes = Component(Point((0, 0, 1)), DisplayableCube(self.shaderProg, 0.05, 0.05, 2, ColorType.SOFTBLUE))
        zAxes.renderingRouting = "vertex"
        self.addChild(xAxes)
        self.addChild(yAxes)
        self.addChild(zAxes)

