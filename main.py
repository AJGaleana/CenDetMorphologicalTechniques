#Instaladores de terminal
#pip install opencv-contrib-python >>Para OpenCV
#pip install numpy >> Para Numpy


#Codigo del proyecto
#Librerias
import cv2
import numpy as np

def BinariFrame(frameHSV,dY,dX,mtzBiPrinFrame, cBajo,cAlto):
    
    for y in range(0,dY,2):
       for x in range(0,dX,2):
            #Comparación de los valores del frame con los deseados
            valInf=(frameHSV[y,x,:]>=cBajo)#Se extrae el valor del frame y se realiza la comparación colorBajo
            valUp= (frameHSV[y,x,:]<=cAlto)#Se extrae el valor del frame y se realiza la comparación colorAlto
            if (valInf[0]==True and valInf[1]==True and valInf[2]==True and valUp[0]==True and valUp[1]==True and valUp[2]==True):
                mtzBiPrinFrame[y,x]=1                    
            else :
                mtzBiPrinFrame[y,x]=0
    return mtzBiPrinFrame



def ErosionBinaria(mtOrig,elemEstr,mtEB,dimX,dimY):
    for x in range(0,dimX-2,2):
        for y in range(0,dimY-2,2):
            #Comparación del elemento estructural
            if (mtOrig[x-2,y-2]==elemEstr[0,0] and mtOrig[x-2,y-1]==elemEstr[0,1] and mtOrig[x-2,y]==elemEstr[0,2] and mtOrig[x-2,y+1]==elemEstr[0,3] and mtOrig[x-2,y+2]==elemEstr[0,4]
            and mtOrig[x-1,y-2]==elemEstr[1,0] and mtOrig[x-1,y-1]==elemEstr[1,1] and mtOrig[x-1,y]==elemEstr[1,2] and mtOrig[x-1,y+1]==elemEstr[1,3] and mtOrig[x-1,y+2]==elemEstr[1,4]
            and mtOrig[x  ,y-2]==elemEstr[2,0] and mtOrig[x  ,y-1]==elemEstr[2,1] and mtOrig[x  ,y]==elemEstr[2,2] and mtOrig[x  ,y+1]==elemEstr[2,3] and mtOrig[x  ,y+2]==elemEstr[2,4]
            and mtOrig[x+1,y-2]==elemEstr[3,0] and mtOrig[x+1,y-1]==elemEstr[3,1] and mtOrig[x+1,y]==elemEstr[3,2] and mtOrig[x+1,y+1]==elemEstr[3,3] and mtOrig[x+1,y+2]==elemEstr[3,4]
            and mtOrig[x+2,y-2]==elemEstr[4,0] and mtOrig[x+2,y-1]==elemEstr[4,1] and mtOrig[x+2,y]==elemEstr[4,2] and mtOrig[x+2,y+1]==elemEstr[4,3] and mtOrig[x+2,y+2]==elemEstr[4,4]):
                mtEB[x,y]=1
            
            else:
                mtEB[x,y]=0
    return mtEB



def CompArrayCentroide(dimYArray,dimXArray,mtBin):
    yArrayUni=np.arange(dimYArray)
    xArrayUni=np.arange(dimXArray)
    ySumArray=np.sum(mtBin,axis=1) #Suma de los componentes en y
    xSumArray=np.sum(mtBin,axis=0) #Suma de los componentes en X
    sumMtTotal=np.sum(mtBin)    
    return  xArrayUni, yArrayUni, xSumArray, ySumArray,sumMtTotal



def Centroide(arrayUni,arraySum,sumTotalMt):
    centroide=int(np.sum(arrayUni*arraySum)/sumTotalMt) #Cálculo del centroide
    return centroide

    

