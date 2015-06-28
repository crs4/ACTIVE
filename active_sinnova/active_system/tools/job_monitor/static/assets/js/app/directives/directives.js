angular.module("jobmonitorServices")
.directive("jobSummary", function(){
	
	return {
		restrict:"E",
		templateUrl:"/static/assets/js/app/views/jobs.html",
		controller: function($scope, $location, $timeout, jobService){
			
			$scope.deleteJob = function(id){
				jobService.deleteJob(id, function(msg){
					$scope.msg = msg;
				});
			};

			$scope.purgeQueues = function(){
				jobService.purgeQueues(function(result){
					$scope.msg = {"status":result.status, "msg":result.data.info};
				});
			};
			
			$scope.getJob = function(id){
				$location.path("/job_monitor/jobs/" + id);
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
.directive("clusterSummary", function(){
	
	return {
		
		restrict:"E",
		templateUrl:"/static/assets/js/app/views/cluster.html",
		controller: function($scope, $location, clusterService){

			$scope.manageCluster = function(command){
				clusterService.manageCluster(command, function(res){
					$scope.msg = res;
				});
			};
			
			$scope.getNode = function(id){
				$location.path("/job_monitor/cluster/" + id);
			};
			
			clusterService.getNodes(function(res){
				$scope.cluster = res.data;
			});
			
		}
	}
	
});
/*.directive('notification', function($timeout){

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

});*/

