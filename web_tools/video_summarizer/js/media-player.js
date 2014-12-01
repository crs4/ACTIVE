

// Variables to store handles to various required elements
var mediaPlayer;
var movehead;
var video_line;
var time_label;

//parametro che indica la durata del summary impostata dall'utente in secondi
var summary_duration = 50;

//durata totale originaria dei segmenti
var total_segments_duration = 60

//durata del summary dopo eventuale drop
var duration_after_drop;

//minima durata di un segmento ammessa
var min_track_duration = 2

//numero di segmenti troppo corti e quindi droppati
var count_tracks_dropped = 0

//indici dei video presenti relamente nel summary(insiemte compreso in video_arr)
var distinct_video_frommap;

//persona che comapre nel summary
var person="Giovanni Pili"

var time_offset = 0;

var percentage;

var video_index = 0;

var play;
var stop;
var pause;

var initTime;
var currentTime;
var player_time;

var track_timeout;

var track_id = 0;



var time_video_track_map;


var video1 = {
    title:"basket",
    url: "video/basket.mp4",
    time: [5, 20, 40],
    duration: [10, 18, 5], // 33
    end: 85
}; 


var video3 = {
	
    title:"Datome",
    url: "video/sample.mp4",
    time: [0,8],    
    duration: [7,3], //43 
    end: 14
    
}; 

var video2 = {
    
    title:"parrots",
    url: "video/parrots.mp4",
    time: [8, 23],
    duration: [4,3], //50
    end: 33
}; 
 
var video4 = {
    
    title:"beli",
    url: "video/beli.mp4",
    time: [0,6,12],    
    duration: [4,4,2], // 60
    end: 78
    
}; 





var video_arr = [video1,video2,video3,video4]; //4
//~ var video_arr = [video1,video2,video3,video4,video5,video6]; //6
//~ var video_arr = [video3,video4]; //2

//~ var video_arr = [video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4]; //12
//~ var video_arr = [video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4]; //36





// Wait for the DOM to be loaded before initialising the media player
//~ document.addEventListener("DOMContentLoaded", function() { initialiseMediaPlayer(); }, false);

//~ 
//~ $.getScript("files_management.js", function(){
//~ 
   //~ 
   //~ // Here you can use anything you defined in the loaded script
   //~ 
   //~ console.log(readTextFile("Caredda_Giorgio.YAML"));
//~ });

