import asyncio
import os
import json
import configparser
import time

from selenium import webdriver
from selenium.common.exceptions import InvalidCookieDomainException


class RecordMusicSpotify:
    path = f'{os.environ["tg_path"]}/utils/'

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=os.environ['chromedriver'])
        self.driver.implicitly_wait(10)

    def _save_cookie(self):
        with open(f'{self.path}spotify_cookies', 'w') as file:
            json.dump(self.driver.get_cookies(), file)

    def _load_cookie(self):
        with open(f'{self.path}spotify_cookies', 'r') as file:
            cookies = json.load(file)
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def auth(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if os.path.exists(f'{os.environ["tg_path"]}/utils/spotify_cookies'):
            try:
                self.driver.get("https://open.spotify.com/")
                self._load_cookie()
                self.driver.get("https://open.spotify.com/")
            except InvalidCookieDomainException:
                self.driver.get("https://open.spotify.com/")
        else:
            self.driver.get("https://www.spotify.com")
            self.driver.find_element_by_xpath(
                """//a[@data-tracking='{"category": "menu", "action": "log-in"}']""").click()
            self.driver.find_element_by_xpath('//input[@ng-model="form.username"]').send_keys(
                config.get('Spotify', 'username'))
            self.driver.find_element_by_xpath('//input[@ng-model="form.password"]').send_keys(
                config.get('Spotify', 'password'))
            self.driver.find_element_by_xpath('//button[@id="login-button"]').click()
            time.sleep(10)
            self._save_cookie()

    async def record_track(self, url_track, artist_name, track_name):
        self.driver.get(url_track)

        # Длительность аудио
        time: str = self.driver.find_element_by_xpath(
            '//span[@class="_qbBHRjaGvaZoEZDZ_IY __whSyV64vHUPUxZSpRJ"][2]').text

        self.driver.find_element_by_xpath('//button[@style="--size:56px;"]').click()

        # Создание процесса
        proc = await asyncio.create_subprocess_shell(f'bash /home/alexandr/PycharmProjects/tg_music_bot/utils/record_music.sh'
                                                     f' "{artist_name}" "{track_name}" {(time.replace(":", "."))}')
        # Ожидание окончания работы процесса
        await proc.communicate()

        self.driver.quit()



