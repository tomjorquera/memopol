Local development tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~

This tutorial drives through a local installation of the project for
development on Linux. It requires git, a fairly recent version of python2,
virtualenv and PostgreSQL.

Setup the database
==================

Memopol requires PostgreSQL 9.1 or higher.  It used to run with SQLite, too, but
that is no longer the case. It is better to install and configure you're local
PostgreSQL server before starting to install Memopol.

On Debian
---------

To setup you're PostgreSQL database on a debian stable distribution, you can use
the package manager apt::

  $ apt install postgresql postgresql-server-dev-9.X

Then you need to create the 'memopol'  user and the 'memopol' database::

  # To have a root access on Postgres, you need to connect as user 'postgres'
  $ su - postgres
  $ psql -c "create user memopol with password 'memopol';"
  $ psql -c "alter role memopol with createdb;"
  $ psql -c "create database memopol with owner memopol;"
  $ exit

You're database is now setup for Memopol. You can now launch the 'quickstart.sh'
script to automatically install all the components or do it manually.

In General
----------

Make sure the corresponding user and database exist on your system; the user
will need the 'createdb' permission in order to be able to run tests.  To create
them, you may use the following commands::

    $ psql -c "create user memopol with password 'memopol';" -U postgres
    $ psql -c "alter role memopol with createdb;" -U postgres
    $ psql -c "create database memopol with owner memopol;" -U postgres


Automatic Install
=================

There is a quickstart script used and tested manually by some of the
developers. Feel free to try it, but don't worry if it doesn't work for you
then you can do each install step manually, which is recommended because well
that's how you will learn most.

Here's how to try it::

    $ git clone gitlab@git.laquadrature.net:memopol/memopol.git
    $ cd memopol
    $ source bin/quickstart.sh

At this point, you should now run the development server and access to Memopol::

  $ memopol runserver

If you want more control or if it doesn't work for you, then follow the steps
below or have a look at what the quickstart script does.

Development helper
===================

You can run the script 'bin/dev.sh' to automaticaly setup some aliases. It works
only with Bash and Zsh.

The script build a custom file named '.memopol.alias' at the root of the project
containing all the aliases for memopol. All the path to the project are build
automatically. A single line is added to your '$HOME/.bashrc' or '$HOME/.zshrc'
to source the aliases.

After execute 'bin/dev.sh' you should close the current terminal and open
another one to have access to the aliases.

There is a quick list of available aliases::

  memopol-code : Go into the repository and activate virtualenv and
  set Django in debug mode
  memopol-launch : Run the development server echo
  memopol-update-all : Get all the production data
  memopol-refresh-scores : Refresh all scores

.. warning:: If you are using multiple setup of Memopol, it is not recommended to
  use this script.

If you need to change the location of the project, you should remove this line
from your .bashrc or .zshrc::

  source $PATH_TO_THE_PROJECT/.memopol.alias

Make a virtual environment
==========================

For the sake of the tutorial, we'll do this in the temporary directory, but you
could do it anywhere::

    $ cd /tmp

Create a python virtual environment and activate it::

    $ virtualenv memopol_env
    Using real prefix '/usr'
    New python executable in memopol_env/bin/python2
    Also creating executable in memopol_env/bin/python
    Installing setuptools, pip, wheel...done.

    $ source memopol_env/bin/activate

Alternatively, use the tox command::

    $ tox -e py27
    $ source .tox/py27/bin/activate

Clone the repository
====================

The project is hosted on https://git.laquadrature.net/memopol/memopol

You can get the code with git ::

    $ git clone https://git.laquadrature.net/memopol/memopol
    Clonage dans 'memopol'...
    remote: Counting objects: 7972, done.
    remote: Compressing objects: 100% (2668/2668), done.
    remote: Total 7972 (delta 5203), reused 7830 (delta 5099)
    Réception d'objets: 100% (7972/7972), 4.88 MiB | 4.73 MiB/s, fait.
    Résolution des deltas: 100% (5203/5203), fait.
    Vérification de la connectivité... fait.

    $ cd memopol/

Create your own branch, ie::

    $ git checkout -b yourbranch
    Branch yourbranch set up to track remote branch pr from origin.
    Switched to a new branch 'yourbranch'

Install Python dependencies
===========================

Then, install the package for development::

    $ pip install -e .
    Obtaining file:///tmp/memopol
    Collecting django (from memopol==0.0.1)
      Using cached Django-1.9-py2.py3-none-any.whl

    [output snipped for readability]

    Installing collected packages: django, sqlparse, django-debug-toolbar, django-pdb, six, django-extensions, werkzeug, south, pygments, markdown, hamlpy, django-coffeescript, ijson, python-dateutil, pytz, memopol
      Running setup.py develop for memopol
    Successfully installed django-1.9 django-coffeescript-0.7.2 django-debug-toolbar-1.4 django-extensions-1.5.9 django-pdb-0.4.2 hamlpy-0.82.2 ijson-2.2 markdown-2.6.5 memopol pygments-2.0.2 python-dateutil-2.4.2 pytz-2015.7 six-1.10.0 south-1.0.2 sqlparse-0.1.18 werkzeug-0.11.2

Install client dependencies
===========================

We'll also need to download client libraries::

    $ src/memopol/bin/install_client_deps.sh
    * Downloading jquery/jquery (2.1.4) from Github...
    * Downloading FortAwesome/Font-Awesome (v4.3.0) from Github...
    * Downloading lipis/flag-icon-css (0.7.1) from Github...
    * Downloading twbs/bootstrap (v3.3.5) from Github...
    * Done

Activate ``DJANGO_DEBUG``
=========================

``DEBUG`` is disabled by default, the development server
won't run properly by default then, to enable it export
the ``DJANGO_DEBUG`` variable in the current shell::

    $ export DJANGO_DEBUG=True


Database migrations
===================

Database migrations ensure the database schema is up to date with the project.
If you're not sure, you can run them anyway, they won't do any harm.  Use the
following command::

    $ memopol migrate
    Operations to perform:
      Synchronize unmigrated apps: django_filters, staticfiles, datetimewidget, autocomplete_light, messages, adminplus, compressor, humanize, django_extensions, constance, bootstrap3
      Apply all migrations: legislature, votes, database, admin, positions, sessions, representatives, auth, contenttypes, representatives_votes, taggit
    Synchronizing apps without migrations:
      Creating tables...
        Running deferred SQL...
      Installing custom SQL...
    Running migrations:
      Rendering model states... DONE
      Applying contenttypes.0001_initial... OK

    [output snipped for readability]

      Applying taggit.0002_auto_20150616_2121... OK

Provision with data
===================

You can load a small data sample for quick setup:

    $ memopol loaddata small_sample.json

If you launch memopol for the first time, you need to launch this command :

    $ memopol refresh_scores

Or actual data (takes a while)::

    $ bin/update_all

Run the development server
==========================

Run the development server::

    $ memopol runserver

    Performing system checks...

    System check identified no issues (0 silenced).
    December 09, 2015 - 21:26:47
    Django version 1.8.7, using settings 'memopol.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    [09/Dec/2015 21:26:48] "GET / HTTP/1.1" 200 13294

The website is running on ``http://127.0.0.1:8000/``.

Continue to :doc:`administration`.
