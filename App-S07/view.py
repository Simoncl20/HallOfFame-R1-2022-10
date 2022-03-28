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

from tabulate import tabulate
import textwrap
import config as cf
import sys
default_limit = 1000
sys.setrecursionlimit(default_limit*100)
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar los albumes en un periodo de tiempo")
    print("3- Encontrar los artistas más populares")
    print("4- Encontrar las canciones más populares")
    print("5- Encontrar la canción más popular de un artista")
    print("6- Encontrar la discografia de un artista")
    print("7- Clasificar las canciones con mayor distribución")
    print("8- Seleccionar algoritmo de ordenamiento")
    print("0- Salir")

def loadData(tipo_lista, file_size):
    return controller.loadData(tipo_lista, file_size)

def formatName(name):
    name = name.strip()
    name_str = textwrap.wrap(name, 16)
    name_str = '\n'.join(name_str)
    return name_str

def formatArtists(artistas, list_artistas, track=False):
    if not track:
        for artista in lt.iterator(artistas):
            name = artista['name']
            name = formatName(name)
            followers = artista['followers']
            popularity = artista['artist_popularity']
            genres = artista['genres']
            genres_str = ', '.join(genres)
            genres_str = textwrap.wrap(genres_str,16)
            genres_str = '\n'.join(genres_str)
            list_artistas.append([name,popularity,followers,genres_str])
    else:
        for artista in lt.iterator(artistas):
            name = artista['name']
            name = formatName(name)
            followers = artista['followers']
            popularity = artista['artist_popularity']
            track_name = artista['revelant_track_name']
            track_name = textwrap.wrap(track_name, 16)
            track_name = '\n'.join(track_name)
            genres = artista['genres']
            genres_str = ', '.join(genres)
            genres_str = textwrap.wrap(genres_str,16)
            genres_str = '\n'.join(genres_str)
            list_artistas.append([name,popularity,followers,track_name,genres_str])


def formatAlbums(albums, list_albums, artist=False, year=True):
    if not artist:
        for album in lt.iterator(albums):
            name = album['name']
            name = formatName(name)
            release_date = album['release_date']
            album_type = album['album_type']
            total_tracks = album['total_tracks']
            markets = album['available_markets']
            markets_str = ', '.join(markets)
            markets_str = textwrap.wrap(markets_str, 16)
            markets_str = '\n'.join(markets_str)
            list_albums.append([name,release_date,total_tracks,album_type,markets_str])
    else:
        for album in lt.iterator(albums):
            name = album['name']
            name = formatName(name)
            if year:
                release_date = album['year']
            else:
                release_date = album['release_date']
            album_type = album['album_type']
            artist_name = album['artist_album_name']
            total_tracks = album['total_tracks']
            external_url = album["external_urls"]
            url = external_url['spotify']
            url = textwrap.wrap(url, 16)
            url = '\n'.join(url)
            list_albums.append([name,release_date,total_tracks,album_type,artist_name, url])

def formatTracks(tracks, list_tracks):
    for track in lt.iterator(tracks):
        name = track['name']
        name = formatName(name)
        duration_ms = float(track['duration_ms'])
        track_number = track['track_number']
        list_tracks.append([name,int(duration_ms),track_number])


