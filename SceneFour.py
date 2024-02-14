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
from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableSphere import DisplayableSphere
from DisplayableTorus import DisplayableTorus

# TODO 4 - my second scene
class SceneFour(Component, Animation):
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
        self.R = [0.7, 0.7]
        self.S = [0.02, 0.02]
        self.A = [0, np.pi]
        self.a = [0, 0.5*np.pi, np.pi]
        self.r = [2, 3, 4]
        self.s = [0.01, 0.007, 0.005]

        sun1 = Component(Point((1, 0, 0)), DisplayableSphere(shaderProg, 0.5, ColorType.DARKORANGE1))
        sun2 = Component(Point((-1, 0, 0)), DisplayableSphere(shaderProg, 0.5, ColorType.SOFTRED))
        l1 = Light(Point((1, 0, 0)), np.array([*ColorType.YELLOW, 0.5]) * 2)
        l2 = Light(Point((-1, 0, 0)), np.array([*ColorType.RED, 0.5]) * 2)
        planet1 = Component(Point((3, 0, 0)), DisplayableSphere(shaderProg, 0.3, ColorType.GRAY))
        planet2 = Component(Point((4, 0, 0)), DisplayableEllipsoid(shaderProg, 0.4, 0.3, 0.4))
        planet3 = Component(Point((5, 0, 0)), DisplayableSphere(shaderProg, 0.2, ColorType.NAVY))
        ring = Component(Point((0,0,0)), DisplayableTorus(shaderProg, 0.1, 5))

        flashlight = Component(Point((4.9, 0, 0)), DisplayableCube(shaderProg, 0.2, 0.2, 0.2, ColorType.BLUE))
        l3 = Light(Point((4.9, 0, 0)), np.array([*ColorType.BLUE, 0.5]) * 5, None, np.array([-1, 0, 0]), np.array([0.1, 0.2, 0.1]), np.pi/5)

        l_galaxy = Light(Point((0, 0, 10)), np.array((*ColorType.SILVER, 1.0)) * 3, np.array([0, 0, 100]))

        self.lights = [l1, l2, l3, l_galaxy]
        self.suns = [sun1, sun2]
        self.planets = [planet1, planet2, planet3]


        
        m2 = Material(np.array((0.2, 0.2, 0.2, 0.2)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.5, 0.5, 0.5, 1.0)), 10)
        for sun in self.suns:
            sun.renderingRouting = "vertex"
            sun.setMaterial(m2)
            self.addChild(sun)

        for planet in self.planets:
            planet.renderingRouting = "lighting"
            planet.setMaterial(m2)
            self.addChild(planet)
        
        planet1.renderingRouting = "texture, lighting"
        planet1.setTexture(shaderProg, "assets/stonewall.jpg")
        planet2.renderingRouting = "texture, lighting"
        planet2.setTexture(shaderProg, "assets/cloudySphere.jpg")
        planet3.renderingRouting = "texture, lighting"
        planet3.setTexture(shaderProg, "assets/earth.jpg")

        self.addChild(ring)
        ring.setMaterial(m2)
        self.addChild(flashlight)
        flashlight.setMaterial(m2)
        

    def animationUpdate(self):
        for i, v in enumerate(self.lights[0:2]):
            theta = (self.A[i] + self.S[i]) % (2*np.pi)
            self.A[i] = theta
            x = self.R[i] * np.cos(theta)
            y = self.R[i] * np.sin(theta)
            self.suns[i].setCurrentPosition(Point((x, y, 0)))
            self.lights[i].setPosition(Point((x, y, 0)))
            self.shaderProg.setLight(i, v)

        for i in range(len(self.planets)):
            theta = (self.a[i] + self.s[i]) % (2*np.pi)
            self.a[i] = theta
            x = self.r[i] * np.cos(theta)
            y = self.r[i] * np.sin(theta)
            self.planets[i].setCurrentPosition(Point((x, y, 0)))
            

        for c in self.children:
            if isinstance(c, Animation):
                c.animationUpdate()

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
