define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerFactory("coreService", function ($resource) {
		
		return {
			Item: $resource(appConfig.coreApiUrl + "items/:type/:id/", {type:"@type", id:"@id"}, {query:{isArray:false}}),
			ESItem: $resource(appConfig.esBaseUrl, {}, {query:{isArray:false}, query:{method:"POST"}}),
			KeywordItem: $resource(appConfig.coreApiUrl + "keywords/item/:item_id/", {item_id:"@item_id"}, {query:{isArray:true}}),
			Plugin: $resource(appConfig.coreApiUrl + "plugins/:id/", {id:"@id"}, {query:{isArray:true}}),
			Script: $resource(appConfig.coreApiUrl + "scripts/:id/", {id:"@id"}, {query:{isArray:true}}),
			Person: $resource(appConfig.coreApiUrl + "search/people/:first_name/:last_name/", {first_name:"@first_name", last_name:"@last_name"}, {query:{isArray:true}}),
			Tool: $resource(appConfig.coreApiUrl + "tools/:id/", {id:"@id"}, {query:{isArray:false}}),
			User: $resource(appConfig.userApiUrl + "users/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}}),
			Group: $resource(appConfig.userApiUrl + "groups/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}}),
			Permission: $resource(appConfig.userApiUrl + "permissions/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}}),
			ContentType: $resource(appConfig.userApiUrl + "content_types/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}})
		}
		
	});
	
});
