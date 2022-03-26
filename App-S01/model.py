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


from os import remove
from posixpath import split
from queue import Empty
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
from tabulate import tabulate
from datetime import date, datetime
import time
assert cf


# Construccion de modelos

def newUserCatalog(listType):
    """
    Inicializa el catálogo de canciones. Crea una lista vacia para guardar
    todas las canciones, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los album. Retorna el catalogo inicializado. Se tienen en cuenta
    parametros dados en el view.
    """
    userCatalog = {'canciones': None,
               'artists': None,
               'albums': None}
    if listType == "ARRAY_LIST":
        userCatalog['canciones'] = lt.newList('ARRAY_LIST')
        userCatalog['artists'] = lt.newList('ARRAY_LIST', cmpfunction = cmpArtistsByFollowers)
        userCatalog['albums'] = lt.newList('ARRAY_LIST')
    elif listType == "SINGLE_LINKED":
        userCatalog['canciones'] = lt.newList('SINGLE_LINKED')
        userCatalog['artists'] = lt.newList('SINGLE_LINKED', cmpfunction = cmpArtistsByFollowers)
        userCatalog['albums'] = lt.newList('SINGLE_LINKED')
    return userCatalog

# Funciones para agregar informacion al catalogo

def addUSERSong(userCatalog, song):
    # Se adiciona la cancion a la lista de canciones. Funcion usada para la carga de datos
    lt.addLast(userCatalog['canciones'], song)


def addUSERartists(userCatalog, artist):
    # Se adiciona el artista a la lista de artistas. Funcion usada para la carga de datos
    lt.addLast(userCatalog['artists'], artist)


def addUSERalbum(userCatalog, album):
    # Se adiciona el album a la lista de albums. Funcion usada para la carga de datos
    lt.addLast(userCatalog['albums'], album)


# Funciones para creacion de datos


def addSong(catalog, song):
    # Se adiciona la cancion a la lista de canciones
    lt.addLast(catalog['canciones'], song)
    return catalog

def addArtist(catalog, artist):
    # Se adiciona el artista a la lista de artistas
    lt.addLast(catalog['artists'], artist)
    return catalog

def addAlbum(catalog, album):
    # Se adiciona el album a la lista de albums
    lt.addLast(catalog['albums'], album)
    return catalog


# Funciones de SIZE basicos

def songUSERSize(userCatalog):
    #retorna el tamaño del catalogo de canciones. Funcion usada en la carga de datos
    lt.size(userCatalog['canciones'])


def artistsUSERSize(userCatalog):
    #retorna el tamaño del catalogo de artistas. Funcion usada en la carga de datos
    lt.size(userCatalog['artists'])


def albumUSERSize(userCatalog):
    #retorna el tamaño del catalogo de albums. Funcion usada en la carga de datos
    lt.size(userCatalog['albums'])

"""------------------------"""

def songSize(catalog):
    #retorna el tamaño del catalogo de canciones.
    return lt.size(catalog['canciones'])


def artistSize(catalog):
    #retorna el tamaño del catalogo de artistas.
    return lt.size(catalog['artists'])


def albumSize(catalog):
    #retorna el tamaño del catalogo de albums
    return lt.size(catalog['albums'])

# Funciones utilizadas para comparar elementos dentro de una lista --------------------------

"""
Req 3 cmp functions.
"""

def cmpSongsByPop(song1, song2):
    #Se comparan las canciones segun su artumento de popularidad.
    if (float(song1['popularity']) > float(song2['popularity'])):
        return True

    #Si la popularidad es la misma, se hace uso de otro cmp auxiliar para compararlos por duracion.
    elif (float(song1['popularity']) == float(song2['popularity'])):
        return cmpByDuration(song1, song2)

def cmpByDuration(song1, song2):
    #Se comparan las canciones segun su argumento de duracion. 'duration_ms'
    if (float(song1['duration_ms']) > float(song2['duration_ms'])):
        return True
    
    #De igual modo, si llegan a ser iguales, se hace un ultimo llamado al cmp de comparar por nombres para continuar,
    elif (float(song1['duration_ms']) == float(song2['duration_ms'])):
        return compareauthors(song1, song2)

"""
Req 2 cmp functions.
"""

