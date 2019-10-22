from math import pi, sin, cos
import numpy as np
import pyglet
from pyglet.gl import *

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True, )
    window = pyglet.window.Window(resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)


@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # gluLookAt(5.0, 5.0, 5.0, 0, 0, 0, 0.0, 1.0, 0.0)
    glLoadIdentity()
    gluPerspective(80., width / float(height), 10., 100.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


def update(dt):
    global rx, ry, rz
    # rx += dt * 1
    ry += dt * 80
    # rz += dt * 30
    rx %= 360
    ry %= 360
    rz %= 360


pyglet.clock.schedule(update)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -20)
    # glRotatef(0, 0, 0, 1)
    # glRotatef(30, 0, 1, 0)
    # glRotatef(0, 1, 0, 0)
    batch.draw()


def setup():
    # One-time GL setup
    glClearColor(1, 1, 1, 1)
    glColor3f(255, 255, 255)
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_CULL_FACE)

    # Uncomment this line for a wireframe view
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
    # but this is not the case on Linux or Mac, so remember to always
    # include it.
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # Define a simple function to create ctypes arrays of floats:
    def vec(*args):
        return (GLfloat * len(args))(*args)

    glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, .5, 1, 0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))
    glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
    glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0, 0.3, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)


class Map(object):
    list = None

    def __init__(self, world, batch, size=1,
                 group=None):
        self.world = world
        self.Obstacles = self.scanObstacles(self.world)

        # self.draw_boundary(self.world)
        self.create_obstacles(self.Obstacles)
        print(self.Obstacles)

    def draw_boundary(self, world, size=1, group=None):
        x = world.shape[0] * size
        y = world.shape[1] * size
        z = world.shape[2] * size
        vertices = []
        vertices.extend([0, 0, 0])
        vertices.extend([x, 0, 0])
        vertices.extend([0, y, 0])
        vertices.extend([0, 0, z])
        vertices.extend([x, y, 0])
        vertices.extend([x, 0, z])
        vertices.extend([0, y, z])
        vertices.extend([x, y, z])

        indices = []
        indices.extend([0, 1])
        indices.extend([0, 2])
        indices.extend([1, 4])
        indices.extend([2, 4])
        indices.extend([0, 3])
        indices.extend([3, 5])
        indices.extend([3, 6])
        indices.extend([5, 7])
        indices.extend([6, 7])
        indices.extend([1, 6])
        indices.extend([4, 7])
        indices.extend([5, 2])

        normals = []
        normals.extend([1, 0, 0])
        normals.extend([1, 0, 0])
        normals.extend([1, 0, 0])
        normals.extend([1, 0, 0])
        normals.extend([0, 0, 0])
        normals.extend([0, 0, 0])
        normals.extend([0, 0, 0])
        normals.extend([0, 0, 0])

        vertex_list = batch.add_indexed(8, GL_LINE,
                                        group,
                                        indices,
                                        ('v3f/static', vertices),
                                        ('n3f/static', normals)
                                        )

    def create_obstacles(self, Obstacles):
        for num in range(0, len(Obstacles)):
            x = Obstacles[num][0]
            y = Obstacles[num][1]
            z = Obstacles[num][2]
            self.add_block(x, y, z)

    def scanObstacles(self, world):
        Obstacles = []
        for i in range(0, world.shape[0]):
            for j in range(0, world.shape[1]):
                for k in range(0, world.shape[2]):
                    if world[i, j, k] == -1:
                        Obstacles.append([i, j, k])
        return Obstacles

    def add_block(self, x, y, z, size=1, color=None, group=None):
        if color is None:
            color = [255, 0, 0]
        vertices = []
        normals = []
        colors = []

        x_ = x + size
        y_ = y + size
        z_ = z + size

        vertices.extend([x, y, z])
        vertices.extend([x_, y, z])
        vertices.extend([x, y_, z])
        vertices.extend([x, y, z_])
        vertices.extend([x_, y_, z])
        vertices.extend([x, y_, z_])
        vertices.extend([x_, y, z_])
        vertices.extend([x_, y_, z_])

        normals.extend([1, 0, 0])
        normals.extend([1, 0, 0])
        normals.extend([1, 0, 0])
        normals.extend([1, 0, 0])
        normals.extend([0, 0, 0])
        normals.extend([0, 0, 0])
        normals.extend([0, 0, 0])
        normals.extend([0, 0, 0])

        # Create a list of triangle indices.
        indices = []

        indices.extend([0, 1, 6])
        indices.extend([0, 6, 3])
        indices.extend([1, 6, 4])
        indices.extend([4, 6, 7])
        indices.extend([4, 7, 2])
        indices.extend([2, 7, 5])
        indices.extend([2, 5, 0])
        indices.extend([0, 5, 3])
        indices.extend([1, 0, 4])
        indices.extend([4, 0, 2])
        indices.extend([3, 6, 7])
        indices.extend([3, 7, 5])

        for i in range(0, 12):
            colors.extend([color])

        vertex_list = batch.add_indexed(8, GL_TRIANGLES,
                                        group,
                                        indices,
                                        ('v3f/static', vertices),
                                        ('n3f/static', normals)
                                        )
        return vertex_list

    def delete(self):
        self.vertex_list.delete()


setup()
batch = pyglet.graphics.Batch()
# world = np.array([[[1, 0, 0],
#                    [0, 0, 0],
#                    [-1, 0, 0]],
#                   [[2, 0, 0],
#                    [0, 0, 0],
#                    [0, 0, -1]],
#                   [[0, 0, 0],
#                    [0, -1, 0],
#                    [-1, 0, 0]]])
world = np.array([[[-1, -1, -1],
                   [0, 0, 0],
                   [0, 0, 0]],
                  [[0, -1, 0],
                   [0, 0, 0],
                   [0, 0, 0]],
                  [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]])
# array order: row/column/depth
torus = Map(world, batch=batch)
rx = ry = rz = 0

pyglet.app.run()
