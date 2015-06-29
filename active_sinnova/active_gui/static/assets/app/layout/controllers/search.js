define(["layout/module"], function(module){

	module.registerController("searchCtrl", function($scope, $rootScope, $state){
		
		$scope.context = {"action":"search_none", "filter_by":{}};
		$scope.entity = "default";

		$scope.showAdvancedOptions = function(event){
			event.preventDefault();
			angular.element("#search_modal").modal("show");
			$scope.entity = "people";
		};
		
		$scope.search = function(){
			switch($state.current.name){
				case "app": break;
				case "app.core.items": 
					initContext("search_items");
					break;
				case "app.core.users": 
					initContext("search_users");
					break;
				case "app.core.group": 
					initContext("search_group");
					break;
				default: 
					initContext("search_none");
					break;
			}
		};

		$scope.closeModal = function(){
			angular.element("#search_modal").modal("hide");
			$scope.entity = "default";
		};

		$scope.searchReset = function(){
			if($state.current.name === "app.core.items")
				$state.reload();
		};

		$scope.searchSimple = function(){
			if($scope.context.action && $scope.context.action !== "search_none")
				if($scope.context.filter_by.entity === "default")
					$rootScope.$broadcast("search_context", $scope.context);
		};
		
		$scope.$watch("context", function(newValue, oldValue){
			if($scope.context.action && $scope.context.action !== "search_none")
				if($scope.context.filter_by.entity !== "default")
					$rootScope.$broadcast("search_entity", $scope.context);
				//if($scope.context.filter_by.entity === "default")
				//	$rootScope.$broadcast("search_context", $scope.context);
				//else
				//	$rootScope.$broadcast("search_entity", $scope.context);
		}, true);

		$scope.$watch("entity", function(newValue, oldValue){
			initParameters();
			$scope.search();
		});

		/**
		*	HANDLERS
		**/

		var initParameters = function(){
			switch($scope.entity){
				case "people":
					$scope.searchParams = {first_name:"", last_name:""};
					break
				default:
					$scope.searchParams = {};
					break;
			}
		};

		var hasOwnProperty = Object.prototype.hasOwnProperty;

		function hasNoFields(obj) {
			for(var key in obj) {
				if(obj.hasOwnProperty(key))
					return false;
			}
			return true;
		};

		function tco(f) {
			var value;
			var active = false;
			var accumulated = [];

			return function accumulator() {
				accumulated.push(arguments);

				if (!active) {
					active = true;

					while (accumulated.length) {
						value = f.apply(this, accumulated.shift());
					}

					active = false;

					return value;
				}
			}
		};
		
		$scope.isEmpty = tco(function(obj) {
			if (obj == null || hasNoFields(obj)) 
				return true;

			for (var key in obj) {
				if (typeof obj[key] == "object") {
					$scope.isEmpty(obj[key]);
				} else if (hasOwnProperty.call(obj, key) && obj[key].length === 0) {
					return true;
				}
			}

			return false;
		});

		var initContext = function(action){
			var dict = {};
			if($scope.isEmpty($scope.searchParams))
				dict.action = "search_none";
			else dict.action = action;
			dict.filter_by = {"entity":$scope.entity}
			dict.filter_by.params = $scope.searchParams;
			$scope.context = dict;
		};
		
	});
	
});
