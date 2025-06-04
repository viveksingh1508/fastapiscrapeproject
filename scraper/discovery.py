from tasks import insert_jobs


def run_scraper():
    """
    Run the scraper task to insert jobs into the database.
    """
    # Call the insert_jobs function to start the scraping process
    # insert_jobs.delay()


if __name__ == "__main__":
    run_scraper()
