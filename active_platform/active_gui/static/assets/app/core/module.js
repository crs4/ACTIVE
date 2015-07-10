define(["angular", 
		"angular-couch-potato", 
		"angular-ui-router", 
		"smart-table", 
		"videogular", 
		"vg-controls", 
		"vg-overlay-play", 
		"vg-buffering", 
		"ng-infinite-scroll",
		"checklist"], 

	function (ng, couchPotato) {

		"use strict";
		
		var module = ng.module("app.core", [
			"ui.router", 
			"smart-table", 
			"com.2fdevs.videogular",
			"com.2fdevs.videogular.plugins.controls",
			"com.2fdevs.videogular.plugins.overlayplay",
			"com.2fdevs.videogular.plugins.buffering", 
			"infinite-scroll",
			"checklist-model"]);

		couchPotato.configureApp(module);

		module.config(function ($stateProvider, $couchPotatoProvider, $urlRouterProvider) {
			
			$stateProvider.state("app.core", {
					abstract: true,
					data: {
						title: 'Core'
					}
				})

				.state("app.core.upload", {
					url: "upload",
					data: {
						title: "Upload"
					},
					views: {
						"content@app": {
							templateUrl: "/assets/app/core/templates/dropzone.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/directives/dropzone"
								])
							}
						}
					}
				})

				.state('app.core.items', {
					url: 'items/:type',
					data: {
						title: 'Items'
					},
					views: {
						"content@app": {
							templateUrl: "/assets/app/core/templates/gallery.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									'core/directives/gallery',
									'core/directives/viewer',
									'core/directives/player',
									//'core/directives/select',
									'core/directives/counter',
									'core/directives/select2',
									'core/directives/context',
									"core/directives/file_reader",
									"core/directives/keywords",
									'core/controllers/context',
									'core/filters/scripts'
								])
							}
						}
					}
				})
				
				.state('app.core.users', {
					url: 'users',
					data: {
						title: 'User table'
					},
					views: {
						"content@app": {
							templateUrl: "/assets/app/core/templates/table.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/directives/table",
									"core/directives/paginator",
									"core/controllers/table",
									"core/controllers/table_users"
								])
							}
						}
					}
				})
				
				.state('app.core.users.edit', {
					url: '/:id',
					data: {
						title: 'User'
					},
					views: {
						"content@app": {
							templateUrl: "/assets/app/core/templates/user.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/controllers/element",
									"core/controllers/user",
									"core/controllers/scrollbar",
									"core/directives/checkbox"
								])
							}
						}
					}
				})
				
				.state('app.core.groups', {
					url: 'groups',
					data: {
						title: 'Groups'
					},
					views: {
						"content@app": {
							templateUrl: "/assets/app/core/templates/table.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/directives/table",
									"core/directives/paginator",
									"core/controllers/table",
									"core/controllers/table_groups"
								])
							}
						}
					}
				})
				
				.state("app.core.groups.edit", {
					url: "/:id",
					data: {
						title: "Groups edit"
					},
					views: {
						"content@app": {
							templateUrl: "/assets/app/core/templates/group.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/controllers/element",
									"core/controllers/group",
									"core/controllers/scrollbar",
									"core/directives/checkbox"
								])
							}
						}
					}
				})
				
				.state('app.core.permissions', {
					url: 'permissions',
					data: {
						title: 'Permissions'
					},
					views: {
						"content@app": {
							templateUrl: "/assets/app/core/templates/table.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/directives/table",
									"core/directives/paginator",
									"core/controllers/table",
									"core/controllers/table_permissions"
								])
							}
						}
					}
				})
				
				.state('app.core.permissions.edit', {
					url: "/:id",
					data: {
						title: "Permissions edit"
					},
					views: {
						"content@app": {
							templateUrl: "/assets/app/core/templates/permission.html",
							resolve: {
								deps: $couchPotatoProvider.resolveDependencies([
									"core/controllers/element",
									"core/controllers/permission",
									"core/controllers/scrollbar",
									"core/directives/radio"
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
