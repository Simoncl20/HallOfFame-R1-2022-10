"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

from re import I
from termios import INLCR
import config as cf
import time
from datetime import datetime
import pycountry
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as isort
from DISClib.Algorithms.Sorting import selectionsort as ssort
from DISClib.Algorithms.Sorting import quicksort as qsort
from DISClib.Algorithms.Sorting import mergesort as msort

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


# Construccion de modelos


def newCatalog():
    """
    Inicializa el catálogo de canciones, artistas y albumes. Crea una lista vacia
    para las canciones, una para los artistas y una para los
    albumes. Retorna el catalogo inicializado.
    """
    catalog = {'songs': None,
               'artists': None,
               'albums': None}

    catalog['songs'] = lt.newList('ARRAY_LIST', cmpfunction=compareSongs)
    catalog['artists'] = lt.newList('ARRAY_LIST', cmpfunction=compareArtists)
    catalog['albums'] = lt.newList('ARRAY_LIST', cmpfunction=compareAlbums)


    return catalog


# Función para el lab 4:

def newCatalogType(list_type):
    """
    Inicializa un catálogo de canciones, artistas y albumes según el tipo de lista ingresado por usuario para el lab 4.
    Crea una lista vacia
    para las canciones, una para los artistas y una para los
    albumes. Retorna el catalogo inicializado.
    """
    catalog = {'songs': None,
               'artists': None,
               'albums': None}

    catalog['songs'] = lt.newList(list_type)
    catalog['artists'] = lt.newList(list_type)
    catalog['albums'] = lt.newList(list_type)

    return catalog


def subList(list, n):
    """retorna una sublista desde la posición 1 hasta n de la lista ingresada por parametro"""
    return lt.subList(list, 1, n)


def truncarCatalogo(catalog, pct):
    """
    Reduce la cantidad de datos al porcentaje ingresado en parametro.
    Args:
        catalog: catalogo a truncar
        pct: porcentaje de la cantidad original de datos que se quiere usar
    """
    new_songs = subList(catalog["songs"], int(pct * songSize(catalog)))
    new_artists = subList(catalog["artists"], int(pct * artistSize(catalog)))
    new_albums = subList(catalog["albums"], int(pct * albumSize(catalog)))

    catalog['songs'] = new_songs
    catalog['artists'] = new_artists
    catalog['albums'] = new_albums


# Funciones para agregar informacion al catalogo

def addSong(catalog, song):
    # se añade el nombre del album al que pertenece la canción
    addSongAlbum(catalog, song)

    # se crea un lista vacia para guardar los nombres de los artistas
    song['artist_names'] = lt.newList()
    idList = song['artists_id'].strip('][').replace("'", '').replace(' ', '').split(',')
    for id in idList:
        addSongArtist(id, catalog, song)

    # se adiciona la canción a la lista de canciones
    lt.addLast(catalog['songs'], song)
    return catalog


def addSongArtist(id, catalog, song):
    '''
    Añade un artista a la lista de nombres de los artistas involucrados de la canción
    Añade la canción a la lista de canciones de los artistas involucrados.
    '''
    artists = catalog['artists']
    # Busca la posición del artista en el catalogo de artistas según el id
    posArtist = lt.isPresent(artists, id)
    if posArtist > 0:
        artist = lt.getElement(artists, posArtist)
        name = artist['name']
        lt.addLast(song['artist_names'], name)
        lt.addLast(artist['songs'], song)
    else:
        lt.addLast(song['artist_names'], "NONAME")
    return catalog


def addSongAlbum(catalog, song):
    """
    Agrega el nombre del album a la cancion bajo la llave 'album_name
    """
    albums = catalog['albums']
    # se busca la posición del album en el catalogo según el id
    posAlbum = lt.isPresent(albums, song['album_id'])
    if posAlbum > 0:
        song['album_name'] = lt.getElement(albums, posAlbum)['name']
    else:
        song['album_name'] = "no se encontró el album"
    return catalog


