# Library Service API

Welcome to the online management system for book borrowings.


## Features

### Books Service

- **CRUD Functionality**: Create, Read, Update, and Delete operations for managing books.
- **Permissions**: Admin users can create, update, and delete books. All users can view the list of books.
- **JWT Token Authentication**: Secure authentication using JWT tokens.

### Users Service

- **CRUD Functionality**: Manage user accounts with Create, Read, Update, and Delete operations.
- **JWT Support**: Secure user authentication with JWT tokens.

### Borrowings Service

- **Create Borrowing**: Users can borrow books with validation for book availability.
- **Filtering**: Users can filter their borrowings. Admins can view all borrowings.
- **Return Borrowing**: Users can return borrowed books, updating the inventory.
- **Notifications**: Receive notifications for borrowing actions via Telegram.
- **Telegram Integration**: Notifications sent to a Telegram chat using a bot.

### ModHeader Integration

- **Chrome Extension Compatibility**: Custom Authorization header for JWT authentication to enhance user experience with the ModHeader Chrome extension.

## API Documentation

- **Spectacular Integration**: Comprehensive API documentation.
- **Swagger UI**: Interactive API documentation available at `/api/doc/swagger/`.
- **Redoc UI**: Clean and readable API documentation at `/api/doc/redoc/`.
- **Schema Endpoint**: API schema available at `/api/schema/`.

### Prerequisites

- Ensure Docker is installed on your machine. You can download it from the official Docker website.

### Building the Docker Image

1. Create a `Dockerfile` in the root directory of your project with the following content:

    ```Dockerfile
    # Use an official Python runtime as a parent image
    FROM python:3.9-alpine

    # Set the maintainer label
    LABEL maintainer="jyjuk1@gmail.com"

    # Set environment variable
    ENV PYTHONUNBUFFERED=1

    # Set the working directory in the container
    WORKDIR /app

    # Copy the requirements file into the container
    COPY requirements.txt /app/requirements.txt

    # Install the dependencies
    RUN pip install --no-cache-dir -r /app/requirements.txt

    # Copy the project files into the container
    COPY . /app

    # Run migrations and start the server
    CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
    ```

2. Create a `.dockerignore` file to specify which files and directories to ignore when building the Docker image:

    ```plaintext
    __pycache__
    *.pyc
    .git
    .vscode
    ```

3. Build the Docker image:

    ```sh
    docker build -t libraryservice .
    ```

### Running the Docker Container

1. Run the Docker container:

    ```sh
    docker run -p 8000:8000 libraryservice
    ```

2. Access the application at `http://localhost:8000/api/books/`.

## Test Coverage Report

| File                                | Statements | Missing | Excluded | Coverage |
|-------------------------------------|------------|---------|----------|----------|
| books\__init__.py                   | 0          | 0       | 0        | 100%     |
| books\admin.py                      | 3          | 0       | 0        | 100%     |
| books\apps.py                       | 4          | 0       | 0        | 100%     |
| books\migrations\__init__.py        | 0          | 0       | 0        | 100%     |
| books\migrations\0001_initial.py    | 5          | 0       | 0        | 100%     |
| books\models.py                     | 15         | 0       | 0        | 100%     |
| books\permissions.py                | 4          | 0       | 0        | 100%     |
| books\serializers.py                | 6          | 0       | 0        | 100%     |
| books\tests.py                      | 72         | 0       | 0        | 100%     |
| books\urls.py                       | 6          | 0       | 0        | 100%     |
| books\views.py                      | 8          | 0       | 0        | 100%     |
| borrowings\__init__.py              | 0          | 0       | 0        | 100%     |
| borrowings\admin.py                 | 13         | 2       | 0        | 85%      |
| borrowings\apps.py                  | 4          | 0       | 0        | 100%     |
| borrowings\migrations\__init__.py   | 0          | 0       | 0        | 100%     |
| borrowings\migrations\0001_initial.py | 9        | 0       | 0        | 100%     |
| borrowings\models.py                | 26         | 2       | 0        | 92%      |
| borrowings\serializers.py           | 46         | 8       | 0        | 83%      |
| borrowings\telegram_api.py          | 18         | 3       | 0        | 83%      |
| borrowings\tests.py                 | 126        | 1       | 0        | 99%      |
| borrowings\urls.py                  | 6          | 0       | 0        | 100%     |
| borrowings\views.py                 | 51         | 1       | 0        | 98%      |
| library_service\__init__.py         | 0          | 0       | 0        | 100%     |
| library_service\settings.py         | 23         | 0       | 0        | 100%     |
| library_service\urls.py             | 4          | 0       | 0        | 100%     |
| manage.py                           | 11         | 2       | 0        | 82%      |
| user\__init__.py                    | 0          | 0       | 0        | 100%     |
| user\admin.py                       | 11         | 0       | 0        | 100%     |
| user\apps.py                        | 4          | 0       | 0        | 100%     |
| user\migrations\__init__.py         | 0          | 0       | 0        | 100%     |
| user\migrations\0001_initial.py     | 7          | 0       | 0        | 100%     |
| user\models.py                      | 36         | 8       | 0        | 78%      |
| user\serializers.py                 | 17         | 7       | 0        | 59%      |
| user\urls.py                        | 5          | 0       | 0        | 100%     |
| user\views.py                       | 14         | 1       | 0        | 93%      |
| **Total**                           | **554**    | **35**  | **0**    | **94%**  |




## Usage

1. Clone the repository.
2. Set up environment variables using `.sample.env` as a guide.
3. Run the application.
4. Feel free to explore and contribute!

## Installation

Python3 must be already installed.

```bash
git clone https://github.com/jyjuk/library-service.git
cd Library-Service-API

python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

set DJANGO_SECRET_KEY=<your django secret key>
set DJANGO_ALLOWED_HOSTS=<your allowed hosts>
set DJANGO_DEBUG=<your debug value>

set TELEGRAM_BOT_TOKEN=<your telegram secret key>
set TELEGRAM_CHAT_ID=<your telegram chat id>

python manage.py migrate
python manage.py runserver
```
Getting Access
Create a user via /api/user/register.
Get access token via /api/user/token.