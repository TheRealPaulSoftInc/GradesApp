# GradesApp

## Install dependencies

```bash
pip install -r ./requirements.txt
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
