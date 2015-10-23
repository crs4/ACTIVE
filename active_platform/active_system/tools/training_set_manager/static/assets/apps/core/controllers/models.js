define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerController("modelCtrl", function ($scope, $stateParams, $state, coreService) {
		
		$scope.models = [];
		$scope.busy = false;
		$scope.page = 1;
		$scope.selectedType = $stateParams.type;
		
		$scope.selectModel = function ($event, model) {
			$state.go("app.core.models.details", {"type":$scope.selectedType, "model_id":model.id});
		};
		
		$scope.nextPage = function(){
			getModels();
		};
		
		$scope.$watch("selectedType", function(newValue, oldValue){
			reset();
			getModels();
		});
		
		/**
		 * HANDLER FUNCTIONS
		 */
		 
		var reset = function(){
			$scope.models.length = 0;
			$scope.page = 1;
			$scope.busy = false;
		};

		var getModels =  function(){
			$scope.busy = true;
			var params  = {page:$scope.page, type:$scope.selectedType};
			var i = coreService.Model.query(params, function(){
				$scope.busy = false;
				$scope.models = $scope.models.concat(i.results);
				if(i.next != null){
					$scope.page += 1;
				} else {
					$scope.busy = true;
				}
			});
		};
		
    });
    
});
