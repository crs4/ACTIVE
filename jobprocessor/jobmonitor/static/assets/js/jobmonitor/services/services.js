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
.constant("wsUrl", "ws://localhost:12345")
.constant("httpUrl", "http://156.148.132.228:8000/jobmonitor/")
.factory("jobService", function($http, $websocket, $timeout, poller, httpUrl, wsUrl){
	
	return {

		startJob: function(algorithm, params, callback){
			var p = params == undefined ? [] : params;
			$http.post(httpUrl + 'start/', {"name":algorithm, "description":"description to do", "params":p}).then(
				function(result){
					callback(result);
				},
				function(errorResult){
					callback(errorResult);
				});
		},
		
		deleteJob: function(id, callback){
			$http.get(httpUrl + 'stop/' + id).then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},
		
		getJob: function(id, callback){
			$http.get(httpUrl + 'get/' + id).then(
				function(result){
					callback(result.data);
				},
				function(errorResult){
					callback(errorResult);
				});
		},
		
		pollJobs: function(callback){
			var url = httpUrl + 'list';
			var p = poller.get(url, {delay:5000, smart:true, catchError:true});
			//p.promise.then(null, null, callback);
			p.promise.then(null, null, function(result){
				if(result.status === 200 || result.status === 301){
					callback(result);
				}else{
					p.stop();
				}
			});
		},
		
		purgeQueues: function(callback){
			$http.post(httpUrl + 'clean/').then(
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
.factory("workerService", function($http, httpUrl){

	startWorkers = function(){
		console.log("TRY TO START WORKERS");
	},

	stopWorkers = function(){
		console.log("TRY TO STOP WORKERS");
	},
	
	getWorkers = function(){
		$http.get(httpUrl + 'workers/').then(
			function(result){
				callback(result.data);
			},
			function(errorResult){
				callback(errorResult);
			});
	}
	
});

