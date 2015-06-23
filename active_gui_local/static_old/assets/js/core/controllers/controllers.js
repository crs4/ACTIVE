angular.module("coreApp")
.controller("ribbonCtrl", function($scope, $route){
	
	$scope.reload = function(){
		$route.reload();
	};
	
})
.controller("navCtrl", function(){
	
	setup = function(){

		// INITIALIZE LEFT NAV
		if (!null) {
			$('nav ul').jarvismenu({
				accordion : true,
				speed : 235,
				closedSign : '<em class="fa fa-expand-o"></em>',
				openedSign : '<em class="fa fa-collapse-o"></em>'
			});
		} else {
			alert("Error - menu anchor does not exist");
		}

		// COLLAPSE LEFT NAV
		$('.minifyme').click(function(e) {
			$('body').toggleClass("minified");
			e.preventDefault();
		});

		// HIDE MENU
		/*$('#hide-menu >:first-child > a').click(function(e) {
			$('body').toggleClass("hidden-menu");
			e.preventDefault();
		});*/
	};
	
	setup();
	
})
.controller("userCtrl", function($scope, $routeParams, $location, userService){
	
	$scope.currentUser = null;
	
	$scope.createUser = function(user){
		new userService.User({"user": user}).$save().then(function(newUser){
			$location.path("/users");
		});
	};
	
	$scope.updateUser = function(user){
		userService.User.update({id:user._id}, user, function(newUser){
			$location.path("/users");
		});
	};
	
	$scope.saveEdit = function(user){
		if(angular.isDefined(user._id))
			$scope.updateUser(user);
		else $scope.createUser(user);
	};
	
	$scope.backUserList = function(){
		$location.path("/users");
	};
	
	$scope.getUser = function(){
		if($routeParams["id"]){
			userService.User.get({id:$routeParams["id"]}).$promise.then(function(user){
				$scope.currentUser = user.data.user;
			});
		}else{
			$scope.currentUser = {};
		}
	};
	
	$scope.getUser();
	
})
.controller("itemUploadCtrl", function($scope, $location){
	
	var myDropzone = new Dropzone("#mydropzone", {
		url: "http://localhost:8080/api/public/items/",
		parallelUploads: 3,
		maxFilesize: 1024 //MB
	});
	
	/*myDropzone.on("sending", function(file, xhr, formData){
		console.log(file);
		
		formData.append("filename", file.name);
		formData.append("filesize", file.size);
		formData.append("type", file.type.split("/")[0]);
		formData.append("format", file.type.split("/")[1]);
		formData.append("published_at", file.lastModified);
		
		formData.append("owner", 1);
		formData.append("visibility", false);
		
		//if(file.type.split("/")[0] == "video" || file.type.split("/")[0] == "audio"){
		formData.append("duration", 123456);	
		formData.append("bitrate", 123456);
		//}
		
		formData.append("frame_width", 123);
		formData.append("frame_height", 123);
	});*/
	
})
.controller("itemDetailsCtrl", function($scope){
	
	$scope.deleteItem = function(item){
		console.log("ITEM TO DELETE: "  + item.id);
		/*item.$delete().then(function(){
			$scope.items.splice($scope.items.indexOf(item), 1);
		});*/
	};
			
})
.controller("pluginUploadCtrl", function($scope){
	
	var myDropzone = new Dropzone("#myDropzonePlugin", {
		url: "http://localhost:8080/api/public/plugins/",
		parallelUploads: 1,
		maxFilesize: 0.5 //MB
	});
	
});
