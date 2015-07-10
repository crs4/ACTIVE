define(["angular", "angular-couch-potato", "angular-ui-router"], 
	
	function (ng, couchPotato) {

		"use strict";

		var module = ng.module("app.errors", ["ui.router"]);

		couchPotato.configureApp(module);

		module.config(function ($stateProvider, $couchPotatoProvider, $urlRouterProvider) {
			
			$stateProvider.state("app.errors", {
				abstract: true,
				url: "error"
			})
			
			.state("app.errors.401", {
				url: "/four-o-one",
				views: {
					"content@app": {
						templateUrl: "/assets/app/errors/templates/error401.html"
					}
				}
			})
			
			.state("app.errors.403", {
				url: "/four-o-three",
				views: {
					"content@app": {
						templateUrl: "/assets/app/errors/templates/error403.html"
					}
				}
			})
			
			.state("app.errors.404", {
				url: "/four-o-four",
				views: {
					"content@app": {
						templateUrl: "/assets/app/errors/templates/error404.html"
					}
				}
			})
			
			.state("app.errors.500", {
				url: "/five-oo",
				views: {
					"content@app": {
						templateUrl: "/assets/app/errors/templates/error500.html"
					}
				}
			})
			
			.state("app.errors.default", {
				url: "/default",
				views: {
					"content@app": {
						templateUrl: "/assets/app/errors/templates/error_default.html"
					}
				}
			});

		});

		module.run(function ($couchPotato) {
			module.lazy = $couchPotato;
		});

		return module;

});