catalog = None
tipo_lista = "ARRAY_LIST"
algoritmo = "merge"

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("1- Array List")
        print("2- Linked List")
        seleccion = input("Seleccione un tipo de lista para continuar:\n")
        if int(seleccion[0]) == 1:
            tipo_lista = "ARRAY_LIST"
        elif int(seleccion[0]) == 2:
            tipo_lista = "LINKED_LIST"


        file_size = input("Ingrese tamaño del archivo: ")
        print("Cargando información de los archivos ....")
        start = controller.getTime()
        tr, al, ar, sorting_time = loadData(tipo_lista, file_size)
        end = controller.getTime()

        elapsed = controller.deltaTime(start, end)
        print(f'Tardó  {round(elapsed-sorting_time,2)}ms en cargar los datos y {round(sorting_time,2)}ms en ordenarlos.')
        print(f'En total tardó {round(elapsed,2)}ms.')

        print('-'*38)
        print('artists ID count: '+ str(ar[0]))
        print('albums ID count: '+ str(al[0]))
        print('tracks ID count: '+ str(tr[0]))
        print('-'*38)

        print('\nThe first 3 and last 3 artists in the range are...')
        first_3_artists = lt.subList(ar[1], 1, 3)
        last_3_artists = lt.subList(ar[1], ar[0]-2, 3)
        list_artists = []
        formatArtists(first_3_artists, list_artists)
        formatArtists(last_3_artists, list_artists)
        print(tabulate(list_artists, headers=['name','artis_popularity','followers', 'genres'], tablefmt='grid'))

        print('\nThe first 3 and last 3 albums in the range are...')
        first_3_albums = lt.subList(al[1], 1, 3)
        last_3_albums = lt.subList(al[1], al[0]-2, 3)
        list_albums = []
        formatAlbums(first_3_albums, list_albums)
        formatAlbums(last_3_albums, list_albums)
        print(tabulate(list_albums, headers=['name','release_date','total_tracks' ,'album_type', 'available_markets'], tablefmt='grid'))

        print('\nThe first 3 and last 3 tracks in the range are...')
        first_3_tracks = lt.subList(tr[1], 1, 3)
        last_3_tracks = lt.subList(tr[1], tr[0]-2, 3)
        list_tracks = []
        formatTracks(first_3_tracks, list_tracks)
        formatTracks(last_3_tracks, list_tracks)
        print(tabulate(list_tracks, headers=['name','duration_ms','track_number'], tablefmt='grid'))


    elif int(inputs[0]) == 2:
        print('Por favor ingrese el rango de años de los albumes a buscar...')
        start = int(input('Año inicial: '))
        end = int(input('Año final: '))
        start_time = controller.getTime()
        sorted_list, delta_time = controller.sortAlbumsByYear(algoritmo, al[1], al[0])
        # print("Algoritmo ", algoritmo, " se demoró ", str(round(delta_time,2)), " milisegundos")

        albumsInRange, size = controller.getAlbumsInRange(sorted_list, start, end)




        albumsInRange, size = controller.searchArtistById(albumsInRange, ar[1])

        end_time = controller.getTime()

        elapsed = controller.deltaTime(start_time, end_time)
        print(f'En total tardó {round(elapsed,2)}ms.')

        print(f'There are {size} albums released between {start} and {end}')
        print('\nThe first 3 and last 3 albums in the range are...')

        if size >= 6:
            first_3_albums = lt.subList(albumsInRange, 1, 3)
            last_3_albums = lt.subList(albumsInRange, size-2, 3)
            prints_albums = lt.newList('ARRAY_LIST')
            for album in lt.iterator(first_3_albums):
                lt.addLast(prints_albums, album)
            for album in lt.iterator(last_3_albums):
                lt.addLast(prints_albums, album)
        else:
            prints_albums = albumsInRange

        list_albums = []
        formatAlbums(prints_albums, list_albums, True)
        # first_3_albums = lt.subList(albumsInRange, 1, 3)
        # last_3_albums = lt.subList(albumsInRange, size-2, 3)

        # list_albums = []
        # formatAlbums(first_3_albums, list_albums, True)
        # formatAlbums(last_3_albums, list_albums, True)
        print(tabulate(list_albums, headers=['name','release_date', 'total_tracks' ,'album_type', 'artist_album_name', 'external_urls'], tablefmt='grid'))



    elif int(inputs[0]) == 3:
        print('Por favor ingrese el numero de artistas del TOP a buscar...')
        n_top = int(input('TOP: '))
        start_time = controller.getTime()
        sorted_list, delta_time = controller.sortArtistsByPopularity(algoritmo, ar[1], ar[0])
        artist_top = lt.subList(sorted_list, 1, n_top)
        artist_top, size = controller.searchTrackById(artist_top, tr[1])

        end_time = controller.getTime()

        elapsed = controller.deltaTime(start_time, end_time)
        print(f'En total tardó {round(elapsed,2)}ms.')

        print(f'\nThe first 3 and last 3 artists in the top {n_top} are...')

        if size >= 6:
            first_3_artists = lt.subList(artist_top, 1, 3)
            last_3_artists = lt.subList(artist_top, size-2, 3)
            prints_artists = lt.newList('ARRAY_LIST')
            for artist in lt.iterator(first_3_artists):
                lt.addLast(prints_artists, artist)
            for artist in lt.iterator(last_3_artists):
                lt.addLast(prints_artists, artist)
        else:
            prints_artists = artist_top

        list_artists = []
        formatArtists(prints_artists, list_artists, True)

        # first_3_artists = lt.subList(artist_top, 1, 3)
        # last_3_artists = lt.subList(artist_top, lt.size(artist_top)-2, 3)

        # list_artists = []
        # formatArtists(first_3_artists, list_artists, True)
        # formatArtists(last_3_artists, list_artists, True)
        print(tabulate(list_artists, headers=['name','artis_popularity','followers', 'revelant_track_name', 'genres'], tablefmt='grid'))

    elif int(inputs[0]) == 4:
        print('TO DO: PEDRO LOPEZ')
    elif int(inputs[0]) == 5:
        print('Por favor ingrese los siguientes datos para encontrar la canción más popular...')
        artist_name = input('Nombre del artista: ')
        market_name = input('País o mercado en el que esta disponible la canción: ')

        start_time = controller.getTime()
        artist_id = controller.getArtistId(ar[1], artist_name)
        if artist_id == -1:
            print('\nNo se encontró el artista.\n')
        else:
            tracksinMarket, size_market, market_id = controller.searchTracksByMarket(tr[1], market_name)
            if size_market <= 0:
                print('\nNo se encontraron canciones en este mercado.\n')
            else:
                print(f"\n'{artist_name}' available discography in {market_name} ({market_id})")
                tracksInMarketArtist, size_artist = controller.searchTracksByArtist(tracksinMarket, artist_id)
                orderedTracks, _ = controller.sortTracksByPopularity(algoritmo, tracksInMarketArtist, size_artist)
                orderedTracksAlbumData, size_album = controller.getAlbumInfo(al[1], orderedTracks)
                print(f'Unique Available Albums: {size_album}')
                print(f'Unique Available tracks: {size_artist}')
                top1 = lt.firstElement(orderedTracksAlbumData)
                end_time = controller.getTime()

                elapsed = controller.deltaTime(start_time, end_time)
                print(f'En total tardó {round(elapsed,2)}ms.')

                name = '\n'.join(textwrap.wrap(top1['name'], 16))
                album_name = '\n'.join(textwrap.wrap(top1['album_name'], 16))
                release_date = top1['release_date']
                artists_names = []
                for artist in top1['artists_id']:
                    artist_name = controller.getArtistName(ar[1], artist)
                    artists_names.append(artist_name)
                artists_str = ', '.join(artists_names)
                artists_str = textwrap.wrap(artists_str, 16)
                artists_str = '\n'.join(artists_str)
                duration = top1['duration_ms']
                popularity = top1['popularity']
                preview_url = top1['preview_url']
                preview_url = '\n'.join(textwrap.wrap(preview_url, 16))
                lyrics = top1['lyrics']
                if lyrics.strip() == '-99':
                    lyrics_str = 'Letra de la canción NO disponible'
                else:
                    lyrics_str = textwrap.shorten(lyrics, width=128, placeholder='...')
                lyrics_str = '\n'.join(textwrap.wrap(lyrics_str, 16))
                track = [[name, album_name, release_date, artists_str, duration, popularity, preview_url, lyrics_str]]

                print('\nThe most popular track are...')
                print(tabulate(track, headers=['name', 'album_name', 'release_date', 'artists_names', 'duration_ms', 'popularity', 'preview_url', 'lyrics'], tablefmt='grid'))


    elif int(inputs[0]) == 6:
        print('Por favor ingrese el nombre del artista para encontrar su discografía...')
        artist_name = input('Nombre del artista: ')

        start_time = controller.getTime()
        artist_id = controller.getArtistId(ar[1], artist_name)
        if artist_id == -1:
            print('\nNo se encontró el artista.\n')
        else:
            albumsByArtist, albums_total, types_count = controller.searchAlbumsByArtist(al[1], artist_id)
            print(f'\nDiscographic Metrics from "{artist_name}"')

            for k,v in types_count.items():
                if v > 0:
                    print(f'Number of "{k}": {v}')
            print(f'Total Albums in  Discography: {albums_total}')


            albumsInRange, size = controller.searchArtistById(albumsByArtist, ar[1])

            end_time = controller.getTime()

            elapsed = controller.deltaTime(start_time, end_time)
            print(f'En total tardó {round(elapsed,2)}ms.')

            print('\n+++ Albums Details +++')
            print('\nThe first 3 and last 3 albums in the range are...')
            if size >= 6:
                first_3_albums = lt.subList(albumsInRange, 1, 3)
                last_3_albums = lt.subList(albumsInRange, size-2, 3)
                prints_albums = lt.newList('ARRAY_LIST')
                for album in lt.iterator(first_3_albums):
                    lt.addLast(prints_albums, album)
                for album in lt.iterator(last_3_albums):
                    lt.addLast(prints_albums, album)
            else:
                prints_albums = albumsInRange

            list_albums = []
            formatAlbums(prints_albums, list_albums, True, False)

            # first_3_albums = lt.subList(albumsInRange, 1, 3)
            # last_3_albums = lt.subList(albumsInRange, size-2, 3)

            # prints_albums = lt.newList('ARRAY_LIST')
            # for album in lt.iterator(first_3_albums):
            #     lt.addLast(prints_albums, album)
            # for album in lt.iterator(last_3_albums):
            #     lt.addLast(prints_albums, album)

            # list_albums = []
            # formatAlbums(first_3_albums, list_albums, True, False)
            # formatAlbums(last_3_albums, list_albums, True, False)
            print(tabulate(list_albums, headers=['name','release_date', 'total_tracks' ,'album_type', 'artist_album_name', 'external_urls'], tablefmt='grid'))

            print('\n+++ Tracks Details +++')

            for album in lt.iterator(prints_albums):
                album_id = album['id']
                tracks, size_tracks = controller.searchTracksByAlbum(tr[1], album_id)
                sorted_tracks, _ = controller.sortTracksByPopularity(algoritmo, tracks, size_tracks)
                top1 = lt.firstElement(sorted_tracks)
                name = '\n'.join(textwrap.wrap(top1['name'], 16))
                artists_names = []
                for artist in top1['artists_id']:
                    artist_name = controller.getArtistName(ar[1], artist)
                    artists_names.append(artist_name)
                artists_str = ', '.join(artists_names)
                artists_str = textwrap.wrap(artists_str, 16)
                artists_str = '\n'.join(artists_str)
                duration = top1['duration_ms']
                popularity = top1['popularity']
                preview_url = top1['preview_url']
                preview_url = '\n'.join(textwrap.wrap(preview_url, 16))
                lyrics = top1['lyrics']
                if lyrics.strip() == '-99':
                    lyrics_str = 'Letra de la canción NO disponible'
                else:
                    lyrics_str = textwrap.shorten(lyrics, width=128, placeholder='...')
                lyrics_str = '\n'.join(textwrap.wrap(lyrics_str, 16))
                track = [[name, artists_str, duration, popularity, preview_url, lyrics_str]]

                print(f'\nMost popular track in "{album["name"]}"')
                print(tabulate(track, headers=['name', 'artists_names', 'duration_ms', 'popularity', 'preview_url', 'lyrics'], tablefmt='grid'))

    elif int(inputs[0]) ==7:
        print('Por favor ingrese el rango de años de las canciones a buscar...')
        start = int(input('Año inicial: '))
        end = int(input('Año final: '))
        print('Por favor ingrese el numero de canciones del top que desea mostrar...')
        n_canciones = int(input('TOP: '))

        start_time = controller.getTime()
        sorted_list, delta_time = controller.sortAlbumsByYear(algoritmo, al[1], al[0])
        albumsInRange, size = controller.getAlbumsInRange(sorted_list, start, end)

        print(f'There are {size} albums released between {start} and {end}')
        print('\nThe first 3 and last 3 albums in the range are...')

        all_tracks = lt.newList('ARRAY_LIST')

        for album in lt.iterator(albumsInRange):
                album_id = album['id']
                tracks, size_tracks = controller.searchTracksByAlbum(tr[1], album_id)
                tracks_in_albums, _ = controller.getAlbumInfo(albumsInRange, tracks)
                lt.addLast(all_tracks, tracks_in_albums)


        all_sorted_tracks = lt.newList('ARRAY_LIST')
        for album_tracks in lt.iterator(all_tracks):
            for track in lt.iterator(album_tracks):
                lt.addLast(all_sorted_tracks, track)

        sorted_tracks, _ = controller.sortTracksByMarkets(algoritmo, all_sorted_tracks, lt.size(all_sorted_tracks))
        top_n = lt.subList(sorted_tracks, 1, n_canciones)

        if n_canciones >= 6:
            first_3_tracks = lt.subList(top_n, 1, 3)
            last_3_tracks = lt.subList(top_n, n_canciones-2, 3)
            print_tracks = lt.newList('ARRAY_LIST')
            for track in lt.iterator(first_3_tracks):
                lt.addLast(print_tracks, track)
            for track in lt.iterator(last_3_tracks):
                lt.addLast(print_tracks, track)
        else:
            print_tracks = top_n


        list_tracks = []
        for track in lt.iterator(print_tracks):
            # print(track)
            name = '\n'.join(textwrap.wrap(track['name'], 16))
            album_name = '\n'.join(textwrap.wrap(track['album_name'], 16))
            num_markets = len(track['available_markets'])
            artists_names = []
            for artist in track['artists_id']:
                artist_name = controller.getArtistName(ar[1], artist)
                artists_names.append(artist_name)
            artists_str = ', '.join(artists_names)
            artists_str = textwrap.wrap(artists_str, 16)
            artists_str = '\n'.join(artists_str)
            duration = track['duration_ms']
            popularity = track['popularity']
            preview_url = track['preview_url']
            preview_url = '\n'.join(textwrap.wrap(preview_url, 16))
            lyrics = track['lyrics']
            if lyrics.strip() == '-99':
                lyrics_str = 'Letra de la canción NO disponible'
            else:
                lyrics_str = textwrap.shorten(lyrics, width=128, placeholder='...')
            lyrics_str = '\n'.join(textwrap.wrap(lyrics_str, 16))
            list_tracks.append([name, album_name, num_markets, artists_str, duration, popularity, preview_url, lyrics_str])

        end_time = controller.getTime()

        elapsed = controller.deltaTime(start_time, end_time)
        print(f'En total tardó {round(elapsed,2)}ms.')

        print(f'\nThe first 3 and last 3 most popular tracks int the top {n_canciones} are...')
        print(tabulate(list_tracks, headers=['name', 'album_name', 'num_markets', 'artists_names', 'duration_ms', 'popularity', 'preview_url', 'lyrics'], tablefmt='grid'))

    elif int(inputs[0]) == 8:
        print("1- Insertion")
        print("2- Selection")
        print("3- Shell")
        print("4- Quick")
        print("5- Merge")
        sel_algoritmo = input("Seleccione un tipo de algoritmo para continuar:\n")

        if int(sel_algoritmo[0]) == 1:
            algoritmo = "insertion"
        elif int(sel_algoritmo[0]) == 2:
            algoritmo = "selection"
        elif int(sel_algoritmo[0]) == 3:
            algoritmo = "shell"
        elif int(sel_algoritmo[0]) == 4:
            algoritmo = "quick"
        elif int(sel_algoritmo[0]) == 5:
            algoritmo = "merge"


    elif int(inputs[0]) == 0:
        sys.exit(0)

    else:
        continue
sys.exit(0)
