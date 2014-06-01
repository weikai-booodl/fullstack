'use strict';

/* Filters */

angular.module('myApp.filters', [])
    .filter('years_to_now', function () {
        return function (date_str) {
            var then = (new Date(date_str)).getTime();
            var now = (new Date()).getTime()
            return Math.ceil((now - then)/365/24/3600/1000).toString()
        };
    });
;
