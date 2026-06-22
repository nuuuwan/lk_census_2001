from census import OriginalDoc


def main():
    OriginalDoc.scrape_remote(max_docs=100, max_urls=200)
    OriginalDoc.validate_status()
    OriginalDoc.build_global_readme()


if __name__ == "__main__":
    main()
