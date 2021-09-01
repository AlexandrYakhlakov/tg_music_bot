from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.spotify_search import SpotifySearch
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('name', 'uri')


def kb_cmd_start():
    buttons = [
        InlineKeyboardButton(text='Search Artist', switch_inline_query_current_chat='ar. '),
        InlineKeyboardButton(text='Search Album', switch_inline_query_current_chat='alb. '),
        InlineKeyboardButton(text='Search Track', switch_inline_query_current_chat='s. ')
    ]

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def kb_album_list(url_artist):
    buttons = []
    albums = SpotifySearch()
    for album in albums.get_list_album(url_artist):
        buttons.append(InlineKeyboardButton(text=album['name'], callback_data=album['url']))
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def kb_download(url_album):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Download', callback_data=url_album))
    return keyboard


def kb_list_track(url_album):
    tracks = SpotifySearch()
    tracks = tracks.get_list_track(url_album=url_album)
    buttons = list()
    for track in tracks['album_tracks']:
        buttons.append(InlineKeyboardButton(text=f"{track['number']}. {track['name']}", callback_data=track['url']))
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def kb_record_audio(url_track):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Download track', callback_data=url_track))
    return keyboard
