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



import config as cf
import time
from datetime import datetime
from pycountry import pycountry
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as shell
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as sel
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(tipo_lista):
    """
    Inicializa el catálogo de spotify.
    Retorna el catalogo inicializado.
    """
    catalog = {
        'tracks': None,
        'albums': None,
        'artists': None
    }

    catalog['tracks'] = lt.newList(tipo_lista)
    catalog['albums'] = lt.newList(tipo_lista)
    catalog['artists'] = lt.newList(tipo_lista)

    return catalog

# Funciones para agregar informacion al catalogo

def addTrack(catalog, track):
    # Se adiciona el track a la lista de tracks
    artists = eval(track['artists_id'])
    track['artists_id'] = artists
    markets = eval(track['available_markets'].strip('"'))
    track['available_markets'] = markets
    lt.addLast(catalog['tracks'], track)

def addAlbum(catalog, album):
    # Se adiciona el album a la lista de albumes
    album = formatYear(album)
    urls = eval(album['external_urls'])
    album['external_urls'] = urls
    markets = eval(album['available_markets'])
    album['available_markets'] = markets
    lt.addLast(catalog['albums'], album)

def addArtist(catalog, artist):
    # Se adiciona el artista a la lista de artistas
    genres = eval(artist['genres'])
    artist['genres'] = genres
    lt.addLast(catalog['artists'], artist)

# Funciones para creacion de datos

# Funciones para formato

def formatYear(album):
    presicion = album["release_date_precision"]
    if presicion == "day":
        date = datetime.strptime(album['release_date'], "%Y-%m-%d")
        year = datetime.strftime(date, "%Y")

    elif presicion == "month":
        date = datetime.strptime(album['release_date'], "%b-%y")
        year = datetime.strftime(date, "%Y")
    else:
        year = album['release_date']
    album["year"] = year
    return album

def formatMarket(market_name):
    market_id = pycountry.countries.search_fuzzy(market_name)
    market_id = market_id[0].alpha_2
    return market_id

# Funciones de consulta

def trackSize(catalog):
    return lt.size(catalog['tracks'])

def albumSize(catalog):
    return lt.size(catalog['albums'])

def artistSize(catalog):
    return lt.size(catalog['artists'])


def getAlbumsInRange(list, lo, hi):
    albumsInRange = lt.newList("ARRAY_LIST")
    for album in lt.iterator(list):
        year = int(album['year'])
        if year > hi:
            return albumsInRange, lt.size(albumsInRange)
        elif year >= int(lo):
            lt.addLast(albumsInRange, album)
    return albumsInRange, lt.size(albumsInRange)

def searchArtistById(list, artists):
    albumsWithArtist = lt.newList("ARRAY_LIST")
    for album in lt.iterator(list):
        id_to_search = album['artist_id']
        index = binarySearch(artists, id_to_search, 1, lt.size(artists))
        if index == -1:
            album['artist_album_name'] = 'Unknown'
        else:
            artist = lt.getElement(artists, index)
            album['artist_album_name'] = artist['name']
        lt.addLast(albumsWithArtist, album)

    return albumsWithArtist, lt.size(albumsWithArtist)

def searchTrackById(list, tracks):
    artistsWithTrack = lt.newList("ARRAY_LIST")
    for artist in lt.iterator(list):
        id_to_search = artist['track_id']
        index = binarySearch(tracks, id_to_search, 1, lt.size(tracks))
        if index == -1:
            artist['revelant_track_name'] = 'Unknown'
        else:
            track = lt.getElement(tracks, index)
            artist['revelant_track_name'] = track['name']
        lt.addLast(artistsWithTrack, artist)
    return artistsWithTrack, lt.size(artistsWithTrack)

def searchTracksByMarket(tracks, market_name):
    market_id = formatMarket(market_name)
    tracksInMarket = lt.newList('ARRAY_LIST')
    for track in lt.iterator(tracks):
        markets = track['available_markets']
        i = 0
        marketFound = False
        while not marketFound and i < len(markets):
            market = markets[i]
            if market == market_id:
                lt.addLast(tracksInMarket, track)
                marketFound = True
            i += 1
    return tracksInMarket, lt.size(tracksInMarket), market_id

