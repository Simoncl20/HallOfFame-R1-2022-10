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

from datetime import datetime
import config as cf
import sys
import controller
import pycountry as pc
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate

default_limit = 1000
sys.setrecursionlimit(default_limit * 10)
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
    print("2- Consultar albumes por periodo de tiempo")
    print("3- Consultar los Top X aritstas más populares")
    print("4- Consultar las Top X canciones más populares")
    print("5- Consultar la canción más popular de un artista")
    print("6- Consultar la discografía de un artista")
    print("7- Clasificar las canciones con mayor distribución")


def loadData():
    """
    retorna el numero de cada tipo de dato cargado
    """
    artists, albums, tracks = controller.loadData(control)
    return artists, albums, tracks


control = newController()


def printResultOption1(artists, albums, tracks):
    #Imprime los primeros 3 y ultimos 3 artistas
    print("Los primeros 3 y los últimos 3 artistas en este rango son...")
    answer = [("name", "genres", "artist_popularity", "followers")]
    for i in range(0, 3):
        index = (lt.getElement(control["model"]["artists"], i)["name"],
                 lt.getElement(control["model"]["artists"], i)["genres"],
                 lt.getElement(control["model"]["artists"],
                               i)["artist_popularity"],
                 lt.getElement(control["model"]["artists"], i)["followers"])
        answer.append(index)
    for i in range(-3, 0):
        index2 = (lt.getElement(control["model"]["artists"], i)["name"],
                  lt.getElement(control["model"]["artists"], i)["genres"],
                  lt.getElement(control["model"]["artists"],
                                i)["artist_popularity"],
                  lt.getElement(control["model"]["artists"], i)["followers"])
        answer.append(index2)
    print(tabulate(answer, headers="firstrow", tablefmt="grid"))
    #Imprime los primeros 3 y ultimos 3 albumes
    print("\n Los primeros 3 y los últimos 3 albumes en este rango son...")
    answer = [("name", "album_type", "available_markets", "release_date")]
    for i in range(0, 3):
        index = (lt.getElement(control["model"]["albums"], i)["name"],
                 lt.getElement(control["model"]["albums"], i)["album_type"],
                 str(
                     lt.getElement(control["model"]["albums"],
                                   i)["available_markets"][:10]) +
                 " continúa...]", lt.getElement(control["model"]["albums"],
                                                i)["release_date"])
        answer.append(index)
    for i in range(-3, 0):
        index2 = (lt.getElement(control["model"]["albums"], i)["name"],
                  lt.getElement(control["model"]["albums"], i)["album_type"],
                  str(
                      lt.getElement(control["model"]["albums"],
                                    i)["available_markets"][:10]) +
                  " continúa...]", lt.getElement(control["model"]["albums"],
                                                 i)["release_date"])
        answer.append(index2)
    print(tabulate(answer, headers="firstrow", tablefmt="grid"))
    #Imprime los primeros 3 y ultimos 3 tracks
    print("\n Las primeras 3 y las últimas 3 canciones en este rango son...")
    answer = [("name", "duration_ms", "track_number")]
    for i in range(0, 3):
        index = (lt.getElement(control["model"]["tracks"], i)["name"],
                 lt.getElement(control["model"]["tracks"], i)["duration_ms"],
                 lt.getElement(control["model"]["tracks"], i)["track_number"])
        answer.append(index)
    for i in range(-3, 0):
        index2 = (lt.getElement(control["model"]["tracks"], i)["name"],
                  lt.getElement(control["model"]["tracks"], i)["duration_ms"],
                  lt.getElement(control["model"]["tracks"], i)["track_number"])
        answer.append(index2)
    print(tabulate(answer, headers="firstrow", tablefmt="grid"))


def printResultOption2(result, año_inicial, año_final):
    print("=" * 10 +
          " Respuestas de \"Consultar albumes por periodo de tiempo\" " +
          "=" * 10)
    print("Hay " + str(lt.size(result)) + " albúmes entre " +
          str(año_inicial) + " y " + str(año_final) + "\n")
    if (lt.size(result) == 0): return
    print("Los primeros 3 y los últimos 3 son...")
    answer = [("name", "release_date", "album_type", "artist_name",
               "total_tracks")]
    if lt.size(result) <= 6:
        rango_1 = lt.size(result) + 1
        rango_2 = 0
    else:
        rango_1 = 4
        rango_2 = -3
    for i in range(1, rango_1):
        index = (lt.getElement(result,
                               i)["name"], lt.getElement(result,
                                                         i)["release_date"],
                 lt.getElement(result, i)["album_type"],
                 lt.getElement(result, i)["artist_name"],
                 lt.getElement(result, i)["total_tracks"])
        answer.append(index)
    for i in range(rango_2, 0):
        index2 = (lt.getElement(result,
                                i)["name"], lt.getElement(result,
                                                          i)["release_date"],
                  lt.getElement(result, i)["album_type"],
                  lt.getElement(result, i)["artist_name"],
                  lt.getElement(result, i)["total_tracks"])
        answer.append(index2)
    print(tabulate(answer, headers="firstrow", tablefmt="grid"))


