angular.module("coreApp")
.factory("authInterceptor", function($rootScope, $q, $sessionStorage, $location){
	
	return {
		request: function (config) {
			var urls = /\w+:\/\/([\w|\.]+)/; //CHECK FOR http://something
			config.headers = config.headers || {};
			if ($sessionStorage.token && urls.test(config.url)) {
				config.headers.Authorization = 'Bearer ' + $sessionStorage.token.access_token;
			}
			return config;
		},
		response: function (response) {
			//if (response.status === 401) {
			// handle the case where the user is not authenticated
			//}
			return response;// || $q.when(response);
		}
	};
	
});
