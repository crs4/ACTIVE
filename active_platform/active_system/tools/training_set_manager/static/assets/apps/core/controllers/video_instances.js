define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerController("videoInstanceCtrl", function ($scope, $location, $q, $state, $stateParams, Mediator, coreService) {
		
		$scope.selectItem = function ($event, item) {
			var unique = true;
			for(var i = 0; i < $scope.selectedItems.length; i++){
				if($scope.selectedItems[i].id === item.id){
					unique = false;
					$scope.selectedItems.splice(i, 1);
					Mediator.mediateSelectedItems($scope.selectedItems);
					if($event) 
						angular.element($event.currentTarget).removeClass("highlight");
					break;
				}
			}
			if(unique){
				$scope.selectedItems.push(item);
				Mediator.mediateSelectedItems($scope.selectedItems);
				if($event) 
					angular.element($event.currentTarget).addClass("highlight");
			}
			$scope.currentItem = item;
		};
		
		$scope.nextPage = function(){
			getItems();
		};

		$scope.getPath = function(id, type){
			return appConfig.apiUrl + "instances/file/" + id + "/?type=" + type;
		};
		
		$scope.$watch("selectedType", function(newValue, oldValue){
			reset();
			//if($scope.selectedType === "video"){
			getItems();
			//}
		});
		
		/**
		 * HANDLER FUNCTIONS
		 */
		 
		var reset = function(){
			$scope.items.length = 0;
			$scope.page = 1;
			$scope.busy = false;
			$scope.selectedItems.length = 0;
			$scope.currentItem = null;
			$scope.selectedModel = null;
		};

		var getItems =  function(){
			$scope.busy = true;
			var params  = {page:$scope.page, type:$scope.selectedType, used:false};
			var i = coreService.Instance.query(params, function(){
				$scope.busy = false;
				$scope.items = $scope.items.concat(i.results);
				if(i.next != null){
					$scope.page += 1;
				} else {
					$scope.busy = true;
				}
			});
		};

    });
    
});
