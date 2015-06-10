
// Variables to store handles to various required elements
var mediaPlayer;
var movehead;
var video_line;
var time_label;

//parametro che indica la durata del summary impostata dall'utente in secondi
var summary_duration = 10;

//durata totale originaria di tutti segmenti
var total_segments_duration = 0;

//durata del summary dopo eventuale drop
var duration_after_drop;

//minima durata di un segmento ammessa
var min_track_duration = 2;

//numero di segmenti troppo corti e quindi droppati
var count_tracks_dropped = 0

//indici dei video presenti relamente nel summary(insieme compreso in video_arr)
var distinct_video_frommap;

//persona che compare nel summary
var firstName;
var lastName;
var entity_id;

//indice dell'operazione dalla time_video_track_map
var op_index = 0;

var time_offset = 0;

var percentage;


//video e segmanto correnti
var video_index = 0;
var track_id = 0;

var play;
var stop;
var pause;

var initTime;
var currentTime;
var player_time;

var track_timeout;


var temp;


var time_video_track_map;


function Video(title, url, starts, durations){

   this.title = title;
   this.url = url;
   this.time = starts;
   this.duration = durations;
}



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


var video5 = {
    title:"basket",
    url: "video/basket.mp4",
    time: [5, 20, 40],
    duration: [10, 18, 5], // 33
    end: 85
}; 


var video7 = {
	
    title:"Datome",
    url: "video/sample.mp4",
    time: [0,8],    
    duration: [7,3], //43 
    end: 14
    
}; 

var video6 = {
    
    title:"parrots",
    url: "video/parrots.mp4",
    time: [8, 23],
    duration: [4,3], //50
    end: 33
}; 
 
var video8 = {
    
    title:"beli",
    url: "video/beli.mp4",
    time: [0,6,12],    
    duration: [4,4,2], // 60
    end: 78
    
}; 




var video_paths = ["yaml/MONITOR072011.YAML","yaml/MONITOR082011.YAML","yaml/MONITOR272010.YAML","yaml/MONITOR0292010.YAML"];
var video_arr = [];

//~ var video_arr = [video1,video2,video3,video4]; //4
//~ var video_arr = [video1,video2,video3,video4,video5,video6,video7,video8]; //8
//~ var video_arr = [video1,video2,video3,video4,video5,video6]; //6
//~ var video_arr = [video3,video4]; //2

//~ var video_arr = [video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4]; //12
//~ var video_arr = [video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4,video1,video2,video3,video4]; //36

//~ 
//~ 
//~ $.getScript("js/files_management.js", function(){
//~ 
   //~ 
   //~ // Here you can use anything you defined in the loaded script
   //~ 
	//~ for(var i=0; i<video_paths.length; i++){
		//~ 
	   //~ getYamlFile(video_paths[i],readTextFile);
		//~ 
    //~ }
//~ });

//~ $.get( "http://156.148.132.79:80/api/dtags/search/person/5/", function( data ) {
$.ajax({
	async: false,
    type: 'GET',
	url: "http://156.148.132.79:80/api/dtags/search/person/"+person_id+"/",
	success: function(data) {
		
		var tags = [];
		var tags_ids = []
		
		$.each(data, function(idx, obj) {
			tags_ids.push(obj.tag);
			total_segments_duration = total_segments_duration + obj.duration
		});	

		tags = tags_ids.filter(onlyUnique)
		
		
		for(var i=0; i<tags.length; i++){
			
			var title = "";
			var url = "";
			
			var item_id="";
			
			$.ajax({
				 async: false,
				 type: 'GET',
				 url: "http://156.148.132.79:80/api/tags/"+tags[i]+"/",
				 success: function(item_tag) {
						item_id = item_tag.item;
						entity_id = item_tag.entity 
				 }
			});
			console.log("item: " + item_id)
			
			$.ajax({
				 async: false,
				 type: 'GET',
				 url:  "http://156.148.132.79:80/api/items/"+item_id+"/",
				 success: function(item_data) {
						title = item_data.filename;
						url = "http://156.148.132.79/api/items/file/"+item_id+"/";
			
				 }
			});
					
			starts = []
			durations = []		
			item_tags = jQuery.grep(data, function( el) {			
				return (el.tag == tags[i]);
			});
			
			//~ console.log("person-tags" + person_tags)
			
			for(var j = 0; j<item_tags.length; j++){
				starts.push(item_tags[j].start)
				durations.push(item_tags[j].duration)
			}
			
			console.log("title" + title)
			console.log("durations" + durations)
			console.log("starts" + starts)
			console.log("url" + url)
			
			var v = new Video(title, url, starts, durations)
			console.log("item_tags" + v)
			video_arr.push(v)
		}
		
	
		
	}
});

