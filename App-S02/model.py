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


from ast import Lambda
from decimal import ROUND_CEILING, ROUND_UP
from tempfile import SpooledTemporaryFile
import time
import datetime
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import selectionsort as sls
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import shellsort as shl
from DISClib.Algorithms.Sorting import mergesort as mgs
from DISClib.Algorithms.Sorting import quicksort as qks
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(listType = 'ARRAY_LIST'):
    """
    Inicializa el catálogo de Spotify Profiling. Crea una lista vacia para guardar
    todos los albums, adicionalmente, crea una lista vacia para los artistas y una
    lista vacia para los tracks. Retorna el catalogo inicializado.
    """
    catalog = {'albums': None, 'artists': None, 'tracks': None, 'albumsByYear': None}

    catalog['albums'] = lt.newList(datastructure = listType, cmpfunction = cmpID)
    catalog['artists'] = lt.newList(datastructure = listType, cmpfunction = cmpID)
    catalog['tracks'] = lt.newList(datastructure = listType, cmpfunction = cmpID)

    return catalog

# Funciones para agregar informacion al catalogo

def addAlbum(catalog, album):
    'El album se añade a la lista de albums'
    try:
        album['year'] = int(album['release_date'][:4].strip())
    except:
        album['year'] = int('19' + album['release_date'][-2:])
    album['tracks'] = lt.newList('ARRAY_LIST')
    album['total_tracks'] = 0
    album['inicial_track_name'] = "No track"
    album['artist_name'] = "Unknown"
    lt.addLast(catalog['albums'], album)
    return catalog

def addArtist(catalog, artist):
    'El artista se añade a la lista de artistas'
    artist['albums'] = lt.newList('ARRAY_LIST')
    artist['tracks'] = lt.newList('ARRAY_LIST')
    artist['relevant_track_name'] = "Unknown"
    lt.addLast(catalog['artists'], artist)
    return catalog

def addTrack(catalog, track):
    'El track se añade a la lista de tracks'
    track['artists_names'] = ''
    if track['lyrics'] == '-99':
        track['lyrics'] = 'La letra NO esta disponible'
    lt.addLast(catalog['tracks'], track)
    return catalog



# Funciones para creacion de datos

def connectFullData(catalog):
    #Se recorre la lista de tracks para añadir cada tracks a su artista y album correspondiente
    for track in lt.iterator(catalog['tracks']):
        album = lt.getElement(catalog['albums'], binarySearch(catalog['albums'], track['album_id'], 'id'))
        artistOfAlbum = lt.getElement(catalog['artists'], binarySearch(catalog['artists'], album['artist_id'], 'id'))
        album['artist'] = artistOfAlbum
        album['artist_name'] = artistOfAlbum['name']
        track['album'] = album
        track['album_name'] = album['name']
        track['release_date'] = int(album['year'])
        lista_paises = strlstdivider(track['available_markets'])
        track['distribution'] = len(lista_paises)
        artistsIds = strlstdivider(track['artists_id'])
        if track['id'] == album['track_id']:
            album['inicial_track_name'] = track['name']

        for artistId in artistsIds:
            artist = lt.getElement(catalog['artists'], binarySearch(catalog['artists'], artistId, 'id'))
            if artist['track_id'] == track['id']:
                artist['relevant_track_name'] =  track['name']
            track['artists_names'] += '- ' + artist['name']
            lt.addLast(artist['tracks'], track)
            lt.addLast(artist['albums'], album)
        lt.addLast(album['tracks'], track)
        album['total_tracks'] += 1
    stop_time = time.process_time()

def strlstdivider(artistStr):
    artistsList = artistStr.replace('[','').replace(']','').replace("'",'').split(',')
    return artistsList

def listsFusion(lst1, lst2):
    fusionList = lt.newList('ARRAY_LIST')
    for element in lt.iterator(lst1):
        lt.addLast(fusionList, element)
    for element in lt.iterator(lst2):
        lt.addLast(fusionList, element)
    return fusionList

# Funciones de consulta

