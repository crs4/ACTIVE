angular.module("jobmonitorApp")
.controller("navCtrl", function(){

	setup = function(){

		if (!null) {
			$('nav ul').jarvismenu({
				accordion : true,
				speed : 235,
				closedSign : '<em class="fa fa-expand-o"></em>',
				openedSign : '<em class="fa fa-collapse-o"></em>'
			});
		} else {
			alert("Error - menu anchor does not exist");
		}

		$('.minifyme').click(function(e) {
			$('body').toggleClass("minified");
			e.preventDefault();
		});
	};
	
	setup();
	
})
.controller("ribbonCtrl", function($scope, $route){
	
	$scope.reload = function(){
		$route.reload();
	};
	
})
/*.controller("jobFormCtrl", function($scope, $location, jobService){
	
	$scope.startJob = function(){
		jobService.startJob(this.algorithm, this.name, this.params, function(result){
			if(result.status === 200)
				$location.path("/jobmonitor/jobs");
		});
	};
	
})*/
.controller("jobCtrl", function($scope, $routeParams, $location, jobService){
	
	var id = $routeParams["id"];
	
	jobService.getJob(id, function(data){
		$scope.job = data;
	});
	
	$scope.deleteJob = function(id){
		jobService.deleteJob(id, function(data){
			$scope.msg = data;
		});
	};
	
	$scope.getBack = function(){
		$location.path("/jobmonitor/jobs");
	};
	 
})
.controller("clusterNodeCtrl", function($scope, $routeParams, $location, clusterService){

	var id = $routeParams["id"];
	
	clusterService.getNode(id, function(data){
		$scope.node = data;
		$('#myTab a').click(function(e){
			e.preventDefault()
		  	$(this).tab('show')
		});
	});

	$scope.getBack = function(){
		$location.path("/jobmonitor/cluster");
	};

});

