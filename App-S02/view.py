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
import pycountry
from DISClib.ADT import list as lt
assert cf
from prettytable import PrettyTable, ALL

default_limit = 10000
sys.setrecursionlimit(default_limit * 10000)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def newController(listType):
    """
    Se crea una instancia del controlador
    """
    control = controller.newController(listType)
    return control

def printMenu():
    print("\nBienvenido querido usuario :)")
    print("1- Cargar informacion en el catalogo")
    print("2- Listar los albumes en un periodo de tiempo")
    print("3- Encontrar los artistas mas populares")
    print("4- Clasificar las canciones por popularidad")
    print("5- Encontrar la cancion mas popular de un artista")
    print("6- Encontrar la discografia de un artista")
    print("7- Clasificar las canciones con mayor distribucion")
    print("8- Analizar los tiempos de ordenamiento de artistas")
    print("0- Salir de la aplicacion.")

def printListOptions():
    print('\nIngrese el numero del tipo de lista que desee: ')
    print(' 1. ARRAY LIST.')
    print(' 2. LINKED LIST.')

def printSortMethods():
    print('\nIngrese el numero del tipo de ordenamiento que desee: ')
    print(' 1. SELECTION_SORT.')
    print(' 2. INSERTION_SORT.')
    print(' 3. SHELL_SORT.')
    print(' 4. MERGE_SORT')
    print(' 5. QUICK_SORT')

def printFileOptions():
    print('\nIngrese el archivo de artistas que desee analizar: ')
    print(' 1. -small')
    print(' 2. -5pct')
    print(' 3. -10pct')
    print(' 4. -20pct')
    print(' 5. -30pct')
    print(' 6. -50pct')
    print(' 7. -80pct')
    print(' 8. -large')

def printSimplePrettyTable(spotifyList, keys):
    table = PrettyTable()
    table.max_width = 20
    table.hrules = ALL
    table.field_names = keys
    rows = []
    for element in lt.iterator(spotifyList):
        row = []
        for key in keys:
            strElement = str(element[key])
            if len(strElement) > 20:
                strElement = strElement[:20]
            row.append(strElement)
        rows.append(row)
    table.add_rows(rows)
    print(table)

def printONEPrettyTable(spotifyList, keys):
    temporal_list = lt.newList ('ARRAY_LIST')
    for element in lt.iterator(spotifyList):
        lt.addLast(temporal_list, element)
        albumname = str(element['album_name'])
        print('Most popular track in ' + albumname)
        printSimplePrettyTable(temporal_list, keys)
        lt.removeLast(temporal_list)

def headers(req_num, messageone, messagetwo):
    print("============= Req No. " + str(req_num) + " Inputs =============")
    print(messageone)
    print("\n============= Req No. " + str(req_num) + " Answer =============" )
    print(messagetwo)

def calculator(control, sortType, suffix, listType):
    return controller.calculator(control, sortType, suffix, listType)

def loadData():
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    albums, artists, tracks = controller.loadData(control)
    return albums, artists, tracks

def sortpopularityartist(control):
    return controller.sortpopularityartist(control)