def searchTracksByArtist(tracks, artist_id):
    tracksByArtist = lt.newList('ARRAY_LIST')
    for track in lt.iterator(tracks):
        artists = track['artists_id']
        for artist in artists:
            artist = artist.strip()
            if artist == artist_id:
                lt.addLast(tracksByArtist, track)
    return tracksByArtist, lt.size(tracksByArtist)

def searchAlbumsByArtist(albums, artist_id):
    albumsByArtist = lt.newList('ARRAT_LIST')
    single = 0
    compilation = 0
    album_count = 0
    for album in lt.iterator(albums):
        if album['artist_id'] == artist_id:
            lt.addLast(albumsByArtist, album)
            if album['album_type'] == 'single':
                single += 1
            elif album['album_type'] == 'compilation':
                compilation += 1
            if album['album_type'] == 'album':
                album_count += 1
    return albumsByArtist, lt.size(albumsByArtist), {'singles':single, 'compiltations':compilation,'albums':album_count}

def searchTracksByAlbum(tracks, album_id):
    tracksByAlbum = lt.newList('ARRAY_LIST')
    for track in lt.iterator(tracks):
        if track['album_id'] == album_id:
            lt.addLast(tracksByAlbum, track)
    return tracksByAlbum, lt.size(tracksByAlbum)

def getArtistId(artists, artist_name):
    for artist in lt.iterator(artists):
        name = artist['name']
        if name == artist_name:
            return artist['id']
    return -1

def getArtistName(artists, artist_id):
    index = binarySearch(artists, artist_id, 1, lt.size(artists))
    if index == -1:
        artist_name = 'Unknown'
    else:
        artist = lt.getElement(artists, index)
        artist_name = artist['name']
    return artist_name

def getAlbumInfo(albums, tracks):
    tracksAlbumInfo = lt.newList('ARRAY_LIST')
    for track in lt.iterator(tracks):
        id_to_search = track['album_id']
        index = binarySearch(albums, id_to_search, 1, lt.size(albums))
        album = lt.getElement(albums, index)
        if index == -1:
            track['album_name'] = 'Unknown'
            track['release_date'] = 'Unknown'
            track['available_markets'] = []
        else:
            track['album_name'] = album['name']
            track['release_date'] = album['release_date']
            track['available_markets'] = album['available_markets']

        lt.addLast(tracksAlbumInfo, track)
    return tracksAlbumInfo, lt.size(tracksAlbumInfo)

def binarySearch(lista, x, low, high):
    """
    Algoritmo recursivo de busqueda binaria, tomado de:
    https://www.programiz.com/dsa/binary-search
    """
    if high >= low:

        mid = low + (high - low)//2

        # If found at mid, then return it
        if lt.getElement(lista, mid)['id'] == x:
            return mid

        # Search the left half
        elif lt.getElement(lista, mid)['id'] > x:
            return binarySearch(lista, x, low, mid-1)

        # Search the right half
        else:
            return binarySearch(lista, x, mid + 1, high)

    else:
        return -1

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpDataById(data1, data2):
    return data1['id'] < data2['id']

def cmpArtistsByPopularity(artist1, artist2):
    """
    Devuelve verdadero (True) si el criterio compuesto de popularidad de artist1 es
    mayor que el del artist2
    Args:
    artist1: informacion del primer artista que incluye su valor 'followers','artist_popularity'
            y 'name'
    artist2: informacion del segundo artista que incluye su valor 'followers','artist_popularity'
            y 'name'
    """
    if artist1['artist_popularity'] == artist2['artist_popularity']:
        if float(artist1['followers']) == float(artist2['followers']):
            return artist1['name'] <= artist2 ['name']
        else:
            return float(artist1['followers'])> float(artist2['followers'])
    else:
        return artist1['artist_popularity'] > artist2['artist_popularity']

