var mainApp = angular.module("mainApp",['ui.bootstrap.pagination', 'ngAnimate','ngRoute']);

// configure the routing of the app
mainApp.config(function ($routeProvider) {       
    $routeProvider.when('/bookings', {
        templateUrl: 'views/bookings.html',
        controller: 'BookingsController'
    }).when('/buildings', {
        templateUrl: 'views/buildings.html',
    }).when('/Contact us', {
        templateUrl: 'views/contactUS.html',
    }).otherwise({
        redirectTo: "/"
    });
});
