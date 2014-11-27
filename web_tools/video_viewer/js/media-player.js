

// Variables to store handles to various required elements
var mediaPlayer;


var timeline;
var timelineWidth;
var playhead;

var movehead;
var percentage;
var time_label;



var person1 = {
    firstName:"John",
    lastName:"Doe",
    time: [5, 25, 16.5],
	duration: [4, 6, 2]
    
}; 

var person2 = {
    firstName:"Pino",
    lastName:"Lamarmora",
    time: [25],
	duration: [6]
}; 

var person3 = {
    firstName:"Salvatore",
    lastName:"Zedda",
    time: [18],
	duration: [2]
}; 

var person4 = {
    firstName:"Nenno",
    lastName:"Lello",
    time: [18],
	duration: [2]
}; 

var person5 = {
    firstName:"Paoletto",
    lastName:"Sardu",
    time: [18],
	duration: [2]
}; 

var person6 = {
    firstName:"Barcisio",
    lastName:"Folis",
    time: [18],
	duration: [2]
}; 

var person7 = {
    firstName:"Corrado",
    lastName:"Fadis",
    time: [18],
	duration: [2]
}; 

var person8 = {
    firstName:"Poldo",
    lastName:"Serrenti",
    time: [18],
	duration: [2]
}; 
var person9 = {
    firstName:"Continio",
    lastName:"Balsamo",
    time: [8],
	duration: [2]
}; 



//~ var people = [person1, person2, person3, person4,person5,person6, person7, person8, person9];
var people = [];
var people_paths = ["yaml/MONITOR072011.mpg-Corona_Giorgia.YAML","yaml/MONITOR072011.mpg-Dessi_Emanuele.YAML", "yaml/MONITOR072011.mpg-Giagnoli_Gerardo.YAML"];
var video_path = 'video/monitor.mp4';


// Wait for the DOM to be loaded before initialising the media player
//~ document.addEventListener("DOMContentLoaded", function() { initialiseMediaPlayer(); }, false);
var countDC = 0;

//gestione della lettura e del parse dei file yaml in cui sono contenuti gli istanti di tempo e la durata dei segmenti
$.getScript("js/files_management.js", function(){

   
   // Here you can use anything you defined in the loaded script
   for(var i=0; i<people_paths.length; i++){
		
	   getYamlFile(people_paths[i],readTextFile)
		
   }
});

//~ $( document ).tooltip();

$(document).ready(function(){
	
	mediaPlayer = document.getElementById('media-video');
	progressBar = document.getElementById('progress-bar');
	movehead = document.getElementById('move_head');
	time_label = document.getElementById('time_span');
	
	mediaPlayer.setAttribute('src', video_path );
	mediaPlayer.controls = false;
	mediaPlayer.autoplay=false;		
	
	$(mediaPlayer).on("durationchange", function(){
		
		countDC++;
		if(countDC<2)
			updateDOM();
	});
	
	$(mediaPlayer).on("timeupdate",  function(){
		
		updateProgressBar();	
	});	
	
	$(mediaPlayer).on("loadeddata", function(){
		
		$("tbody").fadeIn(2000);
	});
	
	
	
	
	//~ $("#icons img:nth-child(1)").animate({ backgroundColor: "#674172" });
	
	$("#icons img").click(function(){
			
			var imgClicked = $(this).attr( "src" );
			if(imgClicked != "icons/voloff.png" && imgClicked != "icons/volon.png" ){
			
				$("#icons img").animate({ backgroundColor: "#22313f" },100);
				$(this).animate({ backgroundColor: "#674172" },100);
			}
			
			
			if( imgClicked == "icons/play.png"){
				mediaPlayer.play();					
			}
			else if ( imgClicked == "icons/pause.png"){
				mediaPlayer.pause();					
			}
			else if ( imgClicked == "icons/stop.png"){
				mediaPlayer.pause();
				mediaPlayer.currentTime = 0;				
			}
			if(imgClicked == "icons/volon.png" ){
				mediaPlayer.muted = true;	
				$("#icons img:nth-child(4)").attr('src',"icons/voloff.png");
				$("#icons img:nth-child(4)").effect("highlight");
				return false;
			}
			if(imgClicked == "icons/voloff.png" ){
				mediaPlayer.muted = false;
				$("#icons img:nth-child(4)").attr('src',"icons/volon.png");
				$("#icons img:nth-child(4)").effect("highlight");
				return false;
			}
			
	
	});
	
});

$(document).on('click','#progressbar',function(e){
	
	
	var progressbar = document.getElementById('progressbar');
	var progressBarWidth = $(progressbar).css("width");
	progressBarWidth = progressBarWidth.replace("px","");
	
	var dx_percent = (e.pageX - progressbar.offsetLeft)/progressBarWidth;	
	mediaPlayer.currentTime = mediaPlayer.duration * dx_percent;
	
});

$(document).on('click','div.timeline > div',function(){
	var ist = $(this)[0].style.left;	
	
	ist = ist.replace("%","");		
	mediaPlayer.currentTime = mediaPlayer.duration * (ist/100);
	
});


function updateDOM(){
	
	
	$("#end_time_span").text((mediaPlayer.duration).toFixed(1));
	
	for(j=0; j<people.length; j++){
		$("#timetable").append('<tr><td width="15%" ><span>'+people[j].firstName+" "+people[j].lastName+'</span></td><td width="85%"><div class="timeline center" id=timeline'+j+'></div></td></tr>');
		
		var count_istants = people[j].time.length;
		for(i=0;i<count_istants;i++){
			
			
			var ph_istant = (people[j].time[i]/mediaPlayer.duration);
			var ph_width = (people[j].duration[i]/mediaPlayer.duration);	
			var title = people[j].time[i]; 
			
			$("#timeline"+j).append('<div id=playhead'+j+"_"+i+' title='+title+'s></div>');		
						
			$("#playhead"+j+"_"+i).css({"left": (ph_istant*100)+"%","width": (ph_width*100)+"%"});
			
		}
	}
}

// Update the progress bar
function updateProgressBar() {
	// Work out how much of the media has played via the duration and currentTime parameters
	percentage = ((100 / mediaPlayer.duration) * mediaPlayer.currentTime);
	
	if(percentage == 100){
		mediaPlayer.pause();
		mediaPlayer.currentTime = 0;
		$("#icons img").animate({ backgroundColor: "#22313f" },100);
		$("#icons img:nth-child(3)").animate({ backgroundColor: "#674172" },100);
		
	}
	else{
		
		manage_movehead();
	
	}
}

function manage_movehead(){
	
	movehead.style.width = percentage+"%";
	$(time_label).text(mediaPlayer.currentTime.toFixed(1));
	time_label.style.left = percentage+"%";
	
	
}
