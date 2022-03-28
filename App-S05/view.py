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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from datetime import datetime


default_limit = 1000
sys.setrecursionlimit(default_limit*10)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

#FUNCIONES FUNCIONES FUNCIONES FUNCIONES FUNCIONES FUNCIONES FUNCIONES FUNCIONES FUNCIONES FUNCIONES
def newController():
    control = controller.newController()
    return control

def printMenu():
    print("\n"+"Bienvenido")
    print("1- Cargar toda información en el catálogo")
    print("2- Listar los albumes en un periodo de tiempo")
    print("3- Encontrar los TOP N artistas más populares")
    print("4- Clasificar las canciones por popularidad")
    print("5- Encontrar la canción más popular de un artista")
    print("6- Encontrar la discografía de un artista")
    print("7- Clasificar las canciones con mayor distribución")
    print("0- Salir")

def loadData():
    can, art, alb = controller.loadData(control)
    return can, art, alb
           
def printInfo1(tracks, artists, albums):
    size1 = lt.size(tracks)
    if size1:
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('ESTAS SON LAS CANCIONES CARGADAS:')
        i=0
        for track in lt.iterator(tracks):
            if i == 3:
                print("---------------->")
                print("")
                print("...")
                print("...")
                print("...")
                print("")        
            print("---------------->")                            
            print('Nombre: '+track['name']+"\n"+
                  'Duracion: '+track['duration_ms']+"\n"+
                  'Numero en album: '+track['track_number'])          
            i+=1 
    else:
        print('No se encontraron canciones')

    size2 = lt.size(artists)
    if size2:
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('ESTOS SON LOS ARTISTAS CARGADOS:')
        i=0
        for artist in lt.iterator(artists):
            if i == 3:
                print("---------------->")
                print("")
                print("...")
                print("...")
                print("...")
                print("")
            print("---------------->")          
            print('Nombre: '+artist['name']+"\n"+
                  'Generos: '+artist['genres']+"\n"+
                  'Popularidad: '+str(artist['artist_popularity'])+"\n"+
                  'Seguidores: '+artist['followers'])          
            i+=1 
    else:
        print('No se encontraron artistas')

    size3 = lt.size(albums)
    if size3:
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('ESTOS SON LOS ALBUMES CARGADOS:')
        i=0
        for album in lt.iterator(albums):
            if i == 3:
                print("---------------->")
                print("")
                print("...")
                print("...")
                print("...")
                print("")
            print("---------------->")            
            print('Nombre: '+album['name']+"\n"+
                  'Tipo: '+album['album_type']+"\n"+
                  'Mercados: '+album['available_markets']+"\n"+
                  'Lanzamiento: '+str(album['release_date'])[0:10])          
            i+=1 
    else:
        print('No se encontraron albumes')

def printInfo2(albums_en_rango):
    size = lt.size(albums_en_rango)
    if size:
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('ESTOS SON LOS ALBUMES DENTRO DEL RANGO:')
        i=0
        for album in lt.iterator(albums_en_rango):
            if i == 3:
                print("---------------->")
                print("")
                print("...")
                print("...")
                print("...")
                print("")        
            print("---------------->")                            
            print('Nombre: '+album['name']+"\n"+
                  'Lanzamiento: '+str(album['release_date'])[0:10]+"\n"+
                  'Tipo: '+album['album_type']+"\n"+
                  'Artista: '+album['artist_name']+"\n"+
                  'Numero de canciones: '+str(int(float(album['total_tracks']))))          
            i+=1 
    else:
        print('No se encontraron albumes dentro del rango')
    
def printInfo3(top_n_artistas, top_n):
    size = lt.size(top_n_artistas)
    if size:
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('ESTOS SON LOS TOP '+str(top_n)+' ARTISTAS:')
        i=0
        for artist in lt.iterator(top_n_artistas):
            if i == 3:
                print("---------------->")
                print("")
                print("...")
                print("...")
                print("...")
                print("")        
            print("---------------->")                            
            print('Nombre: '+artist['name']+"\n"+
                'Popularidad: '+str(artist['artist_popularity'])+"\n"+
                'Seguidores: '+str(artist['followers'])+"\n"+
                'Generos: '+artist['genres']+"\n"+
                'Mejor cancion: '+artist['best_track'])          
            i+=1 
    else:
        print('No se encontraron artistas para ese TOP N')

