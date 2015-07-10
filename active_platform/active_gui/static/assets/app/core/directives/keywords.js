define(["core/module"], function(module){
	
	module.registerDirective("widgetKeywords", function(coreService){
		
		return {
			
			restrict: "EA",
			templateUrl: "/assets/app/core/templates/keywords.html",
			controller: function($scope, $element){
				$element.removeAttr("widget-keywords");
				var k = coreService.KeywordItem.query({item_id:$scope.currentItem.id}, function(){
					var ret = [];
					k.forEach(function(obj){
						if(ret.indexOf(obj["description"]) === -1)
							ret.push(obj["description"]);
					});
					$scope.keywords = ret;
				});
			}
			
		}
	
	});

});

