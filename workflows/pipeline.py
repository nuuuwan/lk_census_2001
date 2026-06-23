import os

from census import OriginalDoc


def main():
    # OriginalDoc.scrape_remote()
    # OriginalDoc.validate_status()
    # OriginalDoc.build_global_readme()

    docs = OriginalDoc.list()
    for doc in docs[40:]:
        os.system(f"open -a firefox {doc.pdf_file_path}")

    os.system('say "Pipeline Done"')


if __name__ == "__main__":
    main()