#Requerimiento 1
def albumsByReleaseYear(catalog, min, max):
    start_time = getTime()
    albumsByReleaseYear = rangeByDate(catalog['albumsByYear'], min, max, 'year')
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return albumsByReleaseYear, delta_time

#Requerimiento 2
def artistByPopularity(catalog, top):
    start_time = getTime()
    topartistpopularity = lt.subList(catalog['artistByPopularity'], 1, top)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return topartistpopularity, delta_time

#Requerimiento 3
def tracksByPopularity(num, catalog):
    start_time = getTime()
    tracksByPopularity = getFirstNum(num, catalog['tracksByPopularity'])
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return tracksByPopularity, delta_time

#Requerimiento 4
def popularTrackByArtist(catalog, artistName, countryCode):
    start_time = getTime()
    filteredTracks = lt.newList('ARRAY_LIST')
    artist = lt.getElement(catalog['artistByName'], binarySearch(catalog['artistByName'], artistName, 'name'))
    for track in lt.iterator(artist['tracks']):
        if str(countryCode) in track['available_markets']:
            lt.addLast(filteredTracks,track)
    popularity = 0
    duration_ms = 0
    name = ''
    maxiumTrack = lt.getElement(filteredTracks, 1)
    for track in lt.iterator(filteredTracks):
        if float(track['popularity']) > float(popularity):
            popularity = float(track['popularity'])
            duration_ms = track['duration_ms']
            name = track['name']
            maxiumTrack = track
        elif float(track['popularity']) == float(popularity):
            if float(track['duration_ms']) > float(duration_ms):
                duration_ms = track['duration_ms']
                name = track['name']
                maxiumTrack = track
            elif float(track['duration_ms']) == float(duration_ms):
                if track['name'] > name:
                    name = track['name']
                    maxiumTrack = track
    trackArray = lt.newList('ARRAY_LIST')
    lt.addLast(trackArray,maxiumTrack)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return trackArray, delta_time

#Requerimiento 5
def albumInfo(catalog, artistName):
    start_time = getTime()
    artist = lt.getElement(catalog['artistByName'], binarySearch(catalog['artistByName'],artistName,'name'))
    sizeAlbumsArtist = lt.size(artist['albums'])
    countByType = countAlbumType(artist['albums'], ('compilation', 'album', 'single'))
    albumssorted = sortLst(artist['albums'], lt.size(artist['albums']), cmpAlbumsByYear)

    trackArray = lt.newList('ARRAY_LIST')
    for albumi in lt.iterator(albumssorted):
        maxiumTrack = linealMaxPopularity(albumi['tracks'])
        lt.addLast(trackArray,maxiumTrack)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sizeAlbumsArtist, countByType, albumssorted, trackArray, delta_time

#Bono
def tracksByDistributionInRange(catalog, min, max, top):
    start_time = getTime()
    listTracksByYear = rangeByDate(catalog['tracksByYear'], min, max, 'release_date')
    orderByDistributionTracks = sortLst(listTracksByYear,lt.size(listTracksByYear), cmpDistribution)
    topDistributionTracks = lt.subList(orderByDistributionTracks, 1, top)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return topDistributionTracks, delta_time

#Funciones de Busqueda

def linealSearch(sortedList,element,parameter):
    pos = None
    while pos == None:
        for album_pos in range(1,lt.size(sortedList)):
            if lt.getElement(sortedList,album_pos)[parameter] == element:
                pos = album_pos
                break
        element += 1
    return pos


def binarySearch(sortedList, element, parameter):
    """
    Busqueda Binaria de un elemento en una lista ordenada ascendentemente
    Resultado: Indice en la lista donde se encuentra el elemento. -1 si no se encuentra.
    """
    i = 0
    f = lt.size(sortedList)
    pos = -1
    found = False
    while i <= f and not found:
        # calcular la posicion de la mitad entre i y f
        m = (i + f) // 2
        if lt.getElement(sortedList, m)[parameter] == element:
            pos = m
            found = True
        elif lt.getElement(sortedList, m)[parameter] > element:
            f = m - 1
        else:
            i = m + 1
    return pos

