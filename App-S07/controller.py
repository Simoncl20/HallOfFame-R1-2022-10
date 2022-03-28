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

csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def loadData(tipo_lista, file_size):
    catalog = model.newCatalog(tipo_lista)
    tracks_size = loadTracks(catalog, file_size)
    albums_size = loadAlbums(catalog, file_size)
    artists_size = loadArtists(catalog, file_size)
    catalog, sorting_time = sortDataById(catalog)
    tracks = tracks_size, catalog['tracks']
    albums = albums_size, catalog['albums']
    artists = artists_size, catalog['artists']
    return tracks, albums, artists, sorting_time
# Funciones para la carga de datos

def loadTracks(catalog, file_size):
    tracksfile = cf.data_dir + f'Spotify/spotify-tracks-utf8-{file_size}.csv'
    input_file = csv.DictReader(open(tracksfile, encoding='utf-8'))
    for track in input_file:
        model.addTrack(catalog, track)
    return model.trackSize(catalog)

def loadAlbums(catalog, file_size):
    albumbsfile = cf.data_dir + f'Spotify/spotify-albums-utf8-{file_size}.csv'
    input_file = csv.DictReader(open(albumbsfile, encoding='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)
    return model.albumSize(catalog)

def loadArtists(catalog, file_size):
    artistsfile = cf.data_dir + f'Spotify/spotify-artists-utf8-{file_size}.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for album in input_file:
        model.addArtist(catalog, album)
    return model.artistSize(catalog)

# Funciones de ordenamiento

def sortDataById(catalog):
    catalog['tracks'], track_time = model.sortDataById('merge', catalog['tracks'], model.trackSize(catalog))
    catalog['albums'], album_time = model.sortDataById('merge', catalog['albums'], model.albumSize(catalog))
    catalog['artists'], artist_time = model.sortDataById('merge', catalog['artists'], model.artistSize(catalog))
    total_time = track_time+album_time+artist_time
    return catalog, total_time

def sortArtistsByPopularity(algoritmo, lista, tamanio):
    return model.sortArtistsByPopularity(algoritmo, lista, tamanio)

def sortAlbumsByYear(algoritmo, lista, tamanio):
    return model.sortAlbumsByYear(algoritmo, lista, tamanio)

def sortTracksByPopularity(algoritmo, lista, tamanio):
    return model.sortTracksByPopularity(algoritmo, lista, tamanio)

def sortTracksByMarkets(algoritmo, tracks, size_tracks):
    return model.sortTracksByMarkets(algoritmo, tracks, size_tracks)

# Funciones de consulta sobre el catálogo

def getAlbumsInRange(list, lo, hi):
    return model.getAlbumsInRange(list, lo, hi)

def searchArtistById(list, artists):
    return model.searchArtistById(list, artists)

def searchTrackById(list, tracks):
    return model.searchTrackById(list, tracks)

def searchTracksByMarket(tracks, market_name):
    return model.searchTracksByMarket(tracks, market_name)

def searchTracksByArtist(tracks, artist_id):
    return model.searchTracksByArtist(tracks, artist_id)

def searchAlbumsByArtist(albums, artist_id):
    return model.searchAlbumsByArtist(albums, artist_id)

def searchTracksByAlbum(tracks, album_id):
    return model.searchTracksByAlbum(tracks, album_id)

def getAlbumInfo(albums, tracks):
    return model.getAlbumInfo(albums, tracks)

def getArtistId(artists, artist_name):
    return model.getArtistId(artists, artist_name)

def getArtistName(artists, artist_id):
    return model.getArtistName(artists, artist_id)

# Funciones para medir tiempos de ejecucion

def getTime():
    return model.getTime()


def deltaTime(start, end):
    elapsed = model.deltaTime(start, end)
    return elapsed