def addArtist(catalog, artist):
    # se crea una lista vacia para guardar la canciones del artist  a (para requerimiento 4)
    artist['songs'] = lt.newList()
    # se crea una lista vacia para guardar los nombres de los albumes del artista (para requerimiento 4)
    artist['albums'] = lt.newList()
    # se adiciona el artista a la lista de artistas
    lt.addLast(catalog['artists'], artist)
    return catalog


def addAlbum(catalog, album):
    # se crea la categoria de 'artist_name' en el album
    artists = catalog['artists']
    # se busca la posición del artista en el catalogo de artistas según el id:
    posartist = lt.isPresent(artists, album['artist_id'])
    if posartist > 0:
        artist = lt.getElement(artists, posartist)
        # se añade el nombre del artista al album en la llave "artist_name"
        album['artist_name'] = artist['name']
        # se añade el album entero a la lista de albumes del artista
        lt.addLast(artist['albums'], album)
    else:
        album['artist_name'] = "no se encontró el nombre"
    # se adiciona el album a la lista de albumes
    lt.addLast(catalog['albums'], album)

    return catalog


# Funciones para creacion de datos


# Funciones de consulta

def songSize(catalog):
    return lt.size(catalog['songs'])


def artistSize(catalog):
    return lt.size(catalog['artists'])


def albumSize(catalog):
    return lt.size(catalog['albums'])


def getSong(catalog, number):
    '''Retorna una canción en una posición dada por parametro'''
    return lt.getElement(catalog["songs"], number)


def getArtist(catalog, number):
    '''Retorna el artista en una posición dada por parametro'''
    return lt.getElement(catalog["artists"], number)


def getAlbum(catalog, number):
    '''Retorna el album en una posición dada por parametro'''
    return lt.getElement(catalog["albums"], number)


def getElement(list, pos):
    return lt.getElement(list, pos)


def getAlbumYear(album):
    """
    Retorna el año de publicación de un album para la función de comparación por año.
    """
    ano = None
    # Revisa si el dato de fecha está en formato AAAA-MM-DD ó AAAA
    if album["release_date_precision"] == 'day':
        fecha = datetime.strptime(album["release_date"], "%Y-%m-%d")
        ano = fecha.year
    elif album["release_date_precision"] == 'year':
        ano = int(album["release_date"])
    else:
        ano = int('19' + album['release_date'][-2:])
    return ano


# (req1)
def albumsInTimePeriod(anoI, anoF, catalog):
    """
    Retorna la sublista de álbumes con años de publicación los años indicados por parametro
    Si el año superior del rango es más pequeño que el primer año de publicación, retorna 0
    Si el año inferior del rango es más grande que el ultimo año de publicación, retorna 0
    """
    # se ordenan los albumes por año de publicación
    albumsByYear, delta_time = mergeSortAlbumsbyYear(catalog)

    posI = 1
    posF = lt.size(albumsByYear)

    start_time = getTime()

    # condición para año superior del rango

    if getAlbumYear(lt.getElement(albumsByYear, posI)) > anoF:
        return 0, 0, 0

    # condición para año superior del rango
    if getAlbumYear(lt.getElement(albumsByYear, posF)) < anoI:
        return 0, 0, 0

    findI = False
    findF = False

    i = 1

    while (not findI) or (not findF):
        anoActual = getAlbumYear(lt.getElement(albumsByYear, i))

        if anoActual >= anoI and (not findI):
            posI = i
            findI = True

        if anoActual > anoF and (not findF):
            posF = i - 1
            findF = True

        i += 1

    albumsByPeriod = lt.subList(albumsByYear, posI, posF + 1 - posI)

    # se mide el tiempo de ejecución del algoritmo:
    end_time = getTime()
    delta_time1 = deltaTime(start_time, end_time)

    return albumsByPeriod, lt.size(albumsByPeriod), delta_time + delta_time1

