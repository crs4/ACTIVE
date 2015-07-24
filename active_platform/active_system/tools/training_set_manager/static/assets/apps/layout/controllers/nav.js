define(["layout/module"], function(module){
	
	module.registerController("navCtrl", function($scope){
		
		$scope.types = [{"option":"video"}, {"option":"audio"}];
		
	});
	
});
