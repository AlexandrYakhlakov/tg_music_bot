import asyncio

import os

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Regexp
import aiogram.utils.markdown as fmt

import subprocess

from keyboards.keyboard import kb_list_track

from utils.spotify_search import SpotifySearch
from utils.data_base import DataBase
from utils.record_audio import RecordMusicSpotify


async def get_album(call: types.CallbackQuery):
    url = call.values['data']
    album_info = SpotifySearch().get_list_track(url_album=url)
    text = f"<b>Artist: {album_info['artist_name']}</b>\n" \
           f"<b>Album: {album_info['album_name']}</b>\n" \
           f"{fmt.hide_link(album_info['image_album'])}"
    kwargs = {'chat_id': call.from_user.id,
              'caption': text,
              'parse_mode': types.ParseMode.HTML,
              'reply_markup': kb_list_track(url),
              'photo': album_info['image_album']}

    db = DataBase()
    tg_id_image = db.search_image_id(url=kwargs['photo'])
    if tg_id_image is not None:
        kwargs['photo'] = tg_id_image
        await call.bot.send_photo(**kwargs)
    else:
        image = await call.bot.send_photo(**kwargs)
        db.save_image_info(tg_id=image.photo[-1].file_id, url=kwargs['photo'])


async def download_track(call: types.CallbackQuery):
    url = call.values['data']
    chat_id = call.from_user.id

    track = SpotifySearch()
    track = track.get_track_info(url_track=url)
    artist_name = track["artist_name"]
    track_name = track["track_name"]
    kwargs = {'chat_id': chat_id,
              'audio': '',
              'performer': artist_name,
              'title': track_name,
              'thumb': track['image']}

    db = DataBase()
    tg_id_image = db.search_image_id(url=kwargs['thumb'])
    if tg_id_image is not None:
        kwargs['thumb'] = tg_id_image

    while True:
        tg_id_file = db.search_track_audio_id(url=url)
        if tg_id_file is not None:
            kwargs['audio'] = tg_id_file
            await call.bot.send_audio(**kwargs)
            break
        else:
            cmd = "bash utils/search_proc.sh".split()
            proc_record = subprocess.check_output(cmd).decode().split('\n')
            proc_record.pop(-1)
            if len(proc_record) > 1:
                await asyncio.sleep(15)
                continue
            else:
                record = RecordMusicSpotify()
                record.auth()
                await record.record_track(url_track=url, artist_name=artist_name, track_name=track_name)
                audio_path = f'/home/alexandr/PycharmProjects/music_bot/utils/{artist_name}-{track_name}'
                kwargs['audio'] = open(audio_path, 'rb')
                audio = await call.bot.send_audio(**kwargs)
                os.remove(path=audio_path)
                db.save_track_info(tg_id=audio.audio.file_id, url=url, artist_name=artist_name, song_name=track_name)
                break


def register_callback_handler(dp: Dispatcher):
    dp.register_callback_query_handler(get_album, Regexp('(https://open.spotify.com/album/).'))
    dp.register_callback_query_handler(download_track, Regexp('(https://open.spotify.com/track/).'))

