define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerDirective("widgetPlayer", function ($sce, $localStorage) {
		
        return {
			
            restrict: "A",
            controller: function ($scope) {
                
				$scope.api = null;
				
				var url = appConfig.coreApiUrl + "items/file/" + $scope.currentItem.id + "/?type=preview";
			
				$scope.assets = [
					{
						sources:[
							{src: $sce.trustAsResourceUrl(url), type: "video/mp4"},
							{src: $sce.trustAsResourceUrl(url), type: "video/ogg"},
							{src: $sce.trustAsResourceUrl(url), type: "video/webm"}
						]
					},{
						sources:[
							{src: $sce.trustAsResourceUrl(url), type: "audio/mp3"},
							{src: $sce.trustAsResourceUrl(url), type: "audio/ogg"}
						]
					}
					
				];
				
				$scope.onPlayerReady = function(API) {
					$scope.api = API;
					$scope.$emit("mediaPlayer", $scope.api);
				};
				
				$scope.config = {
					preload: "auto",
					autoPlay: false,
					sources: $scope.assets[$scope.selectedType === "video" ? 0 : 1].sources,
					theme: {
						url: "/assets/plugins/angular/css/videogular/videogular.css"
					},
					plugins: {
						controls: {
							autoHide: true,
							autoHideTime: 3000
						}
					}
				};

            },
            templateUrl: function(element, attribute){
				if(element.hasClass("audio"))
					return "/assets/app/core/templates/media_audio.html";
				return "/assets/app/core/templates/media_video.html";
			}
        }
        
    });

});


