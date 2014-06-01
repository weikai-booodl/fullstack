'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
    'ngRoute',
    'ngCookies',
    'myApp.filters',
    'myApp.services',
    'myApp.directives',
    'myApp.controllers'
    ])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/', {templateUrl: 'partials/homepage.html', controller: 'HomepageCtrl'});
        $routeProvider.when('/login', {templateUrl: 'partials/login.html', controller: 'LoginCtrl'});
        $routeProvider.when('/employees/:emp_no', {templateUrl: 'partials/employee_info.html', controller: 'EmployeeInfoCtrl'});
        $routeProvider.when('/departments/:dept_no', {templateUrl: 'partials/department_info.html', controller: 'DepartmentInfoCtrl'});
        $routeProvider.otherwise({redirectTo: "/"});
    }])
    .config(['$httpProvider', function($httpProvider){
        $httpProvider.interceptors.push("authRequiredRedirector");
    }]);


