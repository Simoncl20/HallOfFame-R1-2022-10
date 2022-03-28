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
from datetime import datetime
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as IS
from DISClib.Algorithms.Sorting import selectionsort as SS
from DISClib.Algorithms.Sorting import shellsort as ShS
from DISClib.Algorithms.Sorting import quicksort as QS
from DISClib.Algorithms.Sorting import mergesort as MS
from DISClib.Algorithms.Sorting import insertionsort as IS
import re

#medir tiempos de ejecución
from timeit import default_timer as timer

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = { 'tracks': None,
                'artists': None,
                'albums': None}
    
    catalog['tracks'] = lt.newList('ARRAY_LIST')
    catalog['artists'] = lt.newList('ARRAY_LIST')
    catalog['albums'] = lt.newList('ARRAY_LIST')
    
    return catalog

# Funciones para agregar informacion al catalogo
def addTrack(catalog, track):
    lt.addLast(catalog['tracks'], track)
    return catalog

def addArtist(catalog, artist):
    #transformar popularity a int
    artist['artist_popularity']=int(float(artist['artist_popularity']))

    lt.addLast(catalog['artists'], artist)
    return catalog    

def addAlbum(catalog, album):

    #transformar release date str->datetime
    if len(album['release_date'])==10:
        album['release_date'] = datetime.strptime(album['release_date'], "%Y-%m-%d")
    elif len(album['release_date'])==4:
        album['release_date'] = datetime.strptime(album['release_date'], "%Y")
    elif len(album['release_date'])==6:
        album['release_date'] = datetime.strptime(album['release_date'], "%b-%y")

    lt.addLast(catalog['albums'], album)
    return catalog

# Funciones para creacion de datos
def crear_artist_name(lista_auxiliar, album):
    indice = busqueda_binaria(lista_auxiliar, album['artist_id'], 'id', 'igual')
    album['artist_name'] = 'Unknown'
    if indice>0:
        album['artist_name'] = lt.getElement(lista_auxiliar, indice)['name']

def crear_best_track(lista_auxiliar, artist):
    indice = busqueda_binaria(lista_auxiliar, artist['track_id'], 'id', 'igual')
    artist['best_track'] = 'Unknown'
    if indice>0:
        artist['best_track'] = lt.getElement(lista_auxiliar, indice)['name']

def crear_artist(lista_auxiliar, track):
    track['artists_names'] = lt.newList('ARRAY_LIST')
    track['artists_id'] = convertir_str_a_lista(track['artists_id'])
    for i in lt.iterator(track['artists_id']):
        indice = busqueda_binaria(lista_auxiliar, i, 'id', 'igual')
        nombre = 'Unknown'
        if indice>0:
            nombre = lt.getElement(lista_auxiliar, indice)['name']
        lt.addLast(track['artists_names'], nombre)
    track['artists_names_str'] = convertir_lista_a_str(track['artists_names'])

def crear_album(lista_auxiliar, track):
    indice = busqueda_binaria(lista_auxiliar, track['album_id'], 'id', 'igual')
    track['album_name'] = 'Unknown'
    if indice>0:
        track['album_name'] = lt.getElement(lista_auxiliar, indice)['name']
        track['release_date'] = lt.getElement(lista_auxiliar, indice)['release_date']




def crear_territorios(track):
    track['available_markets'] = convertir_str_a_lista(track['available_markets'])
    track['distribution'] = lt.size(track['available_markets'])

def crear_total_albumes_del_artista(lista_auxiliar, artist):
    artist['total_albums'] = 0
    for album in lt.iterator(lista_auxiliar):
        if artist['name'] == album['artist_name']:
            artist['total_albums'] += 1

    
    


def convertir_str_a_lista(s):
    s=s.replace('[','')
    s=s.replace(']','')
    s=s.replace('\'','')
    s=s.replace(' ','')
    s=s.replace('\"','')
    lista = lt.newList('ARRAY_LIST')
    s+=','
    aux = ''
    for i in range(0,len(s),1):
        if s[i]==',':
            lt.addLast(lista, aux)
            aux = ''
        else:
            aux = aux+s[i]
    return lista

def convertir_lista_a_str(l):
    cadena = ''
    for i in lt.iterator(l):
        cadena = cadena+i
        cadena = cadena+', '
    cadena = cadena[0:-2]        
    return cadena


    
# Funciones de consulta
def getInfo1(catalog):
    tracks = catalog['tracks']
    tracks3y3 = lt.newList('ARRAY_LIST')    
    for x in range(1,7,1):
        if x<=3:
            track = lt.getElement(tracks, x)
        else:
            track = lt.getElement(tracks, lt.size(tracks)-(6-x))
        lt.addLast(tracks3y3, track)
    
    artists = catalog['artists']
    artists3y3 = lt.newList('ARRAY_LIST')
    for x in range(1,7,1):
        if x<=3:
            artist = lt.getElement(artists, x)
        else:
            artist = lt.getElement(artists, lt.size(artists)-(6-x))
        lt.addLast(artists3y3, artist)

    albums = catalog['albums']
    albums3y3 = lt.newList('ARRAY_LIST')
    for x in range(1,7,1):
        if x<=3:
            album = lt.getElement(albums, x)
        else:
            album = lt.getElement(albums, lt.size(albums)-(6-x))
        lt.addLast(albums3y3, album)

    return tracks3y3, artists3y3, albums3y3

def getInfo2(catalog, inicial, final):
    sort_list_by(catalog['albums'], cmpAlbumsByYear)
 
    albums_en_rango = lt.newList("ARRAY_LIST")
    mas_alto = busqueda_binaria(catalog['albums'], final, 'release_date', 'max')
    mas_bajo = busqueda_binaria(catalog['albums'], inicial, 'release_date', 'min')
    albums_en_rango = lt.subList(catalog['albums'], mas_bajo, (mas_alto-mas_bajo))

    albums_en_rango3y3 = lt.newList('ARRAY_LIST')
    for x in range(1,7,1):
        if x<=3:
            album = lt.getElement(albums_en_rango, x)
        else:
            album = lt.getElement(albums_en_rango, lt.size(albums_en_rango)-(6-x))
        lt.addLast(albums_en_rango3y3, album)
    
    return albums_en_rango3y3

def getInfo3(catalog, top_n):
    sort_list_by(catalog['artists'], cmpArtistByPopularity)
    top_n_artistas = lt.subList(catalog['artists'], 1, top_n)
    
    top_n_artistas3y3 = lt.newList('ARRAY_LIST')
    for x in range(1,7,1):
        if x<=3:
            artist = lt.getElement(top_n_artistas, x)
        else:
            artist = lt.getElement(top_n_artistas, lt.size(top_n_artistas)-(6-x))
        lt.addLast(top_n_artistas3y3, artist)
    return top_n_artistas3y3
    
def getInfo4(catalog, top_n):
    sort_list_by(catalog['tracks'], cmpTracksByPopularity)
    top_n_tracks = lt.subList(catalog['tracks'], 1, top_n)

    top_n_tracks3y3 = lt.newList('ARRAY_LIST')
    for x in range(1,7,1):
        if x<=3:
            track = lt.getElement(top_n_tracks, x)
        else:
            track = lt.getElement(top_n_tracks, lt.size(top_n_tracks)-(6-x))
        lt.addLast(top_n_tracks3y3, track)
    return top_n_tracks3y3

def getInfo5(catalog, nombre_artista, territorio):

    total_canciones = 0
    canciones_en_territorio = lt.newList('ARRAY_LIST')
    for track in lt.iterator(catalog['tracks']):
        cond1= False
        cond2= False
        for nombre in lt.iterator(track['artists_names']):
            if nombre == nombre_artista:
                cond1= True
                total_canciones+=1
        for pais in lt.iterator(track['available_markets']):
            if pais == territorio:
                cond2= True
        if cond1 and cond2:
            lt.addLast(canciones_en_territorio, track)            

    total_albumes = 0
    for album in lt.iterator(catalog['albums']):
        if nombre_artista == album['artist_name']:
            total_albumes+=1

    sort_list_by(canciones_en_territorio, cmpTracksByPopularity)
    top_track = lt.getElement(canciones_en_territorio, 1)
    return top_track, total_canciones, total_albumes, nombre_artista, territorio

def getInfo6(catalog, nombre_artista):

    singles = 0
    compilations = 0
    albums = 0

    sort_list_by(catalog['tracks'], cmpTracksByPopularity)

    albums_del_artista = lt.newList('ARRAY_LIST')
    for album in lt.iterator(catalog['albums']):
        if nombre_artista == album['artist_name']:
            if album['album_type'] == 'single':
                singles+=1
            elif album['album_type'] == 'compilation':
                compilations+=1
            elif album['album_type'] == 'album':
                albums+=1

            tracks_del_album = lt.newList('ARRAY_LIST')
            for track in lt.iterator(catalog['tracks']):
                if track['album_id'] == album['id']:
                    lt.addLast(tracks_del_album, track)

            album['top_track'] = lt.getElement(tracks_del_album, 1)

            lt.addLast(albums_del_artista, album)


    albums_del_artista3y3 = lt.newList('ARRAY_LIST')
    for x in range(1,7,1):
        if x<=3:
            album = lt.getElement(albums_del_artista, x)
        else:
            album = lt.getElement(albums_del_artista, lt.size(albums_del_artista)-(6-x))
        lt.addLast(albums_del_artista3y3, album)

    return albums_del_artista3y3, singles, compilations, albums