def cmpArtistsByPop(artist1, artist2):
    #Compara la popularidad de dos artistas que tienen como argumento 'artist_popularity'
    if (float(artist1['artist_popularity']) > float(artist2['artist_popularity'])):
        return True

    #Sin embargo, si la popularidad es la misma, se llamada a cmp auxiliar de nombre y seguidores
    elif (float(artist1['artist_popularity']) == float(artist2['artist_popularity'])):
        return cmpNameandFollowers(artist1, artist2)

def cmpNameandFollowers(artist1, artist2):
    #Compara los seguidores como argumento de los artistas. 
    #Del mismo modo, si llegan a ser iguales, se hace uso de otro cmp auxiliar para comparar los nombres.
    if (float(artist1['followers']) > float(artist2['followers'])):
        return True
    elif (float(artist1['followers']) == float(artist2['followers'])):
        return compareauthors(artist1, artist2)

"""
Auxiliar cmp functions.
"""
def cmpAlbumsByDate(album1, album2):
    """
    Devuelve verdadero (True) si la 'fecha de lanzamiento' del album1 es menor que la del album2
    Args:
    album1: informacion del primer album que incluye su valor 'release_date'
    album2: informacion del primer album que incluye su valor 'release_date'
    """
    if album1['release_date_precision'] == 'month':
        album1['release_date'] = '19'+album1['release_date'][-2:]
        date = datetime.strptime(album1['release_date'], "%Y") #se tiene en cuenta el caso en el que la fecha sea de la forma 'month-day'
        #De la fecha obtenida, solo sacamos el elemento year para compararlo.
        year = date.year

    elif album1['release_date_precision'] == 'day':#se tiene en cuenta el caso en el que la fecha sea de la forma 'year-month-day'
        date = datetime.strptime(album1['release_date'], "%Y-%m-%d")
        #De la fecha obtenida, solo sacamos el elemento year para compararlo.
        year = date.year
         

    elif album1['release_date_precision'] == 'year':#se tiene en cuenta el caso en el que la fecha sea de la forma 'year'
        year = album1['release_date'] 

    """"
    Se realiza la misma operatividad para encontrar el año, pero ahora para el album 2
    """
         
    
    if album2['release_date_precision'] == 'month': #se tiene en cuenta el caso en el que la fecha sea de la forma 'month-day'
         album2['release_date'] = '19'+album2['release_date'][-2:]
         date2 = datetime.strptime(album2['release_date'], "%Y") 
         #De la fecha obtenida, solo sacamos el elemento year para compararlo.
         year2 = date2.year

    elif album2['release_date_precision'] == 'day':#se tiene en cuenta el caso en el que la fecha sea de la forma 'year-month-day'
         date2 = datetime.strptime(album2['release_date'], "%Y-%m-%d")
         #De la fecha obtenida, solo sacamos el elemento year para compararlo.
         year2 = date2.year

    elif album2['release_date_precision'] == 'year': #se tiene en cuenta el caso en el que la fecha sea de la forma 'year'
         year2 = album2['release_date']


    return int(year)<int(year2)

def nameArtist(userCatalog, artist_id):
    #Funcion auxiliar para encontrar el nombre de referencia de un artista, mediante solo saber su id.
    nombreArtista = ''

    #Se recorre la lista de artistas guardando sus elementos, hasta que el id de la lista coincida con el parametro.
    for i in range(1, lt.size(userCatalog['artists'])):
        x = lt.getElement(userCatalog['artists'], i)
        if str(x['id']) in str(artist_id):
            nombreArtista = x['name']
    return nombreArtista

def getTrackRef(userCatalog, track_id):
    #Funcion auxiliar para encontrar el nombre de referencia de una cancion, mediante solo saber su id.
    trackRef = ''

    #Se recorre la lista de canciones guardando sus elementos, hasta que el id de la lista coincida con el parametro.
    for i in range(1, lt.size(userCatalog['canciones'])):
        x = lt.getElement(userCatalog['canciones'], i)
        if str(x['id']) in str(track_id):
            trackRef= x['name']
            break
    return trackRef

def getAlbumRef(userCatalog, album_id):
    #Funcion auxiliar para encontrar el nombre de referencia de un album, mediante solo saber su id.
    AlbumRef = ''

    #Se recorre la lista de albums guardando sus elementos, hasta que el id de la lista coincida con el parametro.
    for i in range(1, lt.size(userCatalog['albums'])):
        x = lt.getElement(userCatalog['albums'], i)
        if str(x['id']) in str(album_id):
            AlbumRef = x['name']
            break
    return AlbumRef

def getAlbumDate(userCatalog, album_id):
    #Funcion auxiliar para encontrar la FECHA de un album, mediante solo saber su id. ['release_date']
    AlbumRef = ''

    #Se recorre la lista de albums guardando sus elementos, hasta que el id de la lista coincida con el parametro.
    for i in range(1, lt.size(userCatalog['albums'])):
        x = lt.getElement(userCatalog['albums'], i)
        if str(x['id']) in str(album_id):
            AlbumRef = x['release_date']
            break
    return AlbumRef

def getArtistRef(userCatalog, artists_id):
    #Funcion auxiliar para encontrar el nombre de referencia de un artista, mediante solo saber su id.
    ArtistsRef = []

    #Se recorre la lista de artistas guardando sus elementos, hasta que el id de la lista coincida con el parametro.
    for i in range(1, lt.size(userCatalog['artists'])):
        x = lt.getElement(userCatalog['artists'], i)
        if str(x['id']) in str(artists_id):
            ArtistsRef.append(x['name'])

    #Spliteamos la coma y retornamos el nombre del artista.
    ArtistsRef = ", ".join(ArtistsRef)
    return ArtistsRef


def cmpArtistsByFollowers(artist1, artist2):
    """
    Devuelve verdadero (True) si los 'followers' de artist1 son mayores que los del artist2
    Args:
    artist1: informacion del primer artista que incluye su valor 'followers'
    """
    return (float(artist1['followers']) > float(artist2['followers']))
    
def compareauthors(artist1, artist2):
    """
    Devuelve verdadero (True) si el 'nombre' de artist1 es mayores que los del artist2
    Args:
    artist1: informacion del primer artista que incluye su valor 'name'
    """
    if artist1['name'].lower() > artist2['name'].lower():
        return True

def comparePopularity(song1, song2):
    """
    Devuelve verdadero (True) si la 'popularidad' de song1 es mayor que la de song2
    Args:
    artist1: informacion de la primera cancion que incluye su valor 'popularity'
    """
    if song1['popularity'] > song2['popularity']:
        return True
    elif float(song1['popularity']) > float(song2['popularity']):
        return compareauthors(song1, song2)

def cmpSongsByCountry(song1, song2):
    """
    Devuelve verdadero (True) si la cantidad de 'mercados' de song1 es mayor que la de song2.
    Pero si estas cantidades son equivalentes, se hace llamado de la funcion compartePopularity para continuar.
    Args:
    artist1: informacion del size de los mercados de la cancion 1 que incluye su valor 'available_markets'
    """
    if len(song1['available_markets']) > len(song2['available_markets']):
        return True
    
    elif len(song1['available_markets']) == len(song2['available_markets']):
        return comparePopularity(song1, song2)


""""
Carga de datos e impresion
"""

def LastArtists(tempCatalog):
    
    """ 
    Se recorre el catalgo de artistas en los rangos del 1 al 3, y del ultimo al antepenultimo. 
    La informacion de cada elemento por iteracion, se guarda en un lista auxiliar "headers".
    """

    headers = [["Nombre del artista", "Generos", "Popularidad", "Seguidores"]]
    for i in range(1, lt.size(tempCatalog)):
        if i < 4:
            x = lt.getElement(tempCatalog, i)

            characters = "'"
            coma = ','
            if x['genres'] != "[]":
                for z in range(len(characters)):
                    p = x['genres'][1:-1].replace(characters[z],"")
            else: p = "Unknown"

            for letra in range(len(coma)):
                p = p.replace(coma[letra],",\n")


            headers.append([x['name'], p, x['artist_popularity'], x['followers']])

    for i in range(-3, lt.size(tempCatalog)):
        if 1>i>-3:
            x = lt.getElement(tempCatalog, i)
            coma = ','
            characters = "'"
            if x['genres'] != "[]":
                for z in range(len(characters)):
                    p = x['genres'][1:-1].replace(characters[z],"")
            else: p = "Unknown"

            for letra in range(len(coma)):
                p = p.replace(coma[letra],",\n")

            headers.append([x['name'], p, x['artist_popularity'], x['followers']])

    return headers

def LastAlbums(tempCatalog):

    """ 
    Se recorre el catalgo de albums en los rangos del 1 al 3, y del ultimo al antepenultimo. 
    La informacion de cada elemento por iteracion, se guarda en un lista auxiliar "headers".
    """

    headers = [["Nombre album", "Tipo de album", "Mercados disponibles", "fecha de lanzamiento", "Tracks"]]
    for i in range(1, lt.size(tempCatalog)):
        if i < 4:
            x = lt.getElement(tempCatalog, i)
            characters = "'"
            if x['available_markets'] != "[]":
                for z in range(len(characters)):
                    p = x['available_markets'][1:-1].replace(characters[z],"")
                    p = p[:8]+"[...]"+p[(len(p)-7):]
            else: p = "Unknown"
            headers.append([x['name'], x['album_type'], p, x['release_date'], x['total_tracks']])

    for i in range(-3, lt.size(tempCatalog)):
        if 1>i>-3:
            x = lt.getElement(tempCatalog, i)
            characters = "'"
            if x['available_markets'] != "[]":
                for z in range(len(characters)):
                    p = x['available_markets'][1:-1].replace(characters[z],"")
                    p = p[:8]+"[...]"+p[(len(p)-7):]
            else: p = "Unknown"
            headers.append([x['name'], x['album_type'], p, x['release_date'], x['total_tracks']])

    return headers

def LastSongs(tempCatalog):

    """ 
    Se recorre el catalgo de canciones en los rangos del 1 al 3, y del antepenultimo al ultimo. 
    La informacion de cada elemento por iteracion, se guarda en un lista auxiliar "headers".
    """

    headers = [["Nombre canción", "duración en milisegundos", "Popularidad", "track number"]]
    for i in range(1, lt.size(tempCatalog)):
        if i < 4:
            x = lt.getElement(tempCatalog, i)
            characters = " "
            nombre = x['name']
            if len(x['name'])>30:
                for letra in range(len(characters)):
                    nombre = x['name'].replace(characters[letra], "\n")

            headers.append([nombre, x['duration_ms'], x['popularity'], x['track_number']])

    for i in range(-3, lt.size(tempCatalog)):
        if 1>i>-3:
            x = lt.getElement(tempCatalog, i)
            nombre = x['name']
            characters = " "
            if len(x['name'])>30:

                for letra in range(len(characters)):
                    nombre = x['name'].replace(characters[letra], "\n")
            headers.append([nombre, x['duration_ms'], x['popularity'], x['track_number']])
    return headers

#INICIO DE MODELADO DE LAS FUNCIONES DE LOS REQUIERIMIENTOS.

"""
Req 1 Funciones Main.
"""

def rangedAlbum(userCatalog, añoInicial, añoFinal):

    """
    Retorna una lista de albums ubicada entre periodos iniciales y finales dados, teniendo en cuenta su ['release_date']
    """

    #Se establece los 'headers', osea la cabecera de esas futuras listas de listas que seran impresas en una tabla.
    headers = [['Nombre Album', 'Lanzamiento','Tipo_album','album artista\s','total_tracks']]
    sortedAlbum = ms.sort(userCatalog['albums'], cmpAlbumsByDate)
    #primer recorrido sobre el catalogo de albums guardando sus elementos.
    for i in range(1, lt.size(sortedAlbum)):
        x = lt.getElement(sortedAlbum, i)

        #si el año a comparar esta entre los parametros de año inicial y año final dado, 
        #se guardan los elementos del album en el que estamos.
        if añoInicial<int(x['release_date'][:4])<añoFinal:
            characters = " "

            for letra in range(len(characters)):#compresion del texto 'nombre'
                a = x['name'].replace(characters[letra],"\n")

            artistas = nameArtist(userCatalog, (x['artist_id'])) #Funcion auxiliar para obtener los nombres de los artistas
            headers.append([a,x['release_date'][0:4],x['album_type'],artistas,x['total_tracks']])

    
    return headers

"""
Req 2 Funciones Main.
"""

def topArtists(sortedArtists, userCatalog, N):

    """"
    Retorna los artistas TOP, mas populares, con un tamaño de analisis N.
    """
    #CREACION SUBLISTA SEGUN UN NUMERO DE ELEMENTOS N
    sortedArtists = lt.subList(sortedArtists, 1, N)
    headers = [["Nombre Artista", "Seguidores", "Popularidad", "Generos", "Ref Song"]]


    if N > 6: #Si N es mayor que 6, guardaremos los datos de manera tal que se conforme por los 3 primeros y 3 ultimos elementos.

        #Primer recorrido. Se recorre la lista ordenada de artistas y se guarda sus elementos.
        for i in range(1, N+1):
            if i < 4:
                x = lt.getElement(sortedArtists, i)
                characters = "'"
                characters2 = " "

                trackRef = getTrackRef(userCatalog, x['track_id']) #Funcion auxiliar para obtener el nombre de la cancion
                if trackRef=='':
                    trackRef = "Unknown" #Si la funcion nos retorna un str vacio, su valor sera desconocido.
                else: 
                    for letra in range(len(characters2)):
                        trackRef = trackRef.replace(characters2[letra],"\n")

              
                #compresion del texto 'generos'
                for letra in range(len(characters)):
                    a = x['genres'][1:-1].replace(characters[letra],"")
                

                #se guardan los valores de la lista ordenada del primer recorrido
                headers.append([x['name'], x['followers'], x['artist_popularity'], a, trackRef])

        #Segundo recorrido. Se recorre la lista ordenada de artistas y se guarda sus elementos.
        for i in range(-2, N):
            if i < 1: #Condicion para que los datos guardados en headers sean los 3 ultimos.
                x = lt.getElement(sortedArtists, (N+i))
                characters = "'"
                trackRef = getTrackRef(userCatalog, x['track_id']) #Funcion auxiliar para obtener el nombre de la cancion
                if trackRef == '':
                    trackRef = "Unknown"
                else: 
                    for letra in range(len(characters2)):
                        trackRef = trackRef.replace(characters2[letra],"\n")

                characters = "'"
                #compresion del texto 'generos'
                for letra in range(len(characters)):
                    a = x['genres'][1:-1].replace(characters[letra],"")

                #se guardan los valores de la lista ordenada del segundo recorrido
                headers.append([x['name'], x['followers'], x['artist_popularity'], a, trackRef])

    else: #En caso de que N sea menor a 6, los datos se guardan de manera lineal.
        for i in range(1, N+1):
            x = lt.getElement(sortedArtists, i)
            trackRef = getTrackRef(userCatalog, x['track_id'])
            characters = "'"
            #compresion del texto 'generos'
            for letra in range(len(characters)):
                a = x['genres'][1:-1].replace(characters[letra],"")
            headers.append([x['name'], x['followers'], x['artist_popularity'], a, trackRef])
    return headers

"""
Req 3 Funcion Main.
"""

def TopSongs(sortedSongs, userCatalog, N):

    """
    Retorna las canciones clasificadas por popularidad segun un tamaño N dado.
    """
    #CREACION SUBLISTA SEGUN UN NUMERO DE ELEMENTOS N
    sortedSongs = lt.subList(sortedSongs, 1, N)
    headers = [['Nombre','album','artista\s','Popularidad','duracion', 'href', 'lyrics']]

    #Si N es mayor a 6, se organizara de la manera; 3 ultimos y 3 primeros. 
    #De lo contrario solo se imprimiran en el orden que vienen.
    if N > 6:
        #Primer recorrido. Se guardan los elementos de esa lista de canciones ordenadas.
        for i in range(1, N+1):
            if i < 4:
                x = lt.getElement(sortedSongs, i)

                #Se hace llamado de la funcion auxiliar para obtener el nombre del album
                album = getAlbumRef(userCatalog, x['album_id'])

                #Se hace llamado de la funcion auxiliar para obtener el nombre del artista
                artistas = getArtistRef(userCatalog, x['artists_id'])
                characters = " "
                character2 = "."
                
                #compresion del texto 'name'
                for letra in range(len(characters)):
                        name = x['name'].replace(characters[letra],"\n")

                #compresion del texto 'href'
                for letra in range(len(character2)):
                    href = x['href'].replace(character2[letra],".\n")
                    href = href[:30]+"\n"+href[30:45]+"\n"+href[45:]
                
                #compresion del texto 'artistas nombres'
                for letra in range(len(characters)):
                        artistas = artistas.replace(characters[letra],"\n")

                #Si el elemento lyrics no es -99, osea desconocida, se comprime, de lo contrario se pone 'unknown'
                if x['lyrics'] != "-99":
                    for letra in range(len(characters)):
                        l = x['lyrics'].replace(characters[letra],"\n")
                        l = '"'+l[:50]+'..."'
                else: l = "Unknown..."

                #compresion del texto 'nombre del album'
                for letra in range(len(characters)):
                        album = album.replace(characters[letra],"\n")

                headers.append([name, album, artistas, x['popularity'], x['duration_ms'],href, l])

        #Se repite el mismo ciclo de procedimientos para anexar ahora las ultimas 3 posiciones
        for i in range(-2, N): #Se sigue el mismo procedimiento para todos los subprocesos del anterior caso.
            if i < 1:
                x = lt.getElement(sortedSongs, (N+i))
                album = getAlbumRef(userCatalog, x['album_id'])
                artistas = getArtistRef(userCatalog, x['artists_id'])
                characters = " "
                i = 0

                for letra in range(len(characters)):
                        name = x['name'].replace(characters[letra],"\n")

                for letra in range(len(character2)):
                    href = x['href'].replace(character2[letra],".\n")
                    href = href[:30]+"\n"+href[30:45]+"\n"+href[45:]

                for letra in range(len(characters)):
                        artistas = artistas.replace(characters[letra],"\n")

                if x['lyrics'] != "-99":
                    for letra in range(len(characters)):
                        l = x['lyrics'].replace(characters[letra],"\n")
                        l = '"'+l[:50]+'..."'
                else: l = "Unknown..."

                for letra in range(len(characters)):
                        album = album.replace(characters[letra],"\n")

                headers.append([name, album, artistas, x['popularity'], x['duration_ms'], href, l])

    else: #Si el numero de elementos N es menor a 6, se guardan los datos de manera lineal.

        for i in range(1, N+1): #Se sigue el mismo procedimiento para todos los subprocesos del anterior caso.
            x = lt.getElement(sortedSongs, i)
            album = getAlbumRef(userCatalog, x['album_id'])
            artistas = getArtistRef(userCatalog, x['artists_id'])
            characters = " "
            character2 = "."

            if x['lyrics'] != "-99":
                    for letra in range(len(characters)):
                        lyric = x['lyrics'].replace(characters[letra],"\n")
                        lyric = '"'+lyric[:50]+'..."'
            else: lyric = "Unknown..."

            for letra in range(len(characters)):
                        artistas = artistas.replace(characters[letra],"\n")

            for letra in range(len(characters)):
                        name2 = x['name'].replace(characters[letra],"\n")

            for letra in range(len(character2)):
                    href1 = x['href'].replace(character2[letra],".\n")
                    href1 = href1[:30]+"\n"+href1[30:45]+"\n"+href1[45:]
            
            #Siempre se retorna la lista de listas, osea el headers, para que sea impreso como una tabla con 'tabulate lib'
            headers.append([name2, album, artistas, x['popularity'], x['duration_ms'], href1, lyric])
    return headers


"""
Req 4 Funciones Main.
"""

def getartistsSongs(userCatalog, nombre, codigoPais):

    """
    Retorna la cancion mas popular de un artista segun el codigo de pais que se ingresa
    """

    artist_id = getArtistId(userCatalog, nombre)
    sortedSongs = sortSongsByPop(userCatalog)
    headers = [['nombre cancion', 'album', 'publicacion', 'artist\s', 'duracion(ms)', "popularidad",'url','lyrics']]

    #Primer recorrido. Se recorre la lista de canciones ordenadas segun su popularidad
    for i in range(1, lt.size(sortedSongs)):
        x = lt.getElement(sortedSongs, i)
        idList = str(x['artists_id'])
        idList = idList[2:-2] #Se toma en cuenta este rango para no tener en cuenta las comillas ni los corchetes

        #Si el id del artista esta en el id de la lista ordenada, se cumple la condicion.
        if artist_id in idList:
            marketsList = str(x['available_markets'])
            marketsList = marketsList[2:-2] #Se toma en cuenta este rango para no tener en cuenta las comillas ni los corchetes

            #Ahora bien, si el codigo que nos dan pertenece al mercado de la lista anterior, 
            #procedemos a guardar los datos de la lista ordenada.
            if codigoPais in marketsList:
                album = getAlbumRef(userCatalog, x['album_id'])
                release_date = getAlbumDate(userCatalog, x['album_id'])
                artists = getArtistRef(userCatalog, x['artists_id'])

                #Compresion del texto de "url"
                url = x['preview_url']
                url = url[:14]+"\n"+"[...]"+"\n"+url[-8:]

                #Compresion del texto de "artist\s"
                characters = ' '
                for letra in range(len(characters)):
                        artists = artists.replace(characters[letra],"\n")

                #Compresion del texto de "lyrics"
                if x['lyrics'] != "-99":
                    for letra in range(len(characters)):
                        l = x['lyrics'].replace(characters[letra],"\n")
                        l = '"'+l[:54]+'..."'
                else: l = "Unknown..."

                #Compresion del texto de "Name"
                for letra in range(len(characters)):
                        name1 = x['name'].replace(characters[letra],"\n")
                
                #Compresion del texto de "Album"
                for letra in range(len(characters)):
                        album = album.replace(characters[letra],"\n")

                headers.append([name1, album, release_date, artists, x['duration_ms'], x['popularity'], url, l])
                
                break

    return headers


def getArtistId(userCatalog, nombre):
    #Funcion auxiliar del req., para mediante un nombre recibido por parametro, se pueda obtener el id del artista:
    #atraves de un recorrido en la lista de artistas y buscar que se cumpla la condicion de los nombres.
    artist_id = ''
    for i in range(1, lt.size(userCatalog['artists'])):
        x = lt.getElement(userCatalog['artists'], i)
        if nombre in str(x['name'].lower()):
            artist_id = x['id']
            break
    return artist_id


"""
Req 5 Main Functions
"""
def ctdAlbums(userCatalog, nombre):
    """
    Devuelve la cantidad de albums; cantidad de tipo 'single', tipo 'compilation' y cantidad total albums.
    """
    artist_id = getArtistId(userCatalog, nombre)
    sumAlb = 0
    sumSingle = 0
    sumComp = 0

    #Si el artista id no es un string vacio, se ejecuta el ciclo
    if artist_id != '':

        #Se recorre el catalogo de albums 
        for i in range(1, lt.size(userCatalog['albums'])):
            x = lt.getElement(userCatalog['albums'], i)

            #Si la id del artista corresponde a la id del artista en el catalgo de albums, se ejecuta la condicion.
            if artist_id in (x['artist_id']):
                if x['album_type'] in 'single':
                    sumSingle += 1
                elif x['album_type'] in 'compilation':
                    sumComp += 1
                sumAlb += 1
                
    return sumAlb, sumSingle, sumComp

def albumsSongsArt(userCatalog, nombre):
    """
    Retorna la discografia, informacion de albums y canciones, de un artista mediante el parametro de su nombre.
    """
    artist_id = getArtistId(userCatalog, nombre)
    headersSongs = [['Nombre cancion', 'artista\s', 'duracion[ms]', 'popularidad','preview_url','lyrics']]
    headers = [['fecha de lanzamiento', 'nombre album', 'total tracks', 'tipo de album', 'artista']] 

    characters = " "

    #Primer recorrido. Se recorre el catalogo de canciones y se guarda cada elemento.
    for i in range(1, lt.size(userCatalog['canciones'])):
        x = lt.getElement(userCatalog['canciones'], i)

        #Si el id del artista esta en el catalogo de canciones, entonces la id del album estara en esa lista x.
        if artist_id in (x['artists_id']):
            album_id = x['album_id']

            #Segundo recorrido. Se recorre el catalogo de albums y se guarda sus elementos.
            for p in range(1, lt.size(userCatalog['albums'])):
                al = lt.getElement(userCatalog['albums'], p)

                #Si el id del album de la primera condicion, es igual al id del catalogo de albums, estamos en el la situacion acertada.
                if album_id in al['id']:
                    #organizamos las canciones 
                    orderedSongs = sortSongsByPop(userCatalog)

                    #Tercer recorrido. Se recorre esa lista de canciones ordenadas y se guarda cada elemento.
                    for j in range(1, lt.size(orderedSongs)):
                        k = lt.getElement(orderedSongs, j)

                        #Su se cumple esta condicion, automaticamente estamos en la posicion e id del album correcta 
                        # y procedemos a guardar los datos.
                        if album_id in k['album_id']:

                            #compresion Nombre
                            for letra in range(len(characters)):
                                name1 = k['name'].replace(characters[letra],"\n")

                            #compresion artistas
                            artistas = getArtistRef(userCatalog, k['artists_id'])
                            for letra in range(len(characters)):
                                artistas = artistas.replace(characters[letra],"\n")

                            #compresion url
                            url = k['preview_url']
                            url = url[:14]+"\n"+"[...]"+"\n"+url[-8:]

                            #compresion lyrics
                            if k['lyrics'] != "-99":
                                for letra in range(len(characters)):
                                    l = k['lyrics'].replace(characters[letra],"\n")
                                    l = '"'+l[:53]+'..."'
                            else: l = "Unknown..."
            
                            headersSongs.append([name1,artistas,k['duration_ms'],k['popularity'],url,l])


                    artista = getArtistRef(userCatalog, al['artist_id'])
                    #anexamos todos los datos del album a la cabecera principal
                    headers.append([al['release_date'], al['name'], al['total_tracks'], al['album_type'], artista])

    return headers, headersSongs


