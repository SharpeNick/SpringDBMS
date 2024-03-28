# SpringDBMS
This is a healthcare app that was created for our DBMS class. 
Note: This uses flask framework and python. You will need both of those for this project. In order to use this it's a good idea to go over to https://flask.palletsprojects.com/en/3.0.x/installation/

P.S. You must create a .venv folder in your project folder for this to work. Without it you will get errors. To do this use:
1. Open up a terminal and navigate to the location of the project files
2. Run the follwing command to create a virtual environment: py -3 -m venv .venv
3. Activate the new environment with this command: .venv\Scripts\activate
4. Install the following dependancies using these commands:
- pip install Flask
- pip install sqlalchemy
5. Launch the application using: flask --app Hello run --debug
6. Navigate to the homepage using this url: http://127.0.0.1:5000/


*This code was taken from Flask's website.
**All of the code above is important for the project to work!

### Main Project
Run this command to boot up the server: flask --app Hello run --debug
This starts the developer in debug mode so that when you refresh the page you can see the changes you made.

### Testing Database Connections
For this project, we also created a simple script to test/debug database connections. In order to use this feature, follow these stesps:
1. Use test.sql to load the testing schema into the database to be tested
2. open test.py and modify the username, password, server, and dbname variable to match the database
3. launch the test application using the command: flask --app test run --debug
4. If all the above code worked, you should be able to see your code here: http://127.0.0.1:5000/
5. Fill in the two text fields with anything and click submit. You'll be redirected to a new webpage that will display all the users stored in the database
