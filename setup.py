"""Script to be run to initialize an empty db with seed data."""


from app import db
from app.models import User, Submission


seed_datafiles = ["./ml_backend/raw_data/amazon_cells_labelled.txt",
                  "./ml_backend/raw_data/imdb_labelled.txt",
                  "./ml_backend/raw_data/yelp_labelled.txt", ]


def db_seed():
    """"Converts sentiment data from text files (original form) to app database.

        Usage: To be run when connecting to a empty database for the first time.

        Returns: 3000 instances of 'seed' sentiment data for ML model"""
    # Aggregate .txt files
    data = []
    for file in seed_datafiles:
        with open(file, "r") as fin:
            data += fin.read().split('\n')
    # Data cleanup
    data = [line.split('\t') for line in data if len(line.split('\t')) == 2 and line.split("\t")[1] != '']
    # Format data into list of tuples ('sentence', 'is_good')
    sentence = [item[0] for item in data]
    is_good = [int(item[1]) for item in data]
    submissions = zip(sentence, is_good)
    # Add dummy user
    u = User(username='ADMIN', email='admin@admin.com')
    db.session.add(u)
    # Push to database
    for submission in submissions:
        s = Submission(sentence=submission[0], is_good=submission[1], author=u)
        db.session.add(s)
    db.session.commit()


if __name__ == "__main__":
    db_seed()
