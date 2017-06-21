# MetaStone and PhenoPointer


## Setup and installation of MetaStone and PhenoPointer
### CLI
Most relevant steps needed for setting up MetaStone can be performed via the CLI, that can accessed via `manage.py`. It should be mentioned, that the given python3 interpreter in the header of this file should be changed to the path, as created in the following step of creating a virtual environment. Alternatively, the CLI can be accessed by prefixing the call with `python3` after activating the virtual environment.
```
$ source /PATH/TO/DESIRED/VIRTUALENV/bin/activate
$ python3 manage.py
```

### Required Python3 libraries and virtual env
A python3 virtual environment (venv) should be setup, to install the required release version of python3 libraries and keep these apart from other system-wide libraries to avoid versioning conflicts.
This can be achived by executing `$ python3 -m venv /PATH/TO/DESIRED/VIRTUALENV` and afterwards activating the venv through `$ source /PATH/TO/DESIRED/VIRTUALENV/bin/activate`

Required libraries, as listed below, can be installed utilizing pip.
```
$ pip install scikit_learn==0.18.1
```
- psycopg2 – 2.7.\*
- scikit_learn – 0.18.1 
- ipython – 5.\*
- scipy – 0.19.0
- numpy – 1.12.\*
- Django – 1.9.4-1.9.\* 
- pandas – 0.19.\*
- biom-format – 2.1.\*


### Basic database setup
Create a basic database (postgresql 9.5 tested) and assign a database user as the owner. All ETL steps are executed via this specific user.
In addition to that, the [hstore](https://www.postgresql.org/docs/9.5/static/sql-createextension.html) extension must be installed in postgresql and assigned to the created database.

Go to `Metagenomes/setting.py` and fill the appropiate fields (see [django1.9 - DB](https://docs.djangoproject.com/en/1.9/ref/databases/) for details related to the database backend system):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # DATABASE DEPENDENT BACKEND SYSTEM
        'NAME': 'MetaStone', # YOUR DATABASE NAME
        'USER': 'img', # USER NAME
        'PASSWORD': 'imgimgimg', # PASSWORD
        'HOST': 'localhost',
        'PORT': '5433',
    }
}
```

A directory has to be specified, where the uploaded files is stored. This is set as `MEDIA_ROOT` in the same `settings.py` file.

The database is now ready to be initialized via the django CLI, so go to the root directory and run the following two commands:
```sh
$ ./manage.py makemigrations
$ ./manage.py migrate
```

The database is now filled automatically with required tables and sequences upon these.

For administration purposes, a superuser has to be created via the CLI. The login created is needed for loading genomic data and metadata into MetaStone, that can be performed after starting the development web server. The server can be stopped by pressing <CTRL+c>.
```sh
$ ./manage.py createsuperuser
$ ./manage.py runserver
```

In is worth to be mentioned, that while editing `settings.py`, the `SECRETKEY` should be changed. The key affects the securty mechanisms in a django application and should be changed in your local installation. A helpful online tool is [this](http://www.miniwebtool.com/django-secret-key-generator/) one.

### Filling the database with genomic data and metadata
The directory `DATA` contains normalized data extracted from IMG ready for loading into MetaStone, that can be used for training new ML classification models within PP or for metadata-enrichment of community profiles.
- **Pfam-A.clans.tsv** - General information about protein domains (Pfam v.29)
- **archaea_Mar16.xls** - Archaeal related metadata as of March 2016 (exported from IMG)
- **archaea_Apr17.xls** - New archaeal related metadata as of April 2017 (exported from IMG)
- **bacteria_Mar16.xls** - Bacterial related metadata as of March 2016 (exported from IMG)
- **bacteria_Apr17.xls** - New bacterial related metadata as of April 2017 (exported from IMG)
- **pfams_archaea_Mar16.tsv.gz** - Pfam abundances profiles of March 2016 archaeal genomes
- **pfams_archaea_Apr17.tsv.gz** - Pfam abundances profiles of new April 2017 archaeal genomes
- **pfams_bacteria_Mar16.tsv.gz** - Pfam abundances profiles of March 2016 bacterial genomes
- **pfams_bacteria_Apr17.tsv.gz** - Pfam abundances profiles of new April 2017 bacterial genomes

#### Loading data files into MetaStone
To access the admin site, the developmental web server needs to be started as stated in the previos section. The URL is shown in the output of the CLI and needs to be suffixed with `admin` e.g., `127.0.0.1:8000/admin/` gives access to the admin site.

After logging in as a superuser, the data files have to be uploaded to MetaStone by adding new **Admin file uploads**. Each archaeal and bacterial (meta)data file from IMG has to be uploaded a several times as: **Genome**, **Genome_Lineage**, and **Genome_Metadata**. The reason for this is, that input data can be split into separate files containing only the relevant entries for each organism. In this case, a single file for each time point of extracted data from IMG for archaea and bacteria has been created, containing all relevant fields.

Afterwards, the **Pfam-A.clans.tsv** has to be uploaded as **Pfam**, followed by the Pfam abundance profiles as **Pfam2Genome**.

To fill the database with the uploaded data, the CLI has to be called to open an interactive shell. Within this, the ETL procedure can be finally initiated.
```python
$ ./manage.py shell
[1] from MetaStone.Procedures.Helper import MaintenanceToolkit
[2] MaintenanceToolkit.process_all_imports()
...
...
...
[3] exit
```

## Setup of PhenoPointer
###