angular.module("jobmonitorApp")
.config(function($routeProvider, $locationProvider){
	
	$locationProvider.html5Mode(true);
	
	$routeProvider.when("/jobmonitor/workers", {
		templateUrl:"/assets/js/jobmonitor/views/workers.html"
	});
	
	$routeProvider.when("/jobmonitor/workers/:id", {
		templateUrl:"/assets/js/jobmonitor/views/worker.html"
	});
	
	$routeProvider.when("/jobmonitor/jobs", {
		templateUrl:"/assets/js/jobmonitor/views/jobs_main.html"
	});
	
	$routeProvider.when("/jobmonitor/startjob", {
		templateUrl:"/assets/js/jobmonitor/views/job_form.html",
		controller:"jobFormCtrl"
	});
	
	$routeProvider.when("/jobmonitor/purgejobs", {
		templateUrl:"/assets/js/jobmonitor/views/job_purge.html",
		controller:"jobPurgeCtrl"
	});
	
	$routeProvider.when("/jobmonitor/jobs/:id", {
		templateUrl:"/assets/js/jobmonitor/views/job_main.html",
		controller:"jobCtrl"
	});
	
	$routeProvider.otherwise({
		templateUrl:"/assets/js/jobmonitor/views/home.html"
	});
	
});