# Se crea el controlador asociado a la vista
control = newController('ARRAY_LIST')

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if int(inputs[0]) == 1:
        print("\nCargando información de los archivos ....")
        albums, artists, tracks = loadData()
        print('\n' + 'Albums cargados: ' + str(albums))
        lastNumAlbums = controller.answerLst(control['model']['albums'])
        printSimplePrettyTable(lastNumAlbums, ['name','release_date','inicial_track_name','artist_name','total_tracks','album_type','external_urls'])
        print('\n' + 'Artistas cargados: ' + str(artists))
        lastNumArtists = controller.answerLst(control['model']['artists'])
        printSimplePrettyTable(lastNumArtists, ['name','artist_popularity','followers','relevant_track_name','genres'])
        print('\n' + 'Tracks cargados: ' + str(tracks))
        lastNumTracks = controller.answerLst(control['model']['tracks'])
        printSimplePrettyTable(lastNumTracks, ['name','popularity','album_name','disc_number','track_number','duration_ms','artists_names','href'])
    elif int(inputs[0]) == 2:
        firstYear = input('\nIngrese el primer año: ')
        lastYear = input('Ingrese el ultimo año: ')
        albumsByYear, time, sizeSubList = controller.albumsByReleaseYear(control['model'], firstYear, lastYear)
        message1 = 'Albums released between ' + str(firstYear) + ' and ' + str(lastYear)
        message2 = 'There are ' + str(sizeSubList) + 'released between ' + str(firstYear) + ' and ' + str(lastYear)
        print (headers(1,message1,message2))
        print('\n The first 3 and last 3 albums in the range are ...')
        printSimplePrettyTable(albumsByYear, ['name','release_date','album_type','artist_name','total_tracks','external_urls'])
        print('Tiempo de ejecucion: ', time)

    elif int(inputs[0]) == 3:
        topNum = input('\nIngrese el numero del top de artistas que desea consultar: ')
        topArtists, time, sizeSubList = controller.artistByPopularity(control['model'], int(topNum))
        print(sizeSubList)
        message1 = 'TOP ' + str(sizeSubList) + ' most popular artists in Spotify.'
        message2 = 'The first 3 and last 3 albums in the TOP ' + str(sizeSubList) + ' are ...'
        print (headers(2,message1,message2))

        printSimplePrettyTable(topArtists,['artist_popularity','followers','name','relevant_track_name','genres'])
        print('Tiempo de ejecucion: ', time)

    elif int(inputs[0]) == 4:
        topNum = input('\nIngrese el numero a consultar del top de canciones: ')
        topTracks, time, sizeSubList = controller.tracksByPopularity(int(topNum), control['model'])

        message1 = 'TOP ' + str(sizeSubList) + ' most popular tracks in Spotify.'
        message2 = 'The first 3 and last 3 albums in the TOP ' + str(sizeSubList) + ' are ...'
        print (headers(3,message1,message2))

        printSimplePrettyTable(topTracks, ['name','album_name','artists_names','popularity','duration_ms','href','lyrics'])
        print('Tiempo de ejecucion: ', time)

    elif int(inputs[0]) == 5:
        artistName = input('Ingrese el nombre del artista que desea consultar: ').strip()
        countryCode = input('Ingrese el nombre del pais a consultar (en Ingles): ')
        countryname = pycountry.countries.get(name = str(countryCode))
        countryname = countryname.alpha_2
        tracksFiltered, time, sizeSubList = controller.popularTrackByArtist(control['model'], artistName, countryname)

        message1 = str(artistName) + ' Discography metrics in ' + countryCode + ' Code:' + str(countryname)
        message2 = str(artistName) + ' avilable discography in ' + countryCode + ' Code:' + str(countryname)
        print (headers(4,message1,message2))
        print('\n The first 3 and last 3 albums in the range are ...')
        printSimplePrettyTable(tracksFiltered, ['name', 'album_name', 'artists_names', 'duration_ms', 'popularity', 'preview_url','href','lyrics'])
        print('Tiempo de ejecucion: ', time)

    elif int(inputs[0]) == 6:
        artistName = input('Ingrese el nombre del artista que desea consultar: ').strip()
        sizeAlbumsArtist, countByType, albumssorted, trackArray, delta_time = controller.albumInfo(control['model'],artistName)
        message1 = 'Discography metrics from ' + str(artistName)
        message2 ='Number of "compilation": ' + str(sizeAlbumsArtist) + '\nNumber of "singles": ' + str(countByType[0]) + '\nNumber of "album": ' + str(countByType[1])  + '\n Total Albums in Discorgraphy: ' + str(countByType[2])
        print (headers(5,message1,message2))
        print("\n +++ Albums Details +++ \nThe first and last 3 tracks in the range are ...")
        printSimplePrettyTable(albumssorted,['release_date', 'name' ,'total_tracks','album_type','artist_name', 'external_urls'])
        printONEPrettyTable(trackArray,['popularity','duration_ms','name','disc_number',"track_number",'artists_names','preview_url', 'href','lyrics'])
        print('Tiempo de ejecucion: ', delta_time)

    elif int(inputs[0]) == 7:
        firstYear = input('\nIngrese el primer año: ')
        lastYear = input('Ingrese el ultimo año: ')
        topNum = input('\nIngrese el numero del top de canciones a identificar: ')
        topTracksDistribution, time = controller.tracksByDistributionInRange(control['model'],firstYear, lastYear, int(topNum))
        printSimplePrettyTable(topTracksDistribution, ['name','album_name','artists_names', 'distribution', 'popularity', 'duration_ms' ])
        print('Tiempo de ejecucion: ', time)

    elif int(inputs[0]) == 8:
        listSelection = False
        while listSelection == False:
            printListOptions()
            listTypeSelection = input('Opción seleccionada: ')
            if int(listTypeSelection[0]) == 1:
                listType = 'ARRAY_LIST'
                print('\nSeleciono ARRAY_LIST')
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                listSelection = True
            elif int(listTypeSelection[0]) == 2:
                listType = 'SINGLE_LINKED'
                print('\nSeleciono LINKED_LIST')
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                listSelection = True
            else:
                input('\nSeleccion Erronea! Oprima ENTER para continuar...')
        print("Cargando información de los archivos...\n")

        control = newController(listType)

        sortSelection = False
        while sortSelection == False:
            printSortMethods()
            sortTypeSelection = input('Opción seleccionada: ')
            if int(sortTypeSelection[0]) == 1:
                sortType = 'sls'
                print('\nSeleciono SELECTION_SORT')
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                sortSelection = True
            elif int(sortTypeSelection[0]) == 2:
                sortType = 'ins'
                print('\nSeleciono INSERTION_SORT')
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                sortSelection = True
            elif int(sortTypeSelection[0]) == 3:
                sortType = 'shl'
                print('\nSeleciono SHELL_SORT')
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                sortSelection = True
            elif int(sortTypeSelection[0]) == 4:
                sortType = 'mgs'
                print('\nSeleciono MERGE_SORT')
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                sortSelection = True
            elif int(sortTypeSelection[0]) == 5:
                sortType = 'qks'
                print('\nSeleciono QUICK_SORT')
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                sortSelection = True
            else:
                input('\nSeleccion Erronea! Oprima ENTER para continuar...')

        suffixSelection = False
        while suffixSelection == False:
            printFileOptions()
            suffixFileSelection = input('Opción seleccionada: ')
            if int(suffixFileSelection[0]) == 1:
                suffix = '-small'
                print('\nSeleciono el archivo ' + suffix)
                suffix += '.csv'
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                suffixSelection = True
            elif int(suffixFileSelection[0]) == 2:
                suffix = '-5pct'
                print('\nSeleciono el archivo ' + suffix)
                suffix += '.csv'
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                suffixSelection = True
            elif int(suffixFileSelection[0]) == 3:
                suffix = '-10pct'
                print('\nSeleciono el archivo ' + suffix)
                suffix += '.csv'
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                suffixSelection = True
            elif int(suffixFileSelection[0]) == 4:
                suffix = '-20pct'
                print('\nSeleciono el archivo ' + suffix)
                suffix += '.csv'
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                suffixSelection = True
            elif int(suffixFileSelection[0]) == 5:
                suffix = '-30pct'
                print('\nSeleciono el archivo ' + suffix)
                suffix += '.csv'
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                suffixSelection = True
            elif int(suffixFileSelection[0]) == 6:
                suffix = '-50pct'
                print('\nSeleciono el archivo ' + suffix)
                suffix += '.csv'
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                suffixSelection = True
            elif int(suffixFileSelection[0]) == 7:
                suffix = '-80pct'
                print('\nSeleciono el archivo ' + suffix)
                suffix += '.csv'
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                suffixSelection = True
            elif int(suffixFileSelection[0]) == 8:
                suffix = '-large'
                print('\nSeleciono el archivo ' + suffix)
                suffix += '.csv'
                input('Seleccion exitosa! Oprima ENTER para continuar...')
                suffixSelection = True

        result = calculator(control['model'], sortType, suffix, listType)
        print('El tiempo para el archivo ' + suffix + ' en ' + listType + ' con ' + sortType + ' es ' + str(result))

    else:
        sys.exit(0)
sys.exit(0)
