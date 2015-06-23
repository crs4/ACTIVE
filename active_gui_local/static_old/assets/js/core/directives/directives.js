angular.module("coreApp")
.directive("pageSettings", function(){
	
	"use strict";
	
	return {
		restrict: "A",
		compile: function(element, attributes) {
			element.removeAttr('smart-device-detect data-smart-device-detect');
			var isMobile = (/iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()));
			element.toggleClass('desktop-detected', !isMobile);
			element.toggleClass('mobile-detected', isMobile);
			
			$('#main').resize(function() {
				var main_height = $('#main').height();
				var left_panel_height = $('#left-panel').height();
				var window_height = $(window).height() - 49;

				if (main_height > window_height) {
					$('#left-panel').css('min-height', main_height + 'px');
					$('body').css('min-height', main_height + 49 + 'px');

				} else {
					$('#left-panel').css('min-height', window_height + 'px');
					$('body').css('min-height', window_height + 'px');
				}
			});
			
		}
	}
	
})
.directive("navSettings", function(){
	
	"use strict";
	
	return {
		restrict: "A",
		compile: function(element, attributes) {
			
			$('nav').resize(function() {
				var main_height = $('#main').height();
				var left_panel_height = $('#left-panel').height();
				var window_height = $(window).height() - 49;

				if (main_height > window_height) {
					$('#left-panel').css('min-height', main_height + 'px');
					$('body').css('min-height', main_height + 49 + 'px');

				} else {
					$('#left-panel').css('min-height', window_height + 'px');
					$('body').css('min-height', window_height + 'px');
				}
			});
			
			$('.minifyme').click(function(e) {
				$('body').toggleClass("minified");
				e.preventDefault();
			});
			
		}
	}
	
});

