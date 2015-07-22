define(["angular", "angular-couch-potato", "angular-ui-router"], 
	
	function (ng, couchPotato) {

		"use strict";

		var module = ng.module("app.layout", ["ui.router"]);

		couchPotato.configureApp(module);

		module.config(function ($stateProvider, $couchPotatoProvider, $urlRouterProvider) {
			
			$stateProvider.state("app", {
				url: "/",
				views: {
					"root": {
						templateUrl: "/static/assets/apps/layout/templates/layout.html",
						resolve: {
							deps: $couchPotatoProvider.resolveDependencies([
								"layout/directives/layout",
								"layout/directives/header",
								"layout/directives/nav",
								"layout/controllers/search",
								"layout/controllers/advanced_search",
								"layout/controllers/nav"
							])
						}
					}
				}
			});

		});

		module.run(function ($couchPotato) {
			module.lazy = $couchPotato;
		});

		return module;

});