def run():        
    captura=cv2.VideoCapture(0)#Especificación de la cámara a utilizar, 0 o -1, 1, 2, 3, ...

    #Valores para el color azul
    colorBajo=np.array([100,100,20],np.uint8) #Se crea un array con los valores del color a detectar en su tonalidad baja de rango
    colorAlto=np.array([125,255,255],np.uint8) #Se crea un array con los valores del color a detectar en su tonalidad alta de rango

    #Valores para el color naranja
    #colorBajo=np.array([10,100,20],np.uint8) #Se crea un array con los valores del color a detectar en su tonalidad baja de rango
    #colorAlto=np.array([25,255,255],np.uint8) #Se crea un array con los valores del color a detectar en su tonalidad alta de rango

    banderaUno=0
    while(captura.isOpened()):#Ciclo de leectura de imagen en cada momento
        ret, frame= captura.read()#Leectura de los datos de captura ret (True cuando la imagen ya esta leída, False cuando no se ha inicializado la captura de la imagen) es boleano y imagen en RGB
        if ret==True:

            frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)#Conversión de color RGB a HSV

            if banderaUno==0: #Condicional para la creación de elementos por solo una vez.
                dimenY=len(frame[:,0,0])#Dimensión de Y de la matriz frame
                dimenX=len(frame[0,:,0])#Dimensión de X de la matriz frame
                mtzBiPrin=np.zeros((dimenY,dimenX), dtype=np.uint8, order='F') #Matriz bidimensional para los binarios del frame
                mtEB=np.zeros((dimenY,dimenX), dtype=np.uint8, order='F') #Matriz bidimensional para los binarios con erosión binaria del frame
                mtzElemEstruc=np.zeros((5,5), dtype=np.uint8, order='F')#Elemento estructural bidimensional para la erosión binaria
                mtzElemEstruc[0,0]=np.uint8(1) #Asignación de valor en la posición [0,0] de elemento estructural 
                mtzElemEstruc[0,2]=np.uint8(1) #Asignación de valor en la posición [0,0] de elemento estructural
                mtzElemEstruc[0,4]=np.uint8(1) #Asignación de valor en la posición [0,0] de elemento estructural
                mtzElemEstruc[2,0]=np.uint8(1) #Asignación de valor en la posición [0,0] de elemento estructural
                mtzElemEstruc[2,2]=np.uint8(1) #Asignación de valor en la posición [0,0] de elemento estructural
                mtzElemEstruc[2,4]=np.uint8(1) #Asignación de valor en la posición [0,0] de elemento estructural
                mtzElemEstruc[4,0]=np.uint8(1) #Asignación de valor en la posición [0,0] de elemento estructural                
                mtzElemEstruc[4,2]=np.uint8(1) #Asignación de valor en la posición [0,0] de elemento estructural
                mtzElemEstruc[4,4]=np.uint8(1) #Asignación de valor en la posición [0,0] de elemento estructural
                banderaUno=1 #Bandera
                
            mtzBiPrin = BinariFrame(frameHSV,dimenY,dimenX,mtzBiPrin, colorBajo,colorAlto)
            mtzBinEB = ErosionBinaria(mtzBiPrin,mtzElemEstruc,mtEB,dimenY,dimenX)
            SumMtzTotPrin=np.sum(mtzBiPrin)

            if SumMtzTotPrin>1500: #Un umbral, para que se ejecute la determinación del centroide y se grafique
                xArrayEB, yArrayEB,xSumVecEB,ySumVecEB,SumMtzTotEB=CompArrayCentroide(dimenY,dimenX,mtzBinEB) #Componentes para el cálculo del centroide

                if SumMtzTotPrin==0: SumMtzTotPrin=int(1) #Para no generar una indeterminación
                if SumMtzTotEB==0: SumMtzTotEB=int(1) #Para no generar una indeterminación
                try:
                    #Centroides
                    xCentroideEB=Centroide(xArrayEB,xSumVecEB,SumMtzTotEB) #Centroide en X
                    yCentroideEB=Centroide(yArrayEB,ySumVecEB,SumMtzTotEB) #Centroide en Y
                    
                except:
                    pass
                
                #Graficación de centroide
                    #Circulo del centroide en el frame original
                cv2.circle(frame, (xCentroideEB,yCentroideEB), 7, (255,0,255), -1)
                    #Coordenadas del centroide en el frame original
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '{},{}'.format(xCentroideEB,yCentroideEB),(xCentroideEB+10,yCentroideEB), font, 0.75,(0,255,255),1,cv2.LINE_AA)
                      
            
            #Frames de las matrices con las que se ha trabajado   
            cv2.imshow('FRAME ORIGINAL',frame)
            
            if cv2.waitKey(1) & 0xFF == ord ('s'):# & 0xFF cuando trabajamos con una máquina de 64 bits. ord ('s') -- para decir que tecla vamos a utilizar para salir
                break
        else:break
    captura.release() #Finalizamos la captura
    cv2.destroyAllWindows()#Cerramos cualquier ventana que haya quedado abierta



if __name__=='__main__':    
    run() #Ejecución el código
