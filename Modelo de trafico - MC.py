#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 10:45:09 2021

@author: mint
"""
"""
Nagel-Schreckenberg traffic model
Se tiene una calle de una sola mano, con condiciones periodicas (ruta
circular). Hay M posiciones sobre la ruta y k<M autos. 

Parametros:
    V_max: la velocidad maxima
    k: cantidad de autos
    M: cantidad de posiciones permitidas
    N: total de pasos temporales
"""

import numpy as np
from scipy.optimize import curve_fit, minimize
import matplotlib.pyplot as plt
from random import seed, randint
import matplotlib.animation as animation
from simulacion import Trafico



# Elijo la semilla aleatoriamente de /dev/urandom
archivo=open('/dev/urandom','rb')
semilla=int.from_bytes(archivo.read(3),'big')
archivo.close()

seed(semilla) # Inicializo el generador de num. aleatorios

# Defino valores de los parametros:
M=1000        # Cantidad de posiciones en la ruta
N=1000         # Numero de pasos temporales
V_max=5      # Velocidad maxima: el max. de pos. que puede avanzar en un paso
              # temporal.
k=50         # Cantidad de autos en la ruta


# Posicion inicial de los autos
# Los voy a ubicar de forma equiespaciada (salvo por el primero y el ultimo):
X=np.linspace(0,M-1,k,dtype=int)

# Velocidad inicial: al principio estan todos en reposo
V=np.zeros(k)

# Iniciamos la rutina: Burn-in

N1=100

for paso in range(N1):                  # Hago N1 interaciones
    for i in range(k):                  # Cambio la vel. de cada auto:
        if V[i]+1<V_max:                # Primero aumento la velocidad
            V[i]=V[i]+1

        d=(X[(i+1)%k]-X[i]+M)%M         # Calculo la dist. al auto de adelante,
                                        # con las cond. de contorno periodicas.

        if V[i]>=d:                     # Ahora me fijo si al aumentar la vel.,
                                        # hay choque con el de adelante.
            V[i]=d-1                    # Si hay choque, reduzco la velocidad.

        p=randint(1,3)                  # Tiro un numero aleatorio entre 1 y 3,
                                        # con distr. normal.
        if p==3:                        # Si sale 3, reduzco la velocidad: la 
                                        # probabilidad es 1/3
            V[i]=max(V[i]-1,0)

    for i in range(k):                  # Actualizadas las velocidades, paso a
                                        # cambiar las posiciones.
        X[i]=(X[i]+V[i])%M


# Listo. Ahora repito en la simulacion real:
Pos=np.zeros((N,X.size))               # Aca guardo las posiciones
j=0
for paso in range(N):
    for i in range(k):
        if V[i]+1<V_max:
            V[i]=V[i]+1

        d=(X[(i+1)%k]-X[i]+M)%M
        if V[i]>=d:
            V[i]=d-1

        p=randint(1,3)
        if p==3:
            V[i]=max(V[i]-1,0)

    for i in range(k):
        X[i]=(X[i]+V[i])%M

    Pos[j,:]=X                          # Guardo las posiciones
    j+=1

x=np.arange(N)
plt.figure(figsize=(10,10))
plt.plot(x,Pos,color='grey',marker='.',markersize=0.2, linestyle='')
plt.xlabel('Tiempo')
plt.ylabel('Distancia')
plt.savefig("Simulacion trafico.png",dpi=200)
plt.show()
print('Semilla = ', semilla)

"""
# Voy a graficar una animacion de todo esto.
fig, ax = plt.subplots()

Lista = ['line'+str(i) for i in range(k)]       # los k autos a t=0
Lineas=[]                                       # guardo los plots de cada auto
for i in Lista:
    i, = ax.plot(Pos[0,int(i[-1])],0, '.')
    Lineas.append(i)

plt.xlim([0,M])                                 # Fijo el ancho del plot a M


# Una animacion de cada plot en Lineas
def animate(i):
    temp=[]
    l=0
    for j in Lineas:
        j.set_xdata(Pos[i,l])
        temp.append(j)
        l+=1
    return temp

