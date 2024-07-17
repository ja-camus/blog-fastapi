# Camus-Python Project

This project is a FastAPI application. Below are the steps to set up and run the project.

## Clone Project

First, clone the repository to your local machine.

```
git clone git@github.com:ja-camus/blog-fastapi.git
```

## Create Virtual Environment for FastAPI
Create a virtual environment to manage dependencies for the project.

```
python3 -m venv env
```

## Activate Virtual Environment
Activate the virtual environment.

```
source env/bin/activate
```

# Install Dependencies
## Poetry
Poetry is a tool for dependency management and packaging in Python. It should always be installed in a dedicated virtual environment.

Install Poetry using pip.

```
pip3 install poetry
```

Initialize Poetry in the project directory.

```
poetry init
```

This will create a pyproject.toml file which is used to manage the project's dependencies and settings.


## Add Dependencies
Add the necessary dependencies for the project using Poetry.

```
poetry add fastapi uvicorn sqlalchemy psycopg2-binary pydantic poetry-plugin-dotenv pytest httpx flake8 black
```

# Run the Application
To start the application on localhost, activate the virtual environment and run the following command.

```
source env/bin/activate

uvicorn app.main:app --reload
```

This will start the FastAPI application with auto-reload enabled, which is useful for development.

# Run Tests
To run the tests, use the following command:

```
poetry update
```
```
pytest
```
This will execute all the tests in the project.

# Additional Information

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Uvicorn**: A lightning-fast ASGI server implementation, using uvloop and httptools.
- **SQLAlchemy**: The Python SQL toolkit and Object-Relational Mapping (ORM) library.
- **Alembic**: Database migration tool for SQLAlchemy, enabling schema changes in Python applications.
- **Poetry**: A tool for dependency management and packaging.
- **Psycopg2-binary**: A PostgreSQL database adapter for Python.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **python-dotenv**: Reads key-value pairs from a .env file and can set them as environment variables.
- **pytest**: A framework that makes building simple and scalable test cases easy.
- **httpx**: A fully featured HTTP client for Python, which provides sync and async APIs.

# CI/CD:

- **GitHub Actions**: Automates CI/CD workflows directly in GitHub, running tests, builds, and deployments on push or pull requests.
- **Flake8**: Linting tool that checks Python code against PEP 8, detects errors and complexity.
- **Black**: Automatic code formatter for Python, ensuring uniform style.
- **Coveralls**: Analyzes test coverage, showing untested code areas with detailed reports.

# Security

This project implements several security measures to ensure the safety and integrity of user data:

- **Password Hashing**: User passwords are securely hashed using strong hashing algorithms before being stored in the database.
- **JWT Authentication**: JSON Web Tokens (JWT) are used for secure user authentication and session management.
- **Permissions Management**: The application includes a permissions system to restrict access to resources based on user roles.

# Database Tables

The project uses a relational database to manage data. Below are the key tables used in the application:

- **users**: Stores user information, including username, hashed password, and other relevant details.
- **roles**: Manages user roles and permissions, defining what actions each role can perform within the application.
- **publications**
- **comments**


Feel free to reach out if you have any questions or need further assistance!
