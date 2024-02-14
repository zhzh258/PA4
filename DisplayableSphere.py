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


class DisplayableSphere(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current sphere's information, read-only
    radius = None
    color = None

    def __init__(self, shaderProg, radius=1, color=ColorType.BLUE):
        super(DisplayableSphere, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.radius = radius
        self.color = color
        self.generate()

    def generate(self, stacks=50, slices=50):
        r = self.radius
        v_arr = []
        for phi in np.linspace(-np.pi/2, np.pi/2, stacks):
            row = []
            for theta in np.linspace(-np.pi, np.pi, slices):
                '''
                    note that a duplicated point (theta=-pi and theta=+pi) is inserted into the list
                    Not quite what we want for TODO 1 (the random color between first triangle and the last triangle are not seamless)
                    But it is necessary for TODO 6
                    imagine vector.front() and vector.back() are close but not the same position. 
                        vector.front() <=> v=0, vector.back() <=> v=1
                    this will leave a blank texture in the thin longitude between vector.front() and veector.back(). 
                    therefore, np.linspace(endpoint=True)
                '''

                x = r * np.cos(phi) * np.cos(theta)
                y = r * np.cos(phi) * np.sin(theta)
                z = r * np.sin(phi)
                # nx = np.cos(phi) * np.cos(theta)
                # ny = np.cos(phi) * np.sin(theta)
                # nz = np.sin(phi)
                nx = 2*x/r**2
                ny = 2*y/r**2
                nz = 2*z/r**2
                normal = np.array([nx, ny, nz])
                normal = normal / np.linalg.norm(normal)
                nx, ny, nz = normal
                u = (theta+ np.pi)/(2*np.pi)
                v = (phi + np.pi/2)/np.pi
                P_u_x = -r * np.cos(phi) * np.sin(theta)
                P_u_y = r * np.cos(phi) * np.cos(theta)
                P_u_z = 1
                P_v_x = -r * np.sin(phi) * np.cos(theta)
                P_v_y = -r * np.sin(phi) * np.sin(theta)
                P_v_z = r * np.cos(phi)
                row.append([x, y, z, nx, ny, nz, self.color.r, self.color.g, self.color.b, u, v, P_u_x, P_u_y, P_u_z, P_v_x, P_v_y, P_v_z])
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
        # self.vao.bind()
        # # TODO 1.1 is at here, switch from vbo to ebo
        # self.vbo.draw()
        # self.vao.unbind()
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
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
        
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

