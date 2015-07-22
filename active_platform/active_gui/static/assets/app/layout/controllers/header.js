define(["layout/module"], function(module){

	module.registerController("headerCtrl", function($scope){
		
		angular.element(".dropdown-toggle").click(function(e) {
			e.preventDefault();
			e.stopPropagation();
			return false;
		});
	
	});

});

