angular.module("coreApp")
.config(function($routeProvider, $locationProvider){
	
	$routeProvider.when("/users", {
		templateUrl:"/assets/js/core/views/users_main.html"
	});
	
	$routeProvider.when("/users/new", {
		templateUrl:"/assets/js/core/views/user.html",
		controller:"userCtrl"
	});
	
	$routeProvider.when("/users/:id", {
		templateUrl:"/assets/js/core/views/user.html",
		controller:"userCtrl"
	});
	
	$routeProvider.when("/groups", {
		templateUrl:"/assets/js/core/views/groups_main.html"
	});
	
	$routeProvider.when("/items", {
		templateUrl:"/assets/js/core/views/items_main.html"
	});
	
	$routeProvider.when("/items/upload", {
		templateUrl:"/assets/js/core/views/item.html",
		controller:"itemUploadCtrl"
	});
	
	$routeProvider.when("/plugins", {
		templateUrl:"/assets/js/core/views/plugins_main.html"
	});
	
	$routeProvider.when("/plugins/upload", {
		templateUrl:"/assets/js/core/views/plugin_upload.html",
		controller:"pluginUploadCtrl"
	});
	
	$routeProvider.otherwise({
		templateUrl:"/assets/js/core/views/home.html"
	});
	
});
