angular.module("jobmonitorServices")
.directive("jobSummary", function(){
	
	return {
		restrict:"E",
		templateUrl:"/static/assets/js/app/views/jobs.html",
		controller: function($scope, $location, $timeout, jobService){
            
            		$scope.current_page = 1;
			$scope.job_status = "ALL";
			
            
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
				$scope.job_status = jobsStatus;
				$scope.current_page = 1;
			};

			$scope.selectPage = function(page){
				$scope.current_page = page;
			};

			$scope.$watchGroup(["current_page", "job_status"],function(newValues, oldValues){
				if(newValues){
				    jobService.pollJobs(newValues[1], newValues[0], function(res){
				        if(res.status === 200){
				            $scope.jobs = res.data.data;
				            temp_pages = [];
				            for(var i = 0; i<res.data.num_pages; i++){
				                temp_pages.push(i+1);
				            }    
				            $scope.num_pages = temp_pages;                           
				        }
				    });                
				}    
			});
			
			
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

