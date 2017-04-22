from setuptools import setup, find_packages

setup(name='political-memory',
    version='0.0.1',
    description='Political Memory Project Memopol',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    author='James Pic, Laurent Peuch, Arnaud Fabre, Nicolas Joyard',
    author_email='cortex@worlddomination.be',
    url='http://github.com/political-memory/political_memory/',
    install_requires=[
        'django-autocomplete-light==3.2.0',
        'django-autoslug>=1.9,<1.10',
        'django-bootstrap3>=6,<7',
        'django-coffeescript>=0.7,<0.8',
        'django-compressor>=1,<2',
        'django-datetime-widget>=0.9,<1.0',
        'django-filter>=0.15,<0.16',
        'django-fontawesome>=0.2,<0.3',
        'django-rql-filter>=0.1.3,<0.2',
        'django-taggit>=0.17,<0.18',
        'django>=1.8,<1.9',
        'djangorestframework>=3,<3.5.1',
        'hamlpy>=0.82,<0.83',
        'ijson>=2.2,<2.3',
        'python-dateutil>=2.4,<2.5',
        'unicodecsv>=0.14,<0.15',
        'pytz',  # Always use up-to-date TZ data
        'django-suit>=0.2,<0.3',
        'psycopg2>=2,<3',
        'django-haystack==2.6.0',
        'pysolr==3.6.0'
    ],
    extras_require={
        # Full version hardcode for testing dependencies so that
        # tests don't break on master without any obvious reason.
        'testing': [
            'codecov>=2,<3',
            'flake8>=2,<3',
            'django-responsediff>=0.7,<0.8',
            'pep8>=1,<2',
            'pytest>=2,<3',
            'pytest-django>=2,<3',
            'pytest-cov>=2,<3',
            'mock==2.0.0',
            'tox>=2.3,<3',
        ]
    },
    entry_points={
        'console_scripts': [
            'parltrack_import_representatives = representatives.contrib.parltrack.import_representatives:main',  # noqa
            'parltrack_import_dossiers = representatives_votes.contrib.parltrack.import_dossiers:main',  # noqa
            'parltrack_import_votes = representatives_votes.contrib.parltrack.import_votes:main',  # noqa
            'francedata_import_representatives = representatives.contrib.francedata.import_representatives:main',  # noqa
            'francedata_import_dossiers = representatives_votes.contrib.francedata.import_dossiers:main',  # noqa
            'francedata_import_scrutins = representatives_votes.contrib.francedata.import_scrutins:main',  # noqa
            'francedata_import_votes = representatives_votes.contrib.francedata.import_votes:main',  # noqa
            'memopol_import_positions = representatives_positions.contrib.import_positions:main',  # noqa
            'memopol_import_recommendations = representatives_recommendations.contrib.import_recommendations:main',  # noqa
            'memopol = memopol.manage:main',
        ]
    }
)
