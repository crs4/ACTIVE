define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerController("instanceBaseCtrl", function ($scope, $location, $q, $state, $stateParams, Mediator, coreService) {
		
		$scope.items = [];
		$scope.busy = false;
		$scope.page = 1;
		$scope.selectedItems = [];
		$scope.selectedModel = null;
		$scope.selectedType = $stateParams.type;
		$scope.dataUrl = null;
		
		$scope.$on("unselectItems", function() {
			$scope.selectedItems.length = 0;
			$(".superbox-list").removeClass("highlight");
		});
		
		$scope.$on("selectedModel", function(event, args){
			$scope.selectedModel = args.selectedModel;
		});
		
		$scope.$on("bindInstance", function(event, args){
			bind();
		});

		/**
		 * HANDLER FUNCTIONS
		 */
		
		var bind = function(){
			console.log($scope.selectedModel);
			console.log($scope.selectedItems.length);
			if($scope.selectedModel && $scope.selectedItems.length > 0){
				var promises = [];
				angular.forEach($scope.selectedItems, function(value, key){
					value.entity_model = $scope.selectedModel;
					value.thumbnail = undefined;
					value.features = undefined;
					var p = coreService.Instance.update({"id":value.id}, value);
					promises.push(p);
				});
				$q.all(promises).then(function(){
					$state.go("app.core.models.details", {
						"type":$scope.selectedType,
						"model_id":$scope.selectedModel
					});
				});
			}
		};

    });
    
});