var countDC = 0;
$(document).ready(function(){
	
	
	
	mediaPlayer = document.getElementById('media-video');
	
	time_label = document.getElementById('time_span');
	
	
	
	mediaPlayer.controls = false;
	mediaPlayer.autoplay = false;
	
	
	play = true;
	pause = false;
	stop = false;
	
	//creazione della sequenza dei segmenti. Vengono eliminati segmenti di durata inferiore a min_track_duration
	resizeTracks();
	
	
	
	for (var i = 0; i < time_video_track_map[0].length; i++) {
		console.log(time_video_track_map[0][i]);
	}
	console.log("dropped: " + count_tracks_dropped);
	
	
	initTime = new Date();
	manageTracks();
	
	
	$(mediaPlayer).on("durationchange", function(){
		
		countDC++;
		if(countDC<2)
			updateDOM();
	});
	
	movehead = document.getElementById('move_head');
	video_line = document.getElementById('videoline'); 
	
	$(mediaPlayer).on("timeupdate",  function(){
		
		updateProgressBar();
		
	});	
	
	$("tbody").fadeIn(2000);
	
	
	$("#icons img:nth-child(1)").animate({ backgroundColor: "#674172" });
	$("#videoline").css({"cursor":"pointer"});
	$("#time_label span").css({"cursor":"pointer"});
	
	
	$("#icons img").click(function(){
			
			
			var imgClicked = $(this).attr( "src" );
			
			//~ if(imgClicked != "icons/voloff.png" && imgClicked != "icons/volon.png" ){
			//~ 
				//~ $("#icons img").animate({ backgroundColor: "#22313f" },100);
				//~ $(this).animate({ backgroundColor: "#674172" },100);
			//~ }
			
			
			if( imgClicked == "icons/play.png"){
				$("#videoline").css({"cursor":"pointer"});
				$("#time_label span").css({"cursor":"pointer"});
				mediaPlay();				
			}
			else if ( imgClicked == "icons/pause.png"){
				$("#videoline").css({"cursor":"not-allowed"});
				$("#time_label span").css({"cursor":"not-allowed"});
				mediaPause();					
			}
			else if ( imgClicked == "icons/stop.png"){
				$("#videoline").css({"cursor":"not-allowed"});
				$("#time_label span").css({"cursor":"not-allowed"});
				mediaStop();		
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
	
	$( "#menu" ).click(function() {
		$( "#playlist" ).slideToggle( "slow" );
	});
	
});

//gestione del click sulla videoline e movehead
$(document).on('click','#videoline',function(e){
	
	
	if(play == true){
		
		
		var progressBarWidth = $("#videoline").css("width");
		progressBarWidth = progressBarWidth.replace("px","");	
		//coordinata x del punto in cui viene cliccata la barra, rispetto all' iniziodella barra stessa
		var dx_percent = (e.pageX - video_line.offsetLeft)/progressBarWidth;
		
		//istante di tempo corrispondente al punto della progressbar in cui si clicca	
		var time_position = summary_duration * dx_percent;
		
		// time_index e' il prossimo istante di tempo in cui si cambia track
		// time_index permette di ricavare l'indice della track e del video in play
		var time_index;
		
		for(i=0; i<time_video_track_map[0].length; i++){
			if(time_position < time_video_track_map[0][i]){
				time_index = i;
				break;
			}
		}
		//indice del video e della track corrispondenti al punto della progressbar in cui si clicca
		var video_retrieved_ind = time_video_track_map[1][time_index];
		var track_retrieved_ind = time_video_track_map[2][time_index];
		
		video_index = video_retrieved_ind;
		track_id = track_retrieved_ind;
		
		//istante di tempo in cui scatta il play della prossima track, rispetto al punto cliccato
		var next_track_time = time_video_track_map[0][time_index];
		
		//istante di tempo precedente rispetto al punto cliccato
		var previous_track_time;
		if(time_index != 0){
			previous_track_time = time_video_track_map[0][time_index-1];
		}
		else{
			previous_track_time = 0;
		}
		
		
		//tempo che intercorre tra il punto cliccato e il play della prossima track
		var time_for_next_track = next_track_time - time_position;
		
		
		//tempo trascorso tra il punto cliccato e il play della precedente track
		var time_track_passed = time_position - previous_track_time;
		
		
		var time_start = video_arr[video_retrieved_ind].time[track_retrieved_ind] + time_track_passed;
		var time_end = time_start + time_for_next_track;
		
		track_timeout.stop();
		
		
		
		mediaPlayer.src = video_arr[video_retrieved_ind].url+"#t="+time_start+","+time_end;
		mediaPlayer.play();
		
		//aggiorno la progress bar
		currentTime = new Date();
		initTime.setTime(currentTime.getTime() - time_position*1000);
		
		track_timeout = new Timer(function(){
			manageTracks();
			},time_for_next_track*1000);
		
		
		// incremento track_id in modo che quando scatta track_timeout venga eseguita la track successiva
		track_id = track_id +1 ;
	
	}
	else{
		$("#icons img:nth-child(1)").effect("highlight");
	}
	 
	
	
	
});

$(document).on('click','li',function(e){
	
	if(play == true){
		
		var ph_index = $(this).index();
		
		if(distinct_video_frommap[ph_index] != video_arr.length){
			
			$(this).effect("highlight",{color:"#dcc6eo"});
			video_index = distinct_video_frommap[ph_index];
		
		
			track_id = 0;
			track_timeout.stop();
		
			var time_from_map = time_video_track_map[1].indexOf(video_index);
			if(time_from_map !=0){
			
				time_offset = time_video_track_map[0][time_from_map-1] * 1000;
			}
			else{
				time_offset = 0;
			}
			initTime.setTime(currentTime.getTime() - time_offset);
		
			manageTracks();
		}
	}
	else{
		
		$("#icons img:nth-child(1)").effect("highlight");
		
	}
});



function updateDOM(){
	
	
	var lum;
	
	// index of video after resize tracks
	distinct_video_frommap = time_video_track_map[1].filter(onlyUnique);
	
	//add only videos remaining after resize tracks
	for(var i=0;i<distinct_video_frommap.length;i++){
		$("#playlist > ol").append("<li>"+video_arr[distinct_video_frommap[i]].title+"</li>");
	}
	
	var count_track = time_video_track_map[0].length;
	
	$("#summary_title").text("Summary of " +person);
	
	$("#end_time_span").text((time_video_track_map[0][(count_track-1)]).toFixed(1));
	if(count_tracks_dropped!=0){
		if(video_arr.length != distinct_video_frommap.length){
			var diff_video_length = video_arr.length - distinct_video_frommap.length
			$("#dropped").text(diff_video_length+" video and "+count_tracks_dropped+" segments omitted because too brief. Select a longer summary duration for viewing them.");
		}
		else{
			$("#dropped").text(count_tracks_dropped+" segments omitted because too short. Select a longer summary duration for viewing them.");
		}
	}
	
	
	
	
	for(var i=0;i<count_track;i++){
				
		$("#videoline").append('<div id=playhead'+i+'></div>');
		var ph_istant;
		var ph_istant_width;
		if(i == 0){
			ph_istant = i;
			ph_istant_width = (time_video_track_map[0][i] /summary_duration);
		}
		else{
			ph_istant = time_video_track_map[0][i-1]/summary_duration;
			ph_istant_width = (time_video_track_map[0][i] - time_video_track_map[0][i-1]) /summary_duration;	
			
		}
		
		
		var ind_vid = time_video_track_map[1][i];
		
		var ind_track = time_video_track_map[2][i];
		if(ind_vid % 2 == 0){			
			
			if( ind_track % 2 == 0){
				$("#playhead"+i).css({ "left": (ph_istant*100)+"%","width": (ph_istant_width*100)+"%","background":colorLuminance("#06699c",0.2) }); //1e8bc3   446cb3 colorLuminance("#1e8bc3",i*lum)
			}
			else{
				$("#playhead"+i).css({ "left": (ph_istant*100)+"%","width": (ph_istant_width*100)+"%","background":colorLuminance("#06699c",0.03) });
				
			}
		}
		else{
			
			if( ind_track % 2 == 0){
				$("#playhead"+i).css({ "left": (ph_istant*100)+"%","width": (ph_istant_width*100)+"%","background":colorLuminance("#1e8bc3",0.2) }); //1e8bc3   446cb3 colorLuminance("#1e8bc3",i*lum)
			}
			else{
				$("#playhead"+i).css({ "left": (ph_istant*100)+"%","width": (ph_istant_width*100)+"%","background":colorLuminance("#1e8bc3",0.03) });
				
			}
			
		}
	}
	
	
}




// Update the progress bar
function updateProgressBar() {
	
	if(play == true || stop == true){
	
		
		currentTime = new Date();
	
	
		var diffTime = (currentTime.getTime() - initTime.getTime()); 
		percentage = ( diffTime / (summary_duration*1000) ) * 100
		
		
		manage_movehead();
		
	}
}

function mediaPause(){
	
	if(pause == false && stop == false){
		
		mediaPlayer.pause();
		pause = true;
		play = false;
		stop = false;
	
		track_timeout.pause();
	
		player_time = (percentage/100) * summary_duration * 1000;
		
		$("#icons img").animate({ backgroundColor: "#22313f" },100);
		$("#icons img:nth-child(2)").animate({ backgroundColor: "#674172" },100);
	}
	
}

function mediaPlay(){
	
	if(play == false){
		
		play = true;
		
		
		if(stop == true && pause == false){
			initTime = new Date();
			manageTracks();
		}
		else if(stop == false && pause == true){
			
			track_timeout.resume();
			mediaPlayer.play();
			currentTime = new Date();
			initTime.setTime(currentTime.getTime() - player_time);
			
			
		}	
		
		$("#icons img").animate({ backgroundColor: "#22313f" },100);
		$("#icons img:nth-child(1)").animate({ backgroundColor: "#674172" },100);
		$(movehead).fadeIn("1000");
	
		stop = false;
		pause = false;
	}	
}


function mediaStop(){
	
	mediaPlayer.src = video_arr[0].url;
	mediaPlayer.pause();	
	
	track_timeout.stop();
	time_offset = 0;
	video_index = 0;
	track_id = 0;
	initTime = new Date();
	updateProgressBar();
	//~ manage_movehead();
	$("#icons img").animate({ backgroundColor: "#22313f" },100);
	$("#icons img:nth-child(3)").animate({ backgroundColor: "#674172" },100);
	$(movehead).hide();
	//~ movehead.style.width = "0%";
	
	play = false;
	stop = true;
	pause = false;
	
}

function manageTracks(){
	
	if(play == true){
		
		var video = video_arr[video_index];
	
		var tracks_count = video.time.length;
		
	
		playTracks(video,tracks_count);
	}	
}


function playTracks(video,tracks_count, delta_track_time, total_tracks_duration ){
	
	//nascondo il player per creare successivamente l'effetto di dissolvenza in entrata
	$(mediaPlayer).hide();
	
	
	

	//per il video considerato, verifico se la traccia 
	if(track_id < tracks_count){
		
		var trackStartTime;
		var trackEndTime;
		
		track_timeout = new Timer(function(){
				playTracks(video,tracks_count);
				},video.duration[track_id]*1000);
				
		trackStartTime = video.time[track_id];
		trackEndTime = parseFloat(video.time[track_id]) + parseFloat(video.duration[track_id]);	
	
		
		mediaPlayer.src = video.url+"#t="+trackStartTime+","+trackEndTime;
		mediaPlayer.play();
		
		track_id = track_id + 1;
		$(mediaPlayer).fadeIn("slow");
	}
	else{
		//~ alert("clear");
		track_id = 0;
		track_timeout.stop();
		if(video_index != (video_arr.length - 1)){
			video_index = parseInt(video_index) + 1;
			manageTracks();
		}
		else{
			mediaStop();
		}
		
	}
	
}


function Timer(callback, delay) {
    var timerId;
    var start;
    var remaining = delay;

    this.pause = function() {
        window.clearTimeout(timerId);
        remaining -= new Date() - start;
    };

    this.resume = function() {
        start = new Date();
        timerId = window.setTimeout(callback, remaining);
    };
    
	this.stop = function(){		
		window.clearTimeout(timerId);		
	}

    this.resume();
}

function resizeTracks(){
	
	var acc = 0;
	var video_tempid = [];
	var temp_trackid = [];
	var timeline =[];

		

	for(i=0; i<video_arr.length; i++){
		
		var video = video_arr[i];
		var temp_video_duration = [];
		
		for(j=0; j<video.duration.length; j++){
			
			var temp_duration = video.duration[j] * (summary_duration/total_segments_duration)
			if(temp_duration >= min_track_duration){
				
				temp_video_duration.push(temp_duration);
				acc = acc + temp_duration;
				timeline.push(acc);
				video_tempid.push(i);
				temp_trackid.push(j);
				
			}
			else{
				count_tracks_dropped = count_tracks_dropped + 1;						
			}
			
			
		}
		video.duration = temp_video_duration;
	}
	//definisco una mappa che contiene nel 
	//primo array tutti gli istanti di tempo in cui deve scattare il play di una track
	//nel secondo array, l'indice del video cui appartiene la track appena riprodotta
	//nel terzo array la track appena riprodotta;
	time_video_track_map = [timeline, video_tempid, temp_trackid ];
	duration_after_drop = time_video_track_map[0][time_video_track_map[0].length - 1];
	if(count_tracks_dropped > 0){
		summary_duration = duration_after_drop;
	}
	
}

function manage_movehead(){
	
	movehead.style.width = percentage+"%";
	movehead.style.textAlign = "right";
	//~ movehead.style.paddingRight = "10px";
	time_label.style.left = percentage+"%";
	var timesec = percentage*summary_duration/100;
	$(time_label).text(timesec.toFixed(1));
	$(movehead).html(video_arr[video_index].title + "<br>" + "segment"+track_id );
	
}


function colorLuminance(hex, lum) {

	// validate hex string
	hex = String(hex).replace(/[^0-9a-f]/gi, '');
	if (hex.length < 6) {
		hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
	}
	lum = lum || 0;

	// convert to decimal and change luminosity
	var rgb = "#", c, i;
	for (i = 0; i < 3; i++) {
		c = parseInt(hex.substr(i*2,2), 16);
		c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
		rgb += ("00"+c).substr(c.length);
	}

	return rgb;
}


function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}



