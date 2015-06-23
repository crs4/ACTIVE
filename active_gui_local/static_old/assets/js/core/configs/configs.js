angular.module("coreApp")
.config(function($locationProvider, $resourceProvider, $httpProvider){//, $sessionStorageProvider){
	$locationProvider.html5Mode(true).hashPrefix("!");
	$resourceProvider.defaults.stripTrailingSlashes = false;
	$httpProvider.interceptors.push('authInterceptor');
	//console.log($sessionStorageProvider.$get('ngStorage_token').token);
	//if($sessionStorageProvider.$get('ngStorage_token'))
	//	$httpProvider.defaults.headers.common['Authorization'] = "Bearer " + $sessionStorageProvider.$get('ngStorage_token').token.access_token
});
