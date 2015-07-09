define(["layout/module"], function(module){

	module.registerController("advancedSearchCtrl", function($scope, $rootScope, coreService, Mediator){
	
			$scope.scrollbarPage = 1;
			$scope.hasNextPage = true;
			$scope.elements = [];
			$scope.selected = [];
			
			$scope.$on("search_entity", function(event, args){
				reset();
				init(args);
			});
			
			$scope.doSearch = function(){
				var dict = {};
				dict = angular.copy($scope.context, dict);
				dict.filter_by.params.selected = $scope.selected;
				if(dict.filter_by.params.selected.length > 0)
					$rootScope.$broadcast("search_context", dict);
				$scope.closeModal();
			};

			$scope.$watchCollection("selected", function(newValue, oldValue){
				Mediator.mediateEnableSummarizer(newValue);
			});

			angular.element("#search_modal").on("show.bs.modal", function(e){
				reset();
			});

			//HANDLERS
			
			var myService = angular.element("#search-entity").attr("scrollbar-service");
			
			var parseParams = function(params, page){
				var dict = {};
				for(var key in params)
					dict[key] = params[key];
				dict["page"] = page;
				return dict;
			};
			
			var init = function(context){
				var params = parseParams(context.filter_by.params, $scope.scrollbarPage);
				//$scope.elements = coreService[myService].query(parseParams(params, $scope.scrollbarPage));
				var p = coreService[myService].query(parseParams(params, $scope.scrollbarPage));
				//$scope.elements.$promise.then(function (result) {
				p.$promise.then(function (result) {
					//$scope.elements = result.results;//RICERCA INESATTA - RISULTATI PAGINATI
					$scope.elements.push(result);//RICERCA NON PAGINATA
					angular.element("#search-entity").mCustomScrollbar({
						theme: "rounded-dark",
						scrollInertia: 300,
						scrollEasing: "linear",
						scrollButtons: {
							enable: true
						},
						advanced: {
							updateOnContentResize: true
						},
						callbacks: {
							onTotalScroll: function() {
								next(context);
							}
						}
					});
					if(result.next !== null){
						$scope.scrollbarPage += 1;
					} else {
						$scope.hasNextPage = false;
					}
				});
			};
			
			var next = function (context) {
				if($scope.hasNextPage){
					var params = parseParams(context.filter_by.params, $scope.scrollbarPage);
					var e = coreService[myService].query(params, function(){
						$scope.elements = $scope.elements.concat(e.results);
						if(e.next !== null){
							$scope.scrollbarPage += 1;
						} else {
							$scope.hasNextPage = false;
						}
					});
				}
			};

			var reset = function(){
				$scope.scrollbarPage = 1;
				$scope.hasNextPage = true;
				$scope.elements.length = 0;
				$scope.selected.length = 0;
			};
			
	});
	
});

