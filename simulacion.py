#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 15:56:59 2021

@author: mint
"""
"""
MODULO Simulacion
Contiene funciones que realizan simulaciones. Se importan las que se necesiten
y se pueden realizar varias simulaciones cambiando los parametros.
"""
import numpy as np
from random import seed, randint


"""
1)
Modelo de trafico: Nagel-Schreckenberg traffic model
Se tiene una calle de una sola mano, con condiciones periodicas (ruta
circular). Hay M posiciones sobre la ruta y k<M autos, probabilidad 1/3 
de que los coches se frenen

Parametros:
    V_max: la velocidad maxima
    k: cantidad de autos
    M: cantidad de posiciones permitidas
    N: total de pasos temporales
    semilla: para inicializar el random gen.

Devuelve un array de k listas, una por cada auto, con las N posiciones
que alcanzan en cada iteracion: [[Auto1],[Auto2],...,[Autok]]
"""

def Trafico(M, N, V_max, k, semilla):
    seed(semilla)
    
    #Set-up inicial
    X=np.linspace(0,M-1,k,dtype=int)
    V=np.zeros(k)
    
    #Burn-in: 100 pasos
    N1=100
    for paso in range(N1):
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
    
    #La simulacion real: N pasos
    Pos=np.zeros((N,X.size))
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
    
        # Guardo las posiciones
        Pos[j,:]=X
        j+=1
    
    return Pos
