
#############################################################################################################
##################################     LIBRARY SETUP OPENGL     ############################
#############################################################################################################

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import sys
import thread
import threading
import Queue
import time
import copy
import math

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-width/2, width/2, -height/2, height/2, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw_rect(x, y, width, height):
    glBegin(GL_POLYGON)                                 
    glVertex2f(x, y)                                   
    glVertex2f(x + width, y)                           
    glVertex2f(x + width, y + height)                  
    glVertex2f(x, y + height)                          
    glEnd()                                            
    
def drawhorizon(width,y):
    glBegin(GL_LINES)                                 
    glVertex2f(width/2, y)                                  
    glVertex2f(-width/2, y)                           
    glEnd()

def drawvertical(height,x):
    glBegin(GL_LINES)                                 
    glVertex2f(x,height/2)                                  
    glVertex2f(x,-height/2)                           
    glEnd()

def drawpoly(listnya):
    skala = 0.5
    glBegin(GL_POLYGON)                                  
    for i in listnya:
        a = i[0]*skala
        b = i[1]*skala
        glVertex2f(a, b)                                   
    glEnd()                                            
