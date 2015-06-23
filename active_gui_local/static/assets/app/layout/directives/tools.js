define(["layout/module"], function (module) {

    "use strict";

    module.registerDirective("navTools", function (coreService) {
		
        return {
            restrict: "A",
            templateUrl: "/assets/app/layout/templates/tools.html",
            link: function (scope, element) {
                element.removeAttr("nav-tools");
				
				var t = coreService.Tool.query(function(){
					if(angular.isObject(t)){
						scope.tools = Object.keys(t);
					}
				});
            }
        }
        
    });

});



