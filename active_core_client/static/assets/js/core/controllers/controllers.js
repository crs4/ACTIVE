angular.module("coreApp")
.controller("ribbonCtrl", function($scope, $route){

	console.log($scope.selectedType);
	
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

	};
	
	setup();
	
})
.controller("userCtrl", function($scope, $routeParams, $location, userService){
	
	$scope.currentUser = null;
	
	$scope.createUser = function(user){
		new userService.User(user).$save().then(function(newUser){
			$location.path("/users");
		});
	};
	
	$scope.updateUser = function(user){
		userService.User.update({id:user.id}, user, function(newUser){
			$location.path("/users");
		});
	};
	
	$scope.saveEdit = function(user){
		if(angular.isDefined(user.id))
			$scope.updateUser(user);
		else $scope.createUser(user);
	};
	
	$scope.backUserList = function(){
		$location.path("/users");
	};
	
	$scope.getUser = function(){
		if($routeParams["id"]){
			userService.User.get({id:$routeParams["id"]}).$promise.then(function(user){
				$scope.currentUser = user;
			});
		}else{
			$scope.currentUser = {};
		}
	};
	
	$scope.getUser();
	
})
.controller("itemUploadCtrl", function($scope, $sessionStorage, $location, Scopes){

	var myDropzone = new Dropzone("#mydropzone", {
		url: function(file){
			return 'http://' + window.location.hostname + ':80/api/items/' + file[0].type.split("/")[0] + '/';
		},
		parallelUploads: 100,
		maxFilesize: 10000 //MB
	});
	
	myDropzone.on("sending", function(file, xhr, formData){
		
		formData.append("filename", file.name);
		formData.append("filesize", file.size);
		formData.append("type", file.type.split("/")[0]);
		formData.append("format", file.type.split("/")[1]);
		
		formData.append("owner", 1);
		formData.append("visibility", false);
		
	});
	
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
		url:'http://' + window.location.hostname + ':80/api/items/',
		headers: {
			"Authorization Bearer: ": $sessionStorage.token.access_token
		},
		parallelUploads: 1,
		maxFilesize: 0.5 //MB
	});
	
});
