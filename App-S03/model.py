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

from datetime import date, time, datetime
from operator import lshift
from unicodedata import name
import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as merge

from typing import Callable, TypedDict, Union
assert cf


# tipos de datos
class Catalog(TypedDict):
    artists: "dict[str,any]"
    albums: "dict[str,any]"
    tracks: "dict[str,any]"


class Artist(TypedDict):
    # propiedades del csv
    id: str
    artist_popularity: float
    genres: "dict[str,any]"
    followers: int
    track_id: str
    name: str
    # TODO: propiedades agregadas (albums, canciones mas populares, ...)


class Album(TypedDict):
    # propiedades del csv
    id: str
    release_date: str
    available_markets: "dict[str, str]"
    total_tracks: int
    album_type: str
    name: str
    track_id: str
    artist_id: str
    external_urls: "dict[str,str]"
    release_date_precision: str
    images: "dict[str, dict[str,any]]"
    # TODO: propiedades agregadas (cancion mas popular, ...)


class Track(TypedDict):
    # propiedades del csv
    id: str
    key: int
    tempo: float
    energy: float
    lyrics: int
    album_id: str
    artists_id: "dict[str,str]"
    danceability: float
    valence: float
    disc_number: int
    speechiness: float
    playlist: str
    instrumentalness: float
    popularity: float
    available_markets: "dict[str,str]"
    track_number: int
    name: str
    duration_ms: float
    acousticness: float
    liveness: float
    loudness: float
    preview_url: str
    href: str
    # TODO: propiedades agregadas (...)


class Control(TypedDict):
    model: Catalog


# Construccion de modelos
def newCatalog():
    catalog: Catalog = {"artists": None, "albums": None, "tracks": None}
    catalog["artists"] = lt.newList("ARRAY_LIST", cmpfunction=compareIdArtist)
    catalog["albums"] = lt.newList("ARRAY_LIST", cmpfunction=compareIdAlbum)
    catalog["tracks"] = lt.newList("ARRAY_LIST", cmpfunction=compareIdTrack)
    return catalog


# Funciones para agregar informacion al catalogo
def addArtist(catalog: Catalog, artist: Artist):
    a = newArtist(artist["id"], artist["name"], artist["genres"],
                  artist["artist_popularity"], artist["followers"],
                  artist["track_id"])
    lt.addLast(catalog["artists"], a)
    return catalog


def addAlbum(catalog: Catalog, album: Album):
    a = newAlbum(catalog, album["id"], album["release_date"],
                 album["available_markets"], album["total_tracks"],
                 album["album_type"], album["name"], album["track_id"],
                 album["artist_id"], album["external_urls"],
                 album["release_date_precision"])
    artist = album["artist_id"]
    addAlbumToArtist(catalog, artist.strip(), a)
    lt.addLast(catalog["albums"], a)
    return catalog


def addTrack(catalog: Catalog, track: Track):
    t = newTrack(catalog, track["id"], track["lyrics"], track["album_id"],
                 track["artists_id"], track["track_number"],
                 track["popularity"], track["available_markets"],
                 track["name"], track["duration_ms"], track["preview_url"],
                 track["href"])
    lt.addLast(catalog["tracks"], t)
    return catalog


def addTrackToArtist(catalog, artist_id, track):
    #Crea el apuntador de un Track a un Artista
    artists_list = catalog["artists"]
    artist_pos = binary_search(artists_list, 1, lt.size(artists_list),
                               artist_id)
    artist = lt.getElement(artists_list, artist_pos)
    lt.addLast(artist["songs"], track)
    return catalog


def addTrackToAlbum(catalog, album_id, track):
    #Crea el apuntador de un track a un album
    albums_list = catalog["albums"]
    album_pos = binary_search(albums_list, 1, lt.size(albums_list), album_id)
    album = lt.getElement(albums_list, album_pos)
    lt.addLast(album["songs"], track)
    return catalog


