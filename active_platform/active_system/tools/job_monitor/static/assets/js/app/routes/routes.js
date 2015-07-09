angular.module("jobmonitorApp")
.config(function($routeProvider, $locationProvider){
	
	$locationProvider.html5Mode(true);
	
	$routeProvider.when("/job_monitor/cluster", {
		templateUrl:"/static/assets/js/app/views/cluster_main.html"
	});
	
	$routeProvider.when("/job_monitor/cluster/:id", {
		templateUrl:"/static/assets/js/app/views/cluster_node.html",
		controller:"clusterNodeCtrl"
	});

	//$routeProvider.when("/jobmonitor/startjob", {
	//	templateUrl:"/static/assets/js/app/views/job_form.html",
	//	controller:"jobFormCtrl"
	//});
	
	$routeProvider.when("/job_monitor/jobs/:id", {
		templateUrl:"/static/assets/js/app/views/job.html",
		controller:"jobCtrl"
	});
	
	$routeProvider.otherwise({
		templateUrl:"/static/assets/js/app/views/jobs_main.html"
	});
	
});

