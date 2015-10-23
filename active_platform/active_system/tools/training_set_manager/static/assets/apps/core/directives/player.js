define(["core/module", "mcustom-scrollbar", "appConfig"], function(module){

	"use strict";

	module.registerDirective("widgetPlayer", function($sce, $timeout){

		return {
			restrict: "AE",
			templateUrl: "/static/assets/apps/core/templates/player.html",
			controller: function($scope){

				$scope.api = null;
				$scope.currentInstance = 0;
				$scope.assets = [];
				$scope.selected = [];

				$scope.config = {
					preload: "auto",
					autoPlay: false,
					sources: $scope.assets,
					theme: {
						url: "/static/assets/plugins/videogular/videogular.min.css"
					},
					plugins: {
						poster: "/static/assets/theme/img/audio.jpg"
					}
				};

				/**
				 * Called every time a new instance page has been loaded.
				 **/				
				$scope.init = function(instances){
					$scope.assets.length = 0;
					angular.forEach(instances, function(instance){
						populateSource(instance);
					});
					//if($scope.assets.length > 0)
					//	$scope.config.sources = $scope.assets[0].sources;
				};

				$scope.onPlayerReady = function(api) {
					$scope.api = api;
				};

				/*$scope.onCompleteInstance = function() {
					$scope.isCompleted = true;
					$scope.currentInstance ++;
					if ($scope.currentInstance >= $scope.assets.length) 
						$scope.currentInstance = 0;
					$scope.getInstance($scope.currentInstance);
				};*/

				$scope.$watch("items", function(newValue, oldValue){
					if(newValue){
						if(angular.isArray(newValue) && newValue.length > 0)
							$scope.init(newValue);
					}
				});

				$scope.$watch("currentItem", function(newValue, oldValue){
					if(newValue){
						var indexes = $.map($scope.assets, function(obj, index) {
							if(obj.id == newValue.id) {
								return index;
							}
						});
						if(indexes.length > 0){
							$scope.getInstance(indexes[0]);
						}
					}
				});

				$scope.$on("scrollbarSelection", function(event, attrs){
					$scope.selectItems(attrs.selected);
				});

				$scope.$on("unselectItems", function() {
					$scope.selectedItems.length = 0;
					$scope.selected.length = 0;
					downlightTrack();
					$scope.api.stop();
				});

				$scope.getInstance = function(index) {
					$scope.api.stop();
					$scope.currentInstance = index;
					$scope.config.sources  = $scope.assets[index].sources;
					highlightTrack(index);
                			//$timeout($scope.api.play.bind($scope.api), 100);
				};

				/**
				 * HANDLER FUNCTIONS
				 **/

				var populateSource = function(source) {
					var url = appConfig.apiUrl + "instances/file/" + source.id + "/?type=feature";
					var tpl = [{src: $sce.trustAsResourceUrl(url), type: "audio/mp3"},
						  {src: $sce.trustAsResourceUrl(url), type: "audio/ogg"}];
					$scope.assets.push({id:source.id, sources:tpl});
				};

				var highlightTrack = function(index) {
					$("#player_items span").css("color", "#404040");
					$("#track_" + index + " > span").css("color", "#33cc33");
				};

				var downlightTrack = function() {
					$("#player_items span").css("color", "#404040");
				};

			}
		}
	});

});
