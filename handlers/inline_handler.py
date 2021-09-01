from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Regexp

from utils.spotify_search import SpotifySearch


async def search_artist(query: types.InlineQuery):
    artists = SpotifySearch().search_artist(name=query.query.replace('ar. ', ''))
    await query.answer(
        results=
        [
            types.InlineQueryResultArticle(
                id=artist["url"],
                title=f'{artist["artist_name"]}',
                input_message_content=types.InputTextMessageContent(message_text=artist['url']),
                thumb_url=artist["images"],
            )
            for artist in artists],
        cache_time=15)


async def search_album(query: types.InlineQuery):
    albums = SpotifySearch()
    albums = albums.search_album(name=query.query.replace('alb. ', ''))

    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id=album['url'],
                title=album['album'],
                input_message_content=types.InputTextMessageContent(message_text=album['url']),
                description=album['artist'],
                thumb_url=album['images'],
            )
            for album in albums],
        cache_time=15)


async def search_track(query: types.InlineQuery):
    tracks = SpotifySearch().search_track(name=query.query.replace('s. ', ''))
    await query.answer(
        results=[types.InlineQueryResultArticle(
            id=track['url'],
            title=track['track'],
            description=track['artist'],
            thumb_url=track['images'],
            input_message_content=types.InputTextMessageContent(message_text=track['url']))
            for track in tracks],
        cache_time=15)


def register_inline_handler(dp: Dispatcher):
    dp.register_inline_handler(search_artist, Regexp(r'(ar. ).'))
    dp.register_inline_handler(search_album, Regexp(r'(alb. ).'))
    dp.register_inline_handler(search_track, Regexp(r's. '))
