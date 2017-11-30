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
    for i in range(-height/2,height/2,scale):
        if i!=0 :
            setup_opengl.drawhorizon(width,i)
    for i in range(-width/2,width/2,scale):
        if i!=0 :
            setup_opengl.drawvertical(height,i)
    glColor3f(1, 1, 1)
    
    glLineWidth(4)
    setup_opengl.drawvertical(height,0)
    setup_opengl.drawhorizon(width,0)
    glLineWidth(1)
    
    if status=='exit':      # exit openGL
        sys.exit()
    
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
kAnim = 0.001
tAnim = 0.001
status = 'nothing'

##################################      MENU PENGGUNA      ##################################

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


#Salam Pembuka
print(' _______  __   __  _______  _______  _______    _______  _______  _______  _______  ______        _______  ___      _______  _______  _______ ')
print('|       ||  | |  ||       ||   _   ||       |  |  _    ||       ||       ||   _   ||    _ |      |   _   ||   |    |       ||       ||       |')
print('|_     _||  | |  ||    ___||  |_|  ||  _____|  | |_|   ||    ___||  _____||  |_|  ||   | ||      |  |_|  ||   |    |    ___||    ___||   _   |')
print('  |   |  |  |_|  ||   | __ |       || |_____   |       ||   |___ | |_____ |       ||   |_||_     |       ||   |    |   | __ |   |___ |  | |  |')
print('  |   |  |       ||   ||  ||       ||_____  |  |  _   | |    ___||_____  ||       ||    __  |    |       ||   |___ |   ||  ||    ___||  |_|  |')
print('  |   |  |       ||   |_| ||   _   | _____| |  | |_|   ||   |___  _____| ||   _   ||   |  | |    |   _   ||       ||   |_| ||   |___ |       |')
print('  |___|  |_______||_______||__| |__||_______|  |_______||_______||_______||__| |__||___|  |_|    |__| |__||_______||_______||_______||_______|')
print('by Wildan Dicky Alnatara (13516012) dan Dion Saputra (13516045)')
n = input('Berapa banyak titik : ')

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

# terima perintah user
print('Masukkan input : ')

inp = raw_input()
while(inp!='exit'):
    masukan = inp.split()
    if masukan[0]=='kanim':
        kAnim = input('Masukkan angkanya : ')
    elif masukan[0]=='tanim':
        tAnim = input('Masukkan angkanya : ')
    elif masukan[0]=='status':
        print(temptitik)
    elif masukan[0]!='multiple':
        prosesInput(inp,temptitik)
    elif masukan[0]=='multiple':
        listperintah=[]
        for i in range(0,int(masukan[1])):
            inp2=raw_input()
            listperintah.append(inp2)
        for imp in listperintah:
            prosesInput(imp,temptitik)
    else :
        print('Perintah tidak tersedia')
    inp = raw_input()

if (inp == 'exit') :
    print('Program simulasi transformasi linear telah selesai')
    status = 'exit'

##################################     FINISH     #############################################
