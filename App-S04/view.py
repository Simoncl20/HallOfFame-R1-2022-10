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

from platform import java_ver
from model import deltaTime, getTime
import config as cf
import sys
import pycountry

default_limit = 1000
sys.setrecursionlimit(default_limit * 10)
import controller
from DISClib.ADT import list as lt

assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control


def printMenu():
    print("\nBienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar los álbumes en un periodo de tiempo ")
    print("3- Encontrar el TOP ? de los artistas: ")
    print("4- Encontrar el TOP ? de las canciones: ")
    print("5-Econtrar canción más popular de un artista")
    print("6- Encontrar la discografía de un artista")
    print("0- Salir")


def printOpcion6():
    """
    Muestra al usuario las opciones de cargar los datos en las listas (ARRAY_LIST o SINGLE_LINKED)
    """
    print("\nLas opciones son: ")
    print("1- Lista tipo array")
    print("2- Lista encadenada")


def printOpcionesOrd():
    """Opciones de algoritmos de ordenamiento"""
    print('\nSeleccione el algoritmo de ordenamiento que desea usar: ')
    print('1- Selection Sort')
    print('2- Insertion Sort')
    print('3- Shell Sort')
    print('4- Quick Sort')
    print('5- Merge Sort')


catalog = None


def loadData(control):
    """Solicita al controlador que cargue los datos en el mod"""
    songs, artists, albums = controller.loadData(control)
    return songs, artists, albums


# Se crea el controlador asociado a la vista
control = newController()
catalog = control['model']


# Se crea un contralador alternativo para el caso de querer decidir el tipo de lista (opción 6)
def newControllerType():
    """
    Se crea una instancia del controlador para el caso del uso de la opción 6
    """
    control = controller.newControllerType()
    return control


