define(["core/module"], function(module){
	
	"use strict";
		
	module.registerController("elementCtrl", function($scope, $location, $stateParams, $timeout, Mediator){
		
		$scope.service = null;
		$scope.currentElement = null;
		$scope.createStatus = false;
		
		$scope.createElement = function(element, redirect){
			new $scope.service(element).$save().then(function(newElement){
				$location.path("/" + redirect);
			});
		};
		
		$scope.updateElement = function(element, redirect){
			$scope.service.update({id:element.id}, element, function(newElement){
				$location.path("/" + redirect);
			});
		};
		
		$scope.saveEdit = function(element, redirect){
			if(angular.isDefined(element.id))
				$scope.updateElement(element, redirect);
			else $scope.createElement(element, redirect);
		};
		
		$scope.backList = function(redirect){
			$location.path("/" + redirect);
		};
		
		$scope.getElement = function(service) {
			$scope.service = service;
			if($stateParams.id !== "new") {
				$scope.service.get({id:$stateParams.id}).$promise.then(function(element){
					$scope.currentElement = element;
				});
			} else {
				$scope.createStatus = true;
				$scope.currentElement = {};
			}
		};
		
		$scope.$watch("currentElement", function(newVal, oldVal){
			if(newVal){
				$timeout(function(){
					Mediator.mediateElementReady($scope.currentElement);
				}, 300);
			}
		});
		
	});
	
});
