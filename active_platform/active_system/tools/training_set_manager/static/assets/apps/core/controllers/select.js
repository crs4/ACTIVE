define(["core/module", "appConfig"], function(module){

	module.registerController("selectCtrl", function($scope, $stateParams, coreService){
		var m = coreService.Model.query({type:$stateParams.type}, function(){
			$scope.models = m.results;
		});
	});

});
