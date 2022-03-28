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
from DISClib.ADT import list as lt


csv.field_size_limit(1000000)


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newController():
    control = {
        'model': None
    }
    control['model']=model.newCatalog()
    return control

# Funciones para la carga de datos
def loadData(control):
    catalog = control['model']
    canciones = loadTracks(catalog)
    artistas = loadArtists(catalog)
    albumes = loadAlbums(catalog)
    agregar_datos_relacionados(catalog)
    return canciones, artistas, albumes

def loadTracks(catalog):
    tracksfile = cf.data_dir+ 'Spotify/spotify-tracks-utf8-small.csv'
    input_file = csv.DictReader(open(tracksfile, encoding='utf-8'))
    for track in input_file:
        model.addTrack(catalog, track)
    return model.trackSize(catalog)

def loadArtists(catalog):
    artistsfile = cf.data_dir+ 'Spotify/spotify-artists-utf8-small.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    return model.artistSize(catalog)

def loadAlbums(catalog):
    albumsfile = cf.data_dir+ 'Spotify/spotify-albums-utf8-small.csv'
    input_file = csv.DictReader(open(albumsfile, encoding='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)    
    return model.albumSize(catalog)    

def agregar_datos_relacionados(catalog):
    #agregar artist asociado al album
    lista_auxiliar = lt.subList(catalog['artists'],1,model.artistSize(catalog))
    model.sort_list_by(lista_auxiliar, model.cmpArtistsById)
    for album in lt.iterator(catalog['albums']):
        model.crear_artist_name(lista_auxiliar, album)

    
    #agregar album, artistas y territorios asociados al track
    lista_auxiliar = lt.subList(catalog['artists'],1,model.artistSize(catalog))
    model.sort_list_by(lista_auxiliar, model.cmpArtistsById)
    lista_auxiliar1 = lt.subList(catalog['albums'],1,model.albumSize(catalog))
    model.sort_list_by(lista_auxiliar1, model.cmpAlbumsById) 
    for track in lt.iterator(catalog['tracks']):
        model.crear_artist(lista_auxiliar, track)
        model.crear_album(lista_auxiliar1, track)
        model.crear_territorios(track)

    #agregar best_track asociada al artist
    lista_auxiliar = lt.subList(catalog['tracks'],1,model.trackSize(catalog))
    model.sort_list_by(lista_auxiliar, model.cmpTracksById)
    for artist in lt.iterator(catalog['artists']):
        model.crear_best_track(lista_auxiliar, artist)
    
    

    #modificar territorios de cada cancion
    

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def getInfo1(control):
    info1 = model.getInfo1(control['model'])
    return info1

def getInfo2(control, inicial, final):
    info2 = model.getInfo2(control['model'], inicial, final)
    return info2

def getInfo3(control, top_n):
    info3 = model.getInfo3(control['model'], top_n)
    return info3
    
def getInfo4(control, top_n):
    info4 = model.getInfo4(control['model'], top_n)
    return info4   

def getInfo5(control, nombre_artista, territorio):
    info5 = model.getInfo5(control['model'], nombre_artista, territorio)
    return info5

def getInfo6(control, nombre_artista):
    info6 = model.getInfo6(control['model'], nombre_artista)
    return info6

def getInfo7(control, inicial, final, top_n):
    info7 = model.getInfo7(control['model'], inicial, final, top_n)
    return info7