#Req 2
def getTopXArtists(cantidad, catalog):
    #Se inicia la función de toma de tiempo
    start_time = getTime()
    #Se organizan los artistas por popularidad haciendo uso de Merge Sort 
    artistasOrganizados, tiempo=mergeSortArtists(catalog,lt.size(catalog["artists"]))
    #Se detiene la toma de tiempo
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return artistasOrganizados, delta_time
# req(3)
def getTopXsongs(top, catalog):
    '''
    Crea una sublista con los ultimos X elementos de la lista de canciones
    ordenas por popularidad.
    '''
    sortedSongs, delta_time = mergeSortSongs(catalog)
    # se mide el tiempo de ejecución después del algortimo de ordenamiento
    start_time = getTime()
    # creación de la sublista
    topSongs = lt.subList(sortedSongs, 1, top)
    end_time = getTime()
    # se suma el tiempo medido al tiempo del algoritmo
    delta_time += deltaTime(start_time, end_time)
    return topSongs, delta_time


# req(4):
def getBestSongs(artistName, country, catalog):
    """
    Retorna una lista ordenada por popularidad de las canciones asociadas
    al artista en el pais correspondiente.
    Retorna 0 si no encuentra al artista.
    Args:
        artistaName: str con el nombre del artista de interés
        country: str con el nombre del país.
    """
    artistSongs, artist = findArtistSongs(artistName, catalog)

    if artistSongs == 0:
        return 0, 0, 0

    songsByCountry, delta_time = getSongsByCountry(artistSongs, country)

    return songsByCountry, artist, delta_time


def findArtistSongs(artistName, catalog):
    '''
    Recorre la lista de artistas y retorna la lista de canciones del artista
    Retorna 0 si no la encuentra

    '''
    pos = 1
    artists = catalog['artists']
    for artist in lt.iterator(artists):
        if artist['name'].strip().lower() == artistName.strip().lower():
            return artist['songs'], artist
    return 0, 0


def getSongsByCountry(songs, country):
    """
    Retorna una lista de canciones disponibles en el pais indicado, ordenadas por popularidad de mayor a menor
    Retorna el tiempo de ejecución del ordenamiento

    """
    sortedSongs, delta_time = mergeSortSongList(songs)

    start_time = getTime()
    countryCode = pycountry.countries.search_fuzzy(country)[0].alpha_2
    SongsByCountry = lt.newList()
    for song in lt.iterator(sortedSongs):
        codeList = song['available_markets'].replace('"', '').strip('][').replace("'", '').replace(' ', '').split(',')
        for code in codeList:
            if code == countryCode:
                lt.addLast(SongsByCountry, song)
    end_time = getTime()
    delta_time += deltaTime(start_time, end_time)

    return SongsByCountry, delta_time


def getArtistSongNumber(artist):
    return lt.size(artist['songs'])


def getArtistAlbumNumber(artist):
    return lt.size(artist['albums'])


# Funciones utilizadas para comparar dentro de ordenamiento
def cmpArtistsbyFollowers(artist1, artist2):
    """
    Devuelve verdadero (true) si los follower de artist1 son menores que los de artist2
    Args:
        artist1: información del primer artista que incluye su valor 'followers'
        artist2: información del segundo artista que incluye su valor 'followers'
    """
    return (float(artist1['followers']) < float(artist2["followers"]))


def cmpAlbumByYear(album1, album2):
    """
    Retorna true si el año de publicación de album1 1 es menor al año de publicación de album2"
    Args:
        album1: info de primer album que contiene la información "release date"
        album2: info de segundo album que contiene la información "release date"
    """
    ano1 = getAlbumYear(album1)
    ano2 = getAlbumYear(album2)

    return (ano1 < ano2)


def cmpSong(song2, song1):
    '''
    Retorna True si la canción 1 es menos popular a la canción 2. En caso de que sean iguales
    retorna True si la canción 1 tiene menor duración que la canción 2. Si tienen misma duración
    retorna True si la canción 1 esta antes en orden alfabético a la canción 2, según el nombre.
    '''
    if float(song1['popularity']) < float(song2['popularity']):
        return True
    elif song1['popularity'] == song2['popularity']:
        if float(song1['duration_ms']) < float(song2['duration_ms']):
            return True
        elif float(song1['duration_ms']) == float(song2['duration_ms']):
            return (song1['name'].lower().strip() < song2['name'].lower().strip())
    else:
        return False

#REQ 5: 
    # Funciones de ordenamiento
