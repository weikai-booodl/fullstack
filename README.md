#A sample web app to view mysql employee sample db 


##Overview
* The web site is implemented as a single-page app, wich use restful API to retrieve data from backend
* Frontend is based on Angular.js. The project skeleton is created out from the official angular-seed template
* Backend is based on Flask, SqlAlchemy (for ORM) and Flask-restful (for restful API framework)

##Implementation notes

###Frontend

* The app contains four views and corresponding controllers

  * Homepage view and its controller
    * Implemented in frontend/partials/homepage.html and frontend/js/controllers.js/HomepageCtrl
    * It's actually only used to redirect the browser to the correct landing page depending on whether the user is logged
    in and whether they are managers
    
  * Login view and its controller
    * In frontend/partials/login.html and frontend/js/controllers.js/LoginCtrl
    * When user logged in, the user profile is stored in a session-life-span cookie called "current_user"
      * the cookie is cleared when user log out or closed browser
        
  * Department info view  and its controller
    * In frontend/partials/department_info.html and frontend/js/controllers.js/DepartmentInfoCtrl
    * It's the landing page for managers
    * It shows a list of the employees in this department
    * Filtering and pagination is supported.
    * Deep linking is supported
  
  * Employee info view and its controller
    * In frontend/partials/employee_info.html and frontend/js/controllers.js/EmployeeInfoCtrl
    * List employee detail
    
* About years_to_now filter
  * In frontend/js/filters.js
  * It is used to display years-in-company and age in the employee_info page
  
* About authRequiredRedirector service
  * This service is hooked in the $http service such that whenever backend return 412 (unauthenticated) error, the browser
  will be redirected to the login page
  * You may wonder why not use the standard 401 code. The reason is that most browsers will bring-up its own login dialog 
   when it see such http response and there is no way to disable this behavior. So a different code 412 is used.
   

###Backend 

* DB-access layer and model definition is in backend/app/db

* The application is divided into 2 flask blue print
  * auth_blueprint which sits on /auth url path
    It is based on flask-login and handles authentication related logic of the backend
    
  * api_blueprint which sits on /api url path
    It is based on flask-restful and provides a JSON based restful API to frontend
    
* About static file serving
  * In development env
     The backend/app/static is just a soft-link to frontend/app and flask's built-in static file serving mechnaism is used
     to serve these files
     
  * In production env
     You should setup nginx to serve the static files. 
    
##Live demo
http://54.79.50.177:5000/

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
* or just simpley eidt the fullstack/backend/app/config/settings.py
* you should at least change the SQLALCHEMY_DATABASE_URI file to use the account/password of your mysqldb
* cd fullstack/backend
* python run.py -d
* Open http://localhost:5000 in your browser


##Test

##Backend unit test
```
cd backend
python test/unit_test.py
```

###Frontend unit tets
```
cd frontend
npm test
```
###End-to-end test
```
cd frontend
npm run update-webdriver
npm run protractor
```
Notice, due to time limit, there is only one very basic e2e test case at the moment

##Things to improve if I have more time
* Create more test cases for better code coverage
* Implement frontend build process with Browserify and Grunt
* Add caching layer in API view handlers
* If need to deploy to production,
  * use Nginx+Uwsgi to serve the site
  * enable https
  * create Docker or SaltStack script to automate the provisioning and deployment process 
