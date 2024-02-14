"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType

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

# DisplayableEllipsoid(radiusInX, radiusInY, radiusInZ, slices, stacks)
class DisplayableEllipsoid(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current ellipsoid's information, read-only
    radiusInX = None
    radiusInY = None
    radiusInZ = None

    def __init__(self, shaderProg, radiusInX=0.6, radiusInY=0.8, radiusInZ=1, slices=30, stacks=30):
        super(DisplayableEllipsoid, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.radiusInX = radiusInX
        self.radiusInY = radiusInY
        self.radiusInZ = radiusInZ

        self.color = ColorType.PINK

        self.generate(slices, stacks)

    def generate(self, slices, stacks):
        a = self.radiusInX
        b = self.radiusInY
        c = self.radiusInZ
        v_arr = []
        for phi in np.linspace(-np.pi/2, np.pi/2, stacks):
            row = []
            for theta in np.linspace(-np.pi, np.pi, slices): 
                x = a * np.cos(phi) * np.cos(theta)
                y = b * np.cos(phi) * np.sin(theta)
                z = c * np.sin(phi)
                # nx = -b*np.sin(phi)*np.sin(theta) - b*c*np.cos(phi)*np.cos(theta)*np.cos(theta)
                # ny = a*np.sin(phi)*np.cos(theta) - a*c*np.cos(phi)*np.sin(theta)*np.cos(theta)
                # nz = -a*b*np.sin(phi)*np.cos(phi)*np.cos(theta)*np.cos(theta) - a*b*np.sin(phi)*np.cos(phi)*np.sin(theta)*np.sin(theta)
                nx = 1/a**2 * 2*x
                ny = 1/b**2 * 2*y
                nz = 1/c**2 * 2*z
                normal = np.array([nx, ny, nz])
                normal = normal / np.linalg.norm(normal)
                nx, ny, nz = normal
                v = (phi + np.pi/2)/np.pi
                u = (theta+ np.pi)/(2*np.pi)
                row.append([x, y, z, nx, ny, nz, self.color.r, self.color.g, self.color.b, u, v])
            v_arr.append(row)
    
        e_arr = []
        for stack in range(stacks - 1):
            for slice in range(slices):
                next_stack = stack + 1
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
        in systems that don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=11, offset=6, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"),
                                  stride=11, offset=9, attribSize=2)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