def addAlbumToArtist(catalog, artist_id, album):
    #Crea el apuntador de un album a un artista
    artists_list = catalog["artists"]
    artist_pos = binary_search(artists_list, 1, lt.size(artists_list),
                               artist_id)
    artist = lt.getElement(artists_list, artist_pos)
    lt.addLast(artist["albums"], album)
    return catalog


def prompters(catalog):
    #Crea los apuntadores de la lista 'Tracks' a las listas 'Artists' y 'Albums'
    lista_ordenada = sortTracks(catalog)
    for t in lt.iterator(lista_ordenada):
        artists = t["artists_id"]
        album = t["album_id"]
        for i in artists:
            addTrackToArtist(catalog, i, t)
        addTrackToAlbum(catalog, album.strip(), t)
    return catalog


# Funciones para creacion de datos


def newArtist(id, name, genres, popularity, followers, track_id):
    #Crea un nuevo artista con la información relevante
    artist = {
        "id": "",
        "name": "",
        "genres": list,
        "artist_popularity": 0,
        "followers": 0,
        "track_id": None,
        "songs": None,
        "albums": None
    }
    artist["id"] = id
    artist["name"] = name
    artist["genres"] = genres.strip("[]").replace("'", "")
    artist["artist_popularity"] = float(popularity)
    artist["followers"] = int(float(followers))
    artist["track_id"] = track_id
    artist["songs"] = lt.newList("ARRAY_LIST")
    artist["albums"] = lt.newList("ARRAY_LIST")
    artist["relevant_track_name"] = ""
    return artist


def newAlbum(catalog, id, release_date, available_markets, total_tracks,
             album_type, name, track_id, artist_id, external_urls,
             release_date_precision):
    #Crea un nuevo album con la información relevante
    album = {
        "id": "",
        "release_date": "",
        "available_markets": list,
        "total_tracks": None,
        "album_type": "",
        "name": "",
        "track_id": "",
        "artist_id": "",
        "artist_name": "",
        "external_urls": "",
        "release_date_precision": "",
        "songs": list
    }
    album["id"] = id
    album["available_markets"] = available_markets.strip("[]").replace(
        "'", "").replace(" ", "").split(",")
    album["total_tracks"] = int(float(total_tracks))
    album["album_type"] = album_type
    album["name"] = name
    album["track_id"] = track_id
    album["artist_id"] = artist_id
    album["artist_name"] = searchArtistName(catalog, artist_id)
    album["external_urls"] = external_urls
    album["release_date_precision"] = release_date_precision
    if str(album["release_date_precision"]) == "month":
        año = datetime.strptime(release_date, "%b-%y").year
        album["release_date"] = año
    elif str(album["release_date_precision"]) == "day":
        año = datetime.strptime(release_date, "%Y-%m-%d").year
        album["release_date"] = año
    else:
        año = datetime.strptime(release_date, "%Y").year
        album["release_date"] = año
    album["songs"] = lt.newList("ARRAY_LIST")
    return album


def newTrack(catalog, id, lyrics, album_id, artists_id, track_number,
             popularity, available_markets, name, duration_ms, preview_url,
             href):
    #Crea un nuevo track con la información relevante
    track = {
        "id": str,
        "lyrics": "",
        "album_id": "",
        "artists_id": list,
        "track_number": int,
        "popularity": int,
        "available_markets": "",
        "markets": int,
        "name": "",
        "duration_ms": int,
        "preview_url": "",
        "href": "",
        "artists_names": "",
        "album_name": "",
        "release_date": int
    }
    track["id"] = id
    if lyrics == "-99":
        track["lyrics"] = "Letra de canción NO disponible"
    else:
        track["lyrics"] = lyrics
    track["album_id"] = album_id
    limpio = artists_id.replace("\"",
                                "").strip("[]").replace(" ",
                                                        "").replace("'", "")
    track["artists_id"] = limpio.split(",")
    track["track_number"] = int(float(track_number))
    track["popularity"] = int(float(popularity))
    track["available_markets"] = available_markets.strip("[]").replace(
        "'", "").replace(" ", "").split(",")
    track["markets"] = len(track["available_markets"])
    track["track_number"] = int(float(track_number))
    track["name"] = name
    track["duration_ms"] = float(duration_ms)
    track["preview_url"] = preview_url
    track["href"] = href
    albumsearch = searchAlbumName(catalog, album_id)
    track["artists_names"] = searchArtistsNames(catalog, track["artists_id"])
    track["album_name"] = albumsearch[0]
    track["release_date"] = albumsearch[1]
    return track


