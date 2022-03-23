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

from operator import mod
import config as cf
import model
import csv

csv.field_size_limit(2147483674)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del Catálogo de música (canciones, autores, albumes)

def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }

    control['model'] = model.newCatalog()
    return control


# Creacion de un catalogo solo para el lab4:

def newControllerType():
    """
    Crea un controlador alternativo para la opción
    El catalogo no se inicializa, pues se crea solo en caso de usar la opción 6
    """
    control = {
        'model': None
    }
    return control


# inicalización del catalogo de la opción 6
def newCatalogType(list_type):
    """
    retorna el catalogo inicializado con un tipo de lista especifico
    """
    return model.newCatalogType(list_type)


# otras funciones lab 4

def subList(list, n):
    return model.subList(list, n)


def truncarCatalogo(catalog, pct):
    return model.truncarCatalogo(catalog, pct)


# Funciones para la carga de datos

def loadData(control):
    """carga los datos de los archivos """
    catalog = control['model']
    artists = loadArtists(catalog)
    albums = loadAlbums(catalog)
    songs = loadSongs(catalog)

    return songs, artists, albums


def loadSongs(catalog):
    """Carga las canciones del archivo"""
    songsFile = cf.data_dir + 'GoodReads/spotify-tracks-utf8-small.csv'
    input_file = csv.DictReader(open(songsFile, encoding='utf-8'))
    for song in input_file:
        model.addSong(catalog, song)
    return model.songSize(catalog)


def loadArtists(catalog):
    """Carga los artistas del archivo de artistas"""
    artistsFile = cf.data_dir + 'GoodReads/spotify-artists-utf8-small.csv'
    input_file = csv.DictReader(open(artistsFile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    return model.artistSize(catalog)


def loadAlbums(catalog):
    """carga los albumes del archivo de albumes"""
    albumsFile = cf.data_dir + 'GoodReads/spotify-albums-utf8-small.csv'
    input_file = csv.DictReader(open(albumsFile, encoding='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)
    return model.albumSize(catalog)


# Funciones de consulta
def getSong(catalog, number):
    '''Retorna una canción en una posición dada por parametro'''
    return model.getSong(catalog, number)


def getArtist(catalog, number):
    '''Retorna el artista en una posición dada por parametro'''
    return model.getArtist(catalog, number)


def getAlbum(catalog, number):
    '''Retorna el album en una posición dada por parametro'''
    return model.getAlbum(catalog, number)


def songSize(catalog):
    return model.songSize(catalog)


def artistSize(catalog):
    return model.artistSize(catalog)


def albumSize(catalog):
    return model.albumSize(catalog)


def getElement(list, pos):
    return model.getElement(list, pos)


def albumsInTimePeriod(anoI, anoF, control):
    return model.albumsInTimePeriod(anoI, anoF, control['model'])

def getTopXArtists(cantidad, control):
    return model.getTopXArtists(cantidad, control)
def getTopXsongs(top, control):
    return model.getTopXsongs(top, control['model'])


def getBestSongs(artistName, country, control):
    return model.getBestSongs(artistName, country, control['model'])


def getArtistSongNumber(artist):
    return model.getArtistSongNumber(artist)


def getArtistAlbumNumber(artist):
    return model.getArtistAlbumNumber(artist)


# Funciones de ordenamiento
def insertionSortArtists(control, size):
    """
    Ordena los artistas por número de seguidores por el algoritmo insertion
    """
    return model.insertionSortArtists(control['model'], size)


def selectionSortArtists(control, size):
    """
    Ordena los artistas por número de seguidores por el algoritmo selection
    """
    return model.selectionSortArtists(control['model'], size)


def shellSortArtists(control, size):
    """
    Ordena los artistas por número de seguidores por el algoritmo insertion
    """
    return model.shellSortArtists(control['model'], size)


def quickSortArtists(control, size):
    """
    Ordena los artistas por número de seguidores por el algoritmo insertion
    """
    return model.quickSortArtists(control['model'], size)


def mergeSortArtists(control, size):
    """
    Ordena los artistas por número de seguidores por el algoritmo insertion
    """
    return model.mergeSortArtists(control['model'], size)


def mergeSortAlbumsbyYear(control):
    """
    """
    return model.mergeSortAlbumsbyYear(control['model'])

# Funciones de consulta sobre el catálogo
def buscarCancionID(catalog, id):
    return model.buscarCancionID(catalog,id)
def numeroAlbumesPorTipoPorArtista(catalog,artist):
    return model.numeroAlbumesPorTipoPorArtista(catalog,artist)

def mergeSortSongList(songs):
    return model.mergeSortSongList(songs)