"""
BONO Main Functions
"""

def rangedBonoSongs(userCatalog, sortedSongs, añoInicial, añoFinal, N):
    #CREACION SUBLISTA SEGUN UN NUMERO DE ELEMENTOS N
    sublistSongs = lt.subList(sortedSongs, 1, N)
    headers = [['Nombre','album','artista\s','Cantidad Paises','Popularidad','duracion']]
    #Recorrido en la sublista.
    for i in range(1, lt.size(sublistSongs)):
        x = lt.getElement(sublistSongs, i)
        #llamado a la funcion auxiliar getAlbumDate para obtener el release_Date
        #Condicion de contenencia de la fecha entre los limites de años.
        for album in range(1, lt.size(userCatalog['albums'])):
            albums = lt.getElement(userCatalog['albums'], album)
            if albums['release_date_precision'] == 'month':
                albums['release_date'] = '19'+albums['release_date'][-2:]
                date = datetime.strptime(albums['release_date'], "%Y") #se tiene en cuenta el caso en el que la fecha sea de la forma 'month-day'
                #De la fecha obtenida, solo sacamos el elemento year para compararlo.
                year = date.year

            elif albums['release_date_precision'] == 'day':#se tiene en cuenta el caso en el que la fecha sea de la forma 'year-month-day'
                date = datetime.strptime(albums['release_date'], "%Y-%m-%d")
                #De la fecha obtenida, solo sacamos el elemento year para compararlo.
                year = date.year
            

            elif albums['release_date_precision'] == 'year':#se tiene en cuenta el caso en el que la fecha sea de la forma 'year'
                year = albums['release_date']
                #si el año a comparar esta entre los parametros de año inicial y año final dado, 
                #se guardan los elementos del album en el que estamos.
            nombreartista = getArtistRef(userCatalog, x['artists_id'])
            if añoInicial<int(year)<añoFinal:
                headers.append([x['name'], albums['name'], nombreartista, len(x['available_markets']), x['popularity'], x['duration_ms']])

    return headers


# Funciones de ordenamiento

def sortAlbumByDate(userCatalog):
    #Retorna la lista de albums ordenada segun el cmpfunction de fecha de publicacion.
    sortedAlbums = ms.sort(userCatalog['albums'], cmpAlbumsByDate)
    return sortedAlbums

def sortArtistsByPop(userCatalog):
    #Retorna la lista de artistas ordenada segun el cmpfunction de popularidad para artistas.
    sortedArtists = ms.sort(userCatalog['artists'], cmpArtistsByPop)
    return sortedArtists

def sortSongsByPop(userCatalog):
    #Retorna la lista de canciones ordenada segun el cmpfunction de popularidad.
    sortedSongs = ms.sort(userCatalog['canciones'], cmpSongsByPop)
    return sortedSongs

#BONO ordered list


def dateRelease(userCatalog, album_id):
    """
    se retorna el valor del "date_release" solo con conocer el id del album
    """
    for i in range(1, lt.size(userCatalog['albums'])):
        x = lt.getElement(userCatalog['albums'], i)
        if album_id in x['id']:
            return int(x['release_date'][:4])

def sortSongsByCountry(userCatalog):
    """
    se retorna la lista de canciones ordenada con
    el cmp que funciona en base a la cantidad de mercados, en principio.
    """
    sortedSongs = ms.sort(userCatalog['canciones'],cmpSongsByCountry)
    return sortedSongs


# Funciones de tiempo sobre el catálogo

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

# Funciones de tamaño sobre el catálogo

def tamañoCanciones(userCatalog):
    #retorna el tamaño del catálogo de canciones
    return lt.size(userCatalog['canciones'])

def tamañoArtistas(userCatalog):
    #retorna el tamaño del catálogo de artistas
    return lt.size(userCatalog['artists'])

def tamañoAlbums(userCatalog):
    #retorna el tamaño del catálogo de albums
    return lt.size(userCatalog['albums'])
