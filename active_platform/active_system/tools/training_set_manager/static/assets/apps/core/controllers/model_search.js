define(["core/module"], function(module){

	module.registerController("modelSearchCtrl", function($scope, $state, $stateParams){

		$scope.selectedModel = null;

		$scope.$watch("selectedModel", function(newValue, oldValue){
			if(newValue){
				$state.go("app.core.models.details", {"type":$stateParams.type, "model_id":newValue});
			}
		});

	});

});