def printInfo4(top_n_tracks, top_n):
    size = lt.size(top_n_tracks)
    if size:
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('ESTOS SON LOS TOP '+str(top_n)+' CANCIONES:')
        i=0
        for track in lt.iterator(top_n_tracks):
            if i == 3:
                print("---------------->")
                print("")
                print("...")
                print("...")
                print("...")
                print("")        
            print("---------------->")                            
            print('Nombre: '+str(track['name'])+"\n"+
                'Popularidad: '+str(track['popularity'])+"\n"+
                'Duracion: '+str(track['duration_ms'])+"\n"+
                'Album: '+str(track['album_name'])+"\n"+
                'Artistas: '+str(track['artists_names_str']))          
            i+=1 
    else:
        print('No se encontraron artistas para ese TOP N')

def printInfo5(info5):
    track = info5[0]
    total_canciones = info5[1]
    total_albumes = info5[2]
    nombre_artista = info5[3]
    territorio = info5[4]
    print("\n"+"-----------------------------------------------------------------------------------------------")
    print('TOTAL CANCIONES: '+str(total_canciones))
    print('TOTAL ALBUMES: '+str(total_albumes))
    print("\n"+"-----------------------------------------------------------------------------------------------")
    print('LA CANCION MAS POPULAR DE '+nombre_artista+' EN EL PAIS '+territorio+' ES:')
    print('Nombre: '+str(track['name'])+"\n"+
            'Album: '+str(track['album_name'])+"\n"+
            'Lanzamiento: '+str(track['release_date'])+"\n"+
            'Artistas: '+str(track['artists_names_str'])+"\n"+
            'Duracion: '+str(track['duration_ms'])+"\n"+
            'Popularidad: '+str(track['popularity'])+"\n"+
            'URL: '+str(track['preview_url']))
    if track['lyrics'] != '':
        print('Letra: '+str(track['lyrics'])[0:200]+' [...] \"')
    else:
        print('Letra de la cancion NO disponible')  

def printInfo6(discografia):
    singles = discografia[1]
    compilations = discografia[2]
    albums = discografia[3]
    print("\n"+"-----------------------------------------------------------------------------------------------")
    print('TOTAL SINGLES: '+str(singles))
    print('TOTAL COMPILATIONS: '+str(compilations))
    print('TOTAL ALBUMS: '+str(albums))
    print("\n"+"-----------------------------------------------------------------------------------------------")
    
    size = lt.size(discografia[0])
    if size:
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('ESTOS SON LOS ALBUMES DEL ARTISTA:')
        i=0
        for album in lt.iterator(discografia[0]):
            if i == 3:
                print("---------------->")
                print("")
                print("...")
                print("...")
                print("...")
                print("")        
            print("---------------->")                            
            print('Nombre: '+str(album['name'])+"\n"+
                'Lanzamiento: '+str(album['release_date'])+"\n"+
                '# de canciones: '+str(album['total_tracks'])+"\n"+
                'Tipo: '+str(album['album_type'])+"\n"+
                'Artista: '+str(album['artist_name']))          
            i+=1 
    else:
        print('No se encontraron albumes para dicho artista') 

    
    if size:
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('ESTAS SON LAS CANCIONES MAS POPULARES DE CADA ALBUM:')
        i=0
        for album in lt.iterator(discografia[0]):
            if i == 3:
                print("---------------->")
                print("")
                print("...")
                print("...")
                print("...")
                print("")        
            print("---------------->")                            
            print('Nombre: '+str(album['top_track']['name'])+"\n"+
            'Album: '+str(album['top_track']['album_name'])+"\n"+
            'Artistas: '+str(album['top_track']['artists_names_str'])+"\n"+
            'Duracion: '+str(album['top_track']['duration_ms'])+"\n"+
            'Popularidad: '+str(album['top_track']['popularity'])+"\n"+
            'UR: '+str(album['top_track']['preview_url']))
            if album['top_track']['lyrics'] != '':
                print('Letra: '+str(album['top_track']['lyrics'])[0:200]+' [...] \"')
            else:
                print('Letra de la cancion NO disponible')  
            i+=1 
    else:
        print('No se encontraron albumes para dicho artista') 
    
