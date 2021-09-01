from aiogram.dispatcher.filters import CommandStart, Regexp
from aiogram import types, Dispatcher

from keyboards.keyboard import kb_cmd_start, kb_album_list, kb_list_track, kb_record_audio

from utils.spotify_search import SpotifySearch
from utils.data_base import DataBase


async def cmd_start(msg: types.Message):
    # Возвращает клавиатуру на команду /start
    await msg.answer(text='Search music on Spotify', reply_markup=kb_cmd_start())


async def answer(kwargs, msg):
    db = DataBase()
    tg_image_id = db.search_image_id(kwargs['photo'])
    if tg_image_id is not None:
        kwargs['photo'] = tg_image_id
        await msg.answer_photo(**kwargs)
    else:
        image = await msg.answer_photo(**kwargs)
        db.save_image_info(tg_id=image.photo[-1].file_id, url=kwargs['photo'])


async def download_track(msg: types.Message):
    await msg.delete()
    track = SpotifySearch()
    track = track.get_track_info(msg.text)

    text = f"<b>Artist: {track['artist_name']}\nAlbum: {track['album_name']}\nTrack: {track['track_name']}</b>"
    kwargs = {'photo': track['image'],
              'caption': text,
              'parse_mode': types.ParseMode.HTML,
              'reply_markup': kb_record_audio(url_track=msg.text)}
    await answer(kwargs, msg)


async def list_album(msg: types.Message):
    await msg.delete()
    artist = SpotifySearch()
    artist = artist.artist_info(msg.text)

    text = f"<b>Artist: {artist['name']}</b>"
    kwargs = {'photo': artist['image'],
              'caption': text,
              'parse_mode': types.ParseMode.HTML,
              'reply_markup': kb_album_list(url_artist=msg.text)}
    await answer(kwargs, msg)


async def list_track(msg: types.Message):
    await msg.delete()
    album_info = SpotifySearch()
    album_info = album_info.get_list_track(msg.text)
    text = f"<b>Artist: {album_info['artist_name']}\nAlbum: {album_info['album_name']}</b>"
    kwargs = {'photo': album_info['image_album'],
              'caption': text,
              'parse_mode': types.ParseMode.HTML,
              'reply_markup': kb_list_track(url_album=msg.text)}
    await answer(kwargs, msg)


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(download_track, Regexp('(https://open.spotify.com/track/).'))
    dp.register_message_handler(list_track, Regexp('(https://open.spotify.com/album/).'))
    dp.register_message_handler(list_album, Regexp('(https://open.spotify.com/artist/).'))
    dp.register_message_handler(cmd_start, CommandStart)
