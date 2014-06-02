'use strict';

/* jasmine specs for controllers go here */

describe('controllers', function () {
    beforeEach(module('myApp.controllers'));
    beforeEach(module('ngCookies'));
    beforeEach(function(){
        this.addMatchers({
            toEqualData: function(expected) {
                return angular.equals(this.actual, expected);
            }
        });
    });

    describe('LoginCtrl', function(){
        var scope, ctrl, $httpBackend;
        var manager_credential={username: 'manager.xie', password: 'secret'};
        var manager_login_resp_data={emp_no:1234, first_name: 'victor', departments_currently_managing:[{dept_no:'d001'}]}
        var manager_credential={username: 'employee.xie', password: 'secret'};
        var manager_login_resp_data={emp_no:1235, first_name: 'victor', departments_currently_managing:[]};
        var wrong_credential={username: 'victor.ixe', password: '111111'};
        var wrong_credetional_login_resp_data={message:"Invalid username and password combination"};

        beforeEach(inject(function(_$httpBackend_, $rootScope, $controller, _$location_) {
            $httpBackend = _$httpBackend_;

            scope = $rootScope.$new();
            ctrl = $controller('LoginCtrl', {$scope: scope});  //don't need to
        }));


        it('set error message when credential is wrong', function() {
            $httpBackend.expectPOST('/auth/login', wrong_credential).
                respond(412, wrong_credetional_login_resp_data);

            expect(scope.message).toBeUndefined();
            scope.username = wrong_credential.username;
            scope.password = wrong_credential.password;
            scope.login();
            $httpBackend.flush();
            expect(scope.message).toEqual(wrong_credetional_login_resp_data.message);
        });

        it('should set the user data in cookie and redirect to /', function() {
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


//    it('should ....', inject(function ($controller) {
//        //spec body
//        var myCtrl1 = $controller('MyCtrl1', { $scope: {} });
//        expect(myCtrl1).toBeDefined();
//    }));
//
//    it('should ....', inject(function ($controller) {
//        //spec body
//        var myCtrl2 = $controller('MyCtrl2', { $scope: {} });
//        expect(myCtrl2).toBeDefined();
//    }));
});
