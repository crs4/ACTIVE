define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerController("modelCtrl", function ($scope, $location, $stateParams, $state, coreService) {
		
		$scope.models = [];
		$scope.busy = false;
		$scope.page = 1;
		$scope.context = {name:"search_none", params:""};
		$scope.selectedType = $stateParams.type;
		
		$scope.selectModel = function ($event, model) {
			$state.go("app.core.models.details", {"type":$scope.selectedType, "model_id":model.id});
		};
		
		$scope.nextPage = function(){
			getModels();
		};
		
		$scope.changeModelName = function(new_name, model){
			model.name = new_name;
			model.model_file = undefined;
			coreService.Model.update({"id":model.id}, model, function(){
				$state.reload();
			});
		};

		$scope.centerPopover = function(model_id, index){
			var adjust = 0;
			if(index % 8 === 0){
				adjust -= 47;
			}            
			var el = angular.element.find("a#editable_" + model_id);
			var width = angular.element(el).parent().width();
			var centerX = adjust + angular.element(el).parent().prop('offsetLeft') + width / 2;
			$(".item-wrapper form").css("margin-left",  -centerX);
		};
		
		$scope.$watch("selectedType", function(newValue, oldValue){
			reset();
			getModels();
		});
		
		$scope.$on("search_context", function(event, args){
			$scope.context = args;
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
			$scope.currentModel = null;
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
