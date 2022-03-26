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

from unittest.mock import NonCallableMagicMock
import config as cf
import model
import csv
csv.field_size_limit(2147483647)


# Inicialización del Catálogo de canciones

def listaUsuario(listType):
    userCatalog = model.newUserCatalog(listType)
    return userCatalog


# Funciones para la carga de datos
     
def LoadUserData(userCatalog, muestra):
    loadUserSongs(userCatalog, muestra)
    loadUserArtists(userCatalog, muestra)
    loadUserAlbums(userCatalog, muestra)
    return userCatalog


def loadUserSongs(userCatalog, muestra):
    userSongsfile = cf.data_dir + 'spotify-tracks-utf8-'+muestra+'.csv'
    input_file = csv.DictReader(open(userSongsfile, encoding='utf-8'))
    for song in input_file:
        model.addUSERSong(userCatalog, song)


def loadUserArtists(userCatalog, muestra):
    userArtistsfile = cf.data_dir + 'spotify-artists-utf8-'+muestra+'.csv'
    input_file = csv.DictReader(open(userArtistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addUSERartists(userCatalog, artist)


def loadUserAlbums(userCatalog, muestra):
    userAlbumsfile = cf.data_dir + 'spotify-albums-utf8-'+muestra+'.csv'
    input_file = csv.DictReader(open(userAlbumsfile, encoding='utf-8'))
    for album in input_file:
        model.addUSERalbum(userCatalog, album)


# Funciones de ordenamiento para PRUEBAS

def orderUserCatalog(userCatalog, algType):
    if algType == 'insertion':
        userCatalog = model.insertionSort(userCatalog)
    elif algType == 'selection':
        userCatalog = model.selectionSort(userCatalog)
    elif algType == 'shell':
        userCatalog = model.shellSort(userCatalog)
    elif algType == 'quick':
        userCatalog = model.quickSort(userCatalog)
    elif algType == 'merge':
        userCatalog = model.mergeSort(userCatalog['artists'])
    return userCatalog

# Funciones de consulta sobre el catálogo
"""
Llamados a las funciones del modelo para la carga de datos:
"""

def LastArtists(userCatalog):
    tempCatalog = userCatalog['artists']
    return model.LastArtists(tempCatalog)
    
def LastAlbums(userCatalog):
    tempCatalog = userCatalog['albums']
    return model.LastAlbums(tempCatalog)

def LastSongs(userCatalog):
    tempCatalog = userCatalog['canciones']
    return model.LastSongs(tempCatalog)

"""
Llamado a la función en el modelo para el requerimiento 1:
"""

def rangedAlbum(userCatalog, añoInicial, añoFinal):
    return model.rangedAlbum(userCatalog, añoInicial, añoFinal)

"""
Llamado a la función en el modelo para el requerimiento 2:
"""
def topArtists(sortedArtists, userCatalog, N):
    return model.topArtists(sortedArtists, userCatalog, N)

"""
Llamado a la función en el modelo para el requerimiento 3:
"""

def TopSongs(sortedSongs, userCatalog, N):
    return model.TopSongs(sortedSongs, userCatalog, N)


"""
Llamado a la función en el modelo para el requerimiento 4:
"""


def aristsSongs(userCatalog, nombre, codigoPais):
    return model.getartistsSongs(userCatalog, nombre, codigoPais)


"""
Llamado a la función en el modelo para el requerimiento 5:
"""

def ctdAlbums(userCatalog, nombre):
    return model.ctdAlbums(userCatalog, nombre)

def albumsArt(userCatalog, nombre):
    return model.albumsSongsArt(userCatalog, nombre)

def bestSongsAlb(userCatalog, nombre):
    return model.bestSongsAlb(userCatalog, nombre)


# Funciones de tamaño sobre el catálogo

def tamañoMuestra(userCatalog):
    size1 = model.tamañoArtistas(userCatalog)
    size2 = model.tamañoAlbums(userCatalog)
    size3 = model.tamañoCanciones(userCatalog)
    return size1, size2, size3

# Funciones del ordenamiento sobre el catalogo

def sortArtists(userCatalog):
    return model.sortArtistsByPop(userCatalog)

def sortSongs(userCatalog):
    return model.sortSongsByPop(userCatalog)

#funciones de llamada para el BONO

def sortBonoSongs(userCatalog):
    return model.sortSongsByCountry(userCatalog)

def rangedBonoSongs(userCatalog, sortedSongs, añoInicial, añoFinal, N):
    return model.rangedBonoSongs(userCatalog, sortedSongs, añoInicial, añoFinal, N)
