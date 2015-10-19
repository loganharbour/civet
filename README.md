# civet
Continuous Integration, Verification, Enhancement, and Testing

Moose Build written in Django.

### Installation

See civet/settings.py for required settings. Namely, setting the client_id/secret (if required) for the server to allow
Civet to generate access tokens for users.

Setup the database:

    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py createsupseruser

For public moosebuild.org:

    ./manage.py loaddata public.json

For internal:

    ./manage.py loaddata internal.json
