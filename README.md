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
