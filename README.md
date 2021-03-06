# Flask Application Boilerplate

This starter code was created to get you quickly started developing your flask application without losing time setting up the structure of the application.
This boilerplate includes the following libraries:
- Bootstrap 4.3.1 (css)
- Fontawesome 5.7.2 (CDN)
- Popper 1.12.9
- Bootstrap 4.3.1 (js)
- jQuery 3.3.1


### Boilerplate structure
The application follows the below structure:

```
root_directory/
  manage.py
  requirements.txt
  set_production.sh

  application/
    __init__.py
    config.py
    decorators.py
    models.py
    util.py

    main/
      __init__.py
      views.py

    static/
      css/
        custom.css
        lib/
          bootstrap-4.3.1.min.css
      js/
        app.js
        lib/
          boostrap-4.3.1.min.js
          jquery-3.3.1.min.js

    templates
      base.html
      errors/
        404.html
        500.html
      main/
        home.html
      partials/
        flash.html
        libraries.html
        root.html

  log/
    error.log (file not present, it gets created automatically)

  tests/
    __init__.py
    test_config.py
    test_main.py
    test_user.py
```

## Get started... quickly

Once you have cloned the repository, created your virtual environment, you can proceed installing all the required dependencies with the following command:
```sh
$ sudo pip install -r requirements.txt
```

Before running the server you need to set the environment variable.
```sh
$ export APP_SETTINGS="application.config.DevelopmentConfig"
```

or (for testing)

```sh
$ export APP_SETTINGS="application.config.TestingConfig"
```

This environment variable will tell the application which configuration should be used.

To run the server enter the following command:
```sh
$ python3 manage.py runserver
```

The above command will start the flask server with the configuration set in the `APP_SETTINGS` variable (don't use this command for production)


## manage.py commands
The `manage.py` file uses flask's 'Manager' class to bind the application and then adding commands with the `manager.command` decorator.

The available commands are:

```sh
# Run tests without coverage
$ python3 manage.py test  
```
```sh
# Create the database tables
$ python3 manage.py create_db
```
```sh
# Drop the database tables
$ python3 manage.py drop_db
```
```sh
# Create the admin testing user with following properties
# email = test_admin@domain.com
# password = Admin1234
# admin = True
$ python3 manage.py create_admin
```
```sh
# Create the non-admin testing user with following properties:
# email = test_nonadmin@domain.com
# password = Admin1234
# admin = False
$ python3 manage.py create_user
```
```sh
# Delete the testing users (admin and non admin)
$ python3 manage.py delete_test_users
```
```sh
# Reset the user password. The email should be provided to the command
$ python3 manage.py reset_user_password email@domain.com
```
```sh
# Delete a specific user. Email address of the user to be deleted should be provided.
$ python3 manage.py delete_user email@domain.com
```

## The model
The basic database setup (table and columns) is included in the file called `models.py` inside the `application` folder.
The objec-relational mapper used in this boilerplate is SQLAlchemy.

The SQLAlchemy class is bound to the application instance `app` in a variable called `db`.

Therefore to use the SQLAlchemy wrapper in any file of the application you simply need to add the following import:
```python
from application import db
```

The model that comes included in the boilerplate is the `User` model. The table is called `user` and has the following columns:
```python
id (primary key)
email # (50 chars)
password # (64 chars hashed with flask_bcrypt)
registered_on # Datetime = default now
admin # Boolean - default False
```

The `User` model also includes the serialize method called `serialize_user` that returns the following object:
```python
{
  'id': self.id,
  'email': self.email
}
```

## Production configuration
For production environment there is a shell file that will create the required folders and files and change the permits on those folder in order for the logger to write. This configuration file was created assuming the application will be running on an Apache Server.
To run the shell commands, type the following (assuming you are in the root folder of this boilerplate):
```sh
$ sudo bash set_production.sh
```

The above command will perform the below actions:
```sh
export APP_SETTINGS='application.config.ProductionConfig'


mkdir application/instance
touch application/instance/production.cfg
mkdir log
touch log/error.log
chgrp www-data log
chgrp www-data log/error.log
chmod 700 log
chmod 664 log/error.log
```

For production environment it is not recommended to have environment variable, therefore instead of using the `APP_SETTINGS` variable, it is better to change the `__init__.py` inside the `application` directory. We should comment the line that reads the configuration from the environment variable and hard code it to be the production one. The file should look like the one below. We simply need to comment one line (the first one in the below snippet) and uncomment another one (the third one in the below snippet)

```python
# app.config.from_object(os.environ['APP_SETTINGS'])
# For production
app.config.from_object("application.config.ProductionConfig")
```

Other than the log directory and error log file, the shell script will also create the `instance` directory and the `production.cfg` file. In this last file you will need to add the production keys. Open the file and add the below:
```cfg
[keys]
SECRET_KEY=your_super_secret_key
SECURITY_PASSWORD_SALT=your_password_salt
SQLALCHEMY_DATABASE_URI=postgresql://username:password@host:port/database
```

The application will automatically override the default settings with the values in the configuration file.