def binarySearchMin(sortedList, element, parameter):
    m = 0
    i = 0
    f = lt.size(sortedList)
    pos = -1
    found = False
    while i <= f and not found:
        m = (i + f) // 2
        if lt.getElement(sortedList, m)[parameter] == element:
            pos = m
            found = True
        elif lt.getElement(sortedList, m)[parameter] > element:
            f = m - 1
        else:
            i = m + 1
    if found == True:
        while lt.getElement(sortedList, pos - 1)[parameter] == element:
            pos -= 1
    elif lt.getElement(sortedList, m)[parameter] > element:
        pos = m
        while lt.getElement(sortedList, pos - 1)[parameter] > element:
            pos -= 1
    return pos

def binarySearchMax(sortedList, element, parameter):
    m = 0
    i = 0
    f = lt.size(sortedList)
    pos = -1
    found = False
    while i <= f and not found:
        m = (i + f) // 2
        if lt.getElement(sortedList, m)[parameter] == element:
            pos = m
            found = True
        elif lt.getElement(sortedList, m)[parameter] > element:
            f = m - 1
        else:
            i = m + 1
    if found == True:
        while lt.getElement(sortedList, pos + 1)[parameter] == element:
            pos += 1
    elif lt.getElement(sortedList, m)[parameter] < element:
        pos = m
        while lt.getElement(sortedList, pos + 1)[parameter] > element:
            pos += 1
    return pos

albumsSize = lambda catalog: lt.size(catalog['albums'])

artistsSize = lambda catalog: lt.size(catalog['artists'])

tracksSize = lambda catalog: lt.size(catalog['tracks'])

def getLastNum(number, spotifyList):
    """
    Retorna los primeros number
    """
    if number <= lt.size(spotifyList):
        lasts = lt.newList('ARRAY_LIST')
        for cont in range(0, number):
            element = lt.getElement(spotifyList, lt.size(spotifyList) - cont)
            lt.addFirst(lasts, element)
        return lasts
    else:
        return spotifyList

def getFirstNum(number, spotifyList):
    """
    Retorna los ultimos number
    """
    if number <= lt.size(spotifyList):
        firsts = lt.newList('ARRAY_LIST')
        for cont in range(1, number + 1):
            element = lt.getElement(spotifyList, cont)
            lt.addLast(firsts, element)
        return firsts
    else:
        return spotifyList


# Funciones utilizadas para comparar elementos dentro de una lista

def cmpID(element1, element2):
    if (element1["id"] == element2['id']):
        return 0
    elif (element1["id"] > element2['id']):
        return 1
    return -1

# Funciones para comparar elementos dentro de algoritmos de ordenamientos

def cmpLstsById(element1, element2):
    'Return True if album1 < album2, False otherwise.'
    return element1['id'] < element2['id']

def cmpLstsByName(element1, element2):
    'Return True if album1 < album2, False otherwise.'
    return element1['name'] < element2['name']

def cmpArtistsByFollowers(artist1, artist2):
    'Return True if  artist1 < artist2'
    return float(artist1["followers"]) < float(artist2["followers"])

def cmpAlbumsByYear(album1, album2):
    'Return True if album1 < album2, False otherwise.'
    return int(album1['year']) < (album2['year'])

def cmpTracksByYear(track1, track2):
    return track1['release_date'] < track2['release_date']

def cmpTracksByPopularity(track1, track2):
    if float(track1['popularity']) > float(track2['popularity']):
        return True
    elif float(track1['popularity']) == float(track2['popularity']):
        if float(track1['duration_ms']) > float(track2['duration_ms']):
            return True
        elif float(track1['duration_ms']) == float(track2['duration_ms']):
            if track1['name'] > track2['name']:
                return True
    else:
        return False

def cmpFunctionRdos(artistone, artisttwo):
    if float(artistone['artist_popularity']) > float(artisttwo['artist_popularity']):
        return True
    elif float(artistone['artist_popularity']) == float(artisttwo['artist_popularity']):
        if float(artistone['followers']) > float(artisttwo['followers']):
            return True
        elif float(artistone['followers']) == float(artisttwo['followers']):
            if artistone['name'] > artisttwo['name']:
                return True
    else:
        return False

