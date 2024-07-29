# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 14:18:22 2024

@author: Juanjo

Nagel-Schreckenberg traffic model: algunas pruebas
Voy a variar la velocidad máxima entre 1, 3 y 5, en los casos:
    1) Sin aleatoriedad: p=0
    2) p=2: 50% frenado aleatorio
    3) p=4: 25% frenado aleatorio

Bibliografía:
    [1] https://arxiv.org/pdf/cond-mat/9902170
    [2] https://sci-hub.se/https://doi.org/10.1016/0378-4371(95)00442-4
    [3] https://sci-hub.st/https://doi.org/10.1103/PhysRevE.51.2939
"""

from simulacion import Trafico
from matplotlib import pyplot as plt
from os import urandom
from scipy.optimize import curve_fit
import numpy as np

"""
1) Caso sin aleatoriedad: p=0
Voy a obtener el diagrama fundamental con distintas V_max. El caso p=0 es deter
minista, va a depender de las condiciones iniciales.
"""

# Extraigo la semilla
semilla = int.from_bytes(urandom(3),'big')

# Hago una primera prueba
largo = 1000    # Cantidad de posiciones permitidas
tiempos = 1000    # Cantidad de pasos temporales
autos = 150
V_max = 5

resultados = Trafico(largo, tiempos, V_max, autos, 0, semilla)

x = np.arange(tiempos)
plt.figure(figsize=(10,10))
plt.plot(x,resultados,color='grey',marker='.',markersize=0.2, linestyle='')
plt.xlabel('Tiempo')
plt.ylabel('Distancia')
plt.show()

# Diagrama fundamental con autos entre 20 y 1000: p=0, V_max=5
Distancias_totales = []      # La distancia total en cada simulación
for autos in np.arange(20,1020,20):
    # Hago una simulación y la guardo en corrida
    corrida = Trafico(largo, tiempos, V_max, autos, 0, semilla + 2*autos)
    
    distancia_corrida = 0        # La distancia total en la corrida
    
    for i in range(autos):       # será la suma sobre el total de cada auto     
        total_cada_auto = 0
        
        for t in range(tiempos - 1):    # Calculo el avance del auto i y sumo 
            variacion = (corrida[t+1,i] - corrida[t,i])%largo
            total_cada_auto += variacion
        
        distancia_corrida += total_cada_auto
    
    Distancias_totales.append(distancia_corrida)

# Grafico el diagrama correspondiente:
densidad = np.arange(20,1020,20)/largo
flujo = [i/(largo*tiempos) for i in Distancias_totales]

plt.plot(densidad, flujo, 'r.')
plt.xlabel('Densidad [autos/L]')
plt.ylabel('Flujo [distancia/(L.T)')
plt.title("Diagrama fundamental")
plt.show()

# En este caso, la forma funcional exacta del flujo es conocida [1]. Deberían 
# ser rectas hasta densidad = 1/(V_max + 1). Propongamos ajustes lineales:

def F(x, a, b):
    return a*x + b

# Separamos los valores según regimen de densidades: 
x_1 = []
y_1 = []
x_2 = []
y_2 = []
for i, j in zip(densidad, flujo):
    if i <= 1/(V_max+1):
        x_1.append(i)
        y_1.append(j)
    elif i >= 1/(V_max+1):
        x_2.append(i)
        y_2.append(j)
        
# Ahora hago los ajustes lineales en cada uno y grafico:
param_1, covar_1 = curve_fit(F, x_1, y_1)
param_2, covar_2 = curve_fit(F, x_2, y_2)

densidad_1 = np.linspace(min(x_1), max(x_1),100)
densidad_2 = np.linspace(min(x_2), max(x_2),100)

fig, ax = plt.subplots()
ax.plot(densidad, flujo, 'r.', label = "Simulación")
ax.plot(densidad_1, F(densidad_1, param_1[0], param_1[1]), label = f"f(x) = {param_1[0]: .2f}.x"
        f" +{param_1[1]: .2f}")
ax.plot(densidad_2, F(densidad_2, param_2[0], param_2[1]), label = f"f(x) = {param_2[0]: .2f}.x"
        f"+{param_2[1]: .2f}")

# Ubico la discontinuidad según 1/(V_max+1)
ax.axvline(1/(V_max+1), linewidth=0.75, linestyle="dashed", color='black', 
           label=r"$\dfrac{1}{V_{max}+1} = $"f"{1/(V_max+1): .2f}")


ax.set_ylim(0)
ax.set_xlabel("Densidad")
ax.set_ylabel("Flujo")
ax.set_title("Simulación con V_max = {}, p = {}".format(V_max, 0))
ax.legend(fontsize=8)    
# Funciona! Los valores son los esperados.

# Voy a hacer lo mismo manteniendo p=0, en los casos con V_max = 1, V_max = 3
# y V_max = 5:

for velocidad in [1,3,5]:
    largo = 1000       # Cantidad de posiciones permitidas
    tiempos = 1000     # Cantidad de pasos temporales
    autos = 150
    V_max=velocidad
    
    # Diagrama fundamental con autos entre 20 y 1000, p=0:
    Distancias_totales = []      # La distancia total en cada simulación
    for autos in np.arange(20,1020,20):
        # Hago una simulación y la guardo en corrida
        corrida = Trafico(largo, tiempos, V_max, autos, 0, semilla + 2*autos)
        
        distancia_corrida = 0        # La distancia total en la corrida
        
        for i in range(autos):       # será la suma sobre el total de cada auto     
            total_cada_auto = 0
            
            for t in range(tiempos - 1):    # Calculo el avance del auto i y sumo 
                variacion = (corrida[t+1,i] - corrida[t,i])%largo
                total_cada_auto += variacion
            
            distancia_corrida += total_cada_auto
        
        Distancias_totales.append(distancia_corrida)
    
    # Calculo densidad y flujo para esa V_max:
    densidad = np.arange(20,1020,20)/largo
    flujo = [i/(largo*tiempos) for i in Distancias_totales]
    
    # Separolos valores según regimen de densidades cortando en 1/(V_max +1): 
    x_1 = []
    y_1 = []
    x_2 = []
    y_2 = []
    for i, j in zip(densidad, flujo):
        if i <= 1/(V_max+1):
            x_1.append(i)
            y_1.append(j)
        elif i >= 1/(V_max+1):
            x_2.append(i)
            y_2.append(j)
            
    # Ahora hago los ajustes lineales en cada uno y grafico:
    param_1, covar_1 = curve_fit(F, x_1, y_1)
    param_2, covar_2 = curve_fit(F, x_2, y_2)
    
    densidad_1 = np.linspace(min(x_1), max(x_1),100)
    densidad_2 = np.linspace(min(x_2), max(x_2),100)
    
    fig, ax = plt.subplots()
    ax.plot(densidad, flujo, 'r.')
    ax.plot(densidad_1, F(densidad_1, param_1[0], param_1[1]), label = f"f(x) = {param_1[0]: .2f}.x"
            f" +{param_1[1]: .2f}")
    ax.plot(densidad_2, F(densidad_2, param_2[0], param_2[1]), label = f"f(x) = {param_2[0]: .2f}.x"
            f"+{param_2[1]: .2f}")
    ax.set_xlabel("Densidad")
    ax.set_ylabel("Flujo")
    ax.set_title("Simulación con V_max = {}, p = {}".format(V_max, 0))
    ax.legend()

# Funciona, un lujo.

"""
2) Caso con p=2: 50% probabilidad de frenado aleatorio
Voy a obtener el diagrama fundamental con distintas V_max. 
"""

# Hagamos una prueba. Lo mismo de antes, pero ahora con p=2. Ya no tengo ajuste 
# para hacer, no hay resolución analítica.

# Extraigo la semilla
semilla = int.from_bytes(urandom(3),'big')
# Establezco las cantidades
largo = 1000    # Cantidad de posiciones permitidas
tiempos = 1000    # Cantidad de pasos temporales
V_max = 1

# Diagrama fundamental con autos entre 20 y 1000: p=2, V_max=1
Distancias_totales = []      # La distancia total en cada simulación
for autos in np.arange(20,1020,20):
    # Hago una simulación y la guardo en corrida
    corrida = Trafico(largo, tiempos, V_max, autos, 2, semilla + 2*autos)
    
    distancia_corrida = 0        # La distancia total en la corrida
    
    for i in range(autos):       # será la suma sobre el total de cada auto     
        total_cada_auto = 0
        
        for t in range(tiempos - 1):    # Calculo el avance del auto i y sumo 
            variacion = (corrida[t+1,i] - corrida[t,i])%largo
            total_cada_auto += variacion
        
        distancia_corrida += total_cada_auto
    
    Distancias_totales.append(distancia_corrida)

# Grafico el diagrama correspondiente:
densidad = np.arange(20,1020,20)/largo
flujo = [i/(largo*tiempos) for i in Distancias_totales]

plt.plot(densidad, flujo, 'r.', label = "Simulación")

# Ubico la discontinuidad según 1/(V_max+1)
plt.axvline(1/(V_max+1), linewidth=0.75, linestyle="dashed", color='black', 
           label=r"$\dfrac{1}{V_{max}+1} = $"f"{1/(V_max+1): .2f}")

plt.xlabel('Densidad [autos/L]')
plt.ylabel('Flujo [distancia/(L.T)')
plt.title("Simulación con V_max = {}, p = {}".format(V_max, 2))
plt.legend(loc="upper right", fontsize=8)   
plt.show()

# Voy a plotear en el mismo gráfico las simulaciones con V_max = 1,3,5, mante-
# niendo p=2. Para que no explote, voy a calcular las distancias pero no voy
# a guardar todos los datos de cada simulación.

Diagramas=[]     # Acá guardo los diagramas por cada velocidad:
                 # [[flujo_1, densidad_1], [flujo_2, densidad_2], ...]
for velocidad in [1,2,3]:
    largo = 1000       # Cantidad de posiciones permitidas
    tiempos = 1000     # Cantidad de pasos temporales
    V_max=velocidad
    
    # Diagrama fundamental con autos entre 20 y 1000, p=2:
    Distancias_totales = []      # La distancia total en cada simulación
    autos_totales = np.concatenate((np.arange(10,largo//(V_max+1),10),
                                    np.arange(largo//(V_max+1),1000,30)))
    for autos in autos_totales:
        # Hago una simulación y la guardo en corrida
        corrida = Trafico(largo, tiempos, V_max, autos, 2, semilla + 2*autos)
        
        distancia_corrida = 0        # La distancia total en la corrida
        
        for i in range(autos):       # será la suma sobre el total de cada auto     
            total_cada_auto = 0
            
            for t in range(tiempos - 1):    # Calculo el avance del auto i y sumo 
                variacion = (corrida[t+1,i] - corrida[t,i])%largo
                total_cada_auto += variacion
            
            distancia_corrida += total_cada_auto
        
        Distancias_totales.append(distancia_corrida)
    
    # Calculo densidad y flujo para esa V_max:
    densidad = autos_totales/largo
    flujo = [i/(largo*tiempos) for i in Distancias_totales]
    
    # Los guardo el Diagramas:
    Diagramas.append([flujo, densidad])
    
# Y ahora grafico todo en un mismo plot:    
    
velocidad=1
for datos in Diagramas:
    plt.plot(datos[1], datos[0], '.', label="V_max = {}".format(velocidad)) 
    plt.vlines(1/(velocidad+1),ymin=0, ymax= max(datos[0]), linewidth=0.75, 
                linestyles="dashed", colors='black')
    
    velocidad += 1 
    
plt.ylim(0)    
plt.xlabel("Densidad")
plt.ylabel("Flujo")
plt.title("Simulación con probabilidad 0.5")
plt.legend(loc="upper right", fontsize=10)   
plt.show()

# Se nota que el máximo flujo ocurre para densidades menores que en el caso p=0, 
# el tránsito empieza a ser menos fluido para una menor cantidad de autos en 
# la ruta.

# En [3] propusieron aproximaciones con teoría de campo medio, y encontraron que
# la solución es exacta para el caso V_max = 2. Podemos intentar ajustar ese caso.



    
    