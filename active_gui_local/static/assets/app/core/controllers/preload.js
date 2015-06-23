define(["core/module", "appConfig"], function(module){

	module.registerController("preloaderCtrl", function($scope, preloader){
		
		$scope.isLoading = true;
		$scope.isSuccessful = false;
		$scope.percentLoaded = 0;
		$scope.imageLocations = [appConfig.coreApiUrl + "items/file/" + {{item.id}} + "/?type=thumb&cache="];
		
		preloader.preloadImages(imageLocations).then(
			function handleResolve( imageLocations ) {

				// Loading was successful.
				$scope.isLoading = false;
				$scope.isSuccessful = true;

				console.info( "Preload Successful" );

			},
			function handleReject( imageLocation ) {

				// Loading failed on at least one image.
				$scope.isLoading = false;
				$scope.isSuccessful = false;

				console.error( "Image Failed", imageLocation );
				console.info( "Preload Failure" );

			},
			function handleNotify( event ) {

				$scope.percentLoaded = event.percent;

				console.info( "Percent loaded:", event.percent );

			}

		);
		
	});
	
});
