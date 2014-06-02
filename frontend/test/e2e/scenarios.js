'use strict';


describe('Fullstack app', function () {

    describe('landing page', function(){
        it('hit homepage should automatically be redirected to /#/login when not logged in', function () {
            browser.get('/');
            browser.getLocationAbsUrl().then(function (url) {
                expect(url.split('#')[1]).toBe('/login');
            });

        });
    });


    describe('login page', function () {

        it('should redirect to departement_info view when a manager logs in', function () {
            browser.get('/#/login');
            element(by.model('username')).sendKeys("Vishwani.Minakawa");
            element(by.model('password')).sendKeys("110039");
            element(by.css('#login_btn')).click();
            browser.getLocationAbsUrl().then(function (url) {
                expect(url.split('#')[1]).toBe('/departments/d001');
            });
        });


        it('should redirect to employee_info view when a non-manager logs in', function () {
            browser.get('/#/login');
            element(by.model('username')).sendKeys("Georgi.Facello");
            element(by.model('password')).sendKeys("10001");
            element(by.css('#login_btn')).click();
            browser.getLocationAbsUrl().then(function (url) {
                expect(url.split('#')[1]).toBe('/employees/10001');
            });


        });

    });


});
