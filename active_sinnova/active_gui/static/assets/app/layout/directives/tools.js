define(["layout/module"], function (module) {

    "use strict";

    module.registerDirective("navTools", function (coreService) {
		
        return {
            restrict: "A",
            templateUrl: "/assets/app/layout/templates/tools.html",
            controller: function ($scope, $element) {
                $element.removeAttr("nav-tools");

		$scope.summarizerParam = 0;
		$scope.navigatorParam  = 0;

		$scope.$on("enable_summarizer", function(event, args){
			if(args.personList.length > 0)
				$scope.summarizerParam = args.personList[0].id;
		});

		$scope.$on("enable_navigator", function(event, args){
			if(args.itemId === 0){
				$scope.navigatorParam = args.itemId;
				$scope.$applyAsync();
			}
			$scope.navigatorParam = args.itemId;
		});

		var t = coreService.Tool.query(function(){
			if(angular.isObject(t)){
				var ret = [];
				Object.keys(t).forEach(function(key){
					if(key.charAt(0) !== "$")
						ret.push(key);
				});
				$scope.tools = ret;
			}
		});

            }
        }
        
    });

});



