angular.module("jobmonitorServices")
.directive("jobSummary", function(){
	
	return {
		restrict:"E",
		templateUrl:"/static/assets/js/jobmonitor/views/jobs_dt.html",
		controller: function($scope, $location, $timeout, jobService){
			
			$scope.deleteJob = function(id){
				console.log("TRY TO DELETE JOB WITH ID " + id);
				//jobService.deleteJob(id, function(msg){
					//se success rimuovi job dallo scope oppure aspetti ws? oppure lo nascondi e poi aspetti ws?
				//	$scope.msg = msg;
				//});
			};
			
			$scope.getJob = function(id){
				$location.path("/jobmonitor/jobs/" + id);
			};
			
			$scope.purgeQueues = function(){
				console.log("TRY TO PURGE QUEUES");
			};
			
			$scope.filterByStatus = function(jobsStatus){
				jobService.pollJobs(jobsStatus, function(res){
					if(res.status === 200){
						$scope.jobs = res.data;
					}
				});
			};
			
			jobService.pollJobs("ALL", function(res){
				if(res.status === 200){
					$scope.jobs = res.data;
				}
			});
			
			/*jobService.getJobs(function(data){
				$scope.jobs = data;
				$scope.$apply();
			});*/
			
		}
	}
})
.directive("workerSummary", function(){
	
	return {
		
		restrict:"E",
		templateUrl:"/static/assets/js/jobmonitor/views/workers.html",
		controller: function($scope, $location, workerService){
			
			$scope.getWorker = function(id){
				console.log("TRY TO GET WORKKER " + id);
			};
			
			workerService.getWorkers(function(data){
				$scope.workers = data;
			});
			
		}
	}
	
});
