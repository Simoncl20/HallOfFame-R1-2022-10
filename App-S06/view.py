"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import csv
# Pycountry, instalr con pip install pycountry, convierte el nombre de un país en su sigla, ej: Colombia -> CO
import pycountry


default_limit = 1000
sys.setrecursionlimit(default_limit*10)
csv.field_size_limit(2147483647)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar los álbumes en un periodo de tiempo")
    print("3- Encontrar los artistas más populares")
    print("4- Clasificar las canciones por popularidad")
    print("5- Encontrar la canción más popular de un artista")
    print("6- Encontrar la discografía de un artista")
    print("7- Clasificar las canciones con mayor distribución")

catalog = None

def loadData(size):
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    albums, artists, tracks = controller.loadData(size, control)
    return albums, artists, tracks

def print_albums(albums_list):
    for album in lt.iterator(albums_list):
        print('Name: ' + album['name'] + ', Release Date: ' + str(album['release_date']) + ', Total Tracks: ' + str(album['total_tracks']) + ', Album Type: ' + album['album_type'] + ', Artist: ' + album['artist_id'] + ', External URLS: ' + album['external_urls'])
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        

def print_tracks(track_list):
    for track in lt.iterator(track_list):
        print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Disc Number: ' + track['disc_number'] + ', Track Number: ' + track['track_number'] + ', Album Name: ' + track['album_id'] + ', Artist Name: ' + str(track['artists_id']) + ', Href: ' + track['href'] + ', Lyrics: ' + track['lyrics'])
        print('---------------------------------------------------------------------------------------------------------------------------------------')
    