ani = animation.FuncAnimation( fig, animate, frames=N)
ani.save("movie.mp4", dpi=200)
plt.close()
"""

# Calculo la distancia total recorrida por los autos
Distancia=0                                     # La distancia total 
Dist_auto=[]                                    # La recorrida por cada auto
temp=0
for i in range(k):
    temp=0
    for j in range(N-1):
        temp+=(Pos[j+1,i]-Pos[j,i])%M
    Distancia+=temp
    Dist_auto.append(temp)


print("La distancia total recorrida es ", Distancia, " posiciones.")
print("Cada auto recorrio una distancia de:")
for i in range(k):
    print("Auto ", str(i+1).zfill(len(str(k)))," = ", Dist_auto[i],
          " posiciones.")

# Voy a probar hacerlo desde un modulo, deberia dar lo mismo:
Pos1=Trafico(M, N, V_max, k, semilla)
# Perfecto! Funciona


# Aprovechando el modulo, voy a hacer muchas corridas, para
# distinta cantidad de autos: desde 55 a 500, subiendo de a 5

# Armo una lista para guardar los resultados:
Resultados=[]
# Hago las simulaciones:
for k in np.arange(55,505,5):
    temp=Trafico(M, N, V_max, k, semilla*k)
    Resultados.append(temp)

# Voy a graficar la distancia total en cada corrida vs nro. de autos.
Distancia_total=[]
for i in range(len(Resultados)):
    Distancia=0
    for j in range(len(Resultados[i][0,:])):        #loop sobre los autos en 
                                                    #cada corrida.
        temp=0
        for l in range(N-1):
            temp+=(Resultados[i][l+1,j]-Resultados[i][l,j])%M
        Distancia+=temp
    Distancia_total.append(Distancia)

x=np.arange(55,505,5)
plt.plot(x, Distancia_total, 'r.')
plt.xlabel('Cantidad de Autos')
plt.ylabel('Distancia total recorrida')
plt.title("Diagrama fundamental")
plt.show()

# Parece que la maxima distancia se alcanza por los 150 autos; a partir de ahi, 
# los embotellamientos ralentizan cada vez mas el movimiento.

# Voy a buscar el maximo usando alguna rutina de optimizacion de scipy. Primero
# necesito hacer una funcion de interpolacion, y despues buscarle el maximo.
# OJO: en scipy solo existe la funcion 'minimize', asi que una vez que encuen-
# tre la interpolacion f(x), voy a buscar el minimo de g(x)=-f(x).

# Voy a proponer un polinomio a la quinta para interpolar:
def F(x,f, a, b, c, d, e):
    return f*x**5 + a*x**4 + b*x**3 + c*x**2 + d*x + e

# Uso curve_fit para obtener los parametros:
param, covarianza = curve_fit(F, x, Distancia_total)

# Busco el maximo con minimize: primero la funcion resultante
def f(x):
    return F(x, param[0], param[1], param[2], param[3], param[4], param[5])

def g(x):
    return -f(x)
# Y ahora la minimizo:
Max=minimize(g,x0=150)

# Y ahora grafico el resultado:
nueva_x = np.linspace(x.min(), x.max(), 100)
plt.plot(nueva_x, f(nueva_x), '-', label="Ajuste", linewidth=3)
plt.plot(x, Distancia_total, 'r.', label="Datos")
plt.plot(Max.x, f(Max.x), 'go', label="Maximo = {}".format(int(Max.x)),
         markersize=8)
plt.xlabel('Cantidad de Autos')
plt.ylabel('Distancia total recorrida')
plt.title("Diagrama fundamental")
plt.legend()
plt.show()
print("El maximo corresponde a ", int(Max.x), " autos.")

# Muestro los resultados de la simulacion para el k de maximo desplazamiento, 
# y dos mas, uno por debajo y otro por encima
t=np.arange(N)
fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, sharex=True,
     figsize=(30,10))

ax0.set_title("Simulacion {} autos".format(int(Max.x)-10))
ax0.set_xlabel("Tiempo")
ax0.set_ylabel("Distancia")
ax0.plot(t, Resultados[(int(Max.x)-10-55)//5], color='grey', marker='.', markersize=0.2,
                       linestyle='')

ax1.set_title("Simulacion {} autos".format(int(Max.x)))
ax1.set_xlabel("Tiempo")
ax1.set_ylabel("Distancia")
ax1.plot(t, Resultados[(int(Max.x)-55)//5], color='grey', marker='.', markersize=0.2,
                       linestyle='')

ax2.set_title("Simulacion {} autos".format(int(Max.x)+10))
ax2.set_xlabel("Tiempo")
ax2.set_ylabel("Distancia")
ax2.plot(t, Resultados[(int(Max.x)+10-55)//5], color='grey', marker='.', markersize=0.2,
                       linestyle='')

fig.suptitle("Resultados con distinta cantidad de autos")
plt.savefig("Tres corridas.png", dpi=200)
plt.show()

# Ahora me pide que haga tres corridas mas de las simulaciones con distinta 
# cantidad de autos, para hacer una estadistica con eso.









