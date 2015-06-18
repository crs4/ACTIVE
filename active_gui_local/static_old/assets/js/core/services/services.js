angular.module("coreServices", [])
.constant("httpUrl", "http://localhost:8080/api/public")
.factory("userService", function($resource, httpUrl){
	
	return {
		User: $resource(httpUrl + '/users/:id', {}, 
			{query:{params: {'latestId':'00000', 'pageSize':10}, isArray:false}, 
			 update:{method:'PUT'}})
	}
	
})
.factory("groupService", function($resource, httpUrl){
	
	return {
		Group: $resource(httpUrl + '/groups/:id')
	}
	
})
.factory("itemService", function($resource, httpUrl){
	
	return {
		Item: $resource(httpUrl + '/items/:id', {}, 
			{query:{params:{ 'type':'image', 'latestId':'00000', 'pageSize':10 }, isArray:false}})
	}
	
})
.factory("pluginService", function($resource, httpUrl){
	
	return {
		Plugin: $resource(httpUrl + '/plugins/:id', {}, 
			{query:{isArray:false}})
	}
	
});