def printInfo7(top_n_canciones, top_n):
    size = lt.size(top_n_canciones)
    if size:
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('ESTOS SON LAS TOP '+str(top_n)+' CANCIONES POR DISTRIBUCION:')
        i=0
        for track in lt.iterator(top_n_canciones):
            if i == 3:
                print("---------------->")
                print("")
                print("...")
                print("...")
                print("...")
                print("")        
            print("---------------->")                            
            print('Nombre: '+str(track['name'])+"\n"+
                'Album: '+str(track['album_name'])+"\n"+
                'Artistas: '+str(track['artists_names_str'])+"\n"+
                'Paises distribucion: '+str(track['distribution'])+"\n"+
                'Popularidad: '+str(track['popularity'])+"\n"+
                'Duracion: '+str(track['duration_ms'])+"\n"+
                'Lanzamiento: '+str(track['release_date']))          
            i+=1 
    else:
        print('No se encontraron canciones para ese TOP N')



#PROGRAMA PRINCIPAL PROGRAMA PRINCIPAL PROGRAMA PRINCIPAL

control = newController()
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    
    if int(inputs[0]) == 1:
        print("CARGANDO INFORMACION DE LOS ARCHIVOS ....")
        can, art, alb = loadData()
        print("\n"+"-----------------------------------------------------------------------------------------------")
        print('Canciones cargadas: ' + str(can))
        print('Artistas cargados: ' + str(art))
        print('Albumes cargados: ' + str(alb))
        print("-----------------------------------------------------------------------------------------------")
        printInfo1(controller.getInfo1(control)[0], controller.getInfo1(control)[1], controller.getInfo1(control)[2])

    elif int(inputs[0]) == 2:

        inicial = datetime.strptime(input('Ingrese el año inicial AAAA\n'),"%Y")
        final = datetime.strptime(input('Ingrese el año final AAAA\n'),"%Y")
        printInfo2(controller.getInfo2(control, inicial, final))

    elif int(inputs[0]) == 3:
        top_n = int(input('Ingrese cuantos artistas TOP desea conocer:\n'))
        printInfo3(controller.getInfo3(control, top_n), top_n)


    elif int(inputs[0]) == 4:
        top_n = int(input('Ingrese cuantas canciones TOP desea conocer:\n'))
        printInfo4(controller.getInfo4(control, top_n), top_n)
        pass

    elif int(inputs[0]) == 5:
        nombre_artista = input('Ingrese el nombre del artista a buscar:\n')
        territorio = input('ingrese el territorio:\n')
        printInfo5(controller.getInfo5(control, nombre_artista, territorio))

    elif int(inputs[0]) == 6:
        nombre_artista = input('Ingrese el nombre del artista para conocer su discografia:\n')
        printInfo6(controller.getInfo6(control, nombre_artista))
    
    elif int(inputs[0]) == 7:
        inicial = datetime.strptime(input('Ingrese el año inicial AAAA\n'),"%Y")
        final = datetime.strptime(input('Ingrese el año final AAAA\n'),"%Y")
        top_n = int(input('Ingrese el numero TOP de canciones a identificar'))
        printInfo7(controller.getInfo7(control, inicial, final, top_n), top_n)


    elif int(inputs[0]) == 0:
        sys.exit(0)

    else:
        continue
sys.exit(0)


print('Indique el numero de Top Artistas que quiere conocer:', )