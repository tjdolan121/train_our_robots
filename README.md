# Train our Robots <hr>

![TrainOurRobots](app/static/Screenshot.png?raw=true "TrainOurRobots")

#### CONTEXT: This is a follow-up application to <i>Sentiment CLI</i>. <br> <i>Train our Robots</i> is my attempt at integrating a ML algorithm into a web app. <hr>

#### HOW IT WORKS: Robots need a tool to help them understand the sentiment of human language.  Train Our Robots does just that!<br><br>  Robots can enter a sentence they heard from a human and get an instant sentiment analysis!  Human users can help improve the model in real time by first adding sentences to the database, then by clicking "Train the model"! <hr>

#### HOW  TO CONTRIBUTE:

###### Contributions are always welcome!  I am new to Flask, so help is needed!

STEP 1: Clone the project (in the terminal): ```git clone https://github.com/tjdolan121/train_our_robots.git```

STEP 2: Create a new virtual environment: ```virtualenv venv```

STEP 3: Activate the virtual environment: ```source venv/bin/activate```

STEP 4: Navigate to the project directory, then install requirements: ```pip install -r requirements.txt```

STEP 5: Set up flask environment variables: (macOS)<br>```export FLASK_APP=sentiment_app.py```<br>```export FLASK_ENV=development```

STEP 6: Instantiate a database and run migrations: ```flask db upgrade```

STEP 7: Seed the database with starter data for the ML model: ```python setup.py```

STEP 8: Run server: ```flask run```

STEP 10: Navigate to http://127.0.0.1:5000 in browser, create an account, and play around! 

#### Commits to master are automatically pushed to the staging app, found here: https://intense-depths-98176.herokuapp.com/

### Feel free to message me if you have any questions!

To get up and running with Flask, I followed this amazing tutorial:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

The sentiment data came from here:
https://archive.ics.uci.edu/ml/datasets/Sentiment+Labelled+Sentences

