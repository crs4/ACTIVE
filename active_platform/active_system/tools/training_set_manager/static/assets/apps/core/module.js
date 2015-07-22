define(["angular", 
	"angular-couch-potato", 
	"angular-ui-router", 
	"ng-infinite-scroll",
	"xeditable"], 

	function (ng, couchPotato) {

		"use strict";
		
		var module = ng.module("app.core", [
			"ui.router", 
			"infinite-scroll", 
			"xeditable"]);

		couchPotato.configureApp(module);

		module.config(function ($stateProvider, $couchPotatoProvider, $urlRouterProvider) {
			
			$stateProvider.state("app.core", {
					abstract: true,
					data: {
						title: 'Core'
					}
				})

				.state('app.core.models', {
					url: "models/:type",
					data: {
						title: "Model list"
					},
					views: {
						"content@app": {
							templateUrl: "/static/assets/apps/core/templates/models.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									'core/controllers/models',
									'core/directives/context',
									'core/controllers/context'
								])
							}
						}
					}
				})

				.state("app.core.models.details", {
					url: "/:model_id",
					data: {
						title: "Model details"
					},
					views: {
						"content@app": {
							templateUrl: "/static/assets/apps/core/templates/model_details.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/controllers/model_details",
									"core/directives/context",
									"core/controllers/context"
								])
							}
						}
					}
				})

				.state("app.core.instances", {
					url: "instances/:type",
					data: {
						title: "Model list"
					},
					views: {
						"content@app": {
							templateUrl: "/static/assets/apps/core/templates/instances.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/directives/counter",
									"core/directives/select2",
									"core/controllers/instances"
									//"core/controllers/select",
								])
							}
						}
					}
				});
				
				
		});

		module.run(function ($couchPotato, editableOptions) {
			module.lazy = $couchPotato;
			editableOptions.theme = "bs3";
		});

		return module;

});
