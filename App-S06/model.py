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

from operator import pos
from turtle import position
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ia
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as me
from DISClib.Algorithms.Sorting import quicksort as qi
assert cf
import sys
import time

import csv
csv.field_size_limit(2147483647)

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

"""
MODEL BUILDING FUNCTIONS
"""

def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'albums': None,
               'artists': None,
               'tracks': None}
    catalog['albums'] = lt.newList('ARRAY_LIST')
    catalog['artists'] = lt.newList('ARRAY_LIST')
    catalog['tracks'] = lt.newList('ARRAY_LIST')
    return catalog

"""
ADDING DATA FUNCTIONS
"""

def addAlbum(catalog, album):
    # Se adiciona el album a la lista de albums
    if len(album['release_date']) == 10:
        album['release_date'] = int(album['release_date'].split('-')[0])
    elif len(album['release_date']) == 4:
        album['release_date'] = int(album['release_date'])
    else:
        album['release_date'] = int('19' + album['release_date'].split('-')[1])
    
    album['available_markets'] = album['available_markets'].split(',')
    for i in range (0, len(album['available_markets'])):
        album['available_markets'][i] = album['available_markets'][i].replace('[', '')
        album['available_markets'][i] = album['available_markets'][i].replace(']', '')
        album['available_markets'][i] = album['available_markets'][i].replace('\'', '')
        album['available_markets'][i] = album['available_markets'][i].replace(' ', '')
        album['available_markets'][i] = album['available_markets'][i].replace('"', '')
    
    #t = newAlbum(album['id'], album['track_id'], album['total_tracks'], album['external_urls'])
    lt.addLast(catalog['albums'], album)

def addArtist(catalog, artist):
    # Se adiciona el artista a la lista de artistas
    lt.addLast(catalog['artists'], artist)

def addTrack(catalog, track):
    # Se adiciona el album a la lista de albums
    if track['popularity'] == '':
        track['popularity'] = 0
    track['artists_id'] = track['artists_id'].split(',')
    for i in range (0, len(track['artists_id'])):
        track['artists_id'][i] = track['artists_id'][i].replace('[', '')
        track['artists_id'][i] = track['artists_id'][i].replace(']', '')
        track['artists_id'][i] = track['artists_id'][i].replace('\'', '')
        track['artists_id'][i] = track['artists_id'][i].replace(' ', '')
    if track['lyrics'] == '-99':
        track['lyrics'] = 'Letra de la canción NO disponible'
    else:
        track['lyrics'] = track['lyrics'][0:100]
    track['available_markets'] = track['available_markets'].split(',')
    for i in range (0, len(track['available_markets'])):
        track['available_markets'][i] = track['available_markets'][i].replace('[', '')
        track['available_markets'][i] = track['available_markets'][i].replace(']', '')
        track['available_markets'][i] = track['available_markets'][i].replace('\'', '')
        track['available_markets'][i] = track['available_markets'][i].replace(' ', '')
        track['available_markets'][i] = track['available_markets'][i].replace('"', '')
    
    tracks = newTrack(track['id'],track['preview_url'], track['href'], track['album_id'], track['artists_id'], track['popularity'], track['duration_ms'], track['available_markets'], track['lyrics'], track['disc_number'], track['track_number'], track['name'])
    lt.addLast(catalog['tracks'], tracks)

"""
FUNCTIONS FOR CREATING DATA
"""

def newTrack(id, preview_url, href, album_id, artists_id, popularity, duration_ms, available_markets, lyrics, disc_number, track_number, name):
    track = {'id': '','preview_url': '', 'href': '', 'album_id': '', 'artists_id': '', 'popularity': 0, 'duration_ms': 0, 'available_markets': [], 'lyrics': '', 'disc_number': 0, 'track_number': 0, 'name': ''}

    track['id'] = id
    track['preview_url'] = preview_url
    track['href'] = href
    track['album_id'] = album_id
    track['artists_id'] = artists_id
    track['popularity'] = popularity 
    track['duration_ms'] = duration_ms
    track['available_markets'] = available_markets
    track['lyrics'] = lyrics
    track['disc_number'] = disc_number
    track['track_number'] = track_number
    track['name'] = name
    
    return track

"""
SIZE FUNCTION
"""
def sizeList(list):
    return lt.size(list)
"""
SUBLIST FUNCTION
"""
def createSubList(list, position, size):
    return lt.subList(list, position, size)
"""
COMPARING FUNCTIONS
"""

def cmpArtistsByPopularity(artist1, artist2):
    """
    Devuelve verdadero (True) si los 'followers' de artist1 son menores que los del artist2
    Args:
    artist1: informacion del primer artista que incluye su valor 'followers'
    artist2: informacion del segundo artista que incluye su valor 'followers'
    """
    if float(artist1['artist_popularity']) > float(artist2['artist_popularity']):
        return True
    elif float(artist1['artist_popularity']) == float(artist2['artist_popularity']):
        if float(artist1['followers']) > float(artist2['followers']):
            return True
        elif float(artist1['followers']) == float(artist2['followers']):
            if str(artist1['name']) > str(artist2['name']):
                return True
            else: 
                return False
        else:
            return False
    else:
        return False
    
def cmpTracksByPopularity(track1, track2):
    """
    Devuelve verdadero (True) si 'popularity' de track1 es mayor que el del track2
    Args:
    track1: informacion del primer track que incluye su valor 'popularity'
    track2: informacion del segundo track que incluye su valor 'popularity'
    """
    if float(track1['popularity']) > float(track2['popularity']):
        return True
    elif float(track1['popularity']) == float(track2['popularity']):
        if float(track1['duration_ms']) > float(track2['duration_ms']):
            return True
        elif float(track1['duration_ms']) == float(track2['duration_ms']):
            if str(track1['name']) > str(track2['name']):
                return True
            else: 
                return False
        else:
            return False
    else:
        return False

