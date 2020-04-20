# configman
Flask application to handle the configurations and passwords for different app

### Creating Credentials
```
python ./create_update_cred.py
python ./create_update_cred.py [-h] [-a APPLICATION] [-u USERNAME] [-o [OVERWRITE]]
```
Regardless of selection, you will be prompted for password

This user is saved in the yaml file for the application given.  The username is saved as string and the password is encrypted in the file. These files should be in the directory listed in the app_config.yaml file.

**Note: Creating credentials is only possible via the script**

### Validating Credentials
Validation occurs as part of the flask application's tokenization process:

*Get the token
```
curl --location --request POST 'http://127.0.0.1:5000/auth/token/generate' \
--header ': ' \
--header 'Content-Type: application/json' \
--data-raw '{
	"user": "testman",
	"password": "testman",
	"app": "test_application"
}'
```

*Validate the token
```
curl --location --request POST 'http://127.0.0.1:5000/auth/token/validate' \
--header ': ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user": "testman",
    "token": "<token>"
}'
```
