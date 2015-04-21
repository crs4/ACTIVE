
// Variables to store handles to various required elements
var mediaPlayer;


var timeline;
var timelineWidth;
var playhead;

var movehead;
var percentage;
var time_label;



function Person(firstName, lastName, starts, durations){

   this.firstName = firstName;
   this.lastName = lastName;
   this.time = starts;
   this.duration = durations;
}




var people = [];

$.get( "http://156.148.132.79:80/api/dtags/search/item/"+item_id+"/", function( data ) {
	var tags = [];
	var tags_ids = []
	$.each(data, function(idx, obj) {
		tags_ids.push(obj.tag);
	});	
	tags = tags_ids.filter(onlyUnique)
	for(var i=0; i<tags.length; i++){
		var first_name = ""
		var last_name = ""
		var entity="";
		
		$.ajax({
			 async: false,
			 type: 'GET',
			 url: "http://156.148.132.79:80/api/tags/"+tags[i]+"/",
			 success: function(people_data) {
					entity = people_data.entity;
			 }
		});
		console.log("entity: " + entity)
		
		$.ajax({
			 async: false,
			 type: 'GET',
			 url:  "http://156.148.132.79:80/api/people/"+entity+"/",
			 success: function(entity_data ) {
					first_name = entity_data.first_name;
					last_name = entity_data.last_name;		
						
			 }
		});
		//~ console.log(first_name)			
				
		starts = []
		durations = []		
		person_tags = jQuery.grep(data, function( el) {			
			return (el.tag == tags[i]);
		});
		
		//~ console.log("person-tags" + person_tags)
		
		for(var j = 0; j<person_tags.length; j++){
			starts.push(person_tags[j].start)
			durations.push(person_tags[j].duration)
		}
		
		//~ console.log("starts" + starts)
		//~ console.log("durations" + durations)
		//~ console.log("firstName" + first_name)
		//~ console.log("lastName" + last_name)
		
		var p = new Person(first_name,last_name,starts,durations)
		//~ console.log("people-tags" + p)
		people.push(p)
	}
	
});

var person7 = {
    firstName:"Corrado",
    lastName:"Fadis",
    time: [0],
	duration: [5]
}; 

var person8 = {
    firstName:"Poldo",
    lastName:"Serrenti",
    time: [5],
	duration: [5]
}; 
var person9 = {
    firstName:"Continio",
    lastName:"Balsamo",
    time: [10],
	duration: [5]
}; 

//~ people =[person7, person8, person9]


var video_path = "http://156.148.132.79/api/items/file/"+item_id;
//~ var video_path="http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4"
//~ var video_path = "video/FicMix2.mp4"



// Wait for the DOM to be loaded before initialising the media player
//~ document.addEventListener("DOMContentLoaded", function() { initialiseMediaPlayer(); }, false);
var countDC = 0;

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
			if(imgClicked != "/static/navigator/icons/voloff.png" && imgClicked != "/static/navigator/icons/volon.png"
				&& imgClicked != "/static/navigator/icons/zoom_in.png" && imgClicked != "/static/navigator/icons/zoom_out.png"){
			
				$("#icons img").animate({ backgroundColor: "#22313f" },100);
				$(this).animate({ backgroundColor: "#674172" },100);
			}
			
			
			if( imgClicked == "/static/navigator/icons/play.png"){
				
				mediaPlayer.play();			
					
			}
			else if ( imgClicked == "/static/navigator/icons/pause.png"){
				mediaPlayer.pause();					
			}
			else if ( imgClicked == "/static/navigator/icons/stop.png"){
				mediaPlayer.pause();
				mediaPlayer.currentTime = 0;				
			}
			if(imgClicked == "/static/navigator/icons/volon.png" ){
				mediaPlayer.muted = true;	
				$("#icons img:nth-child(4)").attr('src',"/static/navigator/icons/voloff.png");
				$("#icons img:nth-child(4)").effect("highlight");
				return false;
			}
			if(imgClicked == "/static/navigator/icons/voloff.png" ){
				mediaPlayer.muted = false;
				$("#icons img:nth-child(4)").attr('src',"/static/navigator/icons/volon.png");
				$("#icons img:nth-child(4)").effect("highlight");
				return false;
			}
			if(imgClicked == "/static/navigator/icons/zoom_in.png" ){ 
				$(this).effect("highlight");
				$(".timeline").width( 
					$(".timeline").width() * 1.1 
				); 
				 
			} 
			if(imgClicked == "/static/navigator/icons/zoom_out.png" ){ 
				$(this).effect("highlight");
				$(".timeline").width( 
					$(".timeline").width() * 0.9 
				); 
				 
				 
				 
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


function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}
