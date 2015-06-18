define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerFactory("coreService", function ($resource) {
		
		return {
			Item: $resource(appConfig.coreApiUrl + "items/:type/:id/", {type:"@type", id:"@id"}, {query:{isArray:false}}),
			FilteredItem: $resource(appConfig.coreApiUrl + "keywords/search/:type/:keywords/", {type:"@type", keywords:"@keywords"}, {query:{isArray:false}}),
			TaggedItem: $resource(appConfig.coreApiUrl + "tags/search/item/:type/entity/:id/", {type:"@type", id:"@id"}, {query:{isArray:false}}),
			Plugin: $resource(appConfig.coreApiUrl + "plugins/:id/", {id:"@id"}, {query:{isArray:true}}),
			Script: $resource(appConfig.coreApiUrl + "scripts/:id/", {id:"@id"}, {query:{isArray:true}}),
			Tool: $resource(appConfig.coreApiUrl + "tools/:id/", {id:"@id"}, {query:{isArray:false}}),
			People: $resource(appConfig.coreApiUrl + "people/search/:name/:surname/", {name:"@name", surname:"@surname"}, {query:{isArray:true}}),
			User: $resource(appConfig.userApiUrl + "users/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}}),
			Group: $resource(appConfig.userApiUrl + "groups/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}}),
			Permission: $resource(appConfig.userApiUrl + "permissions/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}}),
			ContentType: $resource(appConfig.userApiUrl + "content_types/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}})
		}
		
	});
	
});
