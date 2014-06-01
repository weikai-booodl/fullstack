#A sample web app to view mysql employee sample db 


##Overview
* The web site is implemented as a single-page app, wich use restful API to retrieve data from backend
* Frontend is based on Angular.js. The project skeleton is created out from the official angular-seed template
* Backend is based on Flask, SqlAlchemy (for ORM) and Flask-restful (for restful API framework)


##How to setup
###Prerequisites
* The following instructions suppose Ubuntu OS is used
* Mysql with the employee sample db loaded
* node/npm 

###Install 

```
sudo apt-get install libmysqlclient-dev python-dev

git clone https://github.com/xwk/fullstack.git fullstack
cd fullstack

virtualenv fullstack
source fullstack/bin/activate

cd backend
pip install -r requirements.txt

cd ../frontend
npm install
```

###Run
* create a config file, use fullstack/backend/app/config/settings.py as sample, then set FULLSTACK_CONFIG_FILE_PATH environment variable to this config file
** or just simpley eidt the fullstack/backend/app/config/settings.py
** you should at least change the SQLALCHEMY_DATABASE_URI file to use the account/password of your mysqldb
* cd fullstack/backend
* python run.py
* Open http://localhost:5000 in your browser


##Test

##Backend unittest
```
cd backend
python test/unit_test.py
```

##Things to improve if I have more time
* Create test cases for frontend UT and functional test with Karma and Protractor
* Implement frontend build process with Browserify and Grunt
* Add caching layer in API view handlers
* If need to deploy to production,
** use Nginx+Uwsgi to serve the site
** enable https
** make Dockerfile to automate the provisoning and deployment process 
