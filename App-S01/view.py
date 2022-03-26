"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from pip import main
from model import deltaTime, getTime
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate
import time
import pycountry
default_limit = 10000 
sys.setrecursionlimit(default_limit*10)



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

"""
Menu principal
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- REQ.1: Listar los álbumes en un periodo de tiempo")
    print("3- REQ.2: Encontrar los artistas mas populares")
    print("4- REQ.3: Clasificar las canciones por popularidad")
    print("5- REQ.4: Encontrar la cancion mas popular de un artista")
    print("6- REQ.5: Encontrar la discografia de un artista")
    print("7- REQ.BONO: Clasificar las canciones con mayor distribucion")
    print("0- Salir")

"""
Menu de operaciones. 
"""

#CARGA DE DATOS

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        c = True
        while c == True:
            listType = input('Ingrese el tipo de lista a crear:\nIngrese 1 para ARRAY_LIST \nIngrese 2 para SINGLE_LINKED\n')
            if listType not in '12':
                print('Ingreso un valor erroneo. Porfavor ingrese el valor de nuevo')
            else: c = False
        
        muestra = input('ingrese el tamaño de la muestra:\n ej. small, 5pct, 10pct, 30pct, 80pct, large\n')
        if listType == '1':
            listType = 'ARRAY_LIST'
        elif listType == '2':
            listType = 'SINGLE_LINKED'

        userList = controller.listaUsuario(listType) 
        userCatalog = controller.LoadUserData(userList, muestra)
        tamañoMuestra = controller.tamañoMuestra(userCatalog)

        lastArtists = controller.LastArtists(userCatalog)
        lastAlbums = controller.LastAlbums(userCatalog)
        lastSongs = controller.LastSongs(userCatalog)
        
        print("--------------------------")
        print(f"artists ID count:{tamañoMuestra[0]}\nalbums ID count:{tamañoMuestra[1]}\ntracks ID count:{tamañoMuestra[2]}")
        print("--------------------------")

        print("\nThe first 3 and last 3 artists in range are...\n")
        print(tabulate(lastArtists, headers='firstrow', tablefmt='fancy_grid',stralign='center', numalign='center'))
        print("\nThe first 3 and last 3 Albums in range are...\n")
        print(tabulate(lastAlbums, headers='firstrow', tablefmt='fancy_grid',stralign='center', numalign='center'))
        print("\nThe first 3 and last 3 Songs in range are...\n")
        print(tabulate(lastSongs, headers='firstrow', tablefmt='fancy_grid', stralign='center', numalign='center'))
        
        print("tamaño muestra:",lt.size(userCatalog['canciones'])+lt.size(userCatalog['albums'])+lt.size(userCatalog['artists']))

#REQ 1 START UP. 

    elif int(inputs[0]) == 2:

        
        print("================ Req No. 1 Input ================\n")
        while True:
            añoInicial = int(input("Año inicial del periodo a consultar (con formato AAAA):"))
            añoFinal = int(input("Año final del periodo a consultar (con formato AAAA):"))
            if añoInicial>añoFinal:
                print("Ingreso una fecha inicial mayor a la final. Porfavor ingrese las fechas de nuevo.\n")
            else: break
        start_time = getTime()
        print("================ Req No. 1 Answer ================\n")
        rangedAlbum = controller.rangedAlbum(userCatalog, añoInicial, añoFinal)
        mainHeaders = [['Nombre Album', 'Lanzamiento','Tipo_album','album artista\s','total_tracks']]

        
        print('The first 3 albums in the range are...')
        print(tabulate(rangedAlbum[:4], headers='firstrow', tablefmt='fancy_grid',stralign='left', numalign='left'))
        print('The last 3 albums in the range are...')
        print(tabulate(rangedAlbum[-3:], headers='firstrow', tablefmt='fancy_grid',stralign='left', numalign='left'))
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        

#REQ 2 START UP.--------------------------------------------

    elif int(inputs[0]) == 3:

        
        print("================ Req No. 2 Input ================\n")
        N = input("ingrese el tamaño del grupo de artistas a encontrar (ej.: TOP 3, 5, 10 o 20):\n")
        if N not in 'TOP':
            N = int(N)
        else: N = 1
        sortedArtists = controller.sortArtists(userCatalog)
        TopArtists = controller.topArtists(sortedArtists, userCatalog, N)

        start_time = getTime()

        print("================ Req No. 2 Answer ================\n")
        print("The first 3 and last 3 arists in the top",str(N)," are...")
        print(tabulate(TopArtists, headers='firstrow', tablefmt='fancy_grid',stralign='left', numalign='left'))
        end_time = getTime()

        delta_time = deltaTime(start_time, end_time)
        

#REQ 3 START UP. 
 

    elif int(inputs[0]) == 4:
        
        print("================ Req No. 3 Input ================\n")
        N = input("ingrese el tamaño de canciones a identificar (ej.: TOP 3, 5, 10 o 20):\n").upper()
        if N not in 'TOP':
            N = int(N)
        else: N = 1
        sortedSongs = controller.sortSongs(userCatalog)
        TopSongs = controller.TopSongs(sortedSongs, userCatalog, N)

        start_time = getTime()

        print("================ Req No. 3 Answer ================\n")
        print("The first 3 and last 3 arists in the top",str(N)," are...\n")
        print(tabulate(TopSongs, headers='firstrow', tablefmt='fancy_grid',stralign='left', numalign='left'))
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        
    
#REQ 4 START UP

    elif int(inputs[0]) == 5:

        print("================ Req No. 4 Inputs ================\n")
        nombre = input("Ingrese el nombre del artista a consultar:\n").lower()
        
        #Obtener el codigo del pais mediante la funcion seach_fuzzy de la libreria Pycountry
        pais = input("Ingrese el pais\mercado para la busqueda:\n")
        infoPais = pycountry.countries.search_fuzzy(pais)
        codigoPais = infoPais[0].alpha_2

        start_time = getTime()

        print("================ Req No. 4 Answer ================\n")

        print('la cancion mas popular del artista',nombre,'con disponiblidad en',pais,'es...\n')
        artistSongs = controller.aristsSongs(userCatalog, nombre, codigoPais)
        print(tabulate(artistSongs, headers='firstrow', tablefmt='fancy_grid',stralign='left', numalign='left'))
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        
        
        
    
#REQ 5 START UP

    elif int(inputs[0]) == 6:
        
        print("================ Req No. 5 Inputs ================\n")
        nombre = input("Ingrese el nombre del artista para consultar su discografia:\n").lower()

        start_time = getTime()

        print("================ Req No. 5 Answer ================\n")
        cantidadAlbums = controller.ctdAlbums(userCatalog, nombre)
        print(f"Number of 'compilation': {cantidadAlbums[2]}\nNumber of 'single': {cantidadAlbums[1]}\nTotal albums in discography:{cantidadAlbums[0]}")
        headers = controller.albumsArt(userCatalog, nombre)
        
        print("\n the first and last 3 tracks in the range are...")
        print(tabulate(headers[0][0:4], headers='firstrow', tablefmt='fancy_grid',stralign='left', numalign='left'))
        print("\n For the albums these are the most popular songs...")
        print(tabulate(headers[1][0:4], headers='firstrow', tablefmt='fancy_grid',stralign='left', numalign='left'))
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        


#BONO START UP. inconluso--------------------------------------------

    elif int(inputs[0]) == 7:

        print("================ BONO Inputs ================\n")
        añoInicial = int(input("Ingrese el año inicial del periodo. Use el formato (AAAA):\n"))
        añoFinal = int(input("Ingrese el año final del periodo. Use el formato (AAAA):\n"))
        N = input("ingrese el tamaño de canciones a identificar (ej.: TOP 3, 5, 10 o 20):\n")
        if N not in 'TOP':
            N = int(N)
        else: N = 1
        start_time = getTime()
        sortedSongs = controller.sortBonoSongs(userCatalog)
        rangedSongs = controller.rangedBonoSongs(userCatalog, sortedSongs, añoInicial, añoFinal, N)

        print("================ BONO Answer ================\n")
        print("las tres primeras canciones son...")
        print(tabulate(rangedSongs[:4], headers='firstrow', tablefmt='fancy_grid',stralign='left', numalign='left'))
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        

#EXIT

    elif int(inputs[0]) == 0:
        sys.exit(0)

    else:
        continue
sys.exit(0)
