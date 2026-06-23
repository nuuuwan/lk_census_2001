import os
import tempfile
import time

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils_base import File, Hash, Log

log = Log("WWW")


class WWW:
    T_TIMEOUT = 120
    MIN_TEXT_FILE_SIZE = 100
    T_SELENIUM_WAIT = 20

    def __init__(
        self,
        url: str,
    ):
        self.url = url

    def __str__(self) -> str:
        return f"🌐{self.url}"

    @property
    def ext(self) -> str:
        return os.path.splitext(self.url)[1].lower().strip(".")

    @property
    def url_md5(self) -> str:
        return Hash.md5(self.url)

    @property
    def temp_path_prefix(self):
        dir_www = os.path.join(tempfile.gettempdir(), "lk_census_2001", "www")
        os.makedirs(dir_www, exist_ok=True)
        return os.path.join(dir_www, f"www.{self.url_md5}")

    def _fetch_html_with_selenium(self) -> str:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        try:
            driver.get(self.url)
            time.sleep(WWW.T_SELENIUM_WAIT)
            return driver.page_source
        finally:
            driver.quit()

    def read_html(self):
        temp_text_file = File(self.temp_path_prefix + ".html")
        if temp_text_file.exists:
            return temp_text_file.read()

        log.debug(f"Fetching {self}")
        html = self._fetch_html_with_selenium()
        temp_text_file.write(html)
        if temp_text_file.size < WWW.MIN_TEXT_FILE_SIZE:
            raise ValueError(f"Content too short for {self}")
        log.debug(f"Wrote {self} to {temp_text_file}")
        return html

    def download_binary(self, dest_path):
        response = requests.get(self.url, stream=True, timeout=WWW.T_TIMEOUT)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        log.debug(f"Wrote {self} to {File(dest_path)}")
