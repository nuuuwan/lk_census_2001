import os

from census import OriginalDoc
from utils_future import Log

log = Log("pipeline")


def main():
    try:
        OriginalDoc.scrape_remote()
        OriginalDoc.validate_status()
        OriginalDoc.build_global_readme()
    except Exception as e:
        log.error(f"Error occurred: {e}")
        os.system('say "Error"')
    finally:
        os.system('say "Pipeline Done"')


if __name__ == "__main__":
    main()