def buscarCancionID(catalog,id):
    canciones=catalog["songs"]
    posCancion = lt.isPresent(canciones, id)
    nombreCancion=lt.getElement(canciones,posCancion)["name"]
    idCancion=lt.getElement(canciones,posCancion)["id"]
    return nombreCancion, idCancion, posCancion

def numeroAlbumesPorTipoPorArtista(catalog,artista):
    #Se empieza a medir el tiempo
    start_time = getTime()
    artistas=catalog["artists"]
    #Se busca el artista en el catálogo a partir del nombre
    posArtista=""
    for i in range(1, lt.size(artistas)+1):
        if lt.getElement(artistas,i)["name"]==artista:
            posArtista=i
    if posArtista=="":
        return "No se encontró el artista"
    artista = lt.getElement(artistas, posArtista)
    #Se inicializan los contadores de tipos de album
    albumesSingle=0
    albumesCompilation=0
    albumesAlbum=0
    albumesArtista = artista['albums']
    cancionesArtista= artista['songs']
    #Se recorren los álbumes del artista y se van contando los tipos de álbum
    for album in lt.iterator(albumesArtista):
        if album["album_type"] == "album":
            albumesAlbum += 1
        if album["album_type"] == "single":
            albumesSingle += 1
        if album["album_type"] == "compilation":
            albumesCompilation += 1
    #Se detiene la función de conteo de tiempo 
    end_time = getTime()
    delta_time = deltaTime(start_time,end_time)
    
    return albumesSingle,albumesCompilation,albumesAlbum, albumesArtista, cancionesArtista, delta_time


# algortimo más eficiente para ordenar en el caso promedio para una lista array list
def mergeSortAlbumsbyYear(catalog):
    """
    Ordena la lista de album por año
     """
    start_time = getTime()
    sorted_list = msort.sort(catalog['albums'], cmpAlbumByYear)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time


def mergeSortSongs(catalog):
    start_time = getTime()
    sorted_list = msort.sort(catalog['songs'], cmpSong)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time


def mergeSortSongList(songs):
    """ordena una sublista de canciones por popularidad"""
    start_time = getTime()
    sorted_list = msort.sort(songs, cmpSong)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time


def insertionSortArtists(catalog, size):
    sub_list = lt.subList(catalog['artists'], 1, size)
    start_time = getTime()
    sorted_list = isort.sort(sub_list, cmpArtistsbyFollowers)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time


def selectionSortArtists(catalog, size):
    sub_list = lt.subList(catalog['artists'], 1, size)
    start_time = getTime()
    sorted_list = ssort.sort(sub_list, cmpArtistsbyFollowers)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time


def shellSortArtists(catalog, size):
    sub_list = lt.subList(catalog['artists'], 1, size)
    start_time = getTime()
    sorted_list = sa.sort(sub_list, cmpArtistsbyFollowers)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time


# ordenamientos recursivos para lab 4

def quickSortArtists(catalog, size):
    sub_list = lt.subList(catalog['artists'], 1, size)
    start_time = getTime()
    sorted_list = qsort.sort(sub_list, cmpArtistsbyFollowers)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time

def cmpArtistsbyPopularity(artist1, artist2):
    """
    Devuelve verdadero (true) si los follower de artist1 son menores que los de artist2
    Args:
        artist1: información del primer artista que incluye su valor 'followers'
        artist2: información del segundo artista que incluye su valor 'followers'
    """
    return (float(artist1['artist_popularity']) > float(artist2["artist_popularity"]))

def mergeSortArtists(catalog, size):
    sub_list = lt.subList(catalog['artists'], 1, size)
    start_time = getTime()
    sorted_list = msort.sort(sub_list, cmpArtistsbyPopularity)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time


# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter() * 1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para comparar elementos dentro de una lista

def compareArtists(id, artist):
    if id == artist['id']:
        return 0
    if id > artist['id']:
        return 1
    return -1


def compareAlbums(id, album):
    if id == album['id']:
        return 0
    if id > album['id']:
        return 1
    return -1


def compareSongs(id, song):
    if id == song['id']:
        return 0
    if id > song['id']:
        return 1
    return -1




