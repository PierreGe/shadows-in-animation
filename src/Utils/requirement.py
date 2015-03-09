__author__ = 'pierre'

NEEDED_REQUIREMENTS = ["PyQt4", "OpenGL", "simpleparse", "numpy", "pygame", "PyQt4", "OpenGL.GLUT", "vispy",
                       "psutil"]


def check():
    for req in NEEDED_REQUIREMENTS:
        statement = "import " + req
        try:
            exec statement
        except:
            print("FATAL : no module named '" + req + "' installed!")
            exit(1)

