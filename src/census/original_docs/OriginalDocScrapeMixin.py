import re

from bs4 import BeautifulSoup

from utils_future import WWW, Log

log = Log("OriginalDocScrapeMixin")


class OriginalDocScrapeMixin:
    URL_BASE = (
        "https://www.statistics.gov.lk" + "/Population/StaticalInformation/"
    )

    INITIAL_URL_INFO_QUEUE = [
        (
            "https://www.statistics.gov.lk"
            + "/Population/PopHouStat_Population",
            "cph2001_population",
        ),
        (
            "https://www.statistics.gov.lk" + "/Population/PopHouStat_Housing",
            "cph2001_housing",
        ),
        (
            "https://www.statistics.gov.lk"
            + "/Population/PopHouStat_Disability",
            "cph2001_disability",
        ),
    ]

    @staticmethod
    def is_valid_url(url: str) -> bool:
        for prefix in [
            "https://www.statistics.gov.lk"
            + "/Population/StaticalInformation/CPH2001/",
            "https://www.statistics.gov.lk"
            + "/Population/PopHouStat_Population",
            "https://www.statistics.gov.lk" + "/Population",
        ]:
            if url.startswith(prefix):
                return True
        return False

    @classmethod
    def parse_iframe(cls, i_frame, label):
        if i_frame:
            src = i_frame.get("src")
            if src and src.endswith(".pdf"):
                url_pdf = src if src.startswith("http") else cls.URL_BASE + src
                original_doc = cls(name=label, url=url_pdf)
                original_doc.download_pdf()
                return original_doc
        return None

    @classmethod
    def clean_label(cls, label):
        label = label.strip()
        label = label.replace("\n", " ")
        label = re.sub(r"\s+", " ", label)
        return label

    @classmethod
    def scrape_remote_url(
        cls,
        label,
        url,
        url_info_queue,
        visited_urls,
        original_docs,
        i_original_doc,
    ):
        www = WWW(url)
        html = www.read_html()
        soup = BeautifulSoup(html, "html.parser")

        i_frame = soup.find("iframe")
        original_doc = cls.parse_iframe(i_frame, label)
        if original_doc:
            i_original_doc += 1
            original_docs.append(original_doc)
            log.info(f"Found {i_original_doc}) {original_doc}")
            log.debug("-" * 20)

        for a in soup.find_all("a", href=True):
            label_a = cls.clean_label(a.text)
            url_a = a["href"].strip()
            if not url_a.startswith("http"):
                url_a = cls.URL_BASE + url_a

            if (cls.is_valid_url(url_a)) and url_a not in visited_urls:
                log.debug(f"\tQueued {url_a}")
                url_info_queue.append((url_a, label_a))

        return i_original_doc, original_docs, url_info_queue, visited_urls

    @classmethod
    def scrape_remote(cls, max_docs, max_urls):

        url_info_queue = cls.INITIAL_URL_INFO_QUEUE
        visited_urls = set()
        original_docs = []
        i_original_doc = 0
        while url_info_queue:
            url, label = url_info_queue.pop(0)
            if url in visited_urls:
                continue
            visited_urls.add(url)
            if len(visited_urls) > max_urls:
                log.warning(f"🛑 max_urls={max_urls} reached, stopping scrape")
                break

            i_original_doc, original_docs, url_info_queue, visited_urls = (
                cls.scrape_remote_url(
                    label,
                    url,
                    url_info_queue,
                    visited_urls,
                    original_docs,
                    i_original_doc,
                )
            )

            if i_original_doc >= max_docs:
                log.warning(f"🛑 max_docs={max_docs} reached, stopping scrape")
                break

        cls.write_metadata(original_docs)
        return original_docs
