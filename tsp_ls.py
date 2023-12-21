import random
import math
import matplotlib.pyplot as plt
import time

def crear_puntos_aleatorios(num_puntos):
    puntos = []
    for i in range(num_puntos):
        x = random.uniform(0, 200)
        y = random.uniform(0, 200)
        puntos.append((x, y))
    return puntos

def distancia_euclidiana(punto_1, punto_2):
    x1, y1 = punto_1
    x2, y2 = punto_2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def longitud_camino(points, camino):
    total_peso = 0
    for i in range(len(camino)):
        j = (i + 1) % len(camino)
        peso = distancia_euclidiana(points[camino[i]], points[camino[j]])
        total_peso += peso
    return total_peso

def crear_vertices(num_puntos, punto_origen):
    lista_vertices = list(range(num_puntos))
    lista_vertices.remove(punto_origen)
    random.shuffle(lista_vertices)
    lista_vertices.insert(0, punto_origen)
    lista_vertices.append(punto_origen)  
    return lista_vertices

def busqueda_local(puntos, camino):
    start_time = time.time() 
    # Inicializamos la mejor ruta y su longitud con la ruta proporcionada
    mejor_camino = camino
    mejor_peso = longitud_camino(puntos, camino)
    flag = True 
    iteraciones = 0
    while flag:
        flag = False  
        for i in range(1, len(camino) - 1):  # No se intercambio el origen y el destino
            for j in range(i + 1, len(camino) - 1):
                # Creamos una copia de la ruta actual y realizamos el intercambio
                nuevo_camino = camino[:]
                nuevo_camino[i], nuevo_camino[j] = nuevo_camino[j], nuevo_camino[i]
                # Calculamos la longitud de la nueva ruta
                nuevo_peso = longitud_camino(puntos, nuevo_camino)
                # Verificamos si la nueva ruta es más corta que la mejor conocida
                if nuevo_peso < mejor_peso:
                    mejor_camino = nuevo_camino
                    mejor_peso = nuevo_peso
                    flag = True  
                    iteraciones+=1
        camino = mejor_camino

    # Devolvemos la mejor ruta y su longitud
    end_time = time.time()  # Marca el tiempo de finalización
    elapsed_time = end_time - start_time  # Calcula el tiempo transcurrido
    print("Tiempo transcurrido: ", elapsed_time)
    return mejor_camino, mejor_peso, iteraciones

def graficar(points, path):
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.plot(x, y, 'bo')

    for i in range(len(path) - 1):
        plt.annotate(str(path[i]), (points[path[i]][0], points[path[i]][1]), fontsize=12)  # Muestra el nombre del vértice

        dx = points[path[i + 1]][0] - points[path[i]][0]
        dy = points[path[i + 1]][1] - points[path[i]][1]

        plt.quiver(
            points[path[i]][0], points[path[i]][1], dx, dy,
            angles='xy', scale_units='xy', scale=1, color='red', width=0.005
        )
       
        plt.text(
            0.5 * (points[path[i]][0] + points[path[i + 1]][0]),
            0.5 * (points[path[i]][1] + points[path[i + 1]][1]),
            str(round(distancia_euclidiana(points[path[i]], points[path[i + 1]]), 2)),
            color='blue', fontsize=8
        )


    plt.annotate(str(path[-1]), (points[path[-1]][0], points[path[-1]][1]), fontsize=10)  # Muestra el nombre del último vértice

    #plt.axis('equal')    

#Pasos para ejecutar 

# Parametros
num_puntos = 300
punto_origen = 0

puntos = crear_puntos_aleatorios(num_puntos)
print("Puntos:")
print(puntos)
# Generar una ruta con el punto de origen especificado
vertices = crear_vertices(num_puntos, punto_origen)
print("Ruta Inicial:")
print(vertices)
print("Longitud del camino inicial:", longitud_camino(puntos, vertices))
print("Pesos de la ruta inicial:", [distancia_euclidiana(puntos[vertices[i]], puntos[vertices[i + 1]]) for i in range(len(vertices) - 1)])
plt.title("Solucion Inicial - " + str(num_puntos) + " ciudades")
graficar(puntos, vertices)
plt.savefig("sol_inicial_"+str(num_puntos)+".png")
plt.show()
# Busqueda Local
mejor_camino, mejor_peso, iteraciones = busqueda_local(puntos, vertices)
print("Longitud del camino mejorado:", mejor_peso)
print("Ruta Mejorada:")
print(mejor_camino)
print("iteraciones", str(iteraciones))
print("Pesos de la ruta mejorada:", [distancia_euclidiana(puntos[mejor_camino[i]], puntos[mejor_camino[i + 1]]) for i in range(len(mejor_camino) - 1)])
#plt.figure()
plt.title("Solucion Final - " + str(num_puntos) + " ciudades")
graficar(puntos, mejor_camino)
plt.savefig("sol_final_"+str(num_puntos)+".png")
plt.show()