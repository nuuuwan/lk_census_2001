import os

from census import OriginalDoc


def main():
    OriginalDoc.scrape_remote()
    OriginalDoc.validate_status()
    OriginalDoc.build_global_readme()
    os.system('say "Pipeline Done"')

    docs = OriginalDoc.list()
    for doc in docs[:5]:
        os.system(f"open -a firefox {doc.pdf_file_path}")


if __name__ == "__main__":
    main()
