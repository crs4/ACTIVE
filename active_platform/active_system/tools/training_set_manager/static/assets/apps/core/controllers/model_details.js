define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerController("modelDetailsCtrl", function ($scope, $location, $stateParams, coreService) {
		
		$scope.instances = [];
		$scope.busy = false;
		$scope.page = 1;
		$scope.context = {name:"search_none", params:""};
		$scope.selectedType = $stateParams.type;
		$scope.dataUrl = null;
		
		$scope.selectInstance = function ($event, instance) {
			//TO DO
		};
		
		$scope.nextPage = function(){
			getInstances();
		};
		
		$scope.deleteCurrentModel = function(){
			coreService.Model.delete({type:$scope.selectedType.option, id:$scope.currentModel.id}, function() {
				$scope.models.splice($scope.model.indexOf($scope.currentItem), 1);
				$scope.currentModel = null;
				$("#delete_item_modal").modal("hide");
				//TO ADD: reload state
			});
		};

		$scope.$watch("selectedType", function(newValue, oldValue){
			reset();
			getInstances();
		});
		
		$scope.$on("search_context", function(event, args){
			$scope.context = args;
			reset();
			getInstances();
		});
		
		
		
		/**
		 * HANDLER FUNCTIONS
		 */
		 
		var reset = function(){
			$scope.instances.length = 0;
			$scope.page = 1;
			$scope.busy = false;
			$scope.currentInstance = null;
		};

		var getInstances =  function(){
			$scope.busy = true;
			var params  = {page:$scope.page, model_id:$stateParams.model_id};
			var i = coreService.InstanceSearch.query(params, function(){
				$scope.busy = false;
				$scope.instances = $scope.instances.concat(i.results);
				if(i.next != null){
					$scope.page += 1;
				} else {
					$scope.busy = true;
				}
			});
		};
		
    });
    
});
