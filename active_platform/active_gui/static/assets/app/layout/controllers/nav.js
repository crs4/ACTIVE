define(["layout/module"], function(module){
	
	module.registerController("navCtrl", function($scope){
		
		$scope.types = [{"option":"image"}, {"option":"video"}, {"option":"audio"}];
		
	});
	
});
