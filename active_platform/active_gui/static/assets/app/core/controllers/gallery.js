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

		$scope.$watch("items", function(newValue, oldValue){
			if($scope.context.action === "search_items"){
				if(newValue && $scope.selectedType !== "image")
					get_statistics($scope.context.filter_by.params.keywords, newValue);
			}
		});
		
		$scope.$on("search_context", function(event, args){
			$scope.context = args;
			reset();
			getItems();
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
	
		$scope.getPath = function(id, type, auth){
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

		var get_su_tipu = function(scores){
			var max = 0, maxIndex = -1;
			var keys = Object.keys(scores);
			for(var i=0; i < keys.length; i++) {
			   if(parseInt(scores[keys[i]], 10) > max) {
				  maxIndex = i;
			   }
			}
			return keys[maxIndex];
		};

		var get_statistics = function(token, items){
			var scores = [];
			token = token.toLowerCase();
			for(var i = 0; i < items.length; i++){
				for(var j = 0; j < items[i].keywords.length; j++){
					if(items[i].keywords[j].match(" ") && items[i].keywords[j].toLowerCase().match(token))
						if(scores[items[i].keywords[j]])
							scores[items[i].keywords[j]] += 1;
						else scores[items[i].keywords[j]] = 1;
				}
			}

			var su_tipu = get_su_tipu(scores);
			if(su_tipu){
				var url = appConfig.coreApiUrl + 'search/person/' + su_tipu.split(" ")[0] + "/" + su_tipu.split(" ")[1] + "/";
				$http.get(url).then(function(response){
					Mediator.mediateEnableSummarizer(response.data.id);
				}, function(error){
					console.log(error);
				});
			} else {
				Mediator.mediateEnableSummarizer(0);
			}
			
		};

		var getItems =  function(){
			$scope.busy = true;
			var params  = {page:$scope.page, type:$scope.selectedType};
			var service = coreService.Item;
			if($scope.context.action === "search_items") {
				service = coreService.ESItem;
				params  = {
					doc_type:"items",
					from:($scope.page - 1)*appConfig.itemPageSize, 
					size:appConfig.itemPageSize, 
					query_params: {
						"filter": {"field":"type", "value":$scope.selectedType},
						"query": {"text":$scope.context.filter_by.params.keywords, "fields": ["keywords"]}
					}
				};
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
			var audiogular  = angular.element('<div class="col-xs-12 col-sm-7 col-md-7 col-lg-7"><div class="superbox-current-audio videogular-container audio" widget-player></div></div>' + infobox);
			var superboxclose = angular.element('<div class="superbox-close txt-color-white"><i class="fa fa-times fa-lg"></i></div>');
			
			switch($scope.selectedType){
				case "image": 
					superbox.append(superboximg).append(superboxclose); 
					Mediator.mediateEnableNavigator(0);
					break;
				case "video": 
					superbox.append(videogular).append(superboxclose); 
					Mediator.mediateEnableNavigator($scope.currentItem.id);
					break;
				case "audio": 
					superbox.append(audiogular).append(superboxclose); 
					Mediator.mediateEnableNavigator($scope.currentItem.id);
					break;
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
				Mediator.mediateEnableNavigator(0);
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
					Mediator.mediateEnableNavigator(0);
					$('.superbox-show').slideUp();                    
					angular.element("div.superbox").find(".superbox-show").detach();
				});
                
                		$('.superbox-current-audio').animate({opacity: 0}, 200, function() {                    
					Mediator.mediateEnableNavigator(0);
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
							'<p class="superbox-img-description" ng-show="currentItem.mime_type">FILE TYPE: {{currentItem.mime_type.split("/")[1]}}</p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.filesize">FILE SIZE: {{currentItem.filesize}}</p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.frame_width">FRAME WIDTH: {{currentItem.frame_width}} px</p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.frame_height">FRAME HEIGHT: {{currentItem.frame_height}} px</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.frame_rate">FRAME RATE: {{currentItem.frame_rate}}</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.num_channels">CHANNELS: {{currentItem.num_channels}}</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.sample_rate">SAMPLE RATE: {{currentItem.sample_rate}}</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.visibility != null">IS VISIBILE: {{currentItem.visibility}}</p>' +
							'<p class="superbox-img-description" ng-show="currentItem.uploaded_at">UPLOADED AT: {{currentItem.uploaded_at | date:"yyyy-MM-dd HH:mm:ss"}}</p>' + 
							'<p class="superbox-img-description" ng-show="currentItem.state">STATUS: {{currentItem.state}}</p>' + 
							'<p widget-keywords class="superbox-img-description" ng-show="keywords.length > 0">KEYWORDS: {{keywords}}</p>' +
							'<p>' + 
								'<a href="javascript:void(0);" class="btn btn-sm btn-primary">Edit Item</a>' + 
								' <a data-target="#delete_item_modal" data-toggle="modal" class="btn btn-sm btn-danger">Delete Item</a>' + 
								' <a href="javascript:void(0);" class="btn btn-sm btn-warning">Share Item</a>' +
								' <a ng-href="' + appConfig.coreApiUrl + 'items/file/{{currentItem.id}}/?type=original" class="btn btn-sm btn-success">Download</a>' +
							'</p>' + 
						'</span>' + 
					'</div>';
		
    });
    
});