# Funciones de consulta
def artistsSize(catalog: Catalog) -> int:
    return lt.size(catalog["artists"])


def albumsSize(catalog: Catalog) -> int:
    return lt.size(catalog["albums"])


def tracksSize(catalog: Catalog) -> int:
    return lt.size(catalog["tracks"])


def binary_search(catalog, low, high, object_id):
    if high >= low:
        mid = (high + low) // 2
        # If element is present at the middle itself
        if lt.getElement(catalog, mid)["id"] == object_id:
            return mid
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif lt.getElement(catalog, mid)["id"] > object_id:
            return binary_search(catalog, low, mid - 1, object_id)
        # Else the element can only be present in right subarray
        else:
            return binary_search(catalog, mid + 1, high, object_id)
    else:
        # Element is not present in the array
        return 0


def searchArtistName(catalog, artist_id):
    #Busca el nombre de un artista dada su ID
    pos = binary_search(catalog["artists"], 1, lt.size(catalog["artists"]),
                        artist_id)
    if pos > 0:
        artist = lt.getElement(catalog["artists"], pos)
        name = artist["name"]
        return name
    else:
        return "Unknown"


def searchArtistsNames(catalog, artists_id):
    #Busca los nombres de artistas que están contenidos en una lista de IDs
    nombres = ""
    for i in artists_id:
        pos = binary_search(catalog["artists"], 1, lt.size(catalog["artists"]),
                            i)
        artist = lt.getElement(catalog["artists"], pos)
        nombres = nombres + artist["name"] + ", "
    return nombres[:-2]


def searchAlbumName(catalog, album_id):
    #Busca el nombre de un album dada su ID
    pos = binary_search(catalog["albums"], 1, lt.size(catalog["albums"]),
                        album_id)
    if pos > 0:
        album = lt.getElement(catalog["albums"], pos)
        return album["name"], album["release_date"]
    else:
        return "Unknown", "Unknown"


def searchTrackName(catalog, track_id):
    #Busca el nombre de un track dada su ID
    pos = binary_search(catalog["tracks"], 1, lt.size(catalog["tracks"]),
                        track_id)
    if pos > 0:
        track = lt.getElement(catalog["tracks"], pos)
        return track["name"]
    else:
        return "Unknown"


def relevantTrackName(catalog):
    #Busca el nombre de la canción relevante de un artista
    artists = catalog["artists"]
    for a in lt.iterator(artists):
        name = searchTrackName(catalog, a["track_id"])
        a["relevant_track_name"] = name
    return catalog


def getAlbumsByYear(catalog: Catalog, a_inicio, a_final):
    #Devuelve los albumes publicados en un periodo de tiempo
    # start_time = getTime()
    lst = sortAlbums(catalog["albums"])
    result = lt.newList("ARRAY_LIST")
    for album in lt.iterator(lst):
        if a_inicio <= int(album["release_date"]) <= a_final:
            lt.addLast(result, album)
        elif a_final < int(album["release_date"]):
            break
    # end_time = getTime()
    # print("\n" + "-" * 20 +
    #       "\nEl tiempo de ejecución de este algoritmo fue: " +
    #       str(deltaTime(start_time, end_time)) + "\n" + "-" * 20)
    return result


