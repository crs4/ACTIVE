define(["core/module", "appConfig"], function (module) {

    "use strict";

    module.registerController("galleryCtrl", function ($scope, $compile, $window, $q, $http, $stateParams, $localStorage, Mediator, coreService) {
		
		$scope.items = [];
		$scope.latestId = "-";
		$scope.busy = false;
		$scope.pages = 0; //DELETE
		$scope.page = 1;
		$scope.plugins = [];
		$scope.selectedItems = [];
		$scope.selectedScript = null;
		$scope.context = {name:"search_none", params:""};
		$scope.selectedType = $stateParams.type;
		$scope.dataUrl = null;
		
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
				Mediator.mediateSelectedItems($scope.selectedItems);
				angular.element($event.currentTarget).addClass("highlight");
			}
			$scope.currentItem = item;
			itemDetails($event);
		};
		
		$scope.nextPage = function(){
			getItems();
		};
		
		$scope.deleteCurrentItem = function(){
			coreService.Item.delete({type:$scope.selectedType.option, id:$scope.currentItem.id}, function() {
				$scope.items.splice($scope.items.indexOf($scope.currentItem), 1);
				$scope.selectedItems.splice($scope.selectedItems.indexOf($scope.currentItem), 1);
				$scope.currentItem = null;
				$("#delete_item_modal").modal("hide");
				checkPages();
				//getItems();
			});
		};
		
		$scope.$on("unselectItems", function() {
			$scope.selectedItems.length = 0;
			$(".superbox-list").removeClass("highlight");
		});
		
		$scope.$on("loadedScripts", function(event, args) {
			$scope.plugins = args.loadedScripts;
		});
		
		$scope.$watch("selectedType", function(newValue, oldValue){
			reset();
			getItems();
		});
		
		$scope.$on("search_context", function(event, args){
			console.log(args);
			$scope.context = args;
			reset();
			//getItems();
		});
		
		$scope.$on("selectedScript", function(event, args){
			$scope.selectedScript = args.selectedScript;
		});
		
		$scope.$on("executeScript", function(event, args){
			executeScript();
		});

		$scope.$on("mediaPlayer", function(event, args){
			$scope.player = args;
		});

		//DA RIMUOVERE lA OPZIONE AUTH ESTRAENDO IL TOKEN DAL COOKIE PRESENTE NELLA REQUEST		
		$scope.getPath = function(id, type, auth){
			if(auth)
				return appConfig.coreApiUrl + "items/file/" + id + "/?type=" + type + "&token=" + $localStorage.token.access_token;
			return appConfig.coreApiUrl + "items/file/" + id + "/?type=" + type;
		};
		
		/**
		 * HANDLER FUNCTIONS
		 */
		 
		var reset = function(){
			$scope.items.length = 0;
			$scope.latestId = "-";
			$scope.pages = 0; //DELETE
			$scope.page = 1;
			$scope.busy = false;
			$scope.selectedItems.length = 0;
			$scope.currentItem = null;
			$scope.selectedScript = null;
		};
		
		var checkPages = function(){
			var ret = appConfig.checkPages($scope.items.length, appConfig.itemPageSize);
			$scope.page += ret;
		};
		
		//VERSIONE CHE DOVREBBE ESSERE UTILIZZATA PASSANDO TUTTI I FILTRI COME PARAMETRI.
		/*var getItems =  function(){
			$scope.busy = true;
			var params = {page:$scope.page, type:$scope.selectedType};
			var service = coreService.Item;
			if($scope.context.name === "search_items" && $scope.context.params.length > 0){
				service = coreService.FilteredItem;
				params["keywords"] = $scope.context.params;
			}
			var i = service.query(params, function(){
				$scope.busy = false;
				$scope.items = $scope.items.concat(i.results);
				if(i.next != null){
					$scope.page += 1;
				} else {
					$scope.busy = true;
				}
			});
		};*/

		//VERSIONE TONTA		
		var getItems =  function(){
			$scope.busy = true;
			var params = {page:$scope.page, type:$scope.selectedType};
			if(!$scope.context.filter_by || $scope.context.filter_by === "default"){
				var service = coreService.Item;
				if($scope.context.name === "search_items" && $scope.context.params.length > 0){
					service = coreService.FilteredItem;
					params["keywords"] = $scope.context.params;
				}
				var i = service.query(params, function(){
					$scope.busy = false;
					$scope.items = $scope.items.concat(i.results);
					if(i.next != null){
						$scope.page += 1;
					} else {
						$scope.busy = true;
					}
				});
			} else {
				if($scope.context.name === "search_items" && $scope.context.params.length > 0){
					var people = coreService.People.query({name:$scope.context.params}, function(){
						console.log(people);	
					});	
				}
			}
		};
		
		var executeScript = function(){
			if($scope.selectedScript && $scope.selectedItems.length > 0){
				$window.open(appConfig.jobmonitorBaseUrl, "_blank");
				$q.all([
					angular.forEach($scope.selectedItems, function(value, key){
						var url = appConfig.coreApiUrl + "triggers/script/" + $scope.selectedScript + "/";
						$http.post(url, {"auth_params":{}, "func_params":value}).then(function(response){
							console.log(response);
						});
					})
				]).then(function(){
						Mediator.mediateAfterExecuteScript();
				});
			}
		};
		
		var itemDetails = function(event){
			var superbox    = angular.element('<div class="superbox-show"></div>');
			var superboximg = angular.element('<div class="col-xs-12 col-sm-7 col-md-7 col-lg-7"><div class="superbox-current-img" widget-viewer></div></div>' + infobox);
			var videogular  = angular.element('<div class="col-xs-12 col-sm-7 col-md-7 col-lg-7"><div class="superbox-current-img videogular-container" widget-player></div></div>' + infobox);
			var audiogular  = angular.element('<div class="col-xs-12 col-sm-7 col-md-7 col-lg-7"><div class="superbox-current-img videogular-container audio" widget-player></div></div>' + infobox);
			var superboxclose = angular.element('<div class="superbox-close txt-color-white"><i class="fa fa-times fa-lg"></i></div>');
			
			switch($scope.selectedType){
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
				if($scope.player)
					$scope.player.stop();
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
				if($scope.player)
					$scope.player.stop();
				$('.superbox-current-img').animate({opacity: 0}, 200, function() {
					$('.superbox-show').slideUp();
					angular.element("div.superbox").find(".superbox-show").detach();
				});
			});
			
		};
		
		var infobox = '<div id="imgInfoBox" class="superbox-imageinfo inline-block col-xs-12 col-sm-5 col-md-5 col-lg-5">' + 
						'<h1>{{currentItem.filename | limitTo:18}}</h1>' + 
						'<span>' + 
							'<p><em>{{currentItem.path}}</em></p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.title">Image description</p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.format">FILE TYPE: {{currentItem.format}}</p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.filesize">FILE SIZE: {{currentItem.filesize}}</p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.frame_width">FRAME WIDTH: {{currentItem.frame_width}} px</p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.frame_height">FRAME HEIGHT: {{currentItem.frame_height}} px</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.frame_rate">FRAME RATE: {{currentItem.frame_rate}}</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.num_channels">CHANNELS: {{currentItem.num_channels}}</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.sample_rate">SAMPLE RATE: {{currentItem.sample_rate}}</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.visibility != null">IS VISIBILE: {{currentItem.visibility}}</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.uploaded_at">UPLOADED AT: {{currentItem.uploaded_at | date:"yyyy-MM-dd HH:mm:ss"}}</p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.state">STATUS: {{currentItem.state}}</p>' + 
							'<p>' + 
								'<a href="javascript:void(0);" class="btn btn-sm btn-primary">Edit Item</a>' + 
								' <a data-target="#delete_item_modal" data-toggle="modal" class="btn btn-sm btn-danger">Delete Item</a>' + 
								' <a href="javascript:void(0);" class="btn btn-sm btn-warning">Share Item</a>' +
								' <a ng-href="' + appConfig.coreApiUrl + 'items/file/{{currentItem.id}}/?type=original&token=' + $localStorage.token.access_token + '" class="btn btn-sm btn-success">Download</a>' +
							'</p>' + 
						'</span>' + 
					'</div>';
		
    });
    
});
