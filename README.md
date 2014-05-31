#Full stack sample


##Overview
* The web site is implemented as a single-page app, wich use restful API to retrieve data from backend
* Frontend is based on Angular.js. The project skeleton is created out from the official angular-seed template
* Backend is based on Flask, SqlAlchemy (for ORM) and Flask-restful (for restful API framework)


##How to setup
The following instructions suppose Ubuntu OS is used
```
git clone the repos 
cd frontend
npm install
cd ../backend
wget https://launchpad.net/test-db/employees-db-1/1.0.6/+download/employees_db-full-1.0.6.tar.bz2
tar jxvf employees_db-full-1.0.6.tar.bz2 
cd employees_db
mysql -u root --password=fullstack < employees.sql
```


###How to run test

##Frontend unittest
```
cd frontend
npm test
```

##Backend unittest
```
cd backend
python test/unit_test.py
```

##
