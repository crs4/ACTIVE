angular.module("jobmonitorServices")
.directive("jobSummary", function(){
	
	return {
		restrict:"E",
		templateUrl:"/static/assets/js/jobmonitor/views/jobs.html",
		controller: function($scope, $location, $timeout, jobService){
			
			$scope.deleteJob = function(id){
				console.log("TRY TO DELETE JOB WITH ID " + id);
				jobService.deleteJob(id, function(msg){
					$scope.msg = msg;
				});
			};
			
			$scope.getJob = function(id){
				$location.path("/jobmonitor/jobs/" + id);
			};
			
			jobService.pollJobs(function(res){
				if(res.status === 200)
					$scope.jobs = res.data;
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

			$scope.startWorkers = function(){
				workerService.startWorkers();
			};

			$scope.stopWorkers = function(){
				workerService.stopWorkers();
			};
			
			$scope.getWorker = function(id){
				console.log("TRY TO GET WORKKER " + id);
			};
			
			workerService.getWorkers(function(data){
				$scope.workers = data;
			});
			
		}
	}
	
})
.directive('notification', function($timeout){

	return {
    		restrict:"A",
    		replace: true,
		    scope: {
		      ngModel: '='
		    },
		template: '<b class="alert fade" bs-alert="ngModel"></b>',
		link: function(scope, element, attrs) {
			$timeout(function(){
				element.hide();
			}, 3000);
		}
  	}

});

