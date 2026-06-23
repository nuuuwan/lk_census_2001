import re

from bs4 import BeautifulSoup

from utils_future import WWW, Log

log = Log("OriginalDocScrapeMixin")


class OriginalDocScrapeMixin:
    URL_BASE = (
        "https://www.statistics.gov.lk" + "/Population/StaticalInformation/"
    )

    INDEX_URLS = [
        "https://www.statistics.gov.lk" + "/Population/PopHouStat_Population",
        "https://www.statistics.gov.lk" + "/Population/PopHouStat_Housing",
        "https://www.statistics.gov.lk" + "/Population/PopHouStat_Disability",
    ]

    @staticmethod
    def is_valid_url(url: str) -> bool:
        for prefix in [
            "https://www.statistics.gov.lk"
            + "/Population/StaticalInformation/CPH2001/",
            "https://www.statistics.gov.lk" + "/Population/p",
            "https://www.statistics.gov.lk" + "/Population/Housing/p",
            "https://www.statistics.gov.lk" + "/Population/Disability/p",
        ]:
            if url.startswith(prefix):
                return True
        return False

    @classmethod
    def clean_label(cls, label):
        label = label.strip()
        label = label.replace("\n", " ")
        label = re.sub(r"\s+", " ", label)
        return label

    @classmethod
    def get_link_urls(cls, url):
        www = WWW(url)
        html = www.read_html()
        soup = BeautifulSoup(html, "html.parser")

        url_info_queue = []
        for a in soup.find_all("a", href=True):
            label_a = cls.clean_label(a.text)
            url_a = a["href"].strip()
            if not url_a.startswith("http"):
                url_a = cls.URL_BASE + url_a

            if cls.is_valid_url(url_a):
                url_info_queue.append((url_a, label_a))
        log.debug(f"Found {len(url_info_queue)} valid links in {url=}")
        return url_info_queue

    @classmethod
    def get_url_pdf(cls, url: str) -> str:
        www = WWW(url)
        html = www.read_html()
        soup = BeautifulSoup(html, "html.parser")
        i_frame = soup.find("iframe")
        if i_frame:
            src = i_frame.get("src", "").strip()
            if src.endswith(".pdf"):
                url_pdf = (
                    src if src.startswith("http") else cls.URL_BASE + src
                )
                return url_pdf
            else:
                raise ValueError("Iframe src is not a PDF")
        else:
            raise ValueError("No iframe found in the page")

    @classmethod
    def scrape_remote(cls):
        docs = []
        for index_url in cls.INDEX_URLS:
            url_info_queue = cls.get_link_urls(index_url)
            for url, label in url_info_queue:
                url_pdf = cls.get_url_pdf(url)
                doc = cls(name=label, url=url_pdf)
                doc.build()
                docs.append(doc)
                i_doc = len(docs)
                log.info(f"{i_doc:02d}. Built {doc}")
                log.debug("-" * 40)

        log.debug(f"Scraped {len(docs)} documents from remote sources")
        return docs
