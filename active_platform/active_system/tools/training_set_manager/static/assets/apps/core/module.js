define(["angular", 
		"angular-couch-potato", 
		"angular-ui-router", 
		"ng-infinite-scroll",
		"videogular", 
		"vg-controls",
		"vg-poster", 
		"checklist-model"], 

	function (ng, couchPotato) {

		"use strict";
		
		var module = ng.module("app.core", [
			"ui.router", 
			"infinite-scroll",
			"com.2fdevs.videogular",
			"com.2fdevs.videogular.plugins.controls",
			"com.2fdevs.videogular.plugins.poster", 
			"checklist-model"]);

		couchPotato.configureApp(module);

		module.config(function ($stateProvider, $couchPotatoProvider, $urlRouterProvider) {
			
			$stateProvider.state("app.core", {
					abstract: true,
					data: {
						title: 'Core'
					}
				})

				.state("app.core.models", {
					url: "models/:type",
					data: {
						title: "Model list"
					},
					views: {
						"content@app": {
							templateUrl: function(params){
								switch(params.type){
									case "new": return "/static/assets/apps/core/templates/model_form.html"; break;							
									default: return "/static/assets/apps/core/templates/models.html"; break;
								}
							},
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/directives/context",
									"core/directives/editable",
									"core/directives/scrollbar",
									"core/controllers/models",
									"core/controllers/context",
									"core/controllers/model_search",
									"core/controllers/model_form"
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
						title: "Instance list"
					},
					views: {
						"content@app": {
							templateUrl: function(params){
								switch(params.type){
									case "audio": return "/static/assets/apps/core/templates/audio_instances.html"; break;							
									default: return "/static/assets/apps/core/templates/video_instances.html"; break;
								}
							},
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/directives/counter",
									"core/directives/select2",
									"core/directives/scrollbar",
									"core/directives/player",
									"core/controllers/instances_base",
									"core/controllers/audio_instances",
									"core/controllers/video_instances"
								])
							}
						}
					}
				});
				
		});

		module.run(function ($couchPotato){
			module.lazy = $couchPotato;
		});

		return module;

});
