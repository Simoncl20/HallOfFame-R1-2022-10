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

def newController(listType):
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """

    control = {'model': None}
    control['model'] = model.newCatalog(listType)
    return control

# Funciones para la carga de datos

def loadData(control):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    start_time = model.getTime()
    catalog = control['model']
    albums = loadAlbums(catalog)
    artists = loadArtists(catalog)
    tracks = loadTracks(catalog)
    print('Organizando información, espere un momento...')
    model.sortSpotifyLists(catalog)
    print('Fusionando información, espere un momento...')
    model.connectFullData(catalog)
    print('Creando listas auxiliares, espere un momento...')
    model.newSortedAuxLists(catalog)
    end_time = model.getTime()
    delta_time = model.deltaTime(start_time,end_time)
    print('Tiempo de ejecucion: ', delta_time)
    return albums, artists, tracks

def loadAlbums(catalog, suffix = '-large.csv'):
    """
    Carga los albumes del archivo.
    """
    albumsfile = cf.data_dir + 'Spotify/spotify-albums-utf8' + suffix
    input_file = csv.DictReader(open(albumsfile, encoding ='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)
    return model.albumsSize(catalog)

def loadArtists(catalog, suffix = '-large.csv'):
    """
    Carga los albumes del archivo.
    """
    artistsfile = cf.data_dir + 'Spotify/spotify-artists-utf8' + suffix
    input_file = csv.DictReader(open(artistsfile, encoding ='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    return model.artistsSize(catalog)

def loadTracks(catalog, suffix = '-large.csv'):
    """
    Carga los albumes del archivo.
    """
    tracksfile = cf.data_dir + 'Spotify/spotify-tracks-utf8' + suffix
    input_file = csv.DictReader(open(tracksfile, encoding ='utf-8'))
    for track in input_file:
        model.addTrack(catalog, track)
    return model.tracksSize(catalog)

# Funciones de ordenamiento
def sortpopularityartist(catalog):
    return model.sortpopularityartist(catalog)

# Funciones de consulta sobre el catálogo

#Requerimiento 1
def albumsByReleaseYear(catalog, min, max):
    answerLstreq, time = model.albumsByReleaseYear(catalog, min, max)
    return answerLst(answerLstreq), time, model.lt.size(answerLstreq)

#Requerimiento 2
def artistByPopularity(catalog, top):
    answerLstreq, time = model.artistByPopularity(catalog, top)
    return answerLst(answerLstreq), time, model.lt.size(answerLstreq)

#Requerimiento 3
def tracksByPopularity(num, catalog):
    answerLstreq, time = model.tracksByPopularity(num, catalog)
    return answerLst(answerLstreq), time, model.lt.size(answerLstreq)

#Requerimiento 4
def popularTrackByArtist(catalog, artistName, countryCode):
    answerLstreq, time = model.popularTrackByArtist(catalog,artistName, countryCode)
    return answerLst(answerLstreq), time, model.lt.size(answerLstreq)

#Requerimiento 5
def albumInfo(catalog, artistName):
    sizeAlbumsArtist, countByType, albumssorted, trackArray, delta_time = model.albumInfo(catalog, artistName)
    return sizeAlbumsArtist, countByType, answerLst(albumssorted), answerLst(trackArray), delta_time

#Bono
def tracksByDistributionInRange(catalog, min, max, top):
    answerLstreq, time = model.tracksByDistributionInRange(catalog, min, max, top)
    return answerLst(answerLstreq), time

def getLastNum(number, spotifyList):
    'Retorna los "number" ultimos'
    return model.getLastNum(number, spotifyList)

def getFirstNum(number, spotifyList):
    'Retorna los "number" primeros'
    return model.getFirstNum(number, spotifyList)

# Funciones de analisis

def calculator(catalog, sortType, suffix, listType):
    print('Espere un momento mientras se hace el promedio de el sort...')

    catalog['artists'] = model.resetList(listType)
    artists = loadArtists(catalog, suffix)
    time1, sortedLst = model.sortLstWithTime(catalog['artists'], artists, sortType)
    print('Primer sort completado:', time1)

    catalog['artists'] = model.resetList(listType)
    artists = loadArtists(catalog, suffix)
    time2, sortedLst = model.sortLstWithTime(catalog['artists'], artists, sortType)
    print('Segundo sort completado:', time2)

    catalog['artists'] = model.resetList(listType)
    artists = loadArtists(catalog, suffix)
    time3, sortedLst = model.sortLstWithTime(catalog['artists'], artists, sortType)
    print('Tercer sort completado:', time3)

    average = round(((time1 + time2 + time3) / 3),2)
    return average

# Funciones auxiliares

def answerLst(spotifyList):
    if model.lt.size(spotifyList) <= 6:
        return spotifyList
    else:
        firsts = getFirstNum(3, spotifyList)
        lasts = getLastNum(3, spotifyList)
        return model.listsFusion(firsts, lasts)