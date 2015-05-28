
// Variables to store handles to various required elements
var mediaPlayer;


var timeline;
var timelineWidth;
var playhead;

var movehead;
var percentage;
var time_label;



function Person(firstName, lastName, starts, durations, tag_type, tag_id, id){

   this.firstName = firstName;
   this.lastName = lastName;
   this.time = starts;
   this.duration = durations;
   this.tag_type = tag_type;
   this.tag_id = tag_id;
   this.core_id = id;
}




var people = [];
//~ 

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
		var id_person = ""
		var entity="";
		var tag_type=""
        var tag_id;
		
		$.ajax({
			 async: false,
			 type: 'GET',
			 url: "http://156.148.132.79:80/api/tags/"+tags[i]+"/",
			 success: function(people_data) {
					entity = people_data.entity;
					tag_type = people_data.type;
                    tag_id = tags[i];
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
					id_person = entity_data.id
			 }
		});
				
		starts = []
		durations = []		
		person_tags = jQuery.grep(data, function( el) {			
			return (el.tag == tags[i]);
		});
		
		
		for(var j = 0; j<person_tags.length; j++){
			starts.push(person_tags[j].start/1000)
			durations.push(person_tags[j].duration/1000)
		}
		
	
		var p = new Person(first_name,last_name,starts,durations,tag_type,tag_id, id_person)
        console.log(p)
		people.push(p)
	}
	
});

var person7 = {
    firstName:"Corrado",
    lastName:"Fadis",
    time: [0],
	duration: [5],
	tag_type: 'video',
	core_id: 1
}; 

var person8 = {
    firstName:"Poldo",
    lastName:"Serrenti",
    time: [5],
	duration: [5],
	tag_type: 'video',
	core_id: 2
}; 

var person9 = {
    firstName:"Continio",
    lastName:"Balsamo",
    time: [10],
	duration: [5],
	tag_type: 'video',
	core_id: 3
}; 


var person10 = {
    firstName:"Continio",
    lastName:"Balsamo",
    time: [10],
	duration: [5],
	tag_type: 'audio',
	core_id: 4
}; 

people =[person7, person8, person9,person10]


