# Digraph Visualizator

Application to visualize digraphs based on Django an JointJS.

-----------------------

### STEPS TO RUN THE PROJECT

Clone the repo
 
    git clone git@github.com:add00/Digraph-Visualizator.git

Install required pip packages but first (optional but recommended) create and then activate virtualenv using

    virtualenv digraph_env
    source digraph_env/bin/activate
 
or (if you use virtualenvwrapper)

    mkvirtualenv digraph_env
    workon digraph_env

and now you can feel free to run (in root directory)

    pip install -r requirements.pip

Now create database running initial migrations and creating superuser using one command

    ./manage.py syncdb

or two separated ones

    ./manage.py migrate
    ./manage.py createsuperuser

Now you're able to run local server with (for instance)

    ./manage.py runserver 0:8000

and application will be available in your browser under

    http://localhost:8000/

### HOW TO USE

Usage of Digraph Visualizator is pretty simple. To manage digraphs follow instructions in tooltips below each button (hover).
