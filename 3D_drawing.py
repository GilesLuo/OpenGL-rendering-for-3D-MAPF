from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

IS_PERSPECTIVE = True  
VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  
SCALE_K = np.array([1.0, 1.0, 1.0])  
EYE = np.array([0.0, 0.0, 2.0])  
LOOK_AT = np.array([0.0, 0.0, 0.0]) 
EYE_UP = np.array([0.0, 1.0, 0.0])  
WIN_W, WIN_H = 640, 480  
LEFT_IS_DOWNED = False  
MOUSE_X, MOUSE_Y = 0, 0  


def getposture():
    global EYE, LOOK_AT

    dist = np.sqrt(np.power((EYE - LOOK_AT), 2).sum())
    if dist > 0:
        phi = np.arcsin((EYE[1] - LOOK_AT[1]) / dist)
        theta = np.arcsin((EYE[0] - LOOK_AT[0]) / (dist * np.cos(phi)))
    else:
        phi = 0.0
        theta = 0.0

    return dist, phi, theta


DIST, PHI, THETA = getposture() 


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0) 
    glEnable(GL_DEPTH_TEST)  
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glDepthFunc(GL_LEQUAL)  


def draw():
    global IS_PERSPECTIVE, VIEW
    global EYE, LOOK_AT, EYE_UP
    global SCALE_K
    global WIN_W, WIN_H

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if WIN_W > WIN_H:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
    else:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glScale(SCALE_K[0], SCALE_K[1], SCALE_K[2])

    gluLookAt(
        EYE[0], EYE[1], EYE[2],
        LOOK_AT[0], LOOK_AT[1], LOOK_AT[2],
        EYE_UP[0], EYE_UP[1], EYE_UP[2]
    )

    glViewport(0, 0, WIN_W, WIN_H)

    # ---------------------draw boundary-----------------------------

    draw_cube(0, 0, 0, size=1, color=[1, 0, 0, 1], mode="WIRED")
    Obstacles, agents = scan_world(world, mode="WORLD")
    goals_position = scan_world(goals, mode="GOAL")
    create_obstacles(Obstacles, size=world.shape[0])
    create_agents_and_goals(agents, size=world.shape[0], mode="AGENT")
    create_agents_and_goals(goals_position, size=world.shape[0], mode="GOAL")
    # ---------------------------------------------------------------

    glutSwapBuffers()  


def create_obstacles(Obstacles, size):
    for num in range(0, len(Obstacles)):
        x = Obstacles[num][0]
        y = Obstacles[num][1]
        z = Obstacles[num][2]
        draw_cube(x, y, z, size=size, color=[176 / 256, 192 / 256, 222 / 256, 1], mode="SOLID")
        draw_cube(x, y, z, size, [0, 0, 0, 1], mode="WIRED")
        # obstacles color is grey


def create_agents_and_goals(agents, size, mode="AGENT"):
    for num in range(0, len(agents)):
        if num > 9:
            num_color = num % 10
        else:
            num_color = num
        x = agents[num][0]
        y = agents[num][1]
        z = agents[num][2]

        color_set = [[1 * i / 256, 10 * i+10 / 256, 1 * i / 256] for i in range(0, 9)]
        color_r = color_set[num_color][0]
        color_g = color_set[num_color][1]
        color_b = color_set[num_color][2]

        draw_cube(x, y, z, size=size, color=[color_r, color_g, color_b, 1], mode="SOLID")
        if mode is "GOAL":
            draw_cube(x, y, z, size, [1, 1, 0, 1], mode="WIRED")
        # obstacles color is grey


def scan_world(world, mode="WORLD"):
    if mode is "WORLD":
        Obstacles = []
        agents = []
        for i in range(0, world.shape[0]):
            for j in range(0, world.shape[1]):
                for k in range(0, world.shape[2]):
                    if world[i, j, k] == -1:
                        Obstacles.append([i, j, k])
                    elif world[i, j, k] > 0:
                        agents.append([i, j, k])

        return Obstacles, agents

    elif mode is "GOAL":
        goals = []
        for i in range(0, world.shape[0]):
            for j in range(0, world.shape[1]):
                for k in range(0, world.shape[2]):
                    if world[i, j, k] > 0:
                        goals.append([i, j, k])

        return goals


