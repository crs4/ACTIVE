define(["core/module", "appConfig"], function(module){
	
	module.registerDirective("preloadFile", function($http, $q){
		
		return {
			restrict: "A",
			scope: {
				preloadType: "@",
				preloadItem: "="
			},
			controller: function($scope, $element, $attrs){
				$element.removeAttr("preload-file");

				//RESET PREVIOUS DATA				
				$scope.$parent.dataUrl = null;
				
				this.getItem = function(){
					return $scope.preloadItem;
				};
				
				var conf = {
					responseType: "blob",
					params: {
						type: $scope.preloadType
					},
					cache: false
				};
				
				var promise = $http.get(appConfig.coreApiUrl + "items/file/" +  $scope.preloadItem.id + "/", conf);
				
				promise.success(function(data, status, headers, config) {
					var fr = new FileReader();
					fr.onload = function(event){
						$scope.$parent.dataUrl = fr.result;
						$scope.$apply();
					};
					fr.readAsDataURL(data);
				})
				.error(function(data, status, headers, config) {
					console.log(status);
				});
			}
		}
		
	});
	
});
