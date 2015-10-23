define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerFactory("coreService", function ($resource) {
		
		return {
			Model: $resource(appConfig.apiUrl + "models/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}}),
			Instance: $resource(appConfig.apiUrl + "instances/:id/", {id:"@id"}, {query:{isArray:false}, "update":{method:"PUT"}}),
			InstanceSearch: $resource(appConfig.apiUrl + "models/instancesearch/:model_id/", {model_id:"@model_id"}, {query:{isArray:false}}),
			People: $resource(appConfig.coreApiUrl + "people/:id/", {id:"@id"}, {query:{isArray:false}})
		}
		
	});
	
});