def printResultOption3(result, top):
    print("=" * 10 + " Respuestas de \"Consultar los Top " + str(top) +
          " artistas más populares\" " + "=" * 10 + "\n\n")
    print("Los primeros 3 y los últimos 3 artistas en el top " + str(top) +
          " son...\n")
    answer = [("name", "artist_popularity", "followers", "genres",
               "relevant_track_name")]
    if lt.size(result) <= 6:
        rango_1 = lt.size(result) + 1
        rango_2 = 0
    else:
        rango_1 = 4
        rango_2 = -3
    for i in range(1, rango_1):
        index = (lt.getElement(result, i)["name"],
                 lt.getElement(result, i)["artist_popularity"],
                 lt.getElement(result,
                               i)["followers"], lt.getElement(result,
                                                              i)["genres"],
                 lt.getElement(result, i)["relevant_track_name"])
        answer.append(index)
    for i in range(rango_2, 0):
        index2 = (lt.getElement(result, i)["name"],
                  lt.getElement(result, i)["artist_popularity"],
                  lt.getElement(result,
                                i)["followers"], lt.getElement(result,
                                                               i)["genres"],
                  lt.getElement(result, i)["relevant_track_name"])
        answer.append(index2)
    print(tabulate(answer, headers="firstrow", tablefmt="grid"))


def printResultOption4(result, top):
    print("=" * 10 + " Respuestas de \"Consultar los Top " + str(top) +
          " artistas más populares\" " + "=" * 10 + "\n\n")
    print("Los primeros 3 y los últimos 3 artistas en el top " + str(top) +
          " son...\n")
    answer = [("name", "album", "artists", "popularity", "duration_ms", "href",
               "lyrics")]
    if lt.size(result) <= 6:
        rango_1 = lt.size(result) + 1
        rango_2 = 0
    else:
        rango_1 = 4
        rango_2 = -3
    for i in range(1, rango_1):
        cancion = lt.getElement(result, i)
        index = (cancion["name"], cancion["album_name"],
                 cancion["artists_names"], cancion["popularity"],
                 cancion["duration_ms"], cancion["href"][:15],
                 cancion["lyrics"][0:15] + "...")
        answer.append(index)
    for i in range(rango_2, 0):
        cancion = lt.getElement(result, i)
        index2 = (cancion["name"], cancion["album_name"],
                  cancion["artists_names"], cancion["popularity"],
                  cancion["duration_ms"], cancion["href"][:15],
                  cancion["lyrics"][0:15] + "...")
        answer.append(index2)
    print(tabulate(
        answer,
        headers="firstrow",
        tablefmt="grid",
    ))


def printResultOption5(result, artist, country, country_fuzzy):
    print("=" * 10 +
          " Respuestas de \"Consultar la canción más popular de un artista\"" +
          "=" * 10 + "\n\n")
    if (result is None):
        print("El artista " + artist + " no fue encontrado.\n")
        return
    print("Discografía disponile de " + artist + " en " + country + " (" +
          country_fuzzy + ")")
    print("Numero de álbumes relacionados a este artista: " +
          str(lt.size(result[0]["albums"])))
    print("Numero de canciones relacionadas a este artista: " +
          str(lt.size(result[0]["songs"])) + "\n\n")
    print("La canción más popular es...\n")
    answer = [("name", "album_name", "release_date", "artists_names",
               "duration_ms", "popularity", "preview_url", "lyrics")]
    index = (result[1]["name"], result[1]["album_name"],
             result[1]["release_date"], result[1]["artists_names"],
             result[1]["duration_ms"], result[1]["popularity"],
             result[1]["preview_url"][:15] + "...",
             result[1]["lyrics"][:15] + "...")
    answer.append(index)
    print(tabulate(answer, headers="firstrow", tablefmt="grid"))