def getTopArtists(catalog, size):
    #Devuelve el top X de artistas por popularidad
    # start_time = getTime()
    lista_ordenada = sortArtists(catalog["artists"])
    top_artists = lt.newList("ARRAY_LIST")
    # para evitar indx error si size pedido es mayor que size de la lista de artistas
    if (size > lt.size(catalog["artists"])):
        size = lt.size(catalog["artists"])
    for i in range(1, size + 1):
        artist = lt.getElement(lista_ordenada, i)
        lt.addLast(top_artists, artist)
    # end_time = getTime()
    # print("\n" + "-" * 20 +
    #       "\nEl tiempo de ejecución de este algoritmo fue: " +
    #       str(deltaTime(start_time, end_time)) + "\n" + "-" * 20)
    return top_artists


def getTopTracks(catalog: Catalog, size: int):
    """
    Retorna los top x tracks (ordenadas por popularidad de mayor a menor)
    """
    # ya estan ordenadas por popularidad los tracks
    # start_time = getTime()
    mejores_tracks = catalog["tracks"]  # sortTracks(catalog["tracks"])
    top_tracks = lt.newList("ARRAY_LIST")
    # para evitar indx error si size pedido es mayor que size de la lista de artistas
    if (size > lt.size(catalog["tracks"])):
        size = lt.size(catalog["tracks"])
    for i in range(1, size + 1):
        artist = lt.getElement(mejores_tracks, i)
        lt.addLast(top_tracks, artist)
    # end_time = getTime()
    # print("\n" + "-" * 20 +
    #       "\nEl tiempo de ejecución de este algoritmo fue: " +
    #       str(deltaTime(start_time, end_time)) + "\n" + "-" * 20)
    return top_tracks


def getBestTrack(catalog, name, country):
    #Devuelve la mejor canción de un artista
    # start_time = getTime()
    pos = 1
    artist = None
    for art in lt.iterator(catalog["artists"]):
        if art["name"] == name:
            artist = lt.getElement(catalog["artists"], pos)
            break
        pos += 1
    # si artista no fue encontrado, retornan None
    if (artist is None):
        return None
    for t in lt.iterator(artist["songs"]):
        if country in t["available_markets"]:
            best_song = t
            break
    # end_time = getTime()
    # print("\n" + "-" * 20 +
    #       "\nEl tiempo de ejecución de este algoritmo fue: " +
    #       str(deltaTime(start_time, end_time)) + "\n" + "-" * 20)
    return artist, best_song


def getDiscography(catalog, artist_name):
    #Devuelve la discografía completa de un artista
    # start_time = getTime()
    pos = 1
    artist = None
    for art in lt.iterator(catalog["artists"]):
        if art["name"] == artist_name:
            artist = lt.getElement(catalog["artists"], pos)
            break
        pos += 1
        # si artista no fue encontrado, retornar None
    if (artist is None):
        return None
    cont_single = 0
    cont_compilation = 0
    cont_album = 0
    for a in lt.iterator(artist["albums"]):
        if a["album_type"] == "single":
            cont_single += 1
        elif a["album_type"] == "compilation":
            cont_compilation += 1
        elif a["album_type"] == "album":
            cont_album += 1
    # end_time = getTime()
    # print("\n" + "-" * 20 +
    #       "\nEl tiempo de ejecución de este algoritmo fue: " +
    #       str(deltaTime(start_time, end_time)) + "\n" + "-" * 20)
    return cont_single, cont_compilation, cont_album, artist


def getTopTracksbyYear(catalog, a_inicio, a_final, top):
    # start_time = getTime()
    lst = sortTracksbyCountry(catalog)
    result = lt.newList("ARRAY_LIST")
    for track in lt.iterator(lst):
        if int(lt.size(result)) < top:
            if a_inicio <= int(track["release_date"]) <= a_final:
                lt.addLast(result, track)
        else:
            break
    # end_time = getTime()
    # print("\n" + "-" * 20 +
    #       "\nEl tiempo de ejecución de este algoritmo fue: " +
    #       str(deltaTime(start_time, end_time)) + "\n" + "-" * 20)
    return result


# Funciones utilizadas para comparar elementos dentro de una lista


