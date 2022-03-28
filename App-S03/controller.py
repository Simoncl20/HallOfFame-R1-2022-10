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
from model import Control, Catalog

csv.field_size_limit(2147483647)
from typing import Callable
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del Catálogo
def newController() -> Control:
    """
    Crea una instancia del modelo
    """
    control = {'model': None}
    control['model'] = model.newCatalog()
    return control


# Funciones para la carga de datos
def loadArtists(catalog: Catalog) -> int:
    artistsFile = cf.data_dir + "Spotify/spotify-artists-utf8-large.csv"
    input_file = csv.DictReader(open(artistsFile, encoding="utf-8"))
    for artist in input_file:
        model.addArtist(catalog, artist)
    return model.artistsSize(catalog)


def loadAlbums(catalog: Catalog) -> int:
    albumsFile = cf.data_dir + "Spotify/spotify-albums-utf8-large.csv"
    input_file = csv.DictReader(open(albumsFile, encoding="utf-8"))
    for album in input_file:
        model.addAlbum(catalog, album)
    return model.albumsSize(catalog)


def loadTracks(catalog: Catalog) -> int:
    tracksFile = cf.data_dir + "Spotify/spotify-tracks-utf8-large.csv"
    input_file = csv.DictReader(open(tracksFile, encoding="utf-8"))
    for track in input_file:
        model.addTrack(catalog, track)
    return model.tracksSize(catalog)


def loadData(control: Control) -> "tuple[int, int, int]":
    catalog = control["model"]
    artists = loadArtists(catalog)
    sortArtistsbyID(catalog)
    albums = loadAlbums(catalog)
    sortAlbumsbyID(catalog)
    tracks = loadTracks(catalog)
    sortTracksbyID(catalog)
    relevantTrackName(catalog)
    prompters(catalog)
    #Aquí arriba se actualiza el campo artist["relevant_track_name"]
    return artists, albums, tracks


def relevantTrackName(catalog: Catalog):
    return model.relevantTrackName(catalog)


def prompters(catalog: Catalog):
    return model.prompters(catalog)


# Funciones de ordenamiento
def sortArtists(control: Control):
    return model.sortArtists(control["model"])


def sortArtistsbyID(control: Control):
    return model.sortArtistsbyID(control)


def sortAlbumsbyID(control: Control):
    return model.sortAlbumsbyID(control)


def sortTracksbyID(control: Control):
    return model.sortTracksbyID(control)


def sortAlbums(catalog: Catalog):
    model.sortAlbums(catalog)


def sortTracks(catalog: Catalog):
    model.sortTracks(catalog)


# Funciones de consulta sobre el catálogo


def getAlbumsByYear(control, a_inicio, a_final):
    return model.getAlbumsByYear(control["model"], a_inicio, a_final)


def getTopArtists(control, number):
    """
    Retorna los mejores libros
    """
    topArtists = model.getTopArtists(control['model'], number)
    return topArtists


def getTopTracks(control, number):
    """
    Retorna los mejores tracks
    """
    return model.getTopTracks(control["model"], number)


def getBestTrack(control, artist, country):
    return model.getBestTrack(control["model"], artist, country)


def getDiscography(control, artist):
    return model.getDiscography(control["model"], artist)


def getTopTracksbyYear(control, a_inicio, a_final, top):
    return model.getTopTracksbyYear(control["model"], a_inicio, a_final, top)
