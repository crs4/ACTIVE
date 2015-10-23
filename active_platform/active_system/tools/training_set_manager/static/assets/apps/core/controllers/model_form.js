define(["core/module"], function(module){

	"use strict";

	module.registerController("modelFormCtrl", function($scope, $state, coreService){

		$scope.selected = [];
		$scope.currentElement = {};

		$scope.$on("scrollbarSelection", function(event, attrs){
			$scope.selected = attrs.selected;
		});

		$scope.$watchCollection("selected", function(newValue, oldValue){
			if(newValue[0]){
				$scope.currentElement.entity = newValue[0].id;
				$scope.currentElement.name = newValue[0].first_name + " " + newValue[0].last_name;
			}
		});

		$scope.save = function(model){
			if($scope.currentElement.entity && $scope.currentElement.type){
				new coreService.Model(model).$save().then(function(newModel){
					$state.go("app.core.models", {"type":$scope.currentElement.type});
				});
			}
		};

	});

});
