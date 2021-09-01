import asyncio

import configparser

from selenium import webdriver

from time import sleep


class RecordMusicSpotify:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='PATH/to/chromedriver')
        self.driver.implicitly_wait(10)

    def auth(self):
        config = configparser.ConfigParser()
        config.read('setting.ini')
        self.driver.get("https://open.spotify.com/")
        self.driver.find_element_by_xpath('//button[@data-testid="login-button"]').click()
        self.driver.find_element_by_xpath('//input[@ng-model="form.username"]').send_keys(
            config.get('Spotify', 'username'))
        self.driver.find_element_by_xpath('//input[@ng-model="form.password"]').send_keys(
            config.get('Spotify', 'password'))
        self.driver.find_element_by_xpath('//button[@id="login-button"]').click()
        sleep(10)

    async def record_track(self, url_track, artist_name, track_name):
        self.driver.get(url_track)

        # Длительность аудио
        time: str = self.driver.find_element_by_xpath(
            '//span[@class="_qbBHRjaGvaZoEZDZ_IY __whSyV64vHUPUxZSpRJ"][2]').text

        self.driver.find_element_by_xpath('//button[@style="--size:56px;"]').click()

        # Создание процесса
        proc = await asyncio.create_subprocess_shell(f'bash ~/PycharmProjects/music_bot/utils/record_music.sh'
                                                     f' "{artist_name}" "{track_name}" {(time.replace(":", "."))}')
        # Ожидание окончания работы процесса
        await proc.communicate()

        self.driver.quit()



