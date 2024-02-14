"""
Define Torus here.
First version in 11/01/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
from Point import Point
import numpy as np
import ColorType
import math
try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

##### TODO 6/BONUS 6: Texture Mapping
# Requirements:
#   1. Set up each object's vertex texture coordinates(2D) to the self.vertices 9:11 columns
#   (i.e. the last two columns). Tell OpenGL how to interpret these two columns:
#   you need to set up attribPointer in the Displayable object's initialize method.
#   2. Generate texture coordinates for the torus and sphere. Use “./assets/marble.jpg” for the torus and
#   “./assets/earth.jpg” for the sphere as the texture image.
#   There should be no seams in the resulting texture-mapped model.

# DisplayableTorus(innerRadius, outerRadius, nsides, rings)
class DisplayableTorus(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    nsides = 0
    rings = 0
    innerRadius = 0
    outerRadius = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE):
        super(DisplayableTorus, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.nsides = nsides
        self.rings = rings
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.color = color

        self.generate()

    def generate(self):
        r = self.innerRadius
        R = self.outerRadius
        stacks = self.rings
        slices = self.nsides

        v_arr = []
        e_arr = []

        # mesh
        for theta in np.linspace(-np.pi, np.pi, stacks):
            for phi in np.linspace(-np.pi, np.pi, slices):
                x = (R + r*np.cos(phi)) * np.cos(theta)
                y = (R + r*np.cos(phi)) * np.sin(theta)
                z = r * np.sin(phi)
                # nx = -r*np.sin(phi)*np.sin(theta) - r*(R + r*np.cos(phi))*np.cos(theta)*np.cos(theta)
                # ny = -r*np.sin(phi)*np.cos(theta) + r*(R + r*np.cos(phi))*np.sin(theta)*np.cos(theta)
                # nz = -r*(R + r*np.cos(phi))*np.sin(phi)*np.cos(theta)*np.cos(theta) + r*(R + r*np.cos(phi))*np.sin(phi)*np.cos(theta)*np.cos(theta)
                nx = 2*(np.sqrt(x**2+y**2) - R) * x / np.sqrt(x**2+y**2)
                ny = 2*(np.sqrt(x**2+y**2) - R) * y / np.sqrt(x**2+y**2)
                nz = 2*z
                normal = np.array([nx, ny, nz])
                normal = normal / np.linalg.norm(normal)
                nx, ny, nz = normal
                u = (theta + np.pi)/(2*np.pi)
                v = (phi + np.pi/2)/np.pi
                P_u_x = -(R + r*np.cos(phi)) * np.sin(theta)
                P_u_y = (R + r*np.cos(phi)) * np.cos(theta)
                P_u_z = 1
                P_v_x = -r*np.sin(phi) * np.cos(theta)
                P_v_y = -r*np.sin(phi) * np.sin(theta)
                P_v_z = r*np.cos(phi)
                v_arr.append([x, y, z, nx, ny, nz, self.color.r, self.color.g, self.color.b, u, v, P_u_x, P_u_y, P_u_z, P_v_x, P_v_y, P_v_z])

        # ebo
        e_arr = []
        for stack in range(stacks):
            for slice in range(slices):
                next_stack = (stack + 1) % stacks
                next_slice = (slice + 1) % slices
                # e_arr.append([*v_arr[stack][slice], *np.random.rand(3), 0, 0])
                # e_arr.append([*v_arr[next_stack][slice], *np.random.rand(3), 0, 0])
                # e_arr.append([*v_arr[stack][next_slice], *np.random.rand(3), 0, 0])

                # e_arr.append([*v_arr[stack][next_slice], *np.random.rand(3), 0, 0])
                # e_arr.append([*v_arr[next_stack][slice], *np.random.rand(3), 0, 0])
                # e_arr.append([*v_arr[next_stack][next_slice], *np.random.rand(3), 0, 0])
                e_arr.append(stack * slices + slice)
                e_arr.append(next_stack * slices + slice)
                e_arr.append(stack * slices + next_slice)
                e_arr.append(stack * slices + next_slice)
                e_arr.append(next_stack * slices + slice)
                e_arr.append(next_stack * slices + next_slice)


        self.vertices = np.array(v_arr)
        self.indices = np.array(e_arr)

    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems which don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 17)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=17, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=17, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=17, offset=6, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"),
                                  stride=17, offset=9, attribSize=2)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexT"),
                                  stride=17, offset=11, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexB"),
                                  stride=17, offset=14, attribSize=3)
        self.vao.unbind()