angular.module("coreServices")
.directive("smartSelect2", function(){
	
	"use strict";
	
	return {
		restrict: "A",
		templateUrl: "/assets/js/core/views/plugins.html",
		compile: function (element, attributes) {
			element.removeAttr("smart-select2 data-smart-select2");
			element.find('.form-select').select2();
		}
	}
        
})
.directive("activeMediaPlayer", function(){
	
	"use strict";
	
	return {
		restrict: "A",
		controller: function ($scope, $sce) {
			
			$scope.api = null;
			
			$scope.assets = [
				{
					sources:[
						{src: $sce.trustAsResourceUrl("http://localhost:8080/api/public/stream/" + $scope.currentItem._id + "/" + $scope.currentItem.filename), type: "video/mp4"},
						{src: $sce.trustAsResourceUrl("http://localhost:8080/api/public/stream/" + $scope.currentItem._id + "/" + $scope.currentItem.filename), type: "video/ogg"},
						{src: $sce.trustAsResourceUrl("http://localhost:8080/api/public/stream/" + $scope.currentItem._id + "/" + $scope.currentItem.filename), type: "video/webm"}
					]
				},{
					sources:[
						{src: $sce.trustAsResourceUrl("http://localhost:8080/api/public/stream/" + $scope.currentItem._id + "/" + $scope.currentItem.filename), type: "audio/mp3"},
						{src: $sce.trustAsResourceUrl("http://localhost:8080/api/public/stream/" + $scope.currentItem._id + "/" + $scope.currentItem.filename), type: "audio/ogg"}
					]
				}
				
			];
			
			$scope.onCloseMedia = function(){
				if($scope.api) {
					$scope.api.stop();
					$scope.api = null;
				}
			};
			
			$scope.onPlayerReady = function(API) {
				$scope.api = API;
			};
			
			$scope.onUpdateState = function(state){
				console.log("CURRENT STATE: " + state);
			};
			
			$scope.onChangeSource = function(s){
				console.log("CURRENT SOURCE: " + s);
			};
			
			$scope.onError = function(event){
				console.log("ERROR EVENT: " + event);
			};
			
			$scope.config = {
				preload: "auto",
				autoPlay: false,
				sources: $scope.assets[$scope.selectedType.option === "video" ? 0 : 1].sources,
				theme: {
					url: "/assets/plugins/angular/css/videogular/videogular.css"
				},
				plugins: {
					//poster: "/assets/img/videogular/videogular.png",
					controls: {
						autoHide: true,
						autoHideTime: 3000
					}
				}
			};
			
			$scope.onClickReplay = function() {
				$scope.api.play();
			};
			
			$scope.setItem = function(index) {
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
.directive("imageViewer", function(){
	
	return {
		restrict: "A",
		templateUrl : "/assets/js/core/views/media_image.html",
		controller: function($scope){
			
			$scope.onCloseMedia = function(){
				console.log("onCloseMedia for images does nothing");
			};
			
			var galleryElements = angular.element.find(".my_gallery");

			for(var i = 0, l = galleryElements.length; i < l; i++) {
				galleryElements[i].setAttribute("data-pswp-uid", i+1);
				galleryElements[i].onclick = onThumbnailsClick;
			}

			var hashData = photoswipeParseHash();
			
			if(hashData.pid > 0 && hashData.gid > 0) {
				openPhotoSwipe( hashData.pid - 1 ,  galleryElements[ hashData.gid - 1 ], true );
			}
			
		}
	}
	
})
.directive("userSummary", function(){
	
	return {
		restrict: "E",
		templateUrl: "/assets/js/core/views/users.html",
		controller: function($scope, $location, userService){
			
			$scope.deleteUser = function(user){
				userService.User.delete({"id":user._id}, function(){
					$scope.users.splice($scope.users.indexOf(user), 1);
				});
			};
			
			$scope.editOrCreate = function(id){
				var p = id ? "/users/" + id : "/users/new";
				$location.path(p);
			};
			
			var users = userService.User.query(function(){
				$scope.users = users.data.data;
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
				$scope.groups = groups.data.groups;
			});
			
		}
	}
	
})
.directive("itemSummary", function(){
	
	return {
		restrict: "AE",
		templateUrl: "/assets/js/core/views/items.html",
		controller: function($scope, $http, $location, $compile, $window, itemService, pluginService){
			
			$scope.items = [];
			
			$scope.plugins = [];
			
			$scope.selectedItems = [];
			
			$scope.selectedScript = null;
			
			$scope.types = [{'option':'image'}, {'option':'video'}, {'option':'audio'}];
			
			$scope.selectedType = $scope.types[0];
			
			$scope.latestId = '-';
			
			$scope.busy = false;
			
			$scope.pages = 0;
			
			$scope.selectItem = function ($event, item) {
				var unique = true;
				for(var i = 0; i < $scope.selectedItems.length; i++){
					if($scope.selectedItems[i]._id === item._id){
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
				$scope.selectedItems.length = 0;
				$(".superbox-list").removeClass("highlight");
			};
			
			$scope.nextPage = function(){
				getItems();
			};
			
			$scope.uploadItem = function(){
				$location.path("/items/upload");
			};
			
			$scope.deleteItem = function(item){
				item.$delete().then(function(){
					$scope.items.splice($scope.items.indexOf(item), 1);
				});
			};
			
			$scope.$watch("selectedType", function(newValue, oldValue){
				$scope.items.length = 0;
				$scope.latestId = '-';
				$scope.pages = 0;
				$scope.busy = false;
				$scope.selectedItems.length = 0;
				$scope.currentItem = null;
				$scope.selectedScript = null;
				getItems();
			});
			
			$scope.$watch("selectedScript", function(newValue, oldValue){
				if(newValue != null && $scope.selectedItems.length > 0)
					send();
			});
			
			var p = pluginService.Plugin.query(function(){
				$scope.plugins = p.data.plugins;
			});
			
			var getItems =  function(){
				$scope.busy = true;
				var i = itemService.Item.query({latestId:$scope.latestId, type:$scope.selectedType.option, pageSize:32}, function(){
					$scope.busy = false;
					$scope.items = $scope.items.concat(i.data.items);
					$scope.pages += 1;
					if($scope.pages < i.data.pages)
						$scope.latestId = i.data.items.slice(-1)[0]._id;
					else $scope.busy = true;
				});
			};
			
			var send = function(){
				console.log('SEND');
				//$http.post('http://localhost:8080/api/public/script', {"items":$scope.selectedItems, "script":$scope.selectedScript}).then(function(){
				//	$window.open("/jobmonitor", "_blank");
				//});
			};
		
			var itemDetails = function(event){
				var infobox = '<div id="imgInfoBox" class="superbox-imageinfo inline-block col-xs-12 col-sm-4 col-md-4 col-lg-4">' + 
								'<h1>{{currentItem.filename}}</h1>' + 
								'<span>' + 
									'<p><em>{{currentItem.path}}</em></p>' + 
									'<p class="superbox-img-description" ng-show="currentItem.details.title">Image description</p>' + 
									'<p class="superbox-img-description" ng-show="currentItem.details.fileType">FILE TYPE: {{currentItem.details.fileType}}</p>' + 
									'<p class="superbox-img-description" ng-show="currentItem.details.fileSize">FILE SIZE: {{currentItem.details.fileSize}}</p>' + 
									'<p class="superbox-img-description" ng-show="currentItem.details.imageWidth">FRAME WIDTH: {{currentItem.details.imageWidth}} px</p>' + 
									'<p class="superbox-img-description" ng-show="currentItem.details.imageHeight">FRAME HEIGHT: {{currentItem.details.imageHeight}} px</p>' +
									'<p class="superbox-img-description" ng-show="currentItem.details.avgBitrate">BIT RATE: {{currentItem.details.avgBitrate}}</p>' +
									'<p class="superbox-img-description" ng-show="currentItem.details.num_channels">CHANNELS: {{currentItem.details.num_channels}}</p>' +
									'<p class="superbox-img-description" ng-show="currentItem.details.sample_rate">SAMPLE RATE: {{currentItem.details.sample_rate}}</p>' +
									'<p class="superbox-img-description" ng-show="currentItem.details.visibility != null">IS VISIBILE: {{currentItem.details.visibility}}</p>' +
									'<p class="superbox-img-description" ng-show="currentItem.details.uploaded_at">UPLOADED AT: {{currentItem.details.uploaded_at | date:"yyyy-MM-dd HH:mm:ss"}}</p>' + 
									'<p>' + 
										'<a href="javascript:void(0);" class="btn btn-primary btn-sm">Edit Item</a>' + 
										' <a data-target="#myModal" data-toggle="modal" class="btn btn-danger btn-sm">Delete Item</a>' + 
										' <a href="javascript:void(0);" class="btn btn-warning btn-sm">Share Item</a>' +
										' <a href="http://localhost:8080/api/items/file/{{currentItem._id}}/?type=original" class="btn btn-success btn-sm">Download</a>' +
									'</p>' + 
								'</span>' + 
							'</div>'
				var superbox  = angular.element('<div class="superbox-show"></div>');
				var superboximg   = angular.element('<div class="col-xs-12 col-sm-8 col-md-8 col-lg-8"><div class="superbox-current-img" image-viewer></div></div>' + infobox);
				var videogular    = angular.element('<div class="col-xs-12 col-sm-8 col-md-8 col-lg-8"><div class="superbox-current-img videogular-container" active-media-player></div></div>' + infobox);
				var audiogular    = angular.element('<div class="col-xs-12 col-sm-8 col-md-8 col-lg-8"><div class="superbox-current-img videogular-container audio" active-media-player></div></div>' + infobox);
				
				var superbox_old  = angular.element('<div class="superbox-show"></div>');
				var superboximg_old   = angular.element('<div class="superbox-current-img" image-viewer></div>' + 
													'<div id="imgInfoBox" class="superbox-imageinfo inline-block">' + 
														'<h1>{{currentItem.filename}}</h1>' + 
														'<span>' + 
															'<p><em>{{currentItem.path}}</em></p>' + 
															'<p class="superbox-img-description">Image description</p>' + 
															'<p class="superbox-img-description">FILE TYPE: {{currentItem.details.fileType}}</p>' + 
															'<p class="superbox-img-description">IMAGE WIDTH: {{currentItem.details.imageWidth}} px</p>' + 
															'<p class="superbox-img-description">IMAGE HEIGHT: {{currentItem.details.imageHeight}} px</p>' +
															'<p>' + 
																'<a href="javascript:void(0);" class="btn btn-primary btn-sm">Edit Item</a>' + 
																' <a ng-click="deleteItem(currentItem)" class="btn btn-danger btn-sm">Delete Item</a>' + 
															'</p>' + 
														'</span>' + 
													'</div>');
				var superboxclose = angular.element('<div class="superbox-close txt-color-white"><i class="fa fa-times fa-lg"></i></div>');
				var videogular_old    = angular.element('<div class="superbox-current-img videogular-container" active-media-player></div>' + 
													'<div id="imgInfoBox" class="superbox-imageinfo inline-block">' + 
														'<h1>{{currentItem.filename}}</h1>' + 
														'<span>' + 
															'<p><em>{{currentItem.path}}</em></p>' + 
															'<p class="superbox-img-description" ng-show="currentItem.details.title">{{currentItem.details.title}}</p>' + 
															'<p class="superbox-img-description">FILE TYPE: {{currentItem.details.fileType}}</p>' + 
															'<p class="superbox-img-description">IMAGE WIDTH: {{currentItem.details.imageWidth}} px</p>' + 
															'<p class="superbox-img-description">IMAGE HEIGHT: {{currentItem.details.imageHeight}} px</p>' + 
															'<p class="superbox-img-description">AVG BITRATE: {{currentItem.details.avgBitrate}}</p>' + 
															'<p>' + 
																'<a href="javascript:void(0);" class="btn btn-primary btn-sm">Edit Item</a>' +  
																' <a ng-click="deleteItem(currentItem)" class="btn btn-danger btn-sm">Delete Item</a>' + 
															'</p>' + 
														'</span>' + 
													'</div>');
				var audiogular_old    = angular.element('<div class="superbox-current-img videogular-container audio" active-media-player></div>' + 
													'<div id="imgInfoBox" class="superbox-imageinfo inline-block">' + 
														'<h1>{{currentItem.filename}}</h1>' + 
														'<span>' + 
															'<p><em>{{currentItem.path}}</em></p>' + 
															'<p class="superbox-img-description" ng-show="currentItem.details.title">{{currentItem.details.title}}</p>' + 
															'<p class="superbox-img-description">FILE TYPE: {{currentItem.details.fileType}}</p>' + 
															'<p class="superbox-img-description">AUDIO BITRATE: {{currentItem.details.audioBitrate}}</p>' + 
															'<p>' + 
																'<a href="javascript:void(0);" class="btn btn-primary btn-sm">Edit Item</a>' +  
																' <a ng-click="deleteItem(currentItem)" class="btn btn-danger btn-sm">Delete Item</a>' + 
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
					$scope.onCloseMedia();
					var prev = sl.prev();
					sl.detach();
					if (!angular.equals(elm.attr("id"), prev.attr("id")) && elm.hasClass("highlight")) { // se elm diverso dal nodo selezionato in precedenza
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
					$scope.onCloseMedia();
					$('.superbox-current-img').animate({opacity: 0}, 200, function() {
						$('.superbox-show').slideUp();
						angular.element("div.superbox").find(".superbox-show").detach();
					});
				});

			};
			
		}
	}
	
});
