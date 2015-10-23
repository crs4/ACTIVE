angular.module("jobmonitorServices", [])
.config(function($websocketProvider, pollerConfig){
	$websocketProvider.$setup({
        lazy: false,
        reconnect: true,
        reconnectInterval: 2000,
        mock: true,
        enqueue: false
    });
    pollerConfig.resetOnRouteChange = true;
})
.constant("wsUrl", "ws://156.148.14.86:12345")
.constant("jobmonitorUrl", "http://" + window.location.host + "/job_monitor/")
.constant("clusterUrl", "http://"  + window.location.host + "/job_monitor/cluster/")
.factory("jobService", function($http, $websocket, $timeout, poller, jobmonitorUrl, wsUrl){
	
	return {
		
		deleteJob: function(id, callback){
			$http.get(jobmonitorUrl + 'stop/' + id).then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},
		
		getJob: function(id, callback){
			$http.get(jobmonitorUrl + 'get/' + id + '/').then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},
		
		pollJobs: function(jobsStatus, page, callback){
			var url = jobmonitorUrl + 'list';
			var p = poller.get(url, {
				delay:5000, 
				smart:true, 
				catchError:true, 
				argumentsArray: [{params:{status:jobsStatus,size:100,page:page}}]
			});
			p.promise.then(null, null, callback);
		},
		
		purgeQueues: function(callback){
			$http.get(jobmonitorUrl + 'clean/').then(
				function(result){
					callback(result);
				},
				function(errorResult){
					callback(errorResult);
				});
		},

		getJobs: function(callback){
			var ws = $websocket.$new(wsUrl);
			console.log("WS CONNECTION STATUS: " + ws.$status());
			
			ws.$on("$open", function(){
				console.log("WS CONNECTION STATUS: " + ws.$status());
				// send a first message to the websocket server
				var test1 = [{id:11111, name:"job1", status:"QUEUED", progress:[0]}, 
					{id:22222, name:"job2", status:"RUNNING", progress:[0, 30, 60]}, 
					{id:33333, name:"job3", status:"FAILED", progress:[0, 30, 60]},
					{id:44444, name:"job4", status:"COMPLETED", progress:[0, 30, 60, 100]}];
				ws.$emit("list_jobs", test1); 
					
				// send a second message to the websocket server after 15 sec.
				$timeout(function(){
					var test2 = [{id:11111, name:"job1", status:"RUNNING", progress:[0, 20, 60]}, 
					{id:22222, name:"job2", status:"RUNNING", progress:[0, 30, 60]}, 
					{id:33333, name:"job3", status:"FAILED", progress:[0, 30, 60]},
					{id:44444, name:"job4", status:"COMPLETED", progress:[0, 30, 60, 100]}];
					ws.$emit("list_jobs", test2);
				}, 15);
				
				// send a third message to the websocket server after 60 sec.
				$timeout(function(){
					var test3 = [{id:11111, name:"job1", status:"COMPLETED", progress:[0, 20, 100]}, 
					{id:22222, name:"job2", status:"RUNNING", progress:[0, 30, 60]}, 
					{id:33333, name:"job3", status:"FAILED", progress:[0, 30, 60]},
					{id:44444, name:"job4", status:"COMPLETED", progress:[0, 30, 60, 100]}];
					ws.$emit("list_jobs", test3);
				}, 60);
			});
			
			ws.$on("list_jobs", function(data){
				console.log("The websocket server has sent the following data:");
				console.log(data);
				callback(data);
				//ws.$close();
			});
			
			ws.$on("$close", function () {
				console.log("WS CONNECTION STATUS: " + ws.$status());
				console.log("Connection closed!");
			});
		}
		
	}
	
})
.factory("clusterService", function($http, poller, clusterUrl){

	return {

		manageCluster: function(command, callback){
			var url = clusterUrl;
			switch(command){
				case "start"   : url += 'start/'; break;
				case "stop"    : url += 'stop/'; break;
				case "restart" : url += 'restart/'; break;			
			}
			$http.get(url).then(
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
			var url = clusterUrl + 'list/';
			var p = poller.get(url, {
				delay:7000, 
				smart:true, 
				catchError:true
			});
			p.promise.then(null, null, callback);
		}

	}
	
});

