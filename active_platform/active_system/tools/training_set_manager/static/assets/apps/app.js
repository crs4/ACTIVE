define([
    "angular",
    "angular-couch-potato",
    "angular-resource",
    "angular-cookies",
    "angular-ui-router",
    "appConfig"
], function (ng, couchPotato) {
	
	"use strict";

    var app = ng.module("app", [
        "scs.couch-potato",
        "ngResource",
        "ngCookies",
        "ui.router",
        "app.layout",
        "app.core",
        //"app.errors"
    ]);

    couchPotato.configureApp(app);

    app.config(function ($provide, $httpProvider, $resourceProvider, $locationProvider) {

        $provide.factory("ErrorHttpInterceptor", function ($q, $location) {
			
            var errorCounter = 0;
            
            function notifyError(rejection){
                switch (rejection.status) {
					case 401: $location.path("/error/four-o-one"); break;
					case 403: $location.path("/error/four-o-three"); break; 
					//case 404: $location.path("/error/four-o-four"); break; 
					//case 500: $location.path("/error/five-oo"); break; 
					//default:  $location.path("/error/default"); break; 
				}
            }

            return {
                
                requestError: function (rejection) {
                    notifyError(rejection);
                    return $q.reject(rejection);
                },
                responseError: function (rejection) {
                    notifyError(rejection);
                    return $q.reject(rejection);
                }
                
            };
            
        });
        
        $provide.factory("ApiInterceptor", function($cookies){
			
			return {
				
				request: function(config){
					config.headers = config.headers || {};
					var url = config.url + "";
					if ($cookies.get("ciccio") && url.indexOf(appConfig.apiUrl) > -1)
						config.headers.Authorization = "Bearer " + $cookies.get("ciccio");
					return config;
				}
				
			}
			
		});

        $httpProvider.interceptors.push("ErrorHttpInterceptor");
        $httpProvider.interceptors.push("ApiInterceptor");
        $resourceProvider.defaults.stripTrailingSlashes = false;
        $locationProvider.html5Mode(true).hashPrefix("!");
        
    });

    app.run(function ($couchPotato, $rootScope, $state, $stateParams) {
        app.lazy = $couchPotato;
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
    });

    return app;
});