def cmpArtists(artist1: Artist, artist2: Artist):
    """Devuelve verdadero (True) si los 'followers' de artist1 son menores que los del artist2
    Args:
    artist1: información del primer artista que incluye su valor 'followers'
    artist2: información del segundo artista que incluye su valor 'followers'
    """
    if artist1["artist_popularity"] < artist2["artist_popularity"]:
        return False
    elif artist1["artist_popularity"] > artist2["artist_popularity"]:
        return True
    else:
        if artist1["followers"] < artist2["followers"]:
            return False
        elif artist1["followers"] > artist2["followers"]:
            return True
        else:
            if artist1["name"].lower() < artist2["name"].lower():
                return False
            elif artist1["name"].lower() < artist2["name"].lower():
                return True


def comparePopularity(track1: Track, track2: Track):
    #Compara la popularidad de dos tracks, si tienen la mimsa popularidad, compara su duración, y si tienen
    #la misma duración, compara su nombre en minúsculas
    if track1["popularity"] < track2["popularity"]:
        return False
    elif track1["popularity"] > track2["popularity"]:
        return True
    else:
        if track1["duration_ms"] < track2["duration_ms"]:
            return False
        elif track1["duration_ms"] > track2["duration_ms"]:
            return True
        else:
            if track1["name"].lower() < track2["name"].lower():
                return False
            elif track1["name"].lower() < track2["name"].lower():
                return True


def cmpTracksbyCountry(track1: Track, track2: Track):
    if track1["markets"] > track2["markets"]:
        return True
    elif track1["markets"] < track2["markets"]:
        return False
    else:
        if track1["popularity"] > track2["popularity"]:
            return True
        elif track1["popularity"] < track2["popularity"]:
            return False
        else:
            if track1["name"].lower() > track2["name"].lower():
                return True
            elif track1["name"].lower() < track2["name"].lower():
                return False


def compareIdArtist(object_id, objects):
    #Compara el ID de un artista con el de todos los demás
    if object_id == objects['id']:
        return 0
    elif object_id > objects['id']:
        return 1
    else:
        return -1


def cmpArtistsbyID(artist1, artist2):
    return artist1["id"] < artist2["id"]


def cmpAlbumsbyID(album1, album2):
    return album1["id"] < album2["id"]


def cmpTracksbyID(track1, track2):
    return track1["id"] < track2["id"]


def compareIdAlbum(object_id, objects):
    #Compara el ID de un album con el de todos los demás
    if object_id == objects['id']:
        return 0
    elif object_id > objects['id']:
        return 1
    else:
        return -1


def compareIdTrack(object_id, objects):
    #Compara el ID de un track con el de todos los demás
    if object_id == objects['id']:
        return 0
    elif object_id > objects['id']:
        return 1
    else:
        return -1


def compareDate(album1: Album, album2: Album):
    #Compara la fecha de dos albumes
    return int(album1["release_date"]) < int(album2["release_date"])


# Funciones de ordenamiento
def sortArtists(catalog: Catalog):
    #Ordena con "merge" los artistas por popularidad
    return merge.sort(catalog, cmpArtists)


def sortArtistsbyID(catalog: Catalog):
    return merge.sort(catalog["artists"], cmpArtistsbyID)


def sortAlbumsbyID(catalog: Catalog):
    return merge.sort(catalog["albums"], cmpAlbumsbyID)


def sortTracksbyID(catalog: Catalog):
    return merge.sort(catalog["tracks"], cmpTracksbyID)


def sortAlbums(catalog: Catalog):
    #Ordena los albumes por fecha de lanzamiento
    return merge.sort(catalog, compareDate)


def sortTracks(catalog):
    #Ordena los tracks por popularidad
    return merge.sort(catalog["tracks"], comparePopularity)


def sortTracksbyCountry(catalog):
    #Ordena los tracks por cantidad de países donde se ditribuyen
    return merge.sort(catalog["tracks"], cmpTracksbyCountry)


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
