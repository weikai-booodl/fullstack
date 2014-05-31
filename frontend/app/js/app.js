'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
  'myApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login', {templateUrl: 'partials/login.html', controller: 'LoginCtrl'});
  $routeProvider.when('/list', {templateUrl: 'partials/employee_list.html', controller: 'ListCtrl'});
  $routeProvider.when('/detail', {templateUrl: 'partials/employee_list.html', controller: 'DetailCtrl'});
  $routeProvider.otherwise({redirectTo: '/login'});
}]);
