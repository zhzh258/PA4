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

# DisplayableCylinder(endRadius, height, slices, stacks)
class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cylinder's information, read-only
    endRadius = None
    height = None
    slices = None
    stacks = None

    def __init__(self, shaderProg, endRadius=0.5, height=1, slices=30, stacks=30):
        super(DisplayableCylinder, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.endRadius = endRadius
        self.height = height
        self.generate(slices, stacks)

    def generate(self, slices, stacks):
        r = self.endRadius
        h = self.height

        v_arr = []
        e_arr = []

        # vertices (mesh)
        for phi in np.linspace(-h/2, h/2, stacks):
            for theta in np.linspace(-np.pi, np.pi, slices):
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                z = phi
                nx = np.cos(theta)
                ny = np.sin(theta)
                nz = 0
                v = (phi + np.pi/2)/np.pi
                u = (theta+ np.pi)/(2*np.pi)
                v_arr.append([x, y, z, nx, ny, nz, *ColorType.PINK, u, v])
        # vertices (top circle center & bottom circle center)
        # v_arr[-2]: top
        # v_arr[-1]: bottom
        for phi in np.linspace(-h/2, h/2, 2):
            for theta in np.linspace(-np.pi, np.pi , slices):
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                z = phi
                nx = 0
                ny = 0
                nz = np.sign(phi)
                v_arr.append([x, y, z, nx, ny, nz, *ColorType.PINK, 0, 0])
        v_arr.append([0, 0, -h/2, 0, 0, -1, *ColorType.PINK, 0, 0])
        v_arr.append([0, 0, h/2, 0, 0, 1, *ColorType.PINK, 0, 0])

        # bottom circle
        for slice in range(slices):
            # e_arr.append([*v_arr[stacks][slice], *np.random.rand(3), 0, 0])
            # e_arr.append([*v_arr[stacks][next_slice], *np.random.rand(3), 0, 0])
            # e_arr.append([*v_arr[-2], *np.random.rand(3), 0, 0])
            next_slice = (slice + 1) % slices
            e_arr.append(stacks*slices + slice)
            e_arr.append(stacks*slices + next_slice)
            e_arr.append(len(v_arr) - 2)

        # top circle
        for slice in range(slices):
            # e_arr.append([*v_arr[stacks + 1][slice], *np.random.rand(3), 0, 0])
            # e_arr.append([*v_arr[stacks + 1][next_slice], *np.random.rand(3), 0, 0])
            # e_arr.append([*v_arr[-1], *np.random.rand(3), 0, 0])
            next_slice = (slice + 1) % slices
            e_arr.append((stacks + 1)*slices + slice)
            e_arr.append((stacks + 1)*slices + next_slice)
            e_arr.append(len(v_arr) - 1)

        # side rectangle
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

