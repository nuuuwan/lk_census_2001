from census import OriginalDoc


def main():
    OriginalDoc.scrape_remote(max_docs=50, max_urls=50)
    OriginalDoc.validate_status()


if __name__ == "__main__":
    main()
