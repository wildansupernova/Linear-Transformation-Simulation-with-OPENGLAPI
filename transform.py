###################################################################################################
##################################     PROCEDURE DAN FUNGSI     #############################################
#############################################################################################################

import sys
import thread
import threading
import Queue
import time
import copy
import math

MRefX = [[1,0],[0,-1]]  # matriks refleksi terhadap sumbu X
MRefY = [[-1,0],[0,1]]  # matriks refleksi terhadap sumbu y
MRefYX = [[0,1],[1,0]]  # matriks refleksi terhadap garis y=x
MRefYminX = [[0,-1],[-1,0]]     # matriks refleksi terhadap garis y=-x
MRefO = [[-1,0],[0,-1]]         # matriks refleksi terhadap titik (0,0)
kAnim = 0.001
tAnim = 0.001
epsilon = 0.0005

# mengecek kesamaan dua float
def isEqual(a,b):
    return abs(a-b) < epsilon

# mengecek kesamaan dua matriks
def isEqualMatriks(tempawal,tempakhir):
    sama = True
    for i in range(0,len(tempawal)):
        if isEqual(tempawal[i][0],tempakhir[i][0])==False or isEqual(tempawal[i][1],tempakhir[i][1]) == False :
            sama=False
    return sama

# menerima matriks1 (matriks) dan array1 (array), mengembalikan hasil kali matriks1 dan array1
def multiMatrixArray(matriks1, array1): 
    arrayAns = [0 for x in range(len(array1))]
    for i in range(len(matriks1)):
        for j in range(len(array1)):
            arrayAns[i] += matriks1[i][j] * array1[j]
    return arrayAns

# menerima tempawal (titik2 sebelum transformasi) dan tempakhir (titik2 setelah transformasi)
# melakukan animasi dari tempawal hingga tempakhir. Digunakan untuk selain rotasi 
def animate (tempawal,tempakhir):
    rentang = []
    for i in range(0,len(tempawal)):
        temp = [tempawal[i][0]-tempakhir[i][0],tempawal[i][1]-tempakhir[i][1]]
        rentang.append(temp)

    while isEqualMatriks(tempawal,tempakhir)==False:     
        for i in range(0,len(tempawal)):
            dx = rentang[i][0]
            dy = rentang [i][1]
            dx*=-1
            dy*=-1
            tempawal[i][0] += dx*kAnim*10
            tempawal[i][1] += dy*kAnim*10
            time.sleep(tAnim)

    for i in range(0,len(tempawal)):
        tempawal[i][0] = tempakhir[i][0]
        tempawal[i][1] = tempakhir[i][1]

# menerima temppoint (titik2 sebelum transformasi), transX (komponen translasi arah sumbu-X), transY (komponen translasi arah sumbu-Y)
# translasi temppoint sesuai besar trasnlasinya dan menganimasikannya
def translate2D(tempPoint,transX,transY):
    arrTrans = [transX,transY]
    finalPoint = []
    for i in tempPoint:
        temp = [0,0]
        temp[0] = i[0] + transX
        temp[1] = i[1] + transY
        finalPoint.append(temp)
    animate(tempPoint,finalPoint)

# menerima temppoint (titik2 sebelum transformasi), scaleFactor (besar skala dilatasi)
# dilatasi temppoint sesuai besar dilatasinya dan menganimasikannya
def dilate2D(tempPoint,scaleFactor):
    k = scaleFactor
    MDilate = [[k,0],[0,k]]
    finalPoint = []
    for i in tempPoint:
        temp = multiMatrixArray(MDilate,i)
        finalPoint.append(temp)
    animate(tempPoint,finalPoint)

# menerima temppoint (titik2 sebelum transformasi), degree (derajat perputaran counterclockwise), XCenter, YCenter (Titik rotasi)
# rotasi temppoint sesuai besar rotasinya dan menganimasikannya
def rotate2D(tempPoint,degree,XCenter,YCenter):
    dTeta = 0
    while dTeta<abs(degree):
        rot = float(degree)*kAnim
        rad = 3.14*(rot/180)
        a = float(XCenter)
        b = float(YCenter)
        for i in tempPoint:
            x = i[0]
            y = i[1]
            i[0]=((x-a)*math.cos(rad)) - ((y-b)*math.sin(rad)) + a
            i[1]=((x-a)*math.sin(rad)) + ((y-b)*math.cos(rad)) + b
        dTeta = dTeta + abs(float(degree)*kAnim)
        time.sleep(tAnim)    

# menerima temppoint (titik2 sebelum transformasi) dan param (parameter refleksi)
# refleksi temppoint sesuai parameter dan menganimasikannya
def reflect2D(tempPoint,param):
    temptitik2 = []
    for i in tempPoint:
        if param=='x':
            arrayAns = multiMatrixArray(MRefX,i)
        elif param=='y':
            arrayAns = multiMatrixArray(MRefY,i)
        elif param=='y=x':
            arrayAns = multiMatrixArray(MRefYX,i)
        elif param=='y=-x':
            arrayAns = multiMatrixArray(MRefYminX,i)
        else:
            temp = param[1:len(param)-1]
            temp = temp.split(",")
            point_a = float(temp[0])
            point_b = float(temp[1])
            arrayAns = i
            arrayAns[0] -= point_a
            arrayAns[1] -= point_b
            arrayAns = multiMatrixArray(MRefO,arrayAns)
            arrayAns[0] += point_a
            arrayAns[1] += point_b
        temptitik2.append(arrayAns)
    animate(tempPoint,temptitik2)
        
# menerima temppoint (titik2 sebelum transformasi), param (parameter shear), scaleFactor (skala shear)
# shear temppoint sesuai parameter dan besar shear-nya serta menganimasikannya
def shear2D(tempPoint,param,scaleFactor):
    k = scaleFactor
    MShearX = [[1,k],[0,1]]
    MShearY = [[1,0],[k,1]]
    finalPoint = []
    
    if param=='x':
        M = MShearX
    else:
        M = MShearY

    for i in tempPoint:
        temp = multiMatrixArray(M,i)
        finalPoint.append(temp)
    animate(tempPoint,finalPoint)

# menerima temppoint (titik2 sebelum transformasi), param(parameter stretch), scaleFactor(skala stretch)
# stretch temppoint sesuai parameter dan besar stretch-nya serta menganimasikannya
def stretch2D(tempPoint,param,scaleFactor):
    k = scaleFactor
    MStretchX = [[k,0],[0,1]]
    MStretchY = [[1,0],[0,k]]
    finalPoint = []
    
    if param=='x':
        M = MStretchX
    else:
        M = MStretchY

    for i in tempPoint:
        temp = multiMatrixArray(M,i)
        finalPoint.append(temp)
    animate(tempPoint,finalPoint)

# menerima temppoint (titik2 sebelum transformasi), a, b, c, d elemen matriks transformasi yaitu MCustom = [[a,b],[c,d]]
# transformasi temppoint sesuai matriks transformasinya dan menganimasikannya
def custom2D(tempPoint,a,b,c,d):
    MCustom = [[a,b],[c,d]]
    finalPoint = []
    for i in tempPoint:
        temp = multiMatrixArray(MCustom,i)
        finalPoint.append(temp)
    animate(tempPoint,finalPoint)

# ubah tempPoint1 menjadi tempPoint2
def reset2D(tempPoint1, tempPoint2):
    animate(tempPoint1,tempPoint2)
