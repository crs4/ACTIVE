angular.module("jobmonitorApp")
.controller("navCtrl", function(){
	
	nav_page_height = function() {
		setHeight = $('#main').height();
		menuHeight = $('#left-panel').height();
		windowHeight = $(window).height() - 49;

		if (setHeight > windowHeight) {// if content height exceedes actual window height and menuHeight
			$('#left-panel').css('min-height', setHeight + 'px');
			$('body').css('min-height', setHeight + 49 + 'px');

		} else {
			$('#left-panel').css('min-height', windowHeight + 'px');
			$('body').css('min-height', windowHeight + 'px');
		}
	};

	setup = function(){
		nav_page_height()

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
			//$(this).effect("highlight", {}, 500);TO ADD
			e.preventDefault();
		});

		// HIDE MENU
		$('#hide-menu >:first-child > a').click(function(e) {
			$('body').toggleClass("hidden-menu");
			e.preventDefault();
		});
	};
	
	setup();
	
})
.controller("ribbonCtrl", function($scope, $route){
	
	$scope.reload = function(){
		$route.reload();
	};
	
})
.controller("jobFormCtrl", function($scope, $location, jobService){
	
	$scope.startJob = function(){
		console.log("TRY TO START JOB");
		jobService.startJob(this.algorithm, this.params, function(result){
			console.log(result);
			if(result.status === 200)
				$location.path("/jobmonitor/jobs");
		});
	};
	
})
.controller("jobCtrl", function($scope, $routeParams, $location, jobService){
	
	var id = $routeParams["id"];
	
	jobService.getJob(id, function(data){
		$scope.job = data;
	});
	
	$scope.deleteJob = function(id){
		console.log("TRY TO DELETE JOB WITH ID " + id);
		jobService.deleteJob(id, function(data){
			$scope.msg = data;
		});
	};
	
	$scope.getBack = function(){
		$location.path("/jobmonitor/jobs");
	};
	 
});
