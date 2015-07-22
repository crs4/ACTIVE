define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerController("instanceCtrl", function ($scope, $location, $q, $state, $stateParams, Mediator, coreService) {
		
		$scope.items = [];
		$scope.busy = false;
		$scope.page = 1;
		$scope.selectedItems = [];
		$scope.selectedModel = null;
		$scope.selectedType = $stateParams.type;
		$scope.dataUrl = null;
		
		$scope.selectItem = function ($event, item) {
			var unique = true;
			for(var i = 0; i < $scope.selectedItems.length; i++){
				if($scope.selectedItems[i].id === item.id){
					unique = false;
					$scope.selectedItems.splice(i, 1);
					Mediator.mediateSelectedItems($scope.selectedItems);
					angular.element($event.currentTarget).removeClass("highlight");
					break;
				}
			}
			if(unique){
				$scope.selectedItems.push(item);
				Mediator.mediateSelectedItems($scope.selectedItems);
				angular.element($event.currentTarget).addClass("highlight");
			}
			$scope.currentItem = item;
		};
		
		$scope.nextPage = function(){
			getItems();
		};
		
		$scope.deleteCurrentItem = function(){
			coreService.Item.delete({type:$scope.selectedType.option, id:$scope.currentItem.id}, function() {
				$scope.items.splice($scope.items.indexOf($scope.currentItem), 1);
				$scope.selectedItems.splice($scope.selectedItems.indexOf($scope.currentItem), 1);
				$scope.currentItem = null;
				$("#delete_item_modal").modal("hide");
				checkPages();
				//getItems();
			});
		};
		
		$scope.$on("unselectItems", function() {
			$scope.selectedItems.length = 0;
			$(".superbox-list").removeClass("highlight");
		});
		
		$scope.$watch("selectedType", function(newValue, oldValue){
			reset();
			getItems();
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
		
		var bind = function(){
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
					$state.go("app.core.models", {
						"type":$scope.selectedType
						//~ "model_id":$scope.selectedModel
					});
				});
			}
		};
		
    });
    
});
