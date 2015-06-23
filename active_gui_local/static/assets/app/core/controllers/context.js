define(["core/module", "appConfig"], function(module){
	
	"use strict";
		
	module.registerController("contextMenuCtrl", function($scope, $window, $document, $stateParams, $http){
		
		var menu   = $("div.context-menu");
		var active = "context-menu_active";
		
		$scope.selectedType = $stateParams.type;
		
		$window.onkeyup = function (event) {
			if (event.keyCode === 27) {
				menu.removeClass(active);
			}
		};
		
		$window.onresize = function (event) {
			menu.removeClass(active);
		};
		
		$document.onclick = function (event) {
			menu.removeClass(active);
		};
		
		$scope.$on("loadedScripts", function(event, args) {
			var scripts = [];
			for (var i = 0; i < args.loadedScripts.length; i++) {
				for (var j = 0; j < args.loadedScripts[i].scripts.length; j++) {
					var type = args.loadedScripts[i].scripts[j].item_type;
					if(type.indexOf($scope.selectedType) != -1)
						scripts.push(args.loadedScripts[i].scripts[j]);
					}
			}
			$scope.scripts = scripts;
		});
		
		$scope.$on("contextMenu", function(event, args){
			$scope.widgetContextModel = args.widgetContextModel;
		});
		
		$scope.launchScript = function(event, scriptId){
			event.preventDefault();
			if($scope.widgetContextModel && scriptId){
				$window.open(appConfig.jobmonitorBaseUrl, "_blank");
				var url = appConfig.coreApiUrl + "triggers/script/" + scriptId + "/";
				$http.post(url, {"auth_params":{}, "func_params":$scope.widgetContextModel}).then(function(response){
					$scope.widgetContextModel = null;
					menu.removeClass(active);
				});
			}
		};
		
	});
	
});
