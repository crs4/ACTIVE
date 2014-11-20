

// Variables to store handles to various required elements
var mediaPlayer;
var movehead;
var video_line;
var time_label;

//parametro che indica la durata del summary in secondi
var summary_duration = 60;
//parametro che indica il rapporto che deve esserci tra la track piu' lunga e quella piu' corta.
var max_min_ratio = 2;



var delta_time;

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
    time: [5, 20, 35],
    duration: [10, 8, 2],
    end: 85
}; 


var video3 = {
	
    title:"Datome",
    url: "video/sample.mp4",
    time: [0,8],    
    duration: [2,2],
    end: 14
    
}; 

var video2 = {
    
    title:"parrots",
    url: "video/parrots.mp4",
    time: [8, 23],
    duration: [4,3],
    end: 33
}; 
 
var video4 = {
    
    title:"beli",
    url: "video/beli.mp4",
    time: [0,6,12],    
    duration: [2,3,2],
    end: 78
    
}; 




var video_arr = [video1,video2,video3,video4]; //4
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
	
	delta_time = (summary_duration/video_arr.length);
	
	
	mediaPlayer = document.getElementById('media-video');
	
	time_label = document.getElementById('time_span');
	
	
	
	mediaPlayer.controls = false;
	mediaPlayer.autoplay = false;
	
	
	play = true;
	pause = false;
	stop = false;
	
	
	resizeTracks();
	for (var i = 0; i < time_video_track_map[0].length; i++) {
		console.log(time_video_track_map[0][i]);
	}
	
	
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
		if(ph_index != video_arr.length){
			$(this).effect("highlight",{color:"#dcc6eo"});
			video_index = ph_index;
		
		
			track_id = 0;
			track_timeout.stop();
		
		
			time_offset = delta_time * ph_index * 1000;
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
	var count_video = video_arr.length;
	var count_track = time_video_track_map[0].length;
	
	$("#end_time_span").text(summary_duration);
	
	for(var i=0;i<count_video;i++){
		$("#playlist > ol").append("<li>"+video_arr[i].title+"</li>");		
		
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
		
		//imposta le durate delle tracks in modo che per lo stesso video la track piu' lunga sia al massimo max+min_ratio volte la piu'corta
		while( (Math.max.apply(Math, video.duration)/Math.min.apply(Math, video.duration)) > max_min_ratio ){
			
			var max_duration = Math.max.apply(Math, video.duration);
			var min_duration = Math.min.apply(Math, video.duration);
			
			var index = video.duration.indexOf(max_duration);
			video.duration[index] = min_duration * max_min_ratio;
		}
		
		var total_tracks_duration = eval(video.duration.join('+'));
		var tracks_count = video.time.length;
		var delta_track_time = delta_time/tracks_count;
		
		//sulla base delle durate calcolate al punto precedente, ridefinisco le durate distribuendole su delta_time secondi
		// se la somma delle durate del video e' inferiore a delta_time attribuisco a ogni track la stessa durata, verificando di non sforare le durata del video
		
		if(total_tracks_duration <= delta_time){
			for(j=0; j<video.duration.length; j++){
				
				if(video.time[j] + delta_track_time < video.end){
					video.duration[j] = delta_track_time;
				}
				else{
					video.duration[j] = video.end - video.time[j];					
				}
				acc = acc + video.duration[j];
				timeline.push(acc);
				video_tempid.push(i);
				temp_trackid.push(j);
			}
		}
		// se la somma delle durate del video e' superiore a delta_time attribuisco a ogni track la percentuale rispetto a delta time
		else{
			
			for(j=0; j<video.duration.length; j++){
				
				var track_duration = video.duration[j]*(delta_time/total_tracks_duration);
				if(video.time[j] + delta_track_time < video.end){
					video.duration[j] = track_duration;
				}
				else{
					video.duration[j] = video.end - video.time[j];					
				}				
				acc = acc + track_duration;
				timeline.push(acc);
				video_tempid.push(i);
				temp_trackid.push(j);
			}
			
		}
		
	}
	//definisco una mappa che contiene nel 
	//primo array tutti gli istanti di tempo in cui deve scattare il play di una track
	//nel secondo array, l'indice del video cui appartiene la track appena riprodotta
	//nel terzo array la track appena riprodotta;
	time_video_track_map = [timeline, video_tempid, temp_trackid ];
	
	
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