def cmpTracksByMarket(track1, track2):
    if len(track1['available_markets']) > len(track2['available_markets']):
        return True
    else:
        return False
    
def cmpAlbumsByReleaseDate(album1, album2):
    if int(album1['release_date']) > int(album2['release_date']):
        return True
    else:
        return False

def cmpAlbumsByReleaseDateRank(year, album):
    if int(year) == int(album['release_date']):
        return 0
    return -1

def cmpAlbumName(album_id, album):
    if album_id == album['id']:
        return 0

def cmpArtistsIdByArtistsName(artist_id, artist):
    if str(artist_id) == str(artist['id']):
        return 0

def cmpRelevantArtistTrack(track_id, track):
    if track_id == track:
        return 0

"""
SORTING FUNCTIONS
"""

def sortList(list, cmp_function):
    
    sorted_list = me.sort(list, cmp_function)
    
    return sorted_list

def sortArtists(catalog):
    sorted_list = sortList(catalog['artists'], cmpArtistsByPopularity)
    
    return sorted_list

def sortTracks(catalog):
    sorted_list = sortList(catalog['tracks'], cmpTracksByPopularity)
    
    return sorted_list

def sortAlbums(catalog):
    sorted_list = sortList(catalog['albums'], cmpAlbumsByReleaseDate)
    
    return sorted_list

def sortTracksByMarkets(artists_list):
    sorted_list = sortList(artists_list, cmpTracksByMarket)
    
    return sorted_list

def sortBestTracks(list):
    sorted_list =  sortList(list, cmpTracksByPopularity)

    return sorted_list

"""
SEARCHING FUNCTIONS
"""

def linearSearch(list, element, cmp_function):
    pos = -1

    for i in range(0, sizeList(list)):
        if cmp_function(element, lt.getElement(list, i)) == 0:
            pos = i 
    return pos

def findYearPosition(list, year):
    position = linearSearch(list, year, cmpAlbumsByReleaseDateRank)
    return position

def findArtistsInTracks(track_list, sorted_artists):
    for track in lt.iterator(track_list):
    
        for i in range(0, len(track['artists_id'])):
            
            position = linearSearch(sorted_artists, track['artists_id'][i], cmpArtistsIdByArtistsName) 
            artist = lt.getElement(sorted_artists, position)
            name = artist['name']
            track['artists_id'][i] = name
                                
def findAlbumName(track_list, sorted_albums):
    for track in lt.iterator(track_list):
        position = linearSearch(sorted_albums, track['album_id'], cmpAlbumName)
        album = lt.getElement(sorted_albums, position)
        name = album['name']
        track['album_id'] = name

def findArtistRelevantTrack(sorted_artists, sorted_tracks):
    for artist in lt.iterator(sorted_artists):
        position = linearSearch(sorted_tracks, artist['track_id'], cmpRelevantArtistTrack)   
        track = lt.getElement(sorted_tracks, position)  
        if position == -1:
            artist['track_id'] = 'UNNKNOWN'  
        else:            
            name = track['name']
            artist['track_id'] = name

def findartistInAlbums(sorted_albums, sorted_artists):
    for album in lt.iterator(sorted_albums):
        position = linearSearch(sorted_artists, album['artist_id'], cmpArtistsIdByArtistsName)
        artist = lt.getElement(sorted_artists, position)
        name = artist['name']
        album['artist_id'] = name

def findArtistTracks(artist_name, country_name, sorted_tracks, sorted_albums):
    tracks = lt.newList('ARRAY_LIST')
    albums = lt.newList('ARRAY_LIST')
    for track in lt.iterator(sorted_tracks):
        for i in range(0,len(track['artists_id'])):
            for j in range(0, len(track['available_markets'])):
                if track['artists_id'][i] == artist_name and track['available_markets'][j] == country_name:
                    lt.addLast(tracks, track)
                
    for album in lt.iterator(sorted_albums):
        for j in range(0, len(album['available_markets'])):
            if album['artist_id'] == artist_name and album['available_markets'][j] == country_name:
                lt.addLast(albums, album)
    
    sorted_list = sortList(tracks, cmpTracksByPopularity)


    return(lt.getElement(sorted_list, 1), sizeList(sorted_list), sizeList(albums))
    

def findArtistAlbums(artist_name, sorted_tracks, sorted_albums):
    album_album = lt.newList('ARRAY_LIST')
    album_single = lt.newList('ARRAY_LIST')
    album_compilation = lt.newList('ARRAY_LIST')
    albums = lt.newList('ARRAY_LIST')
    best_tracks = lt.newList('ARRAY_LIST')

    for album in lt.iterator(sorted_albums):
        if album['artist_id'] == artist_name:
            lt.addLast(albums, album)
            if album['album_type'] == 'album': 
                lt.addLast(album_album, album)
            elif album['album_type'] == 'single':
                lt.addLast(album_single, album)
            elif album['album_type'] == 'compilation':
                lt.addLast(album_compilation, album)
    
    for album in lt.iterator(albums):
        for track in lt.iterator(sorted_tracks):
            if album['name'] == track['album_id']:
                lt.addLast(best_tracks, track)
                  
    return(sizeList(album_album), sizeList(album_single), sizeList(album_compilation), albums, best_tracks)

def findTracksInAlbums(lista, sorted_tracks):
    
    tracks = lt.newList('ARRAY_LIST')
    for track in lt.iterator(sorted_tracks):
        for album in lt.iterator(lista):
            if track['album_id'] == album['name']:
                lt.addLast(tracks, track)
    
    return(tracks)


        
            
            
        


    
        
        

            

        
        

   
    