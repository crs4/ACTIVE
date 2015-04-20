angular.module("jobmonitorApp")
.config(function($routeProvider, $locationProvider){
	
	$locationProvider.html5Mode(true);
	
	$routeProvider.when("/jobmonitor/workers", {
		templateUrl:"/static/assets/js/jobmonitor/views/workers.html"
	});
	
	$routeProvider.when("/jobmonitor/workers/:id", {
		templateUrl:"/static/assets/js/jobmonitor/views/worker.html"
	});
	
	$routeProvider.when("/jobmonitor/jobs", {
		templateUrl:"/static/assets/js/jobmonitor/views/jobs_main.html"
	});
	
	$routeProvider.when("/jobmonitor/startjob", {
		templateUrl:"/static/assets/js/jobmonitor/views/job_form.html",
		controller:"jobFormCtrl"
	});
	
	$routeProvider.when("/jobmonitor/purgejobs", {
		templateUrl:"/static/assets/js/jobmonitor/views/job_purge.html",
		controller:"jobPurgeCtrl"
	});
	
	$routeProvider.when("/jobmonitor/jobs/:id", {
		templateUrl:"/static/assets/js/jobmonitor/views/job_main.html",
		controller:"jobCtrl"
	});
	
	$routeProvider.otherwise({
		templateUrl:"/static/assets/js/jobmonitor/views/home.html"
	});
	
});
