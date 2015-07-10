define(["core/module", "appConfig"], function(module){
	
	"use strict";
		
	module.registerController("tableCtrl", function($scope, $state){
		
		$scope.gridOptions = { 
			pageSize: appConfig.tablePageSize,
			numberOfPages: 1,
			rowCollection: [],
			currentPage: 1
		};
		
		$scope.getPage = function(page){
			for(var i = 0; i < $scope.pageArray.length; i++){
				if($scope.pageArray[i].current == page){
					$scope.pageArray[i].active = true;
					$scope.gridOptions.currentPage = page;
				} else {
					$scope.pageArray[i].active = false;
				}
			}
		};
		
		$scope.getPrevPage = function(){
			if($scope.gridOptions.currentPage > 1)
				$scope.getPage($scope.gridOptions.currentPage - 1);
		};
		
		$scope.getNextPage = function(){
			if($scope.gridOptions.currentPage < $scope.gridOptions.numberOfPages)
				$scope.getPage($scope.gridOptions.currentPage + 1);
		};
		
		$scope.$on("fetchPage", function(event, args){
			var data = args.service.query({page:$scope.gridOptions.currentPage}, function(){
			//var data = args.service.query({item_number:appConfig.tablePageSize}, function(){
				$scope.gridOptions.rowCollection = data.results;
				$scope.gridOptions.numberOfPages = Math.ceil(data.count / appConfig.tablePageSize);
				$scope.gridOptions.totalItems = data.count;
			});
		});
		
		$scope.$on("removeRow", function(event, args){
			args.service.delete({"id":args.row.id}, function(){
				$state.reload(); //TO DO: CHECK SE ELIMINO ULTIMO ELEMENTO IN CURRENT_PAGE
			});
		});
		
		$scope.$watch("gridOptions.numberOfPages", function(newVal, oldVal){
			var ret = [];
			for(var i = 1; i <= newVal; i++){
				if(i == 1)
					ret.push({"current":i, "active":true});
				else ret.push({"current":i, "active":false});
			}
			$scope.pageArray = ret;
		});
		
	});
	
});
