import math
import numpy as np
import ColorType
from Animation import Animation
from Component import Component
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableSphere import DisplayableSphere
from DisplayableCylinder import DisplayableCylinder

# TODO 4 - my first scene
class SceneThree(Component):
    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None

    lRadius = None
    lAngles = None
    lTransformations = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        self.lTransformations = [self.glutility.translate(0, 2, 0, False),
                                 self.glutility.rotate(60, [0, 0, 1], False),
                                 self.glutility.rotate(120, [0, 0, 1], False)]
        self.lRadius = 3
        self.lAngles = [0, 0, 0]


        m1 = Material(np.array((0.3, 0.3, 0.3, 0.3)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.5, 0.5, 0.5, 0.1)), 100)
        
        obj_d = 3.0
        light_d  = 0
        sphere1 = Component(Point((obj_d, 0, 0)), DisplayableSphere(shaderProg, 1.0, ColorType.PINK))
        sphere1.setMaterial(m1)
        sphere1.renderingRouting = "lighting"
        self.addChild(sphere1)
        # (3, 0.4, 0), red, not_infinite, spot_direction=(-1,0,0), 0.4d^2+0.5d+0.1, pi/6
        l1 = Light(Point((light_d, 0.4, 0)), np.array((*ColorType.PURPLE, 1.0)) * 5, None, np.array([1, 0, 0]), np.array([0.4, 0.5, 0.1]), np.pi/20)
        lightCube1 = Component(Point((light_d, 0.4, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.PURPLE))
        lightCube1.renderingRouting = "vertex"
        l1_test = Light(Point((-1, 0.4, 0)), np.array((*ColorType.PURPLE, 1.0)) * 5, None, np.array([1, 0, 0]), np.array([0.4, 0.5, 0.1]), np.pi/20)
        lightCube1_test = Component(Point((-1, 0.4, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.PURPLE))
        lightCube1_test.renderingRouting = "vertex"

        cube2 = Component(Point((obj_d, 0, -3)), DisplayableCube(shaderProg, 1, 1.2, 1.5, ColorType.PINK))
        cube2.setMaterial(m1)
        cube2.renderingRouting = "lighting"
        self.addChild(cube2)
        # (3, 0.4, -3), green, not_infinite, spot_direction=(1,-1,0), 0.1d^2+0.2d+0.1, pi/6
        l2 = Light(Point((light_d, 0.4, -3)), np.array((*ColorType.GREEN, 1.0)))
        lightCube2 = Component(Point((light_d, 0.4, -3)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.GREEN))
        lightCube2.renderingRouting = "vertex"
        
        
        # (3, 0.4, +3), blue, not_infinite, spot_direction=(1, -1,0), 0.1d^2+0.2d+0.1, pi/6
        cylinder3 = Component(Point((obj_d, 0, 3)), DisplayableCylinder(shaderProg, 0.8, 1, 30, 30))
        cylinder3.setMaterial(m1)
        cylinder3.renderingRouting = "lighting"
        self.addChild(cylinder3)
        l3 = Light(Point((light_d, 0.4, 3)), np.array((*ColorType.BLUE, 1.0)))
        lightCube3 = Component(Point((light_d, 0.4, 3)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.BLUE))
        lightCube3.renderingRouting = "vertex"



        m2 = Material(np.array((1, 1, 1, 1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.2, 0.2, 0.8, 1.0)), 64)
        sphere_sun = Component(Point((0, 25, 0)), DisplayableSphere(shaderProg, 5, ColorType.YELLOW))
        # (0,0.4,0), yellow, infinite, inf_direction=(100, 500, 0)
        l4 = Light(Point((light_d, 0.4, 3)), np.array((*ColorType.YELLOW, 1.0)) * 3, np.array([0, 500, 0]))

        sphere_center = Component(Point((0, 0, 0)), DisplayableSphere(shaderProg, 0.1, ColorType.BLACK))
        sphere_sun.setMaterial(m2)
        sphere_sun.renderingRouting = "vertex"
        sphere_center.setMaterial(m2)
        sphere_center.renderingRouting = "vertex"
        self.addChild(sphere_sun)
        self.addChild(sphere_center)



        self.addChild(lightCube1)
        self.addChild(lightCube2)
        self.addChild(lightCube3)
        self.addChild(lightCube1_test)
        self.lights = [l1, l2, l3, l4, l1_test]
        self.lightCubes = [lightCube1, lightCube2, lightCube3, lightCube1_test]

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