def getInfo7(catalog, inicial, final, top_n):


    sort_list_by(catalog['tracks'], cmpAlbumsByYear)
    tracks_en_rango = lt.newList("ARRAY_LIST")
    mas_alto = busqueda_binaria(catalog['tracks'], final, 'release_date', 'max')
    mas_bajo = busqueda_binaria(catalog['tracks'], inicial, 'release_date', 'min')
    tracks_en_rango = lt.subList(catalog['tracks'], mas_bajo, (mas_alto-mas_bajo))

    sort_list_by(tracks_en_rango, cmpTracksByDistribution)
    top_n_tracks = lt.subList(tracks_en_rango, 1, top_n)

    top_n_tracks3y3 = lt.newList('ARRAY_LIST')
    for x in range(1,7,1):
        if x<=3:
            track = lt.getElement(top_n_tracks, x)
        else:
            track = lt.getElement(top_n_tracks, lt.size(top_n_tracks)-(6-x))
        lt.addLast(top_n_tracks3y3, track)
    return top_n_tracks3y3



    



def trackSize(catalog):
    return lt.size(catalog['tracks'])

def artistSize(catalog):
    return lt.size(catalog['artists'])

def albumSize(catalog):
    return lt.size(catalog['albums'])

# Funciones utilizadas para comparar elementos dentro de una lista


def cmpArtistByPopularity(artist1, artist2):
    if float(artist1['artist_popularity']) > float(artist2['artist_popularity']):
        return 1
    elif float(artist1['artist_popularity']) == float(artist2['artist_popularity']):
        return cmpArtistsByFollowers(artist1, artist2)
    else:
        return 0
def cmpArtistsByFollowers(artist1, artist2):
    if float(artist1['followers']) > float(artist2['followers']):
        return 1
    elif float(artist1['followers']) == float(artist2['followers']):
        return cmpArtistByName(artist1, artist2)
    else:
        return 0
def cmpArtistByName(artist1, artist2):
    if artist1['name'] > artist2['name']:
        return 1
    else:
        return 0
def cmpArtistsById(artist1, artist2):
    if artist1['id'] < artist2['id']:
        return 1
    else:
        return 0


def cmpAlbumsByYear(album1, album2):
    if album1['release_date'] < album2['release_date']:
        return 1
    else:
        return 0
def cmpAlbumsById(album1, album2):
    if album1['id'] < album2['id']:
        return 1
    else:
        return 0

def cmpTracksByDistribution(track1, track2):
    if float(track1['distribution']) > float(track2['distribution']):
        return 1
    elif float(track1['distribution']) == float(track2['distribution']):
        return cmpTracksByPopularity(track1, track2)
    else:
        return 0
def cmpTracksById(track1, track2):
    if track1['id'] < track2['id']:
        return 1
    else:
        return 0
def cmpTracksByPopularity(track1, track2):
    if float(track1['popularity']) > float(track2['popularity']):
        return 1
    elif float(track1['popularity']) == float(track2['popularity']):
        return cmpTracksByDuration(track1, track2)
    else:
        return 0
def cmpTracksByDuration(track1, track2):
    if float(track1['duration_ms']) > float(track2['duration_ms']):
        return 1
    elif float(track1['duration_ms']) == float(track2['duration_ms']):
        return cmpTracksByName(track1, track2)
    else:
        return 0
def cmpTracksByName(track1, track2):
    if track1['name'] > track2['name']:
        return 1
    else:
        return 0    


def cmpCountriesByName(c1, c2):
    if c1 > c2:
        return 1
    else:
        return 0

# Funciones de ordenamiento
def sort_list_by(lst, criterio):
    L = MS.sort(lst, criterio)      #complejidad O(nlogn)
    return L

def insertion_sort(lst):
    L = IS.sort(lst, )


def busqueda_binaria(lista, x, propiedad: str, criterio: str)->int:
    izq=1
    der=lt.size(lista)
    
    while izq<=der:
        medio = int((izq+der)/2)
        if lt.getElement(lista, medio)[propiedad] == x:
            if criterio == 'max':
                i = medio
                while lt.getElement(lista, i)[propiedad] == x:
                    i+=1
                    medio = i
                return medio
            elif criterio == 'min':
                i = medio
                while lt.getElement(lista, i)[propiedad] == x:
                    medio  = i
                    i-=1
                return medio
            elif criterio == 'igual':
                return medio
        elif lt.getElement(lista, medio)[propiedad]>x:
            der = medio-1
        else: 
            izq = medio+1
    if criterio == 'igual':
        return -1
    else:
        return medio

def busqueda_lineal(lista, x, propiedad)->int:
    for i in range(1,lt.size(lista),1):
        if lt.getElement(lista,i)[propiedad] == x:
            return i
    return 0



# Funciones para medir tiempos de ejecucion

def time_start():
    start = timer()
    return start

def time_end(start):    
    end = timer()
    return("tiempo: "+str(1000*(end-start)))