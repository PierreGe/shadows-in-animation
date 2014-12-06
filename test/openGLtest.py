from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

angle = 0
shadowMapSize = 512

def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(600, 600); #//Window size
    glutCreateWindow("Introduction to OpenGL"); #//Create a window
    glClearDepth(1.0);
    glDepthFunc(GL_LEQUAL);
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE);
    glEnable(GL_COLOR_MATERIAL); #//Enables color
    glEnable(GL_LIGHTING); #//Enable lighting
    glEnable(GL_LIGHT0); #//Enable light #0
    glEnable(GL_LIGHT1); #//Enable light #1
    glEnable(GL_NORMALIZE); #//Automatically normalize normals
    glShadeModel(GL_SMOOTH); #//Enable smooth shading

    glClearColor(0.0, 0.0, 0.0, 1.0); #//Sets clear color

def handleResize(width, heigth):
    #//Tell OpenGL how to convert from coordinates to pixel values
    glViewport(0, 0, width, heigth);
    glMatrixMode(GL_PROJECTION); #//Switch to setting the camera perspective
    #//Set the camera perspective
    glLoadIdentity(); #//Reset the camera
    #45 the camera angle, w/h the width-to-height ratio, 
    #1 the near z clipping coordinate, 200 the far z clipping coordinate
    gluPerspective(60.0, width /heigth, 1.0, 200.0);

def update(value):
    #//Makes motion continuous
    global angle
    angle += 1;
    if (angle > 360):
        angle = 0;
     
    glutPostRedisplay(); #//Redraw scene
    
    glutTimerFunc(5, update, 0); #//Call update in 5 milliseconds

#//Called when a key is pressed
def handleKeypress(key, x, y):    #//key, the key pressed and y,x The current mouse coordinates
    if key==27 : exit()  #27==escape key
    elif key==GLUT_KEY_RIGHT : update(0)

def drawScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    gluLookAt(3,5,0,0,0,-8,0,5,0)

    glTranslatef(0.0, 0.0, -8.0);

    #//Add ambient light
    #GLfloat ambientColor[] = {0.2f, 0.2f, 0.2f, 1.0f}; //Color (0.2, 0.2, 0.2)
    #glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1.0));

    #//Add positioned light
    #lightColor0 = {0.5, 0.5, 0.5, 1.0}; #//Color (0.5, 0.5, 0.5)
    #lightPos0 = {4.0, 0.0, 8.0, 1.0}; #//Positioned at (4, 0, 8)
    #glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0));
    #glLightfv(GL_LIGHT0, GL_POSITION, (4.0, 0.0, 8.0, 1.0));

    #//Add directed light
    #lightColor1 = {0.5, 0.2, 0.2, 1.0}; #//Color (0.5, 0.2, 0.2)
    #//Coming from the direction (-1, 0.5, 0.5)
    #lightPos1 = {-1.0, 0.5, 0.5, 0.0};
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1.0));
    glLightfv(GL_LIGHT1, GL_POSITION, (-1.0, 0.5, 0.5, 0.0));

    glColor3f(1,1,1)

    glBegin(GL_TRIANGLES);
    glVertex3f(-20,0,-20)
    glVertex3f(20,0,-20)
    glVertex3f(-20,0,20)
    #glVertex3f(20,0,20)
    
    glVertex3f(20,0,-20)
    glVertex3f(-20,0,20)
    glVertex3f(20,0,20)

    glEnd();

    glRotatef(angle/2, 0.0, 1.0, 0.0);
    glColor3f(1.0, 1.0, 0.0);
    glBegin(GL_QUADS);

    #//Front
    glNormal3f(0.0, 0.0, 1.0);
    glNormal3f(-1.0, 0.0, 1.0);
    glVertex3f(-1.5, -1.0, 1.5);
    glNormal3f(1.0, 0.0, 1.0);
    glVertex3f(1.5, -1.0, 1.5);
    glNormal3f(1.0, 0.0, 1.0);
    glVertex3f(1.5, 1.0, 1.5);
    glNormal3f(-1.0, 0.0, 1.0);
    glVertex3f(-1.5, 1.0, 1.5);
    
    #//Right
    glNormal3f(1.0, 0.0, 0.0);
    glNormal3f(1.0, 0.0, -1.0);
    glVertex3f(1.5, -1.0, -1.5);
    glNormal3f(1.0, 0.0, -1.0);
    glVertex3f(1.5, 1.0, -1.5);
    glNormal3f(1.0, 0.0, 1.0);
    glVertex3f(1.5, 1.0, 1.5);
    glNormal3f(1.0, 0.0, 1.0);
    glVertex3f(1.5, -1.0, 1.5);
    
    #//Back
    glNormal3f(0.0, 0.0, -1.0);
    glNormal3f(-1.0, 0.0, -1.0);
    glVertex3f(-1.5, -1.0, -1.5);
    glNormal3f(-1.0, 0.0, -1.0);
    glVertex3f(-1.5, 1.0, -1.5);
    glNormal3f(1.0, 0.0, -1.0);
    glVertex3f(1.5, 1.0, -1.5);
    glNormal3f(1.0, 0.0, -1.0);
    glVertex3f(1.5, -1.0, -1.5);

    #glColor3f(0.0, 1.0, 1.0);
    
    #//Left
    glNormal3f(-1.0, 0.0, 0.0);
    glNormal3f(-1.0, 0.0, -1.0);
    glVertex3f(-1.5, -1.0, -1.5);
    glNormal3f(-1.0, 0.0, 1.0);
    glVertex3f(-1.5, -1.0, 1.5);
    glNormal3f(-1.0, 0.0, 1.0);
    glVertex3f(-1.5, 1.0, 1.5);
    glNormal3f(-1.0, 0.0, -1.0);
    glVertex3f(-1.5, 1.0, -1.5);

    glEnd()
    glBegin(GL_TRIANGLES)

    glVertex3f(-1.5,1,-1.5)
    glVertex3f(1.5,1,-1.5)
    glVertex3f(-1.5,1,1.5)

    glVertex3f(1.5,1,-1.5)
    glVertex3f(-1.5,1,1.5)
    glVertex3f(1.5,1,1.5) 
    
    glEnd();
    
    glutSwapBuffers();

def test1():
    init(); #//Initialize rendering
    #//Set functions for glutMainLoop to call
    glutDisplayFunc(drawScene)
    #glutKeyboardFunc(handleKeypress);
    glutReshapeFunc(handleResize)
    #glutTimerFunc(5, update, 0); #//Call update 5 milliseconds after program 
    update(0)
    glutMainLoop(); #//Start the main loop. glutMainLoop doesn't return.

if __name__ == "__main__":
    test1()