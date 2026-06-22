import re

from bs4 import BeautifulSoup

from census.original_docs.OriginalDocScrapeConstantsMixin import \
    OriginalDocScrapeConstantsMixin
from utils_future import WWW, Log

log = Log("OriginalDocScrapeMixin")


class OriginalDocScrapeMixin(OriginalDocScrapeConstantsMixin):

    @classmethod
    def parse_iframe(cls, i_frame, label):
        if i_frame:
            src = i_frame.get("src")
            if src and src.endswith(".pdf"):
                url_pdf = (
                    src if src.startswith("http") else cls.URL_BASE + src
                )
                original_doc = cls(name=label, url=url_pdf)
                original_doc.build()
                return original_doc
        return None

    @classmethod
    def clean_label(cls, label):
        label = label.strip()
        label = label.replace("\n", " ")
        label = re.sub(r"\s+", " ", label)
        return label

    @classmethod
    def get_valid_url_infos(cls, soup, visited_urls):
        url_info_queue = []
        for a in soup.find_all("a", href=True):
            label_a = cls.clean_label(a.text)
            url_a = a["href"].strip()
            if not url_a.startswith("http"):
                url_a = cls.URL_BASE + url_a

            if (cls.is_valid_url(url_a)) and url_a not in visited_urls:
                log.debug(f"\tQueued {url_a}")
                url_info_queue.append((url_a, label_a))
        return url_info_queue

    @classmethod
    def scrape_remote_url(
        cls,
        label,
        url,
        visited_urls,
    ):
        www = WWW(url)
        html = www.read_html()
        soup = BeautifulSoup(html, "html.parser")

        i_frame = soup.find("iframe")
        original_doc = cls.parse_iframe(i_frame, label)
        new_url_infos = cls.get_valid_url_infos(soup, visited_urls)

        return (
            visited_urls,
            original_doc,
            new_url_infos,
        )

    @classmethod
    def scrape_remote(cls, max_docs, max_urls):

        url_info_queue = cls.INITIAL_URL_INFO_QUEUE
        visited_urls = set()
        original_docs = []
        while url_info_queue:
            url, label = url_info_queue.pop(0)
            if url in visited_urls:
                continue
            visited_urls.add(url)

            (
                visited_urls,
                original_doc,
                new_url_infos,
            ) = cls.scrape_remote_url(
                label,
                url,
                visited_urls,
            )

            if original_doc:
                original_docs.append(original_doc)
                i_original_doc = len(original_docs)
                log.info(f"Found {i_original_doc}) {original_doc}")
                log.debug("-" * 20)

            url_info_queue.extend(new_url_infos)

            if len(original_docs) >= max_docs:
                log.warning(
                    f"🛑 max_docs={max_docs} reached, stopping scrape"
                )
                break
            if len(visited_urls) > max_urls:
                log.warning(
                    f"🛑 max_urls={max_urls} reached, stopping scrape"
                )
                break
