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

import transform
import setup_opengl
import interface

######################################      SETTING OPENGL      #############################################

window = 0                                           
width, height = 600,600     #ukuran jendela openGL                            

def draw():                                            
    scale = 25
    glColor3f(0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
    glLoadIdentity()                                   
    setup_opengl.refresh2d(width, height)

    glColor3f(0.498039, 1, 0)
    glColor3f(1, 1, 1)
    
    glLineWidth(4)
    setup_opengl.drawvertical(height,0)
    setup_opengl.drawhorizon(width,0)
    glLineWidth(1)
    
    if status=='exit':      # exit openGL
        sys.exit()
    
    glColor3f(0.5, 1, 0)
    setup_opengl.drawpoly(temptitik)     # menggambar titik-titik pada bidang
    glutSwapBuffers()                                  

######################################      SETTING MULTITHREADING OPENGL      ######################################

class windowOpenGl(threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   
   def run(self):   
      glutInit()                                            
      glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
      glutInitWindowSize(width, height)                     
      glutInitWindowPosition(0, 0)                          
      window = glutCreateWindow("Simulasi Tranformasi Linear")              
      glutDisplayFunc(draw)                                  
      glutIdleFunc(draw)                                     
      glutMainLoop()                                              

##################################      KONSTANTA DAN VARIABEL GLOBAL      ##################################

kumpulantitik = []      # list of titik dari inputan user
temptitik = []          # salinan dari kumpulan titik 
status = 'nothing'

##################################      PROCEDURE MENU PENGGUNA      ########################################

def prosesInput(masukan1,temptitik):
    masukan = masukan1.split()
    if masukan[0]=='translate':
        transform.translate2D(temptitik,float(masukan[1]),float(masukan[2]))
    elif masukan[0]=='dilate':
        transform.dilate2D(temptitik,float(masukan[1]))
    elif masukan[0]=='rotate':
        transform.rotate2D(temptitik,float(masukan[1]),float(masukan[2]),float(masukan[3]))    
    elif masukan[0]=='reflect':
        transform.reflect2D(temptitik,masukan[1])
    elif masukan[0]=='shear':
        transform.shear2D(temptitik,masukan[1],float(masukan[2]))
    elif masukan[0]=='stretch':
        transform.stretch2D(temptitik,masukan[1],float(masukan[2]))
    elif masukan[0]=='custom':
        transform.custom2D(temptitik,float(masukan[1]),float(masukan[2]),float(masukan[3]),float(masukan[4]))
    elif masukan[0]=='reset':
        transform.reset2D(temptitik,kumpulantitik)
    else:
        print('Perintah tidak tersedia')

##################################     PROGRAM UTAMA     #############################################

interface.opening()

n = input('Berapa banyak titik : ')
print('')
print('Input titik dengan format <x,y>')

# simpan titik di kumpulantitik
for i in range(1,n+1):
    titik = raw_input().split(",")
    kumpulantitik.append([])
    kumpulantitik[i-1].append(float(titik[0]))
    kumpulantitik[i-1].append(float(titik[1]))

# salin kumpulantitik ke temptitik
for i in range(0,len(kumpulantitik)):
    temptitik.append([])
    for j in range (0,len(kumpulantitik[0])):
        temptitik[i].append(1-1+kumpulantitik[i][j])

# pemanggilan multithreading
thread1 = windowOpenGl(1, "Thread-1", 1)
thread1.daemon = True
thread1.start()

interface.menu()

# terima perintah user
print('Masukkan perintah : ')

inp = raw_input()
while(inp!='exit'):
    masukan = inp.split()
    if masukan[0]=='status':
        print(temptitik)
    elif masukan[0]!='multiple':
        prosesInput(inp,temptitik)
    elif masukan[0]=='multiple':
        listperintah=[]
        i = 0
        while (i < int(masukan[1])) :
            inp2 = raw_input()
            inp3 = inp2.split()
            if (inp3[0]=='multiple' or inp3[0]=='reset' or inp3[0]=='exit'):
                print('multiple tidak boleh mengandung perintah multiple, reset, atau exit')
            else :
                listperintah.append(inp2)
                i = i+1
            
        for imp in listperintah:
            prosesInput(imp,temptitik)
    else :
        print('Perintah tidak tersedia')
    inp = raw_input()

if (inp == 'exit') :
    print('Program simulasi transformasi linear telah selesai')
    status = 'exit'

##################################     FINISH     #############################################
