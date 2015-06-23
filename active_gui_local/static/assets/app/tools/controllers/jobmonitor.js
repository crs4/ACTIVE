define(["tools/module", "appConfig"], function(module){
	
	"use strict";
	
	module.registerController("jobmonitorCtrl", function(toolService, poller){
		
		$scope.job  = null;
		$scope.jobs = [];
		
		$scope.node  = null;
		$scope.nodes = [];
		
		$create = function(){
			toolService.Job.start({});
		};
		
		$read = function(job){
			var j = toolService.Job.get({id:job.id}, function(){
				$scope.job = j;
			});
		};
		
		$delete = function(job){
			toolService.Job.delete({id:job.id}, function(){
				$scope.jobs.splice(job, 1);
			});
		};
		
		$pollJobs = function(jobsStatus){
			var url =  appConfig.jobApiUrl + "list/";
			var p = poller.get(url, {
				delay:5000, 
				smart:true, 
				catchError:true, 
				argumentsArray: [{params:{status:jobsStatus}}]
			});
				
			p.promise.then(null, null, function(result){
				if(result.status === 0 || result.status === 500 || result.status === 503)
					poller.stopAll();
				else $scope.jobs = result;
			});
		};
		
		$pollNodes: function(){
			var url = clusterUrl + "list/";
			var p = poller.get(url, {
				delay:7000, 
				smart:true, 
				catchError:true
			});
			
			p.promise.then(null, null, function(result){
				if(result.status === 0 || result.status === 500 || result.status === 503)
					poller.stopAll();
				else $scope.nodes = result;
			});
		}
		
	});
	
});