def printResultOption6(result, artist):
    if (result is None):
        print("El artista " + artist + " no fue encontrado\n")
        return
    print("=" * 10 +
          " Respuestas de \"Consultar la discografía de un artista\"" +
          "=" * 10 + "\n\n")
    print("Discografía de " + artist + ":")
    print("Número de álbumes tipo 'single': " + str(result[0]))
    print("Número de álbumes tipo 'compilation': " + str(result[1]))
    print("Número de álbumes tipo 'album': " + str(result[2]) + "\n\n\n")
    print(
        "+++ Detalles de álbumes +++\nLos primeros 3 y los últimos 3 áblumes en este rango son..."
    )
    answer1 = [("release_date", "name", "total_tracks", "album_type",
                "artist_name")]
    if lt.size(result[3]["albums"]) <= 6:
        rango_1 = lt.size(result[3]["albums"]) + 1
        rango_2 = 0
    else:
        rango_1 = 4
        rango_2 = -3
    for i in range(1, rango_1):
        album = lt.getElement(result[3]["albums"], i)
        index = (album["release_date"], album["name"], album["total_tracks"],
                 album["album_type"], album["artist_name"])
        answer1.append(index)
    for i in range(rango_2, 0):
        album = lt.getElement(result[3]["albums"], i)
        index = (album["release_date"], album["name"], album["total_tracks"],
                 album["album_type"], album["artist_name"])
        answer1.append(index)
    print(tabulate(answer1, headers="firstrow", tablefmt="grid") + "\n\n\n")
    print("+++ Detalles de canciones +++")
    for i in range(1, rango_1):
        album = lt.getElement(result[3]["albums"], i)
        answer2 = [("name", "artists_names", "duration_ms", "popularity",
                    "preview_url", "lyrics")]
        print("La canción más popular de '" + album["name"] + "':")
        best_song = lt.getElement(album["songs"], 0)
        index = (best_song["name"], best_song["artists_names"],
                 best_song["duration_ms"], best_song["popularity"],
                 best_song["preview_url"][:15], best_song["lyrics"][:20])
        answer2.append(index)
        print(
            tabulate(answer2, headers="firstrow", tablefmt="grid") + "\n\n\n")
    for i in range(rango_2, 0):
        answer3 = [("name", "artists_names", "duration_ms", "popularity",
                    "preview_url", "lyrics")]
        album = lt.getElement(result[3]["albums"], i)
        print("La canción más popular de '" + album["name"] + "':")
        best_song = lt.getElement(album["songs"], 0)
        index = (best_song["name"], best_song["artists_names"],
                 best_song["duration_ms"], best_song["popularity"],
                 best_song["preview_url"][:15], best_song["lyrics"][:20])
        answer3.append(index)
        print(
            tabulate(answer3, headers="firstrow", tablefmt="grid") + "\n\n\n")


def printResultOption7(result, a_inicio, a_final, top):
    print(
        "=" * 10 +
        " Respuestas de \"Clasificar las canciones con mayor distribución\"" +
        "=" * 10 + "\n\n")
    print("Las 3 primeras y 3 últimas canciones en el top " + str(top) +
          " canciones con mayor distribución entre " + str(a_inicio) + " y " +
          str(a_final) + " son...")
    answer = [("name", "release_date", "album_name", "artists_names",
               "number_of_markets", "popularity", "duration_ms")]
    if lt.size(result) <= 6:
        rango_1 = lt.size(result) + 1
        rango_2 = 0
    else:
        rango_1 = 4
        rango_2 = -3
    for i in range(1, rango_1):
        track = lt.getElement(result, i)
        index = (track["name"], track["release_date"], track["album_name"],
                 track["artists_names"], track["markets"], track["popularity"],
                 track["duration_ms"])
        answer.append(index)
    for i in range(rango_2, 0):
        track = lt.getElement(result, i)
        index = (track["name"], track["release_date"], track["album_name"],
                 track["artists_names"], track["markets"], track["popularity"],
                 track["duration_ms"])
        answer.append(index)
    print(tabulate(answer, headers="firstrow", tablefmt="grid") + "\n\n\n")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        artists, albums, tracks = loadData()
        print("\n\n" + "-" * 40 + "\nartistas cargados: " + str(artists) +
              "\nalbumes cargados: " + str(albums) + "\ntracks cargados: " +
              str(tracks) + "\n" + "-" * 40 + "\n\n")
        printResultOption1(artists, albums, tracks)
    elif int(inputs[0]) == 2:
        a_inicio = int(input("Año de inicio: "))
        a_final = int(input("Año final: "))
        result = controller.getAlbumsByYear(control, a_inicio, a_final)
        printResultOption2(result, a_inicio, a_final)
    elif int(inputs[0]) == 3:
        top = input("Buscando los Top ? artistas: ")
        result = controller.getTopArtists(control, int(top))
        printResultOption3(result, int(top))
    elif int(inputs[0]) == 4:
        top = input("Buscando los Top ? canciones: ")
        result = controller.getTopTracks(control, int(top))
        printResultOption4(result, top)
    elif int(inputs[0]) == 5:
        artist = str(input("Nombre del artista: "))
        country = str(input("¿En qué país/mercado?: "))
        country_fuzzy = str(pc.countries.search_fuzzy(country))[18:20]
        result = controller.getBestTrack(control, artist.title(),
                                         country_fuzzy)
        printResultOption5(result, artist.title(), country.title(),
                           country_fuzzy)
    elif int(inputs[0]) == 6:
        artist = input("Nombre del artista: ")
        result = controller.getDiscography(control, artist.title())
        printResultOption6(result, artist.title())
    elif int(inputs[0]) == 7:
        a_inicio = int(input("Ingrese el año de inicio: "))
        a_final = int(input("Ingrese el año final: "))
        top = int(input("Buscando el top?: "))
        result = controller.getTopTracksbyYear(control, a_inicio, a_final, top)
        printResultOption7(result, a_inicio, a_final, top)
    else:
        sys.exit(0)
sys.exit(0)