def cmpDistribution(element1, element2):

    if int(element1["distribution"]) > int(element2["distribution"]):
            return True
    elif float(element1['distribution']) == float(element2['distribution']):
        if float(element1['popularity']) > float(element2['popularity']):
            return True
        elif float(element1['popularity']) == float(element2['popularity']):
            if element1['name'] > element2['name']:
                return True
    else:
        return False

# Funciones de ordenamiento

def sortLstWithTime(lst, size, method):
    sortmet = selectSortMethod(method)
    sub_list = lt.subList(lst, 0, size)
    sub_list = sub_list.copy()
    start_time = time.process_time()
    sorted_list = sortmet.sort(sub_list, cmpArtistsByFollowers)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sortLst(lst, size, parameter):
    sub_list = lt.subList(lst, 1, size)
    sub_list = sub_list.copy()
    sorted_list = mgs.sort(sub_list, parameter)
    return sorted_list

def sortSpotifyLists(catalog):
    catalog['albums'] = sortLst(catalog['albums'], lt.size(catalog['albums']), cmpLstsById)
    catalog['artists'] = sortLst(catalog['artists'], lt.size(catalog['artists']), cmpLstsById)
    catalog['tracks'] = sortLst(catalog['tracks'], lt.size(catalog['tracks']), cmpLstsById)

def newSortedAuxLists(catalog):
    catalog['albumsByYear'] = sortLst(catalog['albums'], lt.size(catalog['albums']), cmpAlbumsByYear)
    catalog['tracksByPopularity'] = sortLst(catalog['tracks'], lt.size(catalog['tracks']), cmpTracksByPopularity)
    catalog['artistByPopularity'] = sortLst(catalog['artists'], lt.size(catalog['artists']), cmpFunctionRdos)
    catalog['artistByName'] = sortLst(catalog['artists'], lt.size(catalog['artists']), cmpLstsByName)
    catalog['tracksByYear'] = sortLst(catalog['tracks'], lt.size(catalog['tracks']), cmpTracksByYear)


# Funciones Auxiliares

def selectSortMethod(method = 'mgs'):
    sortType = mgs
    if method == 'sls':
        sortType = sls
    elif method == 'ins':
        sortType = ins
    elif method ==  'shl':
        sortType = shl
    elif method == 'mgs':
        sortType = mgs
    elif method == 'qks':
        sortType = qks
    return sortType

def resetList(listType):
    return lt.newList(listType)

def rangeByDate(listcatalog, min, max, parameter):
    minYear = linealSearch(listcatalog, int(min), parameter)
    #minYear = binarySearchMin(listcatalog, int(min), parameter)
    maxYear = binarySearchMax(listcatalog, int(max), parameter)
    yearRange = maxYear - minYear
    listByYear = lt.subList(listcatalog, minYear, yearRange + 1)
    return listByYear

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
def countAlbumType(TADlist,types):
    type1 = types[0]
    counttype1 = 0
    type2 = types[1]
    counttype2 = 0
    counttype3 = 0
    for album in lt.iterator(TADlist):
        if album['album_type'] == type1:
            counttype1 += 1
        elif album['album_type'] == type2:
            counttype2 += 1
        else:
            counttype3 += 1
    return (counttype1, counttype2, counttype3)

def linealMaxPopularity(listToCount):
    maxiumTrack = lt.getElement(listToCount, 1)
    for track in lt.iterator(listToCount):
        if float(track['popularity']) > float(maxiumTrack['popularity']):
            maxiumTrack = track
        elif float(track['popularity']) == float(maxiumTrack['popularity']):
            if float(track['duration_ms']) > float(maxiumTrack['duration_ms']):
                maxiumTrack = track
            elif float(track['duration_ms']) == float(maxiumTrack['duration_ms']):
                if track['name'] > maxiumTrack['name']:
                    maxiumTrack = track
    return maxiumTrack
