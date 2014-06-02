'use strict';

/* jasmine specs for controllers go here */

describe('controllers', function () {
    beforeEach(module('myApp.controllers'));
    beforeEach(module('ngCookies'));
    beforeEach(module('ngRoute'));
    beforeEach(function(){
        this.addMatchers({
            toEqualData: function(expected) {
                return angular.equals(this.actual, expected);
            }
        });
    });

    var manager_credential={username: 'manager.xie', password: 'secret'};
    var manager_login_resp_data={emp_no:1234, first_name: 'victor', departments_currently_managing:[{dept_no:'d001'}]};
    var employee_credential={username: 'employee.xie', password: 'secret'};
    var employee_login_resp_data={emp_no:1235, first_name: 'victor', departments_currently_managing:[]};


    describe('LoginCtrl', function(){
        var scope, ctrl, $httpBackend;
        var wrong_credential={username: 'victor.ixe', password: '111111'};
        var wrong_credetional_login_resp_data={message:"Invalid username and password combination"};

        beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
            $httpBackend = _$httpBackend_;

            scope = $rootScope.$new();
            ctrl = $controller('LoginCtrl', {$scope: scope});
        }));


        it('should set error message when credential is wrong', function() {
            $httpBackend.expectPOST('/auth/login', wrong_credential).
                respond(412, wrong_credetional_login_resp_data);

            expect(scope.message).toBeUndefined();
            scope.username = wrong_credential.username;
            scope.password = wrong_credential.password;
            scope.login();
            $httpBackend.flush();
            expect(scope.message).toEqual(wrong_credetional_login_resp_data.message);
        });

        it('should set the user data in cookie and redirect to / when the login succeed', function() {
            $httpBackend.expectPOST('/auth/login', manager_credential).
                respond(manager_login_resp_data);

            expect(scope.logged_in).toBe(false);
            expect(scope.message).toBeUndefined();
            scope.username = manager_credential.username;
            scope.password = manager_credential.password;
            scope.login();
            $httpBackend.flush();
            expect(scope.message).toBeUndefined();
            expect(scope.logged_in).toBe(true);
            expect(scope.get_current_user()).toEqualData(manager_login_resp_data);

        });

    });

    describe('HomepageCtrl', function(){
        var scope, $httpBackend, $location, $cookieStore, $controller, ctrl;

        beforeEach(inject(function($rootScope, _$controller_, _$location_, _$cookieStore_) {
            $location = _$location_;
            $cookieStore = _$cookieStore_;
            $controller = _$controller_;
            scope = $rootScope.$new();

        }));

        describe('When user not logged in', function(){
            it('it should redirect browser to login page', function() {
                $cookieStore.remove("current_user");
                ctrl = $controller('HomepageCtrl', {$scope: scope});
                expect($location.path()).toEqual("/login")
            });

        });

        describe('When manager logged in', function(){
            it('it should redirect browser to dept info page', function() {
                $cookieStore.put("current_user", manager_login_resp_data);
                ctrl = $controller('HomepageCtrl', {$scope: scope});
                expect($location.path()).toEqual("/departments/d001")
            });

        });

        describe('When employee logged in', function(){
            it('it should redirect browser to employee info page', function() {
                $cookieStore.put("current_user", employee_login_resp_data);
                ctrl = $controller('HomepageCtrl', {$scope: scope});
                expect($location.path()).toEqual("/employees/1235")
            });

        })




    });


    describe('DepartmentInfoCtrl', function(){
        var scope, $httpBackend, $location, $cookieStore, $controller, ctrl, $routeParams;
        var first_page_data = {employees:[
            {empo_no:123},
            {empo_no:124}
        ]};

        beforeEach(inject(function($rootScope, _$controller_, _$location_, _$cookieStore_, _$httpBackend_, _$routeParams_) {
            $location = _$location_;
            $cookieStore = _$cookieStore_;
            $controller = _$controller_;
            $httpBackend = _$httpBackend_;
            $routeParams = _$routeParams_;
            scope = $rootScope.$new();
            $cookieStore.put("current_user", manager_login_resp_data);
        }));


        it("should load the first page of employees info", function(){
            var title_options = ["Staff", "Senior Staff"];
            $routeParams.dept_no = "d001";
            $httpBackend.expectGET(/\/api\/departments\/d001\/employees*/)
                .respond(first_page_data);
            $httpBackend.whenGET("/api/titles")
                .respond({titles: title_options});
            ctrl = $controller('DepartmentInfoCtrl', {$scope: scope});
            $httpBackend.flush();
            expect(scope.title_enum).toEqualData(title_options);
            expect(scope.data).toEqualData(first_page_data);
        });



    });

});
