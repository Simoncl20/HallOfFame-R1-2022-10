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
 """

import config as cf
import model
import csv
import sys 
import os

default_limit = 1000
sys.setrecursionlimit(default_limit*10)
csv.field_size_limit(2147483647)


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.newCatalog()
    return control

# Inicialización del Catálogo de libros

def loadData(tamanio_archivo, control):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control['model']
    album = loadAlbums(tamanio_archivo, catalog)
    artist = loadArtists(tamanio_archivo, catalog)
    track = loadTracks(tamanio_archivo, catalog)
    
    return album, artist, track

def loadAlbums(archive_size, catalog):
    albums_file = os.path.join(cf.data_dir, 'Spotify', f'spotify-albums-utf8-{archive_size}.csv')
    input_file = csv.DictReader(open(albums_file, encoding='utf8'))
    for album in input_file:
        model.addAlbum(catalog, album)


def loadArtists(archive_size, catalog):

    artists_file = os.path.join(cf.data_dir, 'Spotify', f'spotify-artists-utf8-{archive_size}.csv')
    input_file = csv.DictReader(open(artists_file, encoding='utf8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    

def loadTracks(archive_size, catalog):

    tracks_file = os.path.join(cf.data_dir, 'Spotify', f'spotify-tracks-utf8-{archive_size}.csv')
    input_file = csv.DictReader(open(tracks_file, encoding='utf8'))
    for track in input_file:
        model.addTrack(catalog, track)


# Ordenamiento artistas

def sizeList(list):
    return model.sizeList(list)

def createSubList(list, position, size):
    return model.createSubList(list, position, size)

def createSubList2(list, position, size):
    return model.createSubList2(list, position, size)

def sortArtists(control):
    """
    Ordena los artistas por followers
    """
    return model.sortArtists(control['model'])

# Ordenamiento canciones

def sortTracks(control):
    """
    Ordena los tracks por popularity
    """
    return model.sortTracks(control['model'])

def sortAlbums(control):
    return model.sortAlbums(control['model'])

def sortTracksByMarket(artists_list):
    return model.sortTracksByMarkets(artists_list)

def findYearPosition(albums, initial_year):
    return model.findYearPosition(albums, initial_year)

def findArtistsInTracks(track_list, sorted_artists):
    return model.findArtistsInTracks(track_list, sorted_artists)

def findAlbumName(track_list, sorted_albums):
    return model.findAlbumName(track_list, sorted_albums)

def findArtistRelevantTrack(sorted_artists, sorted_tracks):
    return model.findArtistRelevantTrack(sorted_artists, sorted_tracks)

def findartistInAlbums(sorted_albums, sorted_artists):
    return model.findartistInAlbums(sorted_albums, sorted_artists)

def findArtistTracks(artist_name, country_name, sorted_tracks, sorted_albums):
    return model.findArtistTracks(artist_name, country_name, sorted_tracks, sorted_albums)

def findArtistAlbums(artist_name, sorted_tracks, sorted_albums):
    return model.findArtistAlbums(artist_name, sorted_tracks, sorted_albums)

def findTracksInAlbums(lista, sorted_tracks):
    return model.findTracksInAlbums(lista, sorted_tracks)

# Primeros  y últimos 3 elementos

def albumSubList(catalog):
    sublist_album = model.albumSublist(catalog)
    return sublist_album

def artistSubList(catalog):
    sublist_artist = model.artistSublist(catalog)
    return sublist_artist

def trackSubList(catalog):
    sublist_track = model.trackSublist(catalog)
    return sublist_track

 # Obtener tamaño de las listas

def albumSize(catalog):
    size_album = model.albumSize(catalog)
    return size_album

def artistSize(catalog):
    size_artist = model.artistSize(catalog)
    return size_artist

def trackSize(catalog):
    size_track = model.trackSize(catalog)
    return size_track

