import os

from census import OriginalDoc


def main():
    OriginalDoc.scrape_remote()
    OriginalDoc.validate_status()
    OriginalDoc.build_global_readme()
    os.system('say "Pipeline Done"')


if __name__ == "__main__":
    main()
