'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', [])
    .value('version', '0.1')
    .factory('authRequiredRedirector', ["$q", "$location", function($q, $location){
        return {
            'responseError': function(rejection) {
                if (rejection.status==412) {
                    $location.path("/login").search({});
                }
                return $q.reject(rejection);
            }
        };
    }]);