control_type = newControllerType()

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('\nSeleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        start_time = getTime()
        songs, artists, albums = loadData(control)
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Tiempo de carga de los datos: ", delta_time, ' ms.')
        print("Canciones cargadas: " + str(songs))
        print("Artistas cargados: " + str(artists))
        print("Albumes cargados: " + str(albums))

        print("Primeras 3 canciones cargadas: \n")

        for i in range(3):
            cancion1 = controller.getSong(catalog, i + 1)
            print("Canción " + str(i + 1) + ":\nNombre: " + cancion1['name'] + "\n" + "Países disponibles: " + cancion1[
                'available_markets'])
            print("Duración en ms: " + cancion1['duration_ms'] + '\n' + "Canción #" + cancion1[
                'track_number'] + " en el albúm\n")

        print("Ultimas 3 canciones cargadas: \n")

        for i in range(3):
            cancion1 = controller.getSong(catalog, songs - i)
            print("Canción " + str(songs - i) + ":\nNombre: " + cancion1['name'] + "\n" + "Países disponibles: " +
                  cancion1['available_markets'])
            print("Duración en ms: " + cancion1['duration_ms'] + '\n' + "Canción #" + cancion1[
                'track_number'] + " en el albúm\n")

        print("Primeros 3 álbumes cargados: \n")

        for i in range(3):
            album = controller.getAlbum(catalog, i + 1)
            print(
                "Albúm " + str(i + 1) + ":\nNombre: " + album['name'] + '\n' + "Tipo de albúm: " + album['album_type'])
            print("Países disponibles: " + album['available_markets'] + '\n' + "Fecha de lanzamiento: " + album[
                'release_date'] + '\n')

        print("Ultimos 3 álbumes cargados: \n")

        for i in range(3):
            album = controller.getAlbum(catalog, albums - i)
            print("Albúm " + str(albums - i) + ":\nNombre: " + album['name'] + '\n' + "Tipo de albúm: " + album[
                'album_type'])
            print("Países disponibles: " + album['available_markets'] + '\n' + "Fecha de lanzamiento: " + album[
                'release_date'] + '\n')

        print("Primeros 3 artistas cargados: \n")

        for i in range(3):
            artista = controller.getArtist(catalog, i + 1)
            print("Artista " + str(i + 1) + "\nNombre: " + artista['name'] + '\nGéneros: ' + artista['genres'])
            print("Popularidad: " + artista['artist_popularity'] + '\nNúmero de seguidores: ' + artista[
                'followers'] + '\n')

        print("Ultimos 3 artistas cargados: \n")

        for i in range(3):
            artista = controller.getArtist(catalog, artists - i)
            print("Artista " + str(artists - i) + "\nNombre: " + artista['name'] + '\nGéneros: ' + artista['genres'])
            print("Popularidad: " + artista['artist_popularity'] + '\nNúmero de seguidores: ' + artista[
                'followers'] + '\n')

    elif int(inputs[0]) == 2:
        anoI = int(input("Ingrese año inicial del periodo: "))
        anoF = int(input("Ingrese año final del periodo: "))

        albumesEnPeriodo, size, delta_time = controller.albumsInTimePeriod(anoI, anoF, control)

        if (albumesEnPeriodo == 0):
            print("Periodo no valido para el catálogo")
            break

        print("Hay ", size, " álbumes en el periodo ", anoI, "-", anoF)
        print("Tiempo de ejecución del requerimiento 1: ", delta_time, ' ms.')

        print("\nPrimeros 3 álbumes en el periodo: \n")

        for i in range(3):
            album = controller.getElement(albumesEnPeriodo, i + 1)
            print("\nAlbúm " + str(i + 1) + ":\nname: " + album['name'] + '\nalbum_type: ' + album['album_type'])
            print("release_date: " + album['release_date'] + '\nartist_album_name: ' + album[
                'artist_name'] + '\nexternal_urls: ' + album['external_urls'])

        print("\nUltimos 3 álbumes en el periodo: \n")

        for i in range(3):
            album = controller.getElement(albumesEnPeriodo, size - i)
            print("\nAlbúm " + str(size - i) + ":\nname: " + album['name'] + '\nalbum_type: ' + album['album_type'])
            print("release_date: " + album['release_date'] + '\nartist_album_name: ' + album[
                'artist_name'] + '\nexternal_urls: ' + album['external_urls'])

    elif int(inputs[0])==3:

        #Se solicita al usuario que ingrese la cantidad
        cantidad=int(input("Cantidad de artistas: "))
        artistasOrganizados, delta_time=controller.getTopXArtists(cantidad, control["model"])
        print("Tiempo de ejecución del requerimiento 2: ", delta_time, " ms. ")

        print("\u0332".join("Detalle de los 3 primeros artistas del TOP "+str(cantidad)))
        for i in range(1,4):
            print("Artista " + str(i) + ":")
            print("Nombre: " + lt.getElement(artistasOrganizados, i)["name"])
            print("Popularidad: " + lt.getElement(artistasOrganizados, i)["artist_popularity"])
            print("Seguidores: " + lt.getElement(artistasOrganizados, i)["followers"])
            print("Géneros: " + lt.getElement(artistasOrganizados, i)["genres"])
            idCancion=lt.getElement(artistasOrganizados, i)["track_id"]
            cancion=controller.buscarCancionID(control["model"],idCancion)
            if cancion[2]==0:
                if idCancion==cancion[1]:
                    nombreCancion=cancion[0]
                else:
                    nombreCancion="No se encontró la canción en la lista"
            else:
                nombreCancion=cancion[0]
            print("Canción referente: " + nombreCancion)
        print("\u0332".join("Detalle de los 3 últimos artistas del TOP " + str(cantidad)))
        for i in range(cantidad-2,cantidad+1):
            print("Artista " + str(i) + ":")
            print("Nombre: " + lt.getElement(artistasOrganizados, i)["name"])
            print("Popularidad: " + lt.getElement(artistasOrganizados, i)["artist_popularity"])
            print("Seguidores: " + lt.getElement(artistasOrganizados, i)["followers"])
            print("Géneros: " + lt.getElement(artistasOrganizados, i)["genres"])
            idCancion = lt.getElement(artistasOrganizados, i)["track_id"]
            cancion = controller.buscarCancionID(control["model"], idCancion)
            if cancion[2] == 0:
                if idCancion == cancion[1]:
                    nombreCancion = cancion[0]
                else:
                    nombreCancion = "No se encontró la canción en la lista"
            else:
                nombreCancion = cancion[0]
            print("Canción referente: " + nombreCancion)
    elif int(inputs[0]) == 4:
        top = int(input("TOP ?: "))
        topSongs, delta_time = controller.getTopXsongs(top, control)
        delta_time = f"{delta_time:.3f}"

        print("Tiempo de ejecución del requerimiento 3: ", delta_time, ' ms.')

        print("\nPrimeras 3 canciones en el top ", top)

        for i in range(3):
            cancion1 = controller.getElement(topSongs, i + 1)
            print("\nCanción TOP " + str(i + 1) + ":\nnombre: " + cancion1['name'] + "\nnombre del album: " + cancion1[
                'album_name'])
            print("artistas involucrados: ")
            artist_names = cancion1['artist_names']
            for i in range(1, lt.size(artist_names) + 1):
                print(controller.getElement(artist_names, i))
            print("Popularidad: " + cancion1['popularity'])
            print("duración: " + cancion1['duration_ms'] + ' ms' + '\n' + "Enlace externo: " + cancion1['href'])

            if cancion1['lyrics'] != '-99':
                print('letra: ' + cancion1['lyrics'][0:60] + "...")
            else:
                print('Letra de la canción NO disponible')

        print("\nUltimas 3 canciones en el top: \n")

        for i in range(3):
            cancion1 = controller.getElement(topSongs, top - 2 + i)
            print("\nCanción TOP " + str(top + i - 2) + ":\nnombre: " + cancion1['name'] + "\nnombre del album: " +
                  cancion1['album_name'])
            print("artistas involucrados: ")
            artist_names = cancion1['artist_names']
            for i in range(1, lt.size(artist_names) + 1):
                print(controller.getElement(artist_names, i))
            print("Popularidad: " + cancion1['popularity'])
            print("duración: " + cancion1['duration_ms'] + ' ms' + '\n' + "Enlace externo: " + cancion1['href'])

            if cancion1['lyrics'] != '-99':
                print('letra: ' + cancion1['lyrics'][0:60] + "...")
            else:
                print('Letra de la canción NO disponible')

    elif int(inputs[0]) == 5:
        artistName = input("Ingrese el nombre del artista: ")
        country = input("Ingrese el nombre del país/mercado disponible de la canción (en ingles): ")

        bestSongs, artist, delta_time = controller.getBestSongs(artistName, country, control)

        print("\nTiempo de ejecución del requerimiento 4: ", delta_time, ' ms.')

        if bestSongs == 0:
            print("\nNo se encontró el nombre del artista")
        if lt.size(bestSongs) == 0:
            print("\nNo se encontraron canciónes para ", artist['name'], "en ", country)
        else:
            print("\nDiscografia disponible de ", artist['name'], " en " + country)
            print("\nAlbumes disponibles: ", controller.getArtistAlbumNumber(artist))
            print("Canciones disponibles: ", controller.getArtistSongNumber(artist))

            print("\nLa canción más popular en en el país es: ")
            cancion1 = controller.getElement(bestSongs, 1)
            print("Nombre: " + cancion1['name'] + "\nnombre del album: " + cancion1['album_name'])
            print("artistas involucrados: ")
            artist_names = cancion1['artist_names']
            for i in range(1, lt.size(artist_names) + 1):
                print(controller.getElement(artist_names, i))
            print("Popularidad: " + cancion1['popularity'])
            print("duración: " + cancion1['duration_ms'] + ' ms' + '\n' + "Enlace externo: " + cancion1['href'])

            if cancion1['lyrics'] != '-99':
                print('letra: ' + cancion1['lyrics'][0:60] + "...")
            else:
                print('Letra de la canción NO disponible')

    elif int(inputs[0])==6:
        nombreArtista=input("Ingresar el nombre del artista: ")
        valores=controller.numeroAlbumesPorTipoPorArtista(control["model"], nombreArtista)
        print("\nTiempo de ejecución del requerimiento 5: ", valores[5], " ms.")
        if valores=="No se encontró el artista":
            print("\u0332".join("No se encontró el artista"))
            continue
        else:
            print("\u0332".join("Número de álbumes de tipo Single: ")+str(valores[0]))
            print("\u0332".join("Número de álbumes de tipo Compilación: ") + str(valores[1]))
            print("\u0332".join("Número de álbumes de tipo Álbum: ") + str(valores[2]))
            albumes=valores[3]
            tamanoAlbumes=lt.size(albumes)
            canciones=valores[4]
            if lt.size(albumes)>=3:
                for i in range(1,4):
                    print("\u0332".join("\nAlbum "+str(i)))
                    print("Fecha: "+lt.getElement(albumes,i)["release_date"])
                    print("Nombre: "+lt.getElement(albumes,i)["name"])
                    print("Número de canciones: "+str(lt.getElement(albumes,i)["total_tracks"]))
                    print("Tipo de álbum: "+lt.getElement(albumes,i)["album_type"])
                    print("Nombre del artista: " + nombreArtista)
                for i in range(tamanoAlbumes-2,tamanoAlbumes+1):
                    print("\u0332".join("\nAlbum " + str(i)))
                    print("Fecha: " + lt.getElement(albumes, i)["release_date"])
                    print("Nombre: " + lt.getElement(albumes, i)["name"])
                    print("Número de canciones: " + str(lt.getElement(albumes, i)["total_tracks"]))
                    print("Tipo de álbum: " + lt.getElement(albumes, i)["album_type"])
                    print("Nombre del artista: " + nombreArtista)
            else:
                for i in range(1,lt.size(albumes)+1):
                    print("\u0332".join("\nAlbum " + str(i)))
                    print("Fecha: " + lt.getElement(albumes, i)["release_date"])
                    print("Nombre: " + lt.getElement(albumes, i)["name"])
                    print("Número de canciones: " + str(lt.getElement(albumes, i)["total_tracks"]))
                    print("Tipo de álbum: " + lt.getElement(albumes, i)["album_type"])
                    print("Nombre del artista: " +nombreArtista)

            cancionesPorAlbum=lt.newList("ARRAY_LIST")
            for i in range(lt.size(albumes)):
                cancionesAlbum=lt.newList("ARRAY_LIST")
                for j in range(lt.size(canciones)):
                    if lt.getElement(canciones,j)["album_id"]==lt.getElement(albumes,i)["id"]:
                        lt.addLast(cancionesAlbum,lt.getElement(canciones,j))
                lt.addLast(cancionesPorAlbum,cancionesAlbum)

            if lt.size(albumes) >= 3:
                for j in range(1,4):
                    listaOrdenada=controller.mergeSortSongList(lt.getElement(cancionesPorAlbum,i))[0]
                    cancionPopular=lt.getElement(listaOrdenada,1)
                    print("\u0332".join("\nCanción más popular del album " + str(j)))
                    print("Nombre: "+cancionPopular["name"])
                    print("Artistas: " + nombreArtista)
                    print("Duración: " + cancionPopular["duration_ms"])
                    print("Popularidad: " + cancionPopular["popularity"])
                    print("Enlace al audio de muestra: " + cancionPopular["preview_url"])
                    if cancionPopular["lyrics"]!="-99":
                        print("Letra: " + cancionPopular["lyrics"][0:60]+"...")
                    else:
                        print("Letra de la canción NO disponible")
            else:
                for j in range(1,lt.size(albumes)+1):
                    listaOrdenada=controller.mergeSortSongList(lt.getElement(cancionesPorAlbum,i))[0]
                    cancionPopular=lt.getElement(listaOrdenada,1)
                    print("\u0332".join("\nCanción más popular del album " + str(j)))
                    print("Nombre: "+cancionPopular["name"])
                    print("Artistas: " + nombreArtista)
                    print("Duración: " + cancionPopular["duration_ms"])
                    print("Popularidad: " + cancionPopular["popularity"])
                    print("Enlace al audio de muestra: " + cancionPopular["preview_url"])
                    if cancionPopular["lyrics"]!="-99":
                        print("Letra: " + cancionPopular["lyrics"][0:60]+"...")
                    else:
                        print("Letra de la canción NO disponible")
    elif int(inputs[0]) == 0:
        sys.exit(0)

    else:
        continue

sys.exit(0)

