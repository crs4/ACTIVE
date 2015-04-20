angular.module("jobmonitorApp")
.config(function ($httpProvider) {
	$httpProvider.interceptors.push(function ($q, $location) {
		return {
			'responseError': function(rejection){
				console.log(rejection);
				if (rejection.status === 500){
					console.log("INTERNAL SERVER ERROR");
				}
				if (rejection.status === 404){
					console.log("PAGE NOT FOUND");
				}
				if (rejection.status === 0){
					console.log("AJAX CALL ABORTED");
				}
				return $q.reject(rejection);
			}
		};
	});
});