$.ajax({
		async: false,
		type: 'GET',
		url: "http://156.148.132.79:80/api/people/"+entity_id+"/",
		success: function(person) {
			console.log(person)
			firstName = person.first_name;
			lastName = person.last_name;
		}
});

console.log("video_arr" +video_arr)


var countDC = 0;


$(document).ready(function(){
	summary_duration = total_segments_duration;
	console.log("ready")
	video_arr.sort(function compare(a,b) {
	  if (a.title < b.title)
		 return -1;
	  if (a.title > b.title)
		return 1;
	  return 0;
	});
	
	mediaPlayer = document.getElementById('media-video');	
	time_label = document.getElementById('time_span');
	movehead = document.getElementById('move_head');
	video_line = document.getElementById('videoline'); 
	
	mediaPlayer.controls = false;
	mediaPlayer.autoplay = false;
	
	
	play = true;
	pause = false;
	stop = false;
	
	//creazione della sequenza dei segmenti. Vengono eliminati segmenti di durata inferiore a min_track_duration
	resizeTracks();
	
	// index of video after resize tracks
	distinct_video_frommap = time_video_track_map[1].filter(onlyUnique);
	
	
	console.log(time_video_track_map);
	console.log("dropped: " + count_tracks_dropped);
	
	updateDOM();
	$("tbody").fadeIn("slow");
	
	initTime = new Date();
	manageTracks();
	
	
	
	
	$(mediaPlayer).on("timeupdate",  function(){
		
		updateProgressBar();
		
	});	
	
	
	
	
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
			
			
			if( imgClicked == "/static/summarizer/icons/play.png"){
				$("#videoline").css({"cursor":"pointer"});
				$("#time_label span").css({"cursor":"pointer"});
				mediaPlay();				
			}
			else if ( imgClicked == "/static/summarizer/icons/pause.png"){
				$("#videoline").css({"cursor":"not-allowed"});
				$("#time_label span").css({"cursor":"not-allowed"});
				mediaPause();					
			}
			else if ( imgClicked == "/static/summarizer/icons/stop.png"){
				$("#videoline").css({"cursor":"not-allowed"});
				$("#time_label span").css({"cursor":"not-allowed"});
				mediaStop();		
			}
			if(imgClicked == "/static/summarizer/icons/volon.png" ){
				mediaPlayer.muted = true;	
				$("#icons img:nth-child(4)").attr('src',"/static/summarizer/icons/voloff.png");
				$("#icons img:nth-child(4)").effect("highlight");
				return false;
			}
			if(imgClicked == "/static/summarizer/icons/voloff.png" ){
				mediaPlayer.muted = false;
				$("#icons img:nth-child(4)").attr('src',"/static/summarizer/icons/volon.png");
				$("#icons img:nth-child(4)").effect("highlight");
				return false;
			}
			
			
	
	});
	
	
	
	$( "#menu" ).click(function() {
		$( "#playlist" ).slideToggle( "slow" );
		$(this).find('img').toggle();
		
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
		op_index = time_index;
		
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
		
		
		// incremento op_index in modo che quando scatta track_timeout venga eseguita l'operazionew successiva
		op_index = op_index + 1;
	
	}
	else{
		$("#icons img:nth-child(1)").effect("highlight");
	}
	 
	
	
	
});

$(document).on('click','li',function(e){
	
	if(play == true){
		
		var ph_index = $(this).index();
		
		
		$(this).effect("highlight",{color:"#00b16a"});
		
		
		track_timeout.stop();
		
		video_index = distinct_video_frommap[ph_index];	
		op_index = time_video_track_map[1].indexOf(video_index);
		
		
		if(op_index !=0){
		
			time_offset = time_video_track_map[0][op_index-1] * 1000;
		}
		else{
			time_offset = 0;
		}
		initTime.setTime(currentTime.getTime() - time_offset);
	
		manageTracks();
		
	}
	else{
		
		$("#icons img:nth-child(1)").effect("highlight");
		
	}
});





