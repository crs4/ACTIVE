define(["layout/module"], function(module){

	module.registerController("searchCtrl", function($scope, $rootScope, $state){
		
		$scope.context = {"action":"search_none", "filter_by":{}};
		$scope.entity = "default";
		
		$scope.showOptions = function(event){
			event.preventDefault();
			angular.element("#search_modal").modal({show:true});
		};

		angular.element("#search_modal").on('show.bs.modal', function (e) {
			$scope.entity = "person";
			$scope.context.action = "search_none";
		});

		angular.element("#search_modal").on('hide.bs.modal', function (e) {
			$scope.entity = "default";
		});
		
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
		
		$scope.$watch("context", function(newValue, oldValue){
			if($scope.context.name)
				$rootScope.$broadcast("search_context", newValue);
		}, true);

		$scope.$watch("entity", function(newValue, oldValue){
			$scope.context.filter_by.entity = newValue;// = {"entity":$scope.entity, "params":{}};
		});

		/**
		*	HANDLERS
		**/

		var hasOwnProperty = Object.prototype.hasOwnProperty;

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
		
		var isEmpty = tco(function(obj) {
			if (obj == null) return true;

			for (var key in obj) {
				if (typeof obj[key] == "object") {
					isEmpty(obj[key]);
				} else if (hasOwnProperty.call(obj, key) && obj[key].length === 0) {
					return true;
				}
			}

			return false;
		});

		var initContext = function(action){
			//var dict = {};
			//console.log($scope.searchParams);
			if(isEmpty($scope.searchParams))
				//dict.action = "search_none";
				$scope.context.action = "search_none";
			else $scope.context.action = action;//dict.action = action;
			//if($scope.entity)
			//	dict["filter_by"] = {"entity": $scope.entity};
			//else dict["filter_by"] = {"entity": "default"};
			//dict["filter_by"]["params"] = $scope.searchParams;
			$scope.context.filter_by.params = $scope.searchParams;
			//$scope.context = dict;
		};
		
	});
	
});
