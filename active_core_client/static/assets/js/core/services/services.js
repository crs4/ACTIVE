angular.module("coreServices", [])
.constant("coreUrl", "http://156.148.132.79:80")
.constant("httpUrl", "http://" + window.location.hostname + ":80/api")
.factory("userService", function($resource, coreUrl){
	
	return {
		User: $resource(coreUrl + '/api/users/:id')
	}
	
})
.factory("groupService", function($resource, coreUrl){
	
	return {
		Group: $resource(coreUrl + '/api/groups/:id')
	}
	
})
.factory("itemService", function($resource, coreUrl){
	
	return {
		Item: $resource(coreUrl + '/api/items/:type/:id/', {type:'@type', id:'@id'}, {query: {isArray:false}})
	}
	
})
.factory("pluginService", function($resource, coreUrl){
	
	return {
		Plugin: $resource(coreUrl + '/api/plugins/:id')
	}
	
})
.factory("scriptService", function($resource, coreUrl){
	
	return {
		Script: $resource(coreUrl + '/api/scripts/:id')
	}
	
})
.factory('Scopes', function ($rootScope) {
	var mem = {};

	return {
		store: function (key, value) {
			mem[key] = value;
		},
		get: function (key) {
		    	return mem[key];
		}
	};
});
