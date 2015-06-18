define(["angular", "angular-couch-potato", "angular-ui-router", "angular-poller"], 
	
	function (ng, couchPotato) {

		"use strict";

		var module = ng.module("app.tools", ["ui.router", "emguo.poller"]);

		couchPotato.configureApp(module);

		module.config(function ($stateProvider, $couchPotatoProvider, $urlRouterProvider, pollerConfig) {
			
			$stateProvider.state("app.tools", {
				abstract: true,
				url: "tools"
			})
			
			.state("app.tools.jobmonitor", {
				url: "/jobmonitor",
				views: {
					"content@app": {
						templateUrl: "/assets/app/tools/templates/jobmonitor.html",
						resolve: {
							deps: $couchPotatoProvider.resolveDependencies([
								"tools/controllers/jobmonitor"
							])
						}
					}
				}
			});
			
			pollerConfig.resetOnRouteChange = true;

		});

		module.run(function ($couchPotato) {
			module.lazy = $couchPotato;
		});

		return module;

});