var video_path = "http://156.148.132.79/api/items/file/"+item_id+"?type=preview";
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
		$("#videotimetable").fadeIn(1000);
		$("#buttondiv").fadeIn(1000);
		$("#progresstable").fadeIn(1000);
		$("#videoButton").css({"background":"#aea8d3"});
	});
	
	
	//~ $("#icons img:nth-child(1)").animate({ backgroundColor: "#674172" });
	
	$("#icons img").click(function(){
				
			//~  add /static/navigator
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



$(document).on('click','#audioButton',function(){
	$("#audiotimetable").show();
	$(this).css({"background":"#aea8d3"});
	$("#videoButton").css({"background":"#6c7a89"});

	$("#videotimetable").hide();
	
	//~ $(this).effect("highlight");
	
});

$(document).on('click','#videoButton',function(){
	$("#audiotimetable").hide();
	$("#videotimetable").show();
	$(this).css({"background":"#aea8d3"});
	$("#audioButton").css({"background":"#6c7a89"});
	
	//~ $(this).effect("highlight");
	
});


$(document).on('click','.rmperson',function(){
	
	mediaPlayer.pause();
	$("#icons img").animate({ backgroundColor: "#22313f" },100);
	$("#icons img:nth-child(2)").animate({ backgroundColor: "#674172" },100);
				
	var id = $(this).attr('id').split("-")[1]
    //~ var id_type = $(this).attr('id').split("-")[0].split['_']
	var person = jQuery.grep(people, function(el) {			
		return (el.tag_id == id);
	});
    
    console.log(person)
    
    
    $.ajax({
        url: 'http://156.148.132.79:80/api/tags/'+id,
        type: 'DELETE',
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        success: function(result) {
        }
    });
	
	$( "#dialog-confirm" ).dialog({
		resizable: false,
		//~ height:220,
		height: 'auto',
		//~ width:400,
		width: 'auto',
		modal: true,
		title: "Remove "+person[0].firstName+" "+person[0].lastName+"?",
		buttons: {
			"Remove person": function() {
				$('#tr'+id).remove();
				$( this ).dialog( "close" );
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		}
	});
	
});

$(document).on('click','.showperson',function(){
	
	mediaPlayer.pause();
	$("#icons img").animate({ backgroundColor: "#22313f" },100);
	$("#icons img:nth-child(2)").animate({ backgroundColor: "#674172" },100);

	var id = $(this).attr('id').split("-")[1]
	
	var person = jQuery.grep(people, function(el) {			
		return (el.core_id == id);
	});
    
	$("#personimage").attr('src', 'http://156.148.132.79:80/api/people/file/'+id);
    $("#personimage").attr('width', 400);
    $("#personimage").attr('height', 'auto');
    
	$('#dialog').dialog({
		modal: true,
		resizable: false,
		draggable: true,
		width: 450,
		title: person[0].firstName+" "+person[0].lastName
    });
});


function updateDOM(){
	
	people.sort(function compare(a,b) {
	  if (a.firstName < b.firstName)
		 return -1;
	  if (a.firstName > b.firstName)
		return 1;
	  return 0;
	});
	
	$("#end_time_span").text((mediaPlayer.duration).toFixed(1));
	
	for(j=0; j<people.length; j++){
		
		if(people[j].tag_type == "speaker"){
			$("#audiotimetable").append('<tr id=tr'+people[j].core_id+'><td style="width=2%;"><img title="Delete person" class="rmperson" id=a_rm-'+people[j].tag_id+' src="/static/navigator/icons/remove.png"/></td><td style="width=2%;"><img title="Show person" class="showperson" id=a_showp-'+people[j].core_id+' src="/static/navigator//icons/person.png"/></td><td id=tdrow'+people[j].core_id+' width="13%" ><span title="Edit person" style="background-color:#aea8d3" class="person" id=a_editp-'+people[j].core_id+' data-type="text" data-pk=a_pk'+people[j].core_id+' data-title="Enter username">'+people[j].firstName+" "+people[j].lastName+'</span></td><td width="85%"><div class="timeline center" id=timeline'+j+'></div></td></tr>');
			$("#a_editp-"+people[j].core_id).editable();
			$("#a_editp-"+people[j].core_id).on('save', function(e, params) {
			
				mediaPlayer.pause();
				var person = $(this);
				updatePerson(e,params,person)
				
			});
		}
		if(people[j].tag_type == "face"){
			$("#videotimetable").append('<tr id=tr'+people[j].core_id+'><td style="width=2%;"><img title="Delete person" class="rmperson" id=v_rm-'+people[j].tag_id+' src="/static/navigator/icons/remove.png"/></td><td style="width=2%;"><img title="Show person" class="showperson" id=v_showp-'+people[j].core_id+' src="/static/navigator/icons/person.png"/></td><td id=tdrow'+people[j].core_id+' width="13%" ><span title="Edit person" style="background-color:#1e8bc3" class="person" id=v_editp-'+people[j].core_id+' data-type="text" data-pk=v_pk'+people[j].core_id+' data-title="Enter username">'+people[j].firstName+" "+people[j].lastName+'</span></td><td width="85%"><div class="timeline center" id=timeline'+j+'></div></td></tr>');
			$("#v_editp-"+people[j].core_id).editable();
			$("#v_editp-"+people[j].core_id).on('save', function(e, params) {
				mediaPlayer.pause();
				var person = $(this);
				updatePerson(e,params,person)
				
				
			});
		}
		
		
		
		var count_istants = people[j].time.length;
		for(i=0;i<count_istants;i++){
			
			
			var ph_istant = (people[j].time[i]/mediaPlayer.duration);
			var ph_width = (people[j].duration[i]/mediaPlayer.duration);	
			var title = people[j].time[i]; 
			
			$("#timeline"+j).append('<div id=playhead'+j+"_"+i+' title='+title+'s></div>');		
			
			if(people[j].tag_type == "audio"){			
				$("#playhead"+j+"_"+i).css({"left": (ph_istant*100)+"%","width": (ph_width*100)+"%", "background-color":"#aea8d3"});
			}
			else{
				$("#playhead"+j+"_"+i).css({"left": (ph_istant*100)+"%","width": (ph_width*100)+"%"});
			}
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



function updatePerson(e,params,person){
	
	
	var id_person = $(person).attr('id').split('-')[1];
    var new_firstName = params.newValue.split(" ")[0]
    var new_lastName = params.newValue.split(" ")[1]
    
    $.ajax({
        url: 'http://156.148.132.79:80/api/people/'+id_person,
        type: 'PUT',
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        data: {'first_name':new_firstName,'last_name': new_lastName},
        success: function(result) {
            alert("update");
        }
    });
	
	$( "#edit-confirm" ).dialog({
		resizable: false,
		//~ height:200,
		height: 'auto',
		modal: true,
		buttons: {
			"Ok": function() {
				$( this ).dialog( "close" );
				location.reload();
			},
			
		}
	});
	
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
