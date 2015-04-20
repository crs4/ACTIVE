angular.module("coreServices")
.directive("smartSelect2", function(){
	
	"use strict";
	
	return {
		restrict: "A",
		templateUrl: "/assets/js/core/views/plugins.html",
		compile: function (element, attributes) {
			element.removeAttr("smart-select2 data-smart-select2");
			element.find('.form-select').select2({placeholder:"Actions", allowClear:true});
		}
	}
        
})
.directive("activeMediaPlayer", function(coreUrl){
	
	"use strict";
	
	return {
		restrict: "A",
		controller: function ($scope, $sce) {
			
			$scope.api = null;
			
			$scope.assets = [
				{
					sources:[
						{src: $sce.trustAsResourceUrl(coreUrl + "/api/items/file/" + $scope.currentItem.id + "/?type=original"), type: "video/mp4"},
						{src: $sce.trustAsResourceUrl(coreUrl + "/api/items/file/" + $scope.currentItem.id + "/?type=original"), type: "video/ogg"},
						{src: $sce.trustAsResourceUrl(coreUrl + "/api/items/file/" + $scope.currentItem.id + "/?type=original"), type: "video/webm"}
					]
				}
			];

			console.log($scope.assets[0].sources);
			
			$scope.onPlayerReady = function(API) {
				console.log("SET API");
				$scope.api = API;
			};

			$scope.onClosePlayer = function(){
				if($scope.api) {
					$scope.api.stop();
					$scope.api = null;
				}
			};
			
			$scope.config = {
				preload: "metadata",
				autoPlay: false,
				sources: $scope.assets[0].sources,
				theme: {
					url: "/assets/plugins/angular/css/videogular/videogular.css"
				},
				plugins: {
					//poster: coreurl + "/api/items/files/" + $scope.currentItem.id + "/?type=thumb",
					controls: {
						autoHide: true,
						autoHideTime: 3000
					}
				}
			};
			
			$scope.onClickReplay = function() {
				$scope.api.play();
			};
			
			$scope.setVideo = function(index) {
				$scope.api.stop();
				$scope.config.sources = $scope.assets[index].sources;
			};
			
		},
		templateUrl: function(element, attribute){
			if(element.hasClass("audio"))
				return "/assets/js/core/views/media_audio.html";
			return "/assets/js/core/views/media_video.html";
		}
	}
	
})
.directive("userSummary", function(){
	
	return {
		restrict: "E",
		templateUrl: "/assets/js/core/views/users.html",
		controller: function($scope, $location, userService){
			
			$scope.deleteUser = function(user){
				userService.User.delete({"id":user.id}, function(){
					$scope.users.splice($scope.users.indexOf(user), 1);
				});
			};
			
			$scope.editOrCreate = function(id){
				var p = id ? "/users/" + id : "/users/new";
				$location.path(p);
			};
			
			var users = userService.User.query(function(){
				$scope.users = users;
			});
			
		}
	}
	
})
.directive("groupSummary", function(){
	
	return {
		restrict: "E",
		templateUrl: "/assets/js/core/views/groups.html",
		controller: function($scope, groupService){
		
			$scope.getGroup = function(id){
				$location.path("/groups/" + id);
			};
			
			$scope.deleteGroup = function(group){
				group.$delete().then(function(){
					$scope.groups.splice($scope.groups.indexOf(group), 1);
				});
			};
			
			var groups = groupService.Group.query(function(){
				$scope.groups = groups;
			});
			
		}
	}
	
})
.directive("itemSummary", function(coreUrl){
	
	return {
		restrict: "AE",
		templateUrl: "/assets/js/core/views/items.html",
		controller: function($scope, $http, $q, $location, $compile, $window, itemService, pluginService, scriptService){

			$scope.items = [];
			
			$scope.plugins = [];
			
			$scope.selectedItems = [];
			
			$scope.types = [{'option':'image'}, {'option':'video'}, {'option':'audio'}];
			
			$scope.selectedType = $scope.types[0];
			
			$scope.selectedScript = null;

			$scope.busy = false;

			$scope.page = 1;
			
			$scope.selectItem = function ($event, item) {
				var unique = true;
				for(var i = 0; i < $scope.selectedItems.length; i++){
					if($scope.selectedItems[i].id === item.id){
						unique = false;
						$scope.selectedItems.splice(i, 1);
						angular.element($event.currentTarget).removeClass("highlight");
						break;
					}
				}
				if(unique){
					$scope.selectedItems.push(item);
					angular.element($event.currentTarget).addClass("highlight");
				}
				$scope.currentItem = item;
				itemDetails($event);
			};

			$scope.unselectItems = function() {
				//$scope.selectedItems.length = 0;
				//$('.superbox-list').removeClass("highlight");
				for(var i = 0; i < $scope.selectedItems.length; i++){
					$scope.deleteItem($scope.selectedItems[i]);
				}
				$scope.selectedItems.length = 0;
			};
			
			$scope.nextPage = function(){
				getItems();
			};
			
			$scope.uploadItem = function(){
				$location.path("/items/upload");
			};
			
			$scope.deleteItem = function(item){
				itemService.Item.delete({id:item.id, type:$scope.selectedType.option}, function(){
					$scope.selectedItems = $scope.selectedItems.splice($scope.items.indexOf(item), 1);
					$scope.items.splice($scope.items.indexOf(item), 1);
					$('#myModal').modal('hide');
				});
			};
			
			$scope.$watch("selectedType", function(newValue, oldValue){
				$scope.items.length = 0;
				$scope.page = 1;
				$scope.busy = false;
				$scope.selectedItems.length = 0;
				$scope.currentItem = null;
				$scope.selectedScript = null;
				getItems();
			});
			
			var s = scriptService.Script.query(function(){
				$scope.plugins = parseScripts(s);
			});

			var parseScripts = function(scripts){
				var plugins = [];
				for(var i = 0; i < scripts.length; i++){
					var p = scripts[i].plugin;
					p["scripts"] = [];
					plugins.push(p);
				}
				for(var i = 1; i < plugins.length;){
					if(plugins[i-1].id === plugins[i].id){
						plugins.splice(i, 1);
					} else {
						i++;
					}
				}
				for(var i = 0; i < plugins.length; i++){
					for(var j = 0; j < scripts.length; j++){
						if(plugins[i].title === scripts[j].plugin.title){
							plugins[i].scripts.push(scripts[j]);
						}
					}
				}
				//TODO: eliminare plugin da ogni script
				return plugins;
			};

			var getItems =  function(){
				$scope.busy = true;
				var i = itemService.Item.query({page:$scope.page, type:$scope.selectedType.option}, function(){
					$scope.busy = false;
					$scope.items = $scope.items.concat(i.results);
					if(i.next != null){
						$scope.page += 1;
					} else {
						$scope.busy = true;
					}
				});
			};
			
			$scope.startScript = function(){
				if($scope.selectedScript && $scope.selectedItems.length > 0){
					$window.open(coreUrl + "/jobmonitor/", "_blank");
					$q.all([
						angular.forEach($scope.selectedItems, function(value, key){
							var url = coreUrl + "/api/triggers/script/" + $scope.selectedScript + "/";
							$http.post(url, {"input_dict":{}, "output_dict":value}).then(function(response){
								console.log(response);
							});
						})
					]).then(function(){
							$scope.selectedScript = null;
							angular.element(".select2").select2("val", null);
					});
				}
			};
		
			var itemDetails = function(event){
				var superbox  = angular.element('<div class="superbox-show"></div>');
				var superboximg   = angular.element('<div class="col-xs-12 col-sm-8 col-md-8 col-lg-8"><img ng-src="http://156.148.132.79:80/api/items/file/{{currentItem.id}}/?type=original" class="superbox-current-img"></div>' + 
												'<div id="imgInfoBox" class="superbox-imageinfo inline-block col-xs-12 col-sm-4 col-md-4 col-lg-4">' + 
													'<h1>{{currentItem.filename}}</h1>' + 
													'<span>' + 
														'<p><em>{{currentItem.path}}</em></p>' + 
														'<p class="superbox-img-description">Image description</p>' + 
														'<p class="superbox-img-description">FILE TYPE: {{currentItem.format}}</p>' + 
														'<p class="superbox-img-description">FILE SIZE: {{currentItem.filesize}}</p>' + 
														'<p class="superbox-img-description">IMAGE WIDTH: {{currentItem.frame_width}} px</p>' + 
														'<p class="superbox-img-description">IMAGE HEIGHT: {{currentItem.frame_height}} px</p>' +
														'<p>' + 
															'<a href="javascript:void(0);" class="btn btn-primary btn-sm">Edit Item</a>' + 
															' <a data-target="#myModal" data-toggle="modal" class="btn btn-danger btn-sm">Delete Item</a>' + 
															' <a href="javascript:void(0);" class="btn btn-warning btn-sm">Share Item</a>' +
														'</p>' + 
													'</span>' + 
												'</div>');
				var superboxclose = angular.element('<div class="superbox-close txt-color-white"><i class="fa fa-times fa-lg"></i></div>');
				var videogular    = angular.element('<div class="col-xs-12 col-sm-8 col-md-8 col-lg-8"><div class="superbox-current-img videogular-container" active-media-player></div></div>' + 
												'<div id="imgInfoBox" class="superbox-imageinfo inline-block col-xs-12 col-sm-4 col-md-4 col-lg-4">' + 
													'<h1>{{currentItem.filename}}</h1>' + 
													'<span>' + 
														'<p><em>{{currentItem.path}}</em></p>' + 
														'<p class="superbox-img-description" ng-show="currentItem.title">{{currentItem.details.title}}</p>' + 
														'<p class="superbox-img-description" ng-show="currentItem.format">FILE TYPE: {{currentItem.format}}</p>' + 
														'<p class="superbox-img-description">FILE SIZE: {{currentItem.filesize}}</p>' + 
														'<p class="superbox-img-description">FRAME WIDTH: {{currentItem.frame_width}} px</p>' + 
														'<p class="superbox-img-description">FRAME HEIGHT: {{currentItem.frame_height}} px</p>' + 
														'<p class="superbox-img-description">FRAME RATE: {{currentItem.frame_rate}}</p>' + 
														'<p>' + 
															'<a href="javascript:void(0);" class="btn btn-primary btn-sm">Edit Item</a>' +  
															' <a data-target="#myModal" data-toggle="modal" class="btn btn-danger btn-sm">Delete Item</a>' + 
															' <a href="javascript:void(0);" class="btn btn-warning btn-sm">Share Item</a>' + 
														'</p>' + 
													'</span>' + 
												'</div>');
				var audiogular    = angular.element('<div class="col-xs-12 col-sm-8 col-md-8 col-lg-8"><div class="superbox-current-img videogular-container audio" active-media-player></div></div>' + 
												'<div id="imgInfoBox" class="superbox-imageinfo inline-block col-xs-12 col-sm-4 col-md-4 col-lg-4">' + 
													'<h1>{{currentItem.filename}}</h1>' + 
													'<span>' + 
														'<p><em>{{currentItem.path}}</em></p>' + 
														'<p class="superbox-img-description" ng-show="currentItem.title">{{currentItem.details.title}}</p>' + 
														'<p class="superbox-img-description">FILE TYPE: {{currentItem.format}}</p>' + 
														'<p class="superbox-img-description">FILE SIZE: {{currentItem.filesize}}</p>' + 
														'<p class="superbox-img-description">AUDIO BITRATE: {{currentItem.audioBitrate}}</p>' + 
														'<p>' + 
															'<a href="javascript:void(0);" class="btn btn-primary btn-sm">Edit Item</a>' +  
															' <a data-target="#myModal" data-toggle="modal" class="btn btn-danger btn-sm">Delete Item</a>' + 
															' <a href="javascript:void(0);" class="btn btn-warning btn-sm">Share Item</a>' +
														'</p>' + 
													'</span>' + 
												'</div>');							
				
				switch($scope.selectedType.option){
					case "image": superbox.append(superboximg).append(superboxclose); break;
					case "video": superbox.append(videogular).append(superboxclose); break;
					case "audio": superbox.append(audiogular).append(superboxclose); break;
				}
				
				var elm = angular.element(event.currentTarget);
				var currentimg = elm.find('.superbox-img');
				
				$('.superbox-list').removeClass('active');
				
				if ($('.superbox-current-img').css('opacity') == 0) {
					$('.superbox-current-img').animate({opacity: 1});
				}
				
				var sl = angular.element("div.superbox").find(".superbox-show");
				
				if (sl.length != 0) {
					$('.superbox-list').removeClass('active');
					if($scope.selectedType.option != 'image')
						$scope.onClosePlayer();
					var prev = sl.prev();
					sl.detach();
					if (!angular.equals(elm.attr("id"), prev.attr("id")) && elm.hasClass("highlight")) {
						superbox.insertAfter(elm).css('display', 'block');
						elm.addClass('active');
						$compile(superbox)($scope);
					}
				} else if(elm.hasClass("highlight")){
					superbox.insertAfter(elm).css('display', 'block');
					elm.addClass('active');
					$compile(superbox)($scope);
				}
				
				$('html, body').animate({
					scrollTop:superbox.position().top - currentimg.width()
				}, 'medium');
				
				$('.superbox').on('click', '.superbox-close', function() {
					$('.superbox-list').removeClass('active');
					if($scope.selectedType.option != 'image')
						$scope.onClosePlayer();
					$('.superbox-current-img').animate({opacity: 0}, 200, function() {
						$('.superbox-show').slideUp();
						angular.element("div.superbox").find(".superbox-show").detach();
					});
				});

			};
			
		}
	}
	
});