def cmpTracksByPopularity(track1, track2):
    """
    Devuelve verdadero (True) si el criterio compuesto de popularidad de track1 es
    mayor que el del track2
    Args:
    artist1: informacion del primer track que incluye su valor 'popularity', 'duration_ms' y 'name'
    artist2: informacion del segundo artista que incluye su valor 'popularity', 'duration_ms' y 'name'
    """
    if track1['popularity'] == track2['popularity']:
        if float(track1['duration_ms']) == float(track2['duration_ms']):
            return track1['name'] <= track2 ['name']
        else:
            return float(track1['duration_ms'])> float(track2['duration_ms'])
    else:
        return track1['popularity'] > track2['popularity']

def cmpTracksByMarkets(track1, track2):
    """
    Devuelve verdadero (True) si el criterio compuesto de popularidad de track1 es
    mayor que el del track2
    Args:
    artist1: informacion del primer track que incluye su valor 'popularity', 'duration_ms' y 'name'
    artist2: informacion del segundo artista que incluye su valor 'popularity', 'duration_ms' y 'name'
    """
    if len(track1['available_markets']) == len(track2['available_markets']):
        if float(track1['popularity']) == float(track2['popularity']):
            return track1['name'] <= track2 ['name']
        else:
            return float(track1['popularity'])> float(track2['popularity'])
    else:
        return len(track1['available_markets']) > len(track2['available_markets'])

def cmpAlbumsByYear(album1, album2):
    """
    Devuelve verdadero (True) si el 'year' de album1 es menor que los del album2
    Args:
    album1: informacion del primer album que incluye su valor 'year'
    album2: informacion del segundo album que incluye su valor 'year'
    """
    return album1["year"] < album2["year"]

# Funciones de ordenamiento

def sortByAlgorithmCmp(algoritmo, lista, cmpFunction):
    if algoritmo == "insertion":
        sorted_list = ins.sort(lista, cmpFunction)
    elif algoritmo == "selection":
        sorted_list = sel.sort(lista, cmpFunction)
    elif algoritmo == "shell":
        sorted_list = shell.sort(lista, cmpFunction)
    elif algoritmo == "quick":
        sorted_list = quick.sort(lista, cmpFunction)
    elif algoritmo == "merge":
        sorted_list = merge.sort(lista, cmpFunction)
    return sorted_list

def sortArtistsByPopularity(algoritmo, artistas, tamanio):
    sub_lista = lt.subList(artistas, 1, tamanio)

    start_time = getTime()

    sorted_list = sortByAlgorithmCmp(algoritmo, sub_lista, cmpArtistsByPopularity)

    end_time = getTime()

    delta_time = deltaTime(start_time, end_time)

    return sorted_list, delta_time

def sortTracksByPopularity(algoritmo, artistas, tamanio):
    sub_lista = lt.subList(artistas, 1, tamanio)

    start_time = getTime()

    sorted_list = sortByAlgorithmCmp(algoritmo, sub_lista, cmpTracksByPopularity)

    end_time = getTime()

    delta_time = deltaTime(start_time, end_time)

    return sorted_list, delta_time

def sortTracksByMarkets(algoritmo, tracks, size_tracks):
    sub_lista = lt.subList(tracks, 1, size_tracks)

    start_time = getTime()

    sorted_list = sortByAlgorithmCmp(algoritmo, sub_lista, cmpTracksByMarkets)

    end_time = getTime()

    delta_time = deltaTime(start_time, end_time)

    return sorted_list, delta_time

def sortAlbumsByYear(algoritmo, albums, tamanio):
    sub_lista = lt.subList(albums, 1, tamanio)

    start_time = getTime()

    sorted_list = sortByAlgorithmCmp(algoritmo, sub_lista, cmpAlbumsByYear)

    end_time = getTime()

    delta_time = deltaTime(start_time, end_time)

    return sorted_list, delta_time

def sortDataById(algoritmo, lista, tamanio):
    sub_lista = lt.subList(lista, 1, tamanio)

    start_time = getTime()

    sorted_list = sortByAlgorithmCmp(algoritmo, sub_lista, cmpDataById)

    end_time = getTime()

    delta_time = deltaTime(start_time, end_time)

    return sorted_list, delta_time


# Funciones para medir tiempos de ejecucion

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