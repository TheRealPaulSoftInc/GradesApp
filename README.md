# GradesApp

## About this project

This is a demo api that provides the functionality of registering academic grades and some calculations.
This solution pretends to solve a problem: ignorance of academic status.
This demo is deployed on heroku but its api is not available for its integration with any client application because of its CORS settings:

- API: https://gradesappapi.herokuapp.com/api/
- Swagger docs: https://gradesappapi.herokuapp.com/swagger/

Also, this demo has a frontend integration. Check it out! 

- Deployed demo: https://gradesapp-web.herokuapp.com/
- Repository: https://github.com/TheRealPaulSoftInc/GradesAppFrontend/

### Features

This demo provides all this features:

- Custom user model
- Custom user authentication (JWT Tokens)
- Custom user authorization (Django Permissions and Custom Django Rest Permissions classes)
- Custom email verification
- Custom authentication backend
- Documentation with OpenAPI (with swagger drf-yasg)
- Unit testings (with Coverage.py)
- CI/CD with docker and github actions
- Mssql database integration
- Filtering, Ordering, Searching and Paging on requests

### API Documentation

In order to use the swagger docs, you must follow this steps:

- Go to the API Documentation provided with swagger: https://gradesappapi.herokuapp.com/swagger/
- Register on [(POST) /accounts/register/] with a real email.
- Go to the link that was send to your email and it will activate the account.
- Login on [(POST) /accounts/login/] with your credentials
- The previous step will provide a token. Copy the token and authorize your access into swagger by clicking the "Authorize" green button on the upper right section of the interface and insert the token with this format:

```bash
Bearer (Token)
```

- You are now authenticated on the swagger interface and you have the authorization of using most of the api endpoints. Some are reserved for staff only.


## Install dependencies

```bash
pip install -r ./requirements.txt
```

## Run tests coverage

```bash
coverage run manage.py test && coverage report && coverage html
```

## Configure .env file

In order to run locally, you must create a .env file on the root folder and set these configurations:

```bash
SECRET_KEY=A$$S0M3-$3CR3T-K3Y # set this to whatever random string
DEBUG=1 # set this to 1 for development configuration. 0 for production.
ALLOWED_HOSTS=localhost 127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost http://127.0.0.1

# You must set a email and enable "Less secure app access" on that account
# if its an gmail account: https://support.google.com/accounts/answer/6010255#zippy=
PAULSOFT_EMAIL_USER=email@email.com
PAULSOFT_EMAIL_PASSWORD=password
EMAIL_VERIFICATION_URL=http://localhost:3000/activate/

# Set the configuration of your local mssql DB
DB_LOCAL_NAME=gradesappdb
DB_LOCAL_USER=sa # set your own credentials
DB_LOCAL_PASSWORD=password # set your own credentials
DB_LOCAL_HOST=localhost
DB_LOCAL_PORT=
```

## Docker

```bash
docker build . -t gradesapp
docker run -p 8000:8000 gradesapp
```
