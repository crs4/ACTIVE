define(["core/module"], function (module) {

    "use strict";

    module.registerController("managerCtrl", function ($scope, $stateParams, Mediator, coreService) {
		
		$scope.selectedItems = [];
		$scope.models = [];
		$scope.selectedModel = null;
		$scope.selectedType = $stateParams.type;
		
		$scope.$on("selectedItems", function(event, args){
			$scope.selectedItems = args.selectedItems;
			if($scope.selectedItems.length === 0)
				$scope.selectedModel = null;
		});
		
		$scope.$watch("selectedModel", function(newValue, oldValue){
			Mediator.mediateSelectedModel($scope.selectedModel);
		});
		
		$scope.bindInstance = function(){
			Mediator.mediateBindInstance();
		};
		
		$scope.unselectItems = function() {
			$scope.selectedItems.length = 0;
			Mediator.mediateUnselectItems();
		};

		/*var m = coreService.Model.query({type:$stateParams.type}, function(){
			$scope.models = m.results;
		});*/
		
	});
    
});
