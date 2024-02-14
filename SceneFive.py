"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
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
from DisplayableTorus import DisplayableTorus
from DisplayableSphere import DisplayableSphere
from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableCylinder import DisplayableCylinder

## TODO 4 - my third scene
class SceneFive(Component):
    shaderProg = None
    glutility = None

    lights = None
    lightCubes = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        m2 = Material(np.array((0.2, 0.2, 0.2, 0.2)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.5, 0.5, 0.5, 1.0)), 64)

        cube = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 1.0))
        m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.4, 0.4, 0.4, 0.1)), 64)
        cube.renderingRouting = "lighting"
        cube.setMaterial(m2)
        # self.addChild(cube)

        sphere = Component(Point((0, 3, 0)), DisplayableSphere(shaderProg, 1.0,  color=ColorType.ORANGE))
        sphere.renderingRouting = "lighting"
        sphere.setMaterial(m2)
        self.addChild(sphere)

        torus = Component(Point((-3, 0, 0)), DisplayableTorus(shaderProg))
        torus.setMaterial(m2)
        torus.renderingRouting = "lighting"
        self.addChild(torus)


        ellipsoid = Component(Point((0, 0, 3)), DisplayableEllipsoid(shaderProg))
        ellipsoid.setMaterial(m2)
        ellipsoid.renderingRouting = "lighting"
        self.addChild(ellipsoid)

        cylinder = Component(Point((3, 0, 0)), DisplayableCylinder(shaderProg))
        cylinder.setMaterial(m2)
        cylinder.renderingRouting = "lighting"
        self.addChild(cylinder)

        l0 = Light(Point([0.0, 1.5, 0.0]),
                   np.array((*ColorType.SOFTRED, 1.0)))
        lightCube0 = Component(Point((0.0, 1.5, 0.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.RED))
        lightCube0.renderingRouting = "vertex"
        
        l1 = Light(Point([2, 3, 0.0]), np.array((*ColorType.SOFTGREEN, 1.0)), None, np.array([-1, 0, 0]), np.array([0.1, 0.1, 0]), np.pi/3)
        lightCube1 = Component(Point((2, 3, 0.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.GREEN))
        lightCube1.renderingRouting = "vertex"
        
        l2 = Light(Point((0,1,0)), np.array((*ColorType.YELLOW, 1.0)) * 3, np.array([0, 10, 0]))

        self.addChild(lightCube0)
        self.addChild(lightCube1)
        self.lights = [l0, l1, l2]
        self.lightCubes = [lightCube0,lightCube1, ]

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
