angular.module("jobmonitorServices", ["ngCookies"])
.config(function($provide, $httpProvider, pollerConfig){

	$provide.factory("HttpInterceptor", function($cookies){
			
		return {
			
			request: function(config){
				config.headers = config.headers || {};
				var url = config.url + "";
				if ($cookies.ciccio && url.indexOf("http://" + window.location.host + "/jobmonitor/") > -1)
					config.headers.Authorization = "Bearer " + $cookies.ciccio;
				return config;
			}
			
		}
		
	});

	$httpProvider.interceptors.push("HttpInterceptor");

    	pollerConfig.resetOnRouteChange = true;

})
.constant("jobmonitorUrl", "http://" + window.location.host + "/jobmonitor/")
.constant("clusterUrl", "http://"  + window.location.host + "/jobmonitor/cluster/")
.factory("jobService", function($http, $websocket, $timeout, poller, jobmonitorUrl){
	
	return {
		
		deleteJob: function(id, callback){
			$http.delete(jobmonitorUrl + 'jobs/' + id).then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},
		
		getJob: function(id, callback){
			$http.get(jobmonitorUrl + 'jobs/' + id).then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},
		
		pollJobs: function(jobsStatus, callback){
			var url = jobmonitorUrl + 'jobs/';
			var p = poller.get(url, {
				delay:5000, 
				smart:true, 
				catchError:true, 
				argumentsArray: [{params:{status:jobsStatus}}]
			});
			p.promise.then(null, null, callback);
		},
		
		purgeQueues: function(callback){
			$http.delete(jobmonitorUrl + 'jobs/').then(
				function(result){
					callback(result);
				},
				function(errorResult){
					callback(errorResult);
				});
		}
		
	}
	
})
.factory("clusterService", function($http, poller, clusterUrl){

	return {

		manageCluster: function(command, callback){
			var url = clusterUrl;
			switch(command){
				case "start"   : url += 'start/'; startCluster(url, callback); break;
				case "stop"    : url += 'stop/'; stopCluster(url, callback); break;
				case "restart" : url += 'restart/'; restartCluster(url, callback); break;			
			}
		},

		startCluster: function(url, callback){
			$http.get(url).then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},

		stopCluster: function(url, callback){
			$http.delete(url).then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},

		restartCluster: function(url, callback){
			$http.put(url).then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},

		getNode: function(id, callback){
			$http.get(clusterUrl + 'node/' + id + '/').then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},
	
		getNodes: function(callback){
			var url = clusterUrl;
			var p = poller.get(url, {
				delay:7000, 
				smart:true, 
				catchError:true
			});
			p.promise.then(null, null, callback);
		}

	}
	
});

