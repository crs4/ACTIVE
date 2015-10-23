
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

var access_token = getCookie("ciccio");


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



var video_arr = [];
var video_arr_master = [];



var req = $.ajax({
    async: false,
    type: 'GET',
    beforeSend: function(xhr, settings) {        
        xhr.setRequestHeader("Authorization", "Bearer "+access_token);        
    },
    url:  "/summarizer/tags/"+person_id,
    success: function(item_data ) {
        for(var i=0; i<item_data.length; i++){
             
            var v_obj = jQuery.parseJSON(item_data[i]);
            v_obj.url = v_obj.url + "&token="+access_token;        
            v = new Video(v_obj.title,v_obj.url,v_obj.starts,v_obj.durations);
            
            video_arr_master.push(v);
            
            var total = 0;
            $.each(v_obj.durations,function() {
                total += this;
            });
            total_segments_duration = total_segments_duration + (total)
        };
        
        video_arr_master.sort(function compare(a,b) {
          if (a.title < b.title)
             return -1;
          if (a.title > b.title)
            return 1;
          return 0;
        });
        
        
    }
});






$.ajax({
		async: false,
		type: 'GET',
		url: "/api/people/"+person_id+"/",
        beforeSend: function(xhr, settings) {        
            xhr.setRequestHeader("Authorization", "Bearer "+access_token);        
        },
		success: function(person) {
			firstName = person.first_name;
			lastName = person.last_name;
		}
});



var countDC = 0;


$(document).ready(function(){
    
    
    
    $( "#slider" ).slider({      
      range: "min",
      value: 100,
      min: 20,
      max: 100,
      slide: function( event, ui ) {
          $( "#amount" ).val( ui.value +"%" );        
      },
      stop: function( event, ui ) {
          resetApp();
          new_duration = total_segments_duration * (parseFloat(ui.value)/100);
        
          init_summarizer(new_duration);
      }
    });
    $( "#amount" ).val( $( "#slider" ).slider( "value" ) + "%");
    
    
	
	mediaPlayer = document.getElementById('media-video');	
	time_label = document.getElementById('time_span');
	movehead = document.getElementById('move_head');
	video_line = document.getElementById('videoline'); 
	
	mediaPlayer.controls = false;
	mediaPlayer.autoplay = false;
	
	
	play = true;
	pause = false;
	stop = false;
	
    
	
    init_summarizer(total_segments_duration);

	
	
	$(mediaPlayer).on("timeupdate",  function(){
		
		updateProgressBar();
		
	});	
	
	
	
	
	$("#icons img:nth-child(1)").animate({ backgroundColor: "#674172" });
	$("#videoline").css({"cursor":"pointer"});
	$("#time_label span").css({"cursor":"pointer"});
	
	
	
	$("#icons img").click(function(){
			
			
			var imgClicked = $(this).attr( "src" );
			
			
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

function init_summarizer(duration){
    checkError(req);
    
    summary_duration = duration;
    video_arr =  clone(video_arr_master);
   
    //creazione della sequenza dei segmenti. Vengono eliminati segmenti di durata inferiore a min_track_duration
	resizeTracks();
	
	// index of video after resize tracks
	distinct_video_frommap = time_video_track_map[1].filter(onlyUnique);
    
    updateDOM();
	$("tbody").fadeIn("slow");
	
	initTime = new Date();
	manageTracks();
    
    
}

function resetApp(){
    mediaStop();
    
    duration_after_drop = 0
    time_video_track_map.length = 0; 
    distinct_video_frommap = [];
    count_tracks_dropped = 0;
    
    video_arr.length = 0;
    
    $("#playlist > ol").empty();
    $(".videomarker").remove();
    $(".playhead").remove();
    
    
}



function updateDOM(){
	
	
	var lum;
	
	
	//add only videos remaining after resize tracks
	for(var i=0;i<distinct_video_frommap.length;i++){
        if (video_arr[distinct_video_frommap[i]].title.length > 20){
		    $("#playlist > ol").append("<li>"+(video_arr[distinct_video_frommap[i]].title).substr(0,20).concat("...")+"</li>");
	    }
        else {
            $("#playlist > ol").append("<li>"+(video_arr[distinct_video_frommap[i]].title)+"</li>");
        }
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
    else{
        $("#dropped").empty();
    }
	
	
	for(var i=0;i<count_track;i++){
				
		$("#videoline").append('<div class=playhead id=playhead'+i+'></div>');
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
		
		$("#marker"+i).css({"left": (percent_time_video_change*100)+"%"}); 
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
	op_index = 0;
	initTime = new Date();
	updateProgressBar();
	$("#icons img").animate({ backgroundColor: "#22313f" },100);
	$("#icons img:nth-child(3)").animate({ backgroundColor: "#674172" },100);
	$(movehead).hide();
	
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
    
	for(var i=0; i<video_arr.length; i++){
		
		var video = video_arr[i];
		var temp_video_duration = [];
		
		var temp_video_time =[];
		var count_dropped_in_a_video = 0;
		
		for(var j=0; j<video.duration.length; j++){
			
			
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
	time_label.style.left = percentage+"%";
	var timesec = percentage*summary_duration/100;
	$(time_label).text(timesec.toFixed(1));
	$(movehead).html(video_arr[video_index].title + "<br>" + "segment"+(track_id+1));
	
}



function checkError(req){
    
    //check if authorized
    req.error(function(httpObj, textStatus) {  
        if(httpObj.status==401){
            $("#error_id").text("You are not authorized. You may try to sign in again.");                
        }
        if(httpObj.status==404){
            $("#error_id").text("Person not found. You may try to search another one");                
        }
        $( "#error" ).dialog({
                closeOnEscape: false,
                open: function(event, ui){$(".ui-dialog-titlebar-close", ui.dialog | ui).hide();},
                dialogClass: "myDialog",
		        resizable: false,
                height: 250,
                width: 400,
                modal: true,
                title: "Error",
                buttons: {
                    "Ok":function(){
                        // Redirect the to the ACTIVE GUI if error
                        location.href = "http://156.148.132.79:4000/";
                        }
                }
        });
        
    });
    
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



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
