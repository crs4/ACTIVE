define(["tools/module", "appConfig"], function(module){
	
	module.registerFactory("toolService", function($resource){
		
		return {
			Job: $resource(appConfig.jobApiUrl + "job/get/:id/", {id:"@id"}, { 
				"start": {method:"POST", url: appConfig.jobApiUrl + "job/start/"},
				"delete": {method:"GET", url: appConfig.jobApiUrl + "job/delete/"},
				"clean": {method:"GET", url: appConfig.jobApiUrl + "job/clean/"}
			}),
			Node: $resource(appConfig.nodeApiUrl + "items/get/:id/", {id:"@id"}, {
				"start": {method:"GET", url: appConfig.nodeApiUrl + "job/start/"},
				"stop": {method:"GET", url: appConfig.nodeApiUrl + "job/stop/"},
				"restart": {method:"GET", url: appConfig.nodeApiUrl + "job/restart/"}
			})
		}
		
	});
	
});
