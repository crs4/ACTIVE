/*
 * VARIABLES
 * Description: All Global Vars
 */
	// Impacts the responce rate of some of the responsive elements (lower value affects CPU but improves speed)
	$.throttle_delay = 350;
	
	// The rate at which the menu expands revealing child elements on click
	$.menu_speed = 235;
	
	// Note: You will also need to change this variable in the "variable.less" file.
	$.navbar_height = 49; 

/*
 * APP DOM REFERENCES
 * Description: Obj DOM reference, please try to avoid changing these
 */	
	$.root_ = $('body');
	$.left_panel = $('#left-panel');
	$.shortcut_dropdown = $('#shortcut');

/*
 * APP CONFIGURATION
 * Description: Enable / disable certain theme features here
 */		
	$.navAsAjax = true; // Your left nav in your app will no longer fire ajax calls
	
	// Please make sure you have included "jarvis.widget.js" for this below feature to work
	$.enableJarvisWidgets = true;
	// $.enableJarvisWidgets needs to be true it to work (could potentially 
	// crash your webApp if you have too many widgets running on mobile view)	
	$.enableMobileWidgets = false;
	
	// Plugin dependency "smartclick.js"
	$.enableFastClick = false; // remove the 300 ms delay in iDevices


/*
 * DETECT MOBILE DEVICES
 * Description: Detects mobile device - if any of the listed device is detected
 * a class is inserted to $.root_ and the variable $.device is decleard. 
 */	

/* so far this is covering most hand held devices */
var ismobile = (/iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()));

	if (!ismobile) {
		// Desktop
		$.root_.addClass("desktop-detected");
		$.device = "desktop";
	} else {
		// Mobile
		$.root_.addClass("mobile-detected");
		$.device = "mobile";
		
		// remove 300ms delay from apple touch devices
		// dependency: plugin/smartclick/smartclick.js
		if ($.enableFastClick){
			$('nav ul a').noClickDelay();
			$('#hide-menu a').noClickDelay();
		}
	}

/* ~ END: CHECK MOBILE DEVICE */

/*
* NAV OR #LEFT-BAR RESIZE DETECT
* Description: changes the page min-width of #CONTENT and NAV when navigation is resized.
* This is to counter bugs for min page width on many desktop and mobile devices.
* Note: This script uses JSthrottle technique so don't worry about memory/CPU usage
*/

// Fix page and nav height
function nav_page_height() {
	setHeight = $('#main').height();
	menuHeight = $.left_panel.height();
	windowHeight = $(window).height() - $.navbar_height;
	//set height

	if (setHeight > windowHeight) {// if content height exceedes actual window height and menuHeight
		$.left_panel.css('min-height', setHeight + 'px');
		$.root_.css('min-height', setHeight + $.navbar_height + 'px');

	} else {
		$.left_panel.css('min-height', windowHeight + 'px');
		$.root_.css('min-height', windowHeight + 'px');
	}
}

$('#main').resize(function() {
	nav_page_height();
	check_if_mobile_width();
})

$('nav').resize(function() {
	nav_page_height();
})

// Setup Desktop Widgets
function setup_widgets_desktop() {

	if ($.fn.jarvisWidgets && $.enableJarvisWidgets) {

		$('#widget-grid').jarvisWidgets({

			grid : 'article',
			widgets : '.jarviswidget',
			localStorage : true,
			deleteSettingsKey : '#deletesettingskey-options',
			settingsKeyLabel : 'Reset settings?',
			deletePositionKey : '#deletepositionkey-options',
			positionKeyLabel : 'Reset position?',
			sortable : true,
			buttonsHidden : false,
			// toggle button
			toggleButton : true,
			toggleClass : 'fa fa-minus | fa fa-plus',
			toggleSpeed : 200,
			onToggle : function() {
			},
			// delete btn
			deleteButton : true,
			deleteClass : 'fa fa-times',
			deleteSpeed : 200,
			onDelete : function() {
			},
			// edit btn
			editButton : true,
			editPlaceholder : '.jarviswidget-editbox',
			editClass : 'fa fa-cog | fa fa-save',
			editSpeed : 200,
			onEdit : function() {
			},
			// color button
			colorButton : true,
			// full screen
			fullscreenButton : true,
			fullscreenClass : 'fa fa-resize-full | fa fa-resize-small',
			fullscreenDiff : 3,
			onFullscreen : function() {
			},
			// custom btn
			customButton : false,
			customClass : 'folder-10 | next-10',
			customStart : function() {
				alert('Hello you, this is a custom button...')
			},
			customEnd : function() {
				alert('bye, till next time...')
			},
			// order
			buttonOrder : '%refresh% %custom% %edit% %toggle% %fullscreen% %delete%',
			opacity : 1.0,
			dragHandle : '> header',
			placeholderClass : 'jarviswidget-placeholder',
			indicator : true,
			indicatorTime : 600,
			ajax : true,
			timestampPlaceholder : '.jarviswidget-timestamp',
			timestampFormat : 'Last update: %m%/%d%/%y% %h%:%i%:%s%',
			refreshButton : true,
			refreshButtonClass : 'fa fa-refresh',
			labelError : 'Sorry but there was a error:',
			labelUpdated : 'Last Update:',
			labelRefresh : 'Refresh',
			labelDelete : 'Delete widget:',
			afterLoad : function() {
			},
			rtl : false, // best not to toggle this!
			onChange : function() {
				
			},
			onSave : function() {
				
			},
			ajaxnav : $.navAsAjax // declears how the localstorage should be saved

		});

	}

}

function check_if_mobile_width() {
	if ($(window).width() < 979) {
		$.root_.addClass('mobile-view-activated')
	} else if ($.root_.hasClass('mobile-view-activated')) {
		$.root_.removeClass('mobile-view-activated');
	}
}

/* ~ END: NAV OR #LEFT-BAR RESIZE DETECT */

// Setup Desktop Widgets
function setup_widgets_mobile() {

	if ($.enableMobileWidgets && $.enableJarvisWidgets) {
		setup_widgets_desktop();
	}

}

/*
 * PAGE SETUP
 * Description: fire certain scripts that run through the page
 * to check for form elements, tooltip activation, popovers, etc...
 */
(function pageSetUp() {

	if ($.device === "desktop"){
		// is desktop
		
		// activate tooltips
		$("[rel=tooltip]").tooltip();
	
		// activate popovers
		$("[rel=popover]").popover();
	
		// activate popovers with hover states
		$("[rel=popover-hover]").popover({
			trigger : "hover"
		});
	
		// activate inline charts
		//runAllCharts();
	
		// setup widgets
		setup_widgets_desktop();
	
		//setup nav height (dynamic)
		nav_page_height();
	
		// run form elements
		//runAllForms();

	} else {
		
		// is mobile
		
		// activate popovers
		$("[rel=popover]").popover();
	
		// activate popovers with hover states
		$("[rel=popover-hover]").popover({
			trigger : "hover"
		});
	
		// activate inline charts
		//runAllCharts();
	
		// setup widgets
		setup_widgets_mobile();
	
		//setup nav height (dynamic)
		nav_page_height();
	
		// run form elements
		//runAllForms();
		
	}

})();


