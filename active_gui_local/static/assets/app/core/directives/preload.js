define(["core/module", "appConfig"], function(module){
	
	module.registerDirective("preloadImg", function(preloader){
		
		return {
			restrict: "A",
			controller: function($scope, $element, $attrs, preloader){
				$element.removeAttr("preload-img");
				
				$scope.isLoading = true;
				$scope.isSuccessful = false;
				$scope.percentLoaded = 0;
				$scope.imageLocations = [];
				
				for (var i = 0; i < $scope.items.length; i++){
					$scope.imageLocations.push(appConfig.coreApiUrl + "items/file/" + $scope.items[i].id + "/?type=thumb");
				}
				
				preloader.preloadImages($scope.imageLocations).then(
					function handleResolve(imageLocations) {
						$scope.isLoading = false;
						$scope.isSuccessful = true;
						console.info("Preload Successful");
					},
					function handleReject(imageLocation) {
						$scope.isLoading = false;
						$scope.isSuccessful = false;
						console.error("Image Failed", imageLocation);
						console.info("Preload Failure");
					},
					function handleNotify(event) {
						$scope.percentLoaded = event.percent;
						console.info("Percent loaded:", event.percent);
					}

				);
				
			}
		}
		
	});
	
});
