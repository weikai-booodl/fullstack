'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
    .run(['$rootScope', '$cookieStore', '$http', '$location', function ($rootScope, $cookieStore, $http, $location) {
        $rootScope.get_current_user = function () {
            return $cookieStore.get('current_user');
        };

        $rootScope.logged_in = $rootScope.get_current_user() ? true : false;

        $rootScope.logout = function () {
            $http.post('/auth/logout')
                .success(function (data, status, headers, config) {
                    $cookieStore.remove('current_user');
                    $rootScope.logged_in = false;
                    $location.path("/login").search({});
                });
        };

    }])
    .controller('LoginCtrl', ['$scope', '$http', '$location', '$cookieStore', '$rootScope',
        function ($scope, $http, $location, $cookieStore, $rootScope) {

            $scope.login = function () {
                $cookieStore.remove('current_user');

                $http
                    .post('/auth/login', {
                        username: $scope.username,
                        password: $scope.password
                    })
                    .success(function (data, status, headers, config) {
                        $cookieStore.put('current_user', data);
                        $rootScope.logged_in = true;
                        $location.path("/").search({});
                    })
                    .error(function (data, status, headers, config) {
                        $scope.message = data.message;
                    })
            };


        }])

    .controller('DepartmentInfoCtrl', ['$scope', '$routeParams', '$http', '$location', '$timeout',
        function ($scope, $routeParams, $http, $location, $timeout) {
            var args = $location.search();
            var offset = args.offset || 0;
            var limit = args.limit || 20;

            $scope.filters = JSON.parse(args.filters || "{}");

            var base_url = '/api/departments/' + $routeParams.dept_no + '/employees?';
            if (args.filters) {
                base_url += ("filters=" + args.filters)
            }

            var paginated_url = base_url + "&offset=" + offset + "&limit=" + limit;

            $http.get(paginated_url)
                .success(function (data, status, headers, config) {
                    $scope.data = data
                });

            $scope.to_page = function (dst_page_info) {
                $location.path($location.path()).search({
                    offset: dst_page_info.offset,
                    limit: dst_page_info.limit,
                    filters: JSON.stringify($scope.filters)})
            };

            $scope.reload = function () {
                $location.path($location.path()).search({
                    offset: 0,
                    limit: 20,
                    filters: JSON.stringify($scope.filters)});
            };

            $scope.reset_search_crtiera = function(){
                $scope.filters = {};
                $scope.reload();
            };

            var auto_search_timer = false;
            var delay = 1000;
            $scope.delayed_reload = function () {
                if (auto_search_timer) {
                    $timeout.cancel(auto_search_timer)
                }
                auto_search_timer = $timeout(function () {
                    $scope.reload();
                }, delay);
            };

            $http.get("/api/titles")
                .success(function (data, status, headers, config) {
                    $scope.titles = data.titles;
                });
        }])

    .controller('EmployeeInfoCtrl', ['$scope', '$routeParams', '$http', function ($scope, $routeParams, $http) {
        $http.get('/api/employees/' + $routeParams.emp_no)
            .success(function (data, status, headers, config) {
                $scope.employee = data
            });
    }])

    .controller('HomepageCtrl', ['$scope', '$location',
        function ($scope, $location) {
            var current_user = $scope.get_current_user();
            var redirect_to_path;
            if (current_user) {
                if (current_user.departments_currently_managing.length > 0) {
                    redirect_to_path = '/departments/' + current_user.departments_currently_managing[0].dept_no;
                } else {
                    redirect_to_path = '/employees/' + current_user.emp_no;
                }
            } else {
                redirect_to_path = "/login";
            }
            $location.path(redirect_to_path).search({}).replace()
        }]);

//      if (current_user == null){
//          return '/login';
//      }else if (current_user.departments_currently_managing.length > 0){
//          return ;
//      }else{
//          return
//      }