def draw_cube(x, y, z, size=1, color=None, mode="SOLID"):
    if color is None:
        color = [1, 1, 1, 1]
    x_ = -1 + 2 / size * (x + 0.5)
    y_ = -1 + 2 / size * (y + 0.5)
    z_ = -1 + 2 / size * (z + 0.5)
    if mode is "SOLID":
        glColor4f(color[0], color[1], color[2], color[3])
        glPushMatrix()
        glTranslatef(x_, y_, z_)
        glutSolidCube(2 / size)
        glPopMatrix()
    elif mode is "WIRED":
        glColor4f(color[0], color[1], color[2], color[3])
        glPushMatrix()
        glTranslatef(x_, y_, z_)
        glutWireCube(2 / size)
        glPopMatrix()
    else:
        print("Mode input error")
        sys.exit(1)


def reshape(width, height):
    global WIN_W, WIN_H

    WIN_W, WIN_H = width, height
    glutPostRedisplay()


def mouseclick(button, state, x, y):
    global SCALE_K
    global LEFT_IS_DOWNED
    global MOUSE_X, MOUSE_Y

    MOUSE_X, MOUSE_Y = x, y
    if button == GLUT_LEFT_BUTTON:
        LEFT_IS_DOWNED = state == GLUT_DOWN
    elif button == 3:
        SCALE_K *= 1.05
        glutPostRedisplay()
    elif button == 4:
        SCALE_K *= 0.95
        glutPostRedisplay()


def mousemotion(x, y):
    global LEFT_IS_DOWNED
    global EYE, EYE_UP
    global MOUSE_X, MOUSE_Y
    global DIST, PHI, THETA
    global WIN_W, WIN_H

    if LEFT_IS_DOWNED:
        dx = MOUSE_X - x
        dy = y - MOUSE_Y
        MOUSE_X, MOUSE_Y = x, y

        PHI += 2 * np.pi * dy / WIN_H
        PHI %= 2 * np.pi
        THETA += 2 * np.pi * dx / WIN_W
        THETA %= 2 * np.pi
        r = DIST * np.cos(PHI)

        EYE[1] = DIST * np.sin(PHI)
        EYE[0] = r * np.sin(THETA)
        EYE[2] = r * np.cos(THETA)

        if 0.5 * np.pi < PHI < 1.5 * np.pi:
            EYE_UP[1] = -1.0
        else:
            EYE_UP[1] = 1.0

        glutPostRedisplay()


def keydown(key, x, y):
    global DIST, PHI, THETA
    global EYE, LOOK_AT, EYE_UP
    global IS_PERSPECTIVE, VIEW

    if key in [b'x', b'X', b'y', b'Y', b'z', b'Z']:
        if key == b'x':  
            LOOK_AT[0] -= 0.01
        elif key == b'X':  
            LOOK_AT[0] += 0.01
        elif key == b'y':  
            LOOK_AT[1] -= 0.01
        elif key == b'Y':  
            LOOK_AT[1] += 0.01
        elif key == b'z':  
            LOOK_AT[2] -= 0.01
        elif key == b'Z':  
            LOOK_AT[2] += 0.01

        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\r':  
        EYE = LOOK_AT + (EYE - LOOK_AT) * 0.9
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\x08':  
        EYE = LOOK_AT + (EYE - LOOK_AT) * 1.1
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b' ':  
        IS_PERSPECTIVE = not IS_PERSPECTIVE
        glutPostRedisplay()


if __name__ == "__main__":
    world = np.array([[[-1, -1, -1, 0, 0],
                       [0, 0, 0, 0, 0],
                       [1, 0, 0, 0, 0]],
                      [[-1, -1, -1, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]],
                      [[-1, -1, -1, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]],
                      [[0, -1, -1, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]],
                      [[0, 0, 2, 0, 0],
                       [-1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]]])

    goals = np.array([[[0, 0, 0, 0, 1],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]],
                      [[2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]]])

    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)

    glutInitWindowSize(WIN_W, WIN_H)
    glutInitWindowPosition(300, 200)
    glutCreateWindow('Quidam Of OpenGL')

    init()  # 初始化画布
    glutDisplayFunc(draw)  
    glutReshapeFunc(reshape)  
    glutMouseFunc(mouseclick)  
    glutMotionFunc(mousemotion)  
    glutKeyboardFunc(keydown)  

    glutMainLoop()  