function updateDOM(){
	
	
	var lum;
	
	
	
	//add only videos remaining after resize tracks
	for(var i=0;i<distinct_video_frommap.length;i++){
		$("#playlist > ol").append("<li>"+video_arr[distinct_video_frommap[i]].title+"</li>");
	}
	
	var count_track = time_video_track_map[0].length;
	
	$("#summary_title").text("Summary of " +firstName+" "+lastName);
	
	$("#end_time_span").text((time_video_track_map[0][(count_track-1)]).toFixed(1));
	if(count_tracks_dropped!=0){
		if(video_arr.length != distinct_video_frommap.length){
			var diff_video_length = video_arr.length - distinct_video_frommap.length
			$("#dropped").text(diff_video_length+" video and "+count_tracks_dropped+" segments omitted because too short. Select a longer summary duration for viewing them.");
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
		
		var ind_from_map = time_video_track_map[1][i];
		var ind_from_dist = distinct_video_frommap.indexOf(ind_from_map);
		
		if(ind_from_dist % 2 == 0){			
			
			if( i % 2 == 0){
				$("#playhead"+i).css({ "left": (ph_istant*100)+"%","width": (ph_istant_width*100)+"%","background":colorLuminance("#06699c",0.2) }); //1e8bc3   446cb3 colorLuminance("#1e8bc3",i*lum)
			}
			else{
				$("#playhead"+i).css({ "left": (ph_istant*100)+"%","width": (ph_istant_width*100).toFixed(1)+"%","background":colorLuminance("#06699c",0.03) });
				
			}
		}
		else{
			
			if( i % 2 == 0){
				$("#playhead"+i).css({ "left": (ph_istant*100)+"%","width": (ph_istant_width*100)+"%","background":colorLuminance("#1e8bc3",0.2) }); //1e8bc3   446cb3 colorLuminance("#1e8bc3",i*lum)
			}
			else{
				$("#playhead"+i).css({ "left": (ph_istant*100)+"%","width": (ph_istant_width*100).toFixed(1)+"%","background":colorLuminance("#1e8bc3",0.03) });
				
			}
			
		}
	
		
	}
	
	$("#videoline").append('<img id="marker0" class="videomarker" src="/static/summarizer/icons/v.png">');
	$("#marker0").css({"left": "0%"});
	for(var i=1; i<distinct_video_frommap.length; i++){
		var time_video_change = time_video_track_map[0][time_video_track_map[1].indexOf(distinct_video_frommap[i])-1];
		var percent_time_video_change = time_video_change/summary_duration;
		$("#videoline").append('<img id="marker'+i+'" class="videomarker" src="/static/summarizer/icons/v.png">');
		var marker_width = $("#marker"+i).css("width").split("%")[0];
		console.log(marker_width);
		
		$("#marker"+i).css({"left": (percent_time_video_change*100)+"%"}); //-parseFloat(marker_width)/2)
	}
	
	var list_width = $("#playlist").css("width");
	list_width = list_width.replace("px","");
	var list_pad = $("#playlist").css("padding-right");
	list_pad = list_pad.replace("%","");
	var head_width = $("#header").css("width");
	head_width = head_width.replace("px","");
	var pad_px = (list_pad*head_width)/100;
	
	$("#menu").css({"width":(parseFloat(list_width)+parseFloat(pad_px))+"px"})
	
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
	op_index = 0;
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
			
			if(op_index < time_video_track_map[0].length){
				
				$(mediaPlayer).hide();
				
				var video = video_arr[time_video_track_map[1][op_index]];
				track_id = time_video_track_map[2][op_index];
				video_index = time_video_track_map[1][op_index];
			
				playTracks(video);
				
				
				
				
				track_timeout = new Timer(function(){
					manageTracks();
					},video.duration[track_id]*1000);
				
				 
				op_index = op_index + 1;
			}
			else{
				mediaStop();
			}
		
		
	}	
}

function playTracks(video){
	
	
	$(mediaPlayer).fadeIn("slow");
		
	var trackStartTime;
	var trackEndTime;
			
	trackStartTime = video.time[track_id];
	trackEndTime = parseFloat(video.time[track_id]) + parseFloat(video.duration[track_id]);

	
	mediaPlayer.src = video.url+"#t="+trackStartTime+","+trackEndTime;
	mediaPlayer.play();
	
	
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
		
		var temp_video_time =[];
		var count_dropped_in_a_video = 0;
		
		for(j=0; j<video.duration.length; j++){
			
			
			var temp_duration = video.duration[j] * (summary_duration/total_segments_duration);
			if(temp_duration >= min_track_duration){
				
				temp_video_time.push(video.time[j]);
				temp_video_duration.push(temp_duration);
				acc = acc + temp_duration;
				timeline.push(acc);
				video_tempid.push(i);
				temp_trackid.push(j-count_dropped_in_a_video);
				
			}
			else{
				count_tracks_dropped = count_tracks_dropped + 1;	
				count_dropped_in_a_video = count_dropped_in_a_video +1;					
			}
			
			
		}
		video.duration = temp_video_duration;
		video.time = temp_video_time;
		//~ console.log(temp_video_time)
		//~ console.log(temp_video_duration)
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
	
};

function manage_movehead(){
	
	movehead.style.width = percentage+"%";
	movehead.style.textAlign = "right";
	//~ movehead.style.paddingRight = "10px";
	time_label.style.left = percentage+"%";
	var timesec = percentage*summary_duration/100;
	$(time_label).text(timesec.toFixed(1));
	$(movehead).html(video_arr[video_index].title + "<br>" + "segment"+(track_id+1));
	
}


function colorLuminance(hex, lum){

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