def print_artists(artists_list):
    for artist in lt.iterator(artists_list):
        print('Popularity: ' + artist['artist_popularity'] + ', Followers: ' + artist['followers'] + ', Name: ' + artist['name'] + ', Relevant Track: ' + artist['track_id'] + ', Genres: ' + str(artist['genres']))
        print('---------------------------------------------------------------------------------------------------------------------------------------')

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs) == 1:
        print("¿Qué tamaño deseas cargar? ")
        print("1- small / 0.5pct")
        print("2- 5pct")
        print("3- 10pct")
        print("4- 20pct")
        print("5- 30pct")
        print("6- 50pct")
        print("7- 80pct")
        print("8- large/100pct")
        size_input = int(input("Escoge que tamaño cargar: \n"))
        if size_input == 1:
            size = "small"
        elif size_input == 2:
            size = "5pct"
        elif size_input == 3:
            size = "10pct"
        elif size_input == 4:
            size = "20pct"
        elif size_input == 5:
            size = "30pct"
        elif size_input == 6:
            size = "50pct"
        elif size_input == 7:
            size = "80pct"
        elif size_input == 8:
            size = "large"
        else:
            print('ERROR -> TAMAÑO INCORRECTO')
        control = newController()
        print("Cargando información de los archivos ....")
        #Trae las variables
        albums, artists, tracks = loadData(size)
        """
        SORTING ---------------------------------------------------------------------------------------------------------------------
        """
        #SORT ARTISTS
        sorted_artists = controller.sortArtists(control)
        #SORT TRACKS
        sorted_tracks = controller.sortTracks(control)
        #SORT ALBUMS
        sorted_albums = controller.sortAlbums(control)
        """
        SEARCHING --------------------------------------------------------------------------------------------------------------------
        """
        #FIND ALBUM NAME
        controller.findAlbumName(sorted_tracks, sorted_albums)
        #FIND ARTISTS TRACK NAMES
        controller.findArtistsInTracks(sorted_tracks, sorted_artists)
        #FIND ARTIST RELEVANT TRACK
        controller.findArtistRelevantTrack(sorted_artists, sorted_tracks)
        #FIND ARTIST ALBUM NAME
        controller.findartistInAlbums(sorted_albums, sorted_artists)
        #Tamaño de los archivo
        #Imprime la información
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        print(f'Álbumes cargados:{controller.sizeList(sorted_albums)}')
        print(f'Artistas cargados: {controller.sizeList(sorted_artists)}')
        print(f'Canciones cargadas: {controller.sizeList(sorted_tracks)}')
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        print('The first three albums: ')
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        first_three_albums = controller.createSubList(sorted_albums, 0, 3)
        print(print_albums(first_three_albums))
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        print('The last three albums: ')
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        last_three_albums = controller.createSubList(sorted_albums, controller.sizeList(sorted_albums) - 2, 3)
        print(print_albums(last_three_albums))
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        print('The first three artists: ')
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        first_three_artists = controller.createSubList(sorted_artists, 0, 3)
        print(print_artists(first_three_artists))
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        print('The last three artists: ')
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        last_three_artists = controller.createSubList(sorted_artists, controller.sizeList(sorted_artists) - 2, 3)
        print(print_artists(last_three_artists))
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        print('The first three tracks: ')
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        first_three_tracks = controller.createSubList(sorted_tracks, 0, 3)
        print(print_tracks(first_three_tracks))
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        print('The last three tracks: ')
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        last_three_tracks = controller.createSubList(sorted_tracks, controller.sizeList(sorted_tracks) - 2, 3)
        print(print_tracks(last_three_tracks))
        
    
    elif int(inputs[0]) == 2:
        initial_year = int(input('Ingresa el año inicial de búsqueda: '))
        last_year = int(input('Ingresar el año final de búsqueda: '))
        initial_albums_years = controller.findYearPosition(sorted_albums, initial_year)
        last_albums_years = controller.findYearPosition(sorted_albums, last_year)
        number = (last_albums_years - initial_albums_years)
        lista = controller.createSubList(sorted_albums, initial_albums_years, number)
        
        if controller.sizeList(lista) > 6:
            first_three = controller.createSubList(lista, 1, 3)
            last_three = controller.createSubList(lista, controller.sizeList(lista) - 2, 3)
            print('The first 3 albums: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for album in lt.iterator(first_three):
                print('Name: ' + album['name'] + ', Release Date: ' + str(album['release_date']) + ', Total Tracks: ' + str(album['total_tracks']) + ', Album Type: ' + album['album_type'] + ', Artist: ' + album['artist_id'] + ', External URLS: ' + album['external_urls'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

            print('The last 3 albums: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for album in lt.iterator(last_three):
                print('Name: ' + album['name'] + ', Release Date: ' + str(album['release_date']) + ', Total Tracks: ' + str(album['total_tracks']) + ', Album Type: ' + album['album_type'] + ', Artist: ' + album['artist_id'] + ', External URLS: ' + album['external_urls'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        else:
            print('The albums: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for album in lt.iterator(lista):
                print('Name: ' + album['name'] + ', Release Date: ' + str(album['release_date']) + ', Total Tracks: ' + str(album['total_tracks']) + ', Album Type: ' + album['album_type'] + ', Artist: ' + album['artist_id'] + ', External URLS: ' + album['external_urls'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

    elif int(inputs[0]) == 3:
        number_artists = int(input("Escoja el top de artistas que desea cargar: "))
        artist_list = controller.createSubList(sorted_artists, 1, number_artists)
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

        if number_artists > 6:
            first_three = controller.createSubList(artist_list, 1, 3)
            last_three = controller.createSubList(artist_list, controller.sizeList(artist_list) - 2, 3)
            print(f'The 3 first artists in TOP {number_artists} are...: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for artist in lt.iterator(first_three):
                print('Popularity: ' + artist['artist_popularity'] + ', Followers: ' + artist['followers'] + ', Name: ' + artist['name'] + ', Relevant Track: ' + artist['track_id'] + ', Genres: ' + str(artist['genres']))
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            
            print(f'The 3 last artists in TOP {number_artists} are...: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for artist in lt.iterator(last_three):
                print('Popularity: ' + artist['artist_popularity'] + ', Followers: ' + artist['followers'] + ', Name: ' + artist['name'] + ', Relevant Track: ' + artist['track_id'] + ', Genres: ' + str(artist['genres']))
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        else:
            print(f'The first artists in TOP {number_artists} are...: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for artist in lt.iterator(artist_list):
                print('Popularity: ' + artist['artist_popularity'] + ', Followers: ' + artist['followers'] + ', Name: ' + artist['name'] + ', Relevant Track: ' + artist['track_id'] + ', Genres: ' + str(artist['genres']))
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

    elif int(inputs[0]) == 4:
        number_tracks = int(input("Ingrese el número de canciones a identificar: "))
        track_list = controller.createSubList(sorted_tracks, 1, number_artists)
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

        if number_tracks > 6:
            first_three = controller.createSubList(track_list, 1, 3)
            last_three = controller.createSubList(track_list, controller.sizeList(track_list) - 2, 3)
            print(f'The 3 first tracks in TOP {number_tracks} are...: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for track in lt.iterator(first_three):
                print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Disc Number: ' + track['disc_number'] + ', Track Number: ' + track['track_number'] + ', Album Name: ' + track['album_id'] + ', Artist Name: ' + str(track['artists_id']) + ', Href: ' + track['href'] + ', Lyrics: ' + track['lyrics'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

            print(f'The 3 last tracks in TOP {number_tracks} are...: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for track in lt.iterator(last_three):
                print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Disc Number: ' + track['disc_number'] + ', Track Number: ' + track['track_number'] + ', Album Name: ' + track['album_id'] + ', Artist Name: ' + str(track['artists_id']) + ', Href: ' + track['href'] + ', Lyrics: ' + track['lyrics'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        else:
            print(f'The first tracks in TOP {number_tracks} are...: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for track in lt.iterator(track_list):
                print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Disc Number: ' + track['disc_number'] + ', Track Number: ' + track['track_number'] + ', Album Name: ' + track['album_id'] + ', Artist Name: ' + str(track['artists_id']) + ', Href: ' + track['href'] + ', Lyrics: ' + track['lyrics'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

    elif int(inputs[0]) == 5:
        artist_name = input("Ingresa el nombre del artista: ")
        country_name = input("Ingresa el país: ")
        country = pycountry.countries.search_fuzzy(country_name)
        country_code = country[0].alpha_2
        artist_tracks = controller.findArtistTracks(artist_name, country_code, sorted_tracks, sorted_albums)
        print(f'Number of albums: {artist_tracks[2]}')
        print(f'Number of tracks: {artist_tracks[1]}')
        track = artist_tracks[0]
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print(f'The best song of {artist_name} in {country_name} ({country_code})')
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Disc Number: ' + track['disc_number'] + ', Track Number: ' + track['track_number'] + ', Album Name: ' + track['album_id'] + ', Artist Name: ' + str(track['artists_id']) + ', Preview URL: ' + track['preview_url'] + ', Href: ' + track['href'] + ', Lyrics: ' + track['lyrics'])

    elif int(inputs[0]) == 6:
        artist_name = input("Ingresa el nombre del artista: ")
        artist_albums = controller.findArtistAlbums(artist_name, sorted_tracks, sorted_albums)
        print(f'Albums: {artist_albums[0]}')
        print(f'Singles: {artist_albums[1]}')
        print(f'Compilations: {artist_albums[2]}')
        print(f'Total: {artist_albums[0] + artist_albums[1] + artist_albums[2]}')
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        if controller.sizeList(artist_albums[3]) > 6:
            first_three = controller.createSubList(artist_albums[3], 1, 3)
            last_three = controller.createSubList(artist_albums[3], controller.sizeList(artist_albums[3]) - 2, 3)
            print(f'The 3 first albums for {artist_name}: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for album in lt.iterator(first_three):
                print('Name: ' + album['name'] + ', Release Date: ' + str(album['release_date']) + ', Total Tracks: ' + str(album['total_tracks']) + ', Album Type: ' + album['album_type'] + ', Artist: ' + album['artist_id'] + ', External URLS: ' + album['external_urls'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

            print(f'The 3 last albums for {artist_name}: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for album in lt.iterator(last_three):
                print('Name: ' + album['name'] + ', Release Date: ' + str(album['release_date']) + ', Total Tracks: ' + str(album['total_tracks']) + ', Album Type: ' + album['album_type'] + ', Artist: ' + album['artist_id'] + ', External URLS: ' + album['external_urls'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        else:
            print(f'The albums for {artist_name}: ')
            for album in lt.iterator(artist_albums[3]):
                print('Name: ' + album['name'] + ', Release Date: ' + str(album['release_date']) + ', Total Tracks: ' + str(album['total_tracks']) + ', Album Type: ' + album['album_type'] + ', Artist: ' + album['artist_id'] + ', External URLS: ' + album['external_urls'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('\n')
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('\n')

        if controller.sizeList(artist_albums[4]) > 6:
            first_three = controller.createSubList(artist_albums[4], 1, 3)
            last_three = controller.createSubList(artist_albums[4], controller.sizeList(artist_albums[4]) - 2, 3)
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for track in lt.iterator(first_three):
                print('Most popular track in' + str({track['album_id']}))
                print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Artist Name: ' + str(track['artists_id']) + ', Preview URL: ' + track['preview_url'] + ', Lyrics: ' + track['lyrics'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

            for track in lt.iterator(last_three):
                print('Most popular track in' + str({track['album_id']}))
                print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Artist Name: ' + str(track['artists_id']) + ', Preview URL: ' + track['preview_url'] + ', Lyrics: ' + track['lyrics'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        else:
            for track in lt.iterator(artist_albums[4]):
                print('Most popular track in' + str({track['album_id']}))
                print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Artist Name: ' + str(track['artists_id']) + ', Preview URL: ' + track['preview_url'] + ', Lyrics: ' + track['lyrics'])
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

    elif int(inputs[0]) == 7:
        initial_year = int(input('Ingresa el año inicial de búsqueda (Año Mayor): '))
        last_year = int(input('Ingresar el año final de búsqueda (Año Menor): '))
        number_tracks = int(input("Ingrese el número de canciones a identificar: "))
        initial_albums_years = controller.findYearPosition(sorted_albums, initial_year)
        last_albums_years = controller.findYearPosition(sorted_albums, last_year)
        number = (last_albums_years - initial_albums_years)
        lista = controller.createSubList(sorted_albums, initial_albums_years, number)
        find_tracks_in_albums = controller.findTracksInAlbums(lista, sorted_tracks)
        sort_tracks = controller.sortTracksByMarket(find_tracks_in_albums)
        first_number = controller.createSubList(sort_tracks, 1, number_tracks)
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        
        if number_tracks > 6:
            first_three = controller.createSubList(first_number, 1, 3)
            last_three = controller.createSubList(first_number, controller.sizeList(first_number) - 2, 3)
            print('The 3 first tracks with more distribution: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for track in lt.iterator(first_three):
                print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Países: ' + str(track['available_markets']) + ', Album Name: ' + track['album_id'] + ', Artist Name: ' + str(track['artists_id']))
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            
            print('The 3 last tracks with more distribution: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for track in lt.iterator(last_three):
                print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Países: ' + str(track['available_markets']) + ', Album Name: ' + track['album_id'] + ', Artist Name: ' + str(track['artists_id']))
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        else:
            first_number = controller.createSubList(sort_tracks, 1, number_tracks)
            print(f'The {number_tracks} first tracks with more distribution: ')
            print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for track in lt.iterator(first_number):
                print('Popularity: ' + track['popularity'] + ', Duración: ' + track['duration_ms'] + ', Nombre: ' + track['name'] + ', Países: ' + str(track['available_markets']) + ', Album Name: ' + track['album_id'] + ', Artist Name: ' + str(track['artists_id']))
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        
    else:
        sys.exit(0)
sys.exit(0)

