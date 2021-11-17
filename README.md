# Full Stack API Project
This project allows users to play a trivia game and test their general knowledge. In this project I created an API and unit test cases for the application that allows the following:


1. Display questions - both all questions and by category. Shows question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

When a user plays the game they play up to five questions of the chosen category. If there are fewer than five questions in a category, the game will end when there are no more questions in that category. 


## Backend
All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

### Installing Python3 and Dependencies

The backend uses [Python v3.10](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
All required packages are included in the requirements file. From the `backend` folder run `pip install -r requirements.txt`.

- Key Dependencies:
  - [Flask](https://flask.palletsprojects.com)
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
  - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)
  - [Flask-Testing](https://pythonhosted.org/Flask-Testing/)
  - [Flask-Expects-Json](https://pypi.org/project/flask-expects-json/)
  - [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)

### Database Setup
1. The backend based on the [PostgreSQL](https://www.postgresql.org) DBMS. You need to set up a database with the following command: `createdb trivia`. You may want to change the database name and path in the `backend/config.py` file. 
2. After setting up the database run `flask db upgrade` command. It will create all the database tables and populate them with some examples seed data. 

### Running the Server
Start the backend application with the following commands: 
 ```shell
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
   ``` 
These commands put the application in development mode and directs the application to use the `__init__.py` file in  `backend/flaskr` folder. If running locally on Windows, look for the commands in the [Flask documentation](https://flask.palletsprojects.com/en/1.0.x/tutorial/factory/).

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.


## Frontend
### Installing Node.js and NPM

This project depends on Nodejs and Node Package Manager (NPM). Download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository.

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```shell
npm start
```

## Tests
1. In order to run tests you need to create a separate database. You can use the following command to create one: `createdb trivia_test`. You can change the database name and path in the `backend/test_flaskr.py` file.
2. After that you can use the `python test_flaskr.py` or `python3 test_flaskr.py` commands to execute the test cases. The `test_flaskr.py` file uses the same migration method and seed data as the `flaskr` application.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API reference
### Getting started
**Base URL:** At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000, which is set as a proxy in the frontend configuration.

**Authentication:** This version of the application does not require authentication or API keys.

### Error handling
Errors are returned as JSON objects in the following format:
```json
{
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:

- [400](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400): Bad Request
- [404](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404): Resource Not Found
- [405](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405): Method Not Allowed
- [422](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422): Not Processable

### Endpoints
#### GET `/api/v1.0/categories`

- **Description:**
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request arguments: None
  - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
- **Example request:** `curl http://127.0.0.1:5000/api/v1.0/categories`
- **Example response:**
    ```json
    {
        "categories": {
            "1": "History",
            "2": "Entertainment",
            "3": "Sports",
            "4": "Geography",
            "5": "Art",
            "6": "Science"
        }
    }
    ```
#### GET `/api/v1.0/questions?page={integer}`
- **Description:**
  - Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
  - Request Arguments: page - integer
  - Returns: An object with 10 paginated questions, total questions, object including all categories. The current category string is not used
- **Example request:** `curl http://127.0.0.1:5000/api/v1.0/questions?page=1`
- **Example response:**
    ```json
    {
    "categories": {
        "1": "History", 
        "2": "Entertainment", 
        "3": "Sports", 
        "4": "Geography", 
        "5": "Art", 
        "6": "Science"
    }, 
    "currentCategory": null, 
    "questions": [
        {
        "answer": "Maya Angelou", 
        "category": 1, 
        "difficulty": 2, 
        "id": 1, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
        "answer": "Muhammad Ali", 
        "category": 1, 
        "difficulty": 1, 
        "id": 2, 
        "question": "What boxer's original name is Cassius Clay?"
        }, 
        {
        "answer": "Apollo 13", 
        "category": 2, 
        "difficulty": 4, 
        "id": 3, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ], 
    "totalQuestions": 3
    }
    ```

#### GET `/api/v1.0/categories/{id}/questions`
- **Description:**
  - Fetch questions for a category specified by id request argument 
  - Request Arguments: id - integer
  - Returns: An object with questions for the specified category, total questions, and current category string 
- **Example request:** `curl http://127.0.0.1:5000/api/v1.0/categories/1/questions`
- **Example response:**
    ```json
    {
    "currentCategory": "History", 
    "questions": [
        {
        "answer": "Maya Angelou", 
        "category": 1, 
        "difficulty": 2, 
        "id": 1, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
        "answer": "Muhammad Ali", 
        "category": 1, 
        "difficulty": 1, 
        "id": 2, 
        "question": "What boxer's original name is Cassius Clay?"
        }
    ], 
    "totalQuestions": 2
    }
    ```

#### DELETE `/api/v1.0/questions/{id}`
- **Description:**
  - Deletes a specified question using the id of the question
  - Request Arguments: id - integer
  - Returns: Does not return anything
- **Example request:** `curl -X DELETE http://127.0.0.1:5000/api/v1.0/questions/{id}`

#### POST `/api/v1.0/questions`
- **Description:**
  - Sends a post request in order to add a new question
  - Request Body:
    ```json
    {
        "question":  "Here's a new question string",
        "answer": "Here's a new answer string",
        "difficulty": 1,
        "category": 3
    }
    ```
  - Returns: Does not return any new data
- **Example request:** `curl -X POST http://127.0.0.1:5000/api/v1.0/questions -H "Content-Type: application/json" -d "{\"question\": \"What is my name?\", \"answer\": \"Anonymous\", \"difficulty\": 5, \"category\": 1}"`

#### POST `/api/v1.0/questions`
- **Description:**
  - Sends a post request in order to search for a specific question by search term 
  - Request Body: 
    ```json
    {
        "searchTerm": "this is the term the user is looking for"
    }
    ```
  - Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
- **Example request:** `curl -X POST http://127.0.0.1:5000/api/v1.0/questions -H "Content-Type: application/json" -d "{\"searchTerm\": \"which\"}"`

#### POST `/api/v1.0/quizzes` 
- **Description:**
    - Sends a post request in order to get the next question 
    - Request Body:
    ```json
    {
        "previous_questions":  [1, 4, 20, 15],
        "quiz_category": "History" 
    }
    ```
    - Returns: a single new question object
- **Example request:** `curl http://127.0.0.1:5000/api/v1.0/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\": [1, 2, 3], \"quiz_category\": {\"type\": \"Science\", \"id\": 1}}"`
- **Example response**:
    ```json
    {
        "question": {
                "id": 1,
                "question": "This is a question",
                "answer": "This is an answer", 
                "difficulty": 5,
                "category": 4
        }
    }
    ```
