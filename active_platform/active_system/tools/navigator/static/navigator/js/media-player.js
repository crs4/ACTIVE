

// Variables to store handles to various required elements
var mediaPlayer;


var timeline;
var timelineWidth;
var playhead;

var movehead;
var percentage;
var time_label;
var people =[];

var access_token = getCookie("ciccio");

var video_path;

function Person(firstName, lastName, starts, durations, tag_type, tag_id, id){

   this.firstName = firstName;
   this.lastName = lastName;
   this.time = starts;
   this.duration = durations;
   this.tag_type = tag_type;
   this.tag_id = tag_id;
   this.core_id = id;
}

function getData(){
    
    var request = $.ajax({
        async: false,
        type: 'GET',
        beforeSend: function(xhr, settings) {        
            xhr.setRequestHeader("Authorization", "Bearer "+access_token);        
        },
        url:  "/navigator/tags/"+item_id,
        success: function(people_data ) {
             
            for(var i=0; i<people_data.length; i++){ 
                var p_obj = jQuery.parseJSON(people_data[i]);           
                p = new Person(p_obj.first_name,p_obj.last_name,p_obj.starts,p_obj.durations,p_obj.tag_type,p_obj.tad_id,p_obj.person_id);
                people.push(p);
            };
            updateDOM();
            initTables();
            
        }
        

    });
    return request;
}



function getVideo(){
    
    var request = $.ajax({
        async: false,
        type: 'GET',
        beforeSend: function(xhr, settings) {        
            xhr.setRequestHeader("Authorization", "Bearer "+access_token);        
        },
        url:  "/api/items/"+item_id,
        success: function(item){
            
            video_path = "/api/items/file/"+item_id+"?type=preview";
        }
    });
    return request;
}



var countDC = 0;

$(document).ready(function(){
    
	mediaPlayer = document.getElementById('media-video');
	progressBar = document.getElementById('progress-bar');
	movehead = document.getElementById('move_head');
	time_label = document.getElementById('time_span');
    
    //check if error  
    checkError(getVideo());
    
	mediaPlayer.setAttribute('src', video_path+"" );
	mediaPlayer.controls = false;
	mediaPlayer.autoplay=false;	
    
    

    

    
    //Update DOM with dynamic tags	
	$(mediaPlayer).on("durationchange", function(){
		
		countDC++;
		if(countDC<2){
            checkError(getData());  
            
        }
	});
	
	//manage progress bar
	$(mediaPlayer).on("timeupdate",  function(){
		
        manage_movehead();
	});	
	
    //manage player controls
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
					$(".timeline").width() * (11/10) 
				); 
              
               				 
               
				 
			} 
			if(imgClicked == "/static/navigator/icons/zoom_out.png" ){ 
               
				$(this).effect("highlight");
				$(".timeline").width( 
					$(".timeline").width() * (10/11) 
				); 
              
               				 
				 
			}
			
	
	});
    
    //manage video ended event
    $(mediaPlayer).bind("ended", function() {
        mediaPlayer.pause();
        mediaPlayer.currentTime = 0;
		$("#icons img").animate({ backgroundColor: "#22313f" },100);
		$("#icons img:nth-child(3)").animate({ backgroundColor: "#674172" },100);
    });
    
   
    
	
});

 
//manage update of person
$(document).on('click',".mediatable tr td span",function(event){
	var edit_id = $(this).attr('id');
    
    
    $(this).on('save', function(e, params){
        console.log("on save")
        mediaPlayer.pause();
        $("#icons img").animate({ backgroundColor: "#22313f" },100);
	    $("#icons img:nth-child(2)").animate({ backgroundColor: "#674172" },100);
        updatePerson(e,params,edit_id)
        
    });
	
});



$(document).ajaxSend(function(event, request, settings) {
    $('.tabs').hide();
    $('#loading-indicator').show();
});

$(document).ajaxComplete(function(event, request, settings) {
    
    $('#loading-indicator').hide();
    $('.tabs').show();
});


//manage click on the progress bar
$(document).on('click','#progressbar',function(e){
	
	var progressbar = document.getElementById('progressbar');
	var progressBarWidth = $(progressbar).css("width");
	progressBarWidth = progressBarWidth.replace("px","");
	
	var dx_percent = (e.pageX - progressbar.offsetLeft)/progressBarWidth;	
	mediaPlayer.currentTime = mediaPlayer.duration * dx_percent;
	
});

//manage click on dynamic tag
$(document).on('click','div.timeline > div',function(){
	var ist = $(this)[0].style.left;	
	
	ist = ist.replace("%","");		
	mediaPlayer.currentTime = mediaPlayer.duration * (ist/100);
	
});


//manage click on audio button
$(document).on('click','#audioButton',function(){
	$("#audiotimetable").show();
	$(this).css({"background":"#aea8d3"});
	$("#videoButton").css({"background":"#6c7a89"});
    $("#mixedButton").css({"background":"#6c7a89"});
	$("#videotimetable").hide();
    $("#mixedtimetable").hide();
	
});

//manage click on video button
$(document).on('click','#videoButton',function(){
	$("#audiotimetable").hide();
    $("#mixedtimetable").hide();
	$("#videotimetable").show();
	$(this).css({"background":"#aea8d3"});
	$("#audioButton").css({"background":"#6c7a89"});
    $("#mixedButton").css({"background":"#6c7a89"});
	
});//manage click on mixed button
$(document).on('click','#mixedButton',function(){
	$("#audiotimetable").hide();
    $("#mixedtimetable").show();
	$("#videotimetable").hide();
	$(this).css({"background":"#aea8d3"});
	$("#audioButton").css({"background":"#6c7a89"});
    $("#videoButton").css({"background":"#6c7a89"});
	
});



//manage click on 'delete' person button
$(document).on('click','.rmperson',function(){
	var row_id = $(this).parent().parent().attr('id');
    
	mediaPlayer.pause();
	$("#icons img").animate({ backgroundColor: "#22313f" },100);
	$("#icons img:nth-child(2)").animate({ backgroundColor: "#674172" },100);
				
	var tag_id = $(this).attr('id').split("-")[1]
	var person = jQuery.grep(people, function(el) {			
		return (el.tag_id == tag_id);
	});
    
    console.log("remove"+person)
    
    
	
	$( "#dialog-confirm" ).dialog({
		resizable: false,
		height: 'auto',
		width: 'auto',
		modal: true,
		title: "Remove "+person[0].firstName+" "+person[0].lastName+"?",
		buttons: {
			"Remove person": function() {
                //delete person from database
                $.ajax({
                    url: '/api/tags/'+tag_id,
                    type: 'DELETE',
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                        xhr.setRequestHeader("Authorization", "Bearer "+access_token);
                    },
                    success: function(result) {
                       
                        $("#"+row_id).remove();
                    }
                });
				
				$( this ).dialog( "close" );
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		}
	});
	
});


//manage click on the 'show person' button
$(document).on('click','.showperson',function(){
	
	mediaPlayer.pause();
	$("#icons img").animate({ backgroundColor: "#22313f" },100);
	$("#icons img:nth-child(2)").animate({ backgroundColor: "#674172" },100);

	var id = $(this).attr('id').split("-")[1]
	
	var person = jQuery.grep(people, function(el) {			
		return (el.core_id == id);
	});
    
    
    $("#personimage").attr('src', '/api/people/file/'+id+'/?token='+access_token);
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
    $("#end_time_span").css({"color": "#89c4f4"});
    
    $('#timeline_collector').append('<div id="tabs_video" class="tabs"><table id="videotimetable" class="timetable mediatable"></table></div>');
    $('#timeline_collector').append('<div id="tabs_audio" class="tabs"><table id="audiotimetable" class="timetable mediatable" style = "display: none"></table></div>');
    $('#timeline_collector').append('<div id="tabs_mixed" class="tabs"><table id="mixedtimetable" class="timetable mediatable" style = "display: none"></table></div>');
	
    console.log(people.length);
	for(j=0; j<people.length; j++){
		
		if(people[j].tag_type == "speaker"){
			$("#audiotimetable").append('<tr id=a_tr'+people[j].core_id+'><td style="width=2%;"><img title="Delete person" class="rmperson" id=a_rm-'+people[j].tag_id+' src="/static/navigator/icons/remove.png"/></td><td style="width=2%;"><img title="Show person" class="showperson" id=a_showp-'+people[j].core_id+' src="/static/navigator//icons/person.png"/></td><td id=atdrow'+people[j].core_id+' width="13%" ><span title="Edit person" style="background-color:#aea8d3" class="person" id=a_editp-'+people[j].core_id+' data-type="text" data-pk=a_pk'+people[j].core_id+' data-title="Enter username">'+people[j].firstName+" "+people[j].lastName+'</span></td><td width="85%"><div class="timeline center" id=timeline'+j+'></div></td></tr>');
			$("#a_editp-"+people[j].core_id).editable();
            
		}
		if(people[j].tag_type == "face"){
			$("#videotimetable").append('<tr id=v_tr'+people[j].core_id+'><td style="width=2%;"><img title="Delete person" class="rmperson" id=v_rm-'+people[j].tag_id+' src="/static/navigator/icons/remove.png"/></td><td style="width=2%;"><img title="Show person" class="showperson" id=v_showp-'+people[j].core_id+' src="/static/navigator/icons/person.png"/></td><td id=vtdrow'+people[j].core_id+' width="13%" ><span title="Edit person" style="background-color:#1e8bc3" class="person" id=v_editp-'+people[j].core_id+' data-type="text" data-pk=v_pk'+people[j].core_id+' data-title="Enter username">'+people[j].firstName+" "+people[j].lastName+'</span></td><td width="85%"><div class="timeline center" id=timeline'+j+'></div></td></tr>');
			$("#v_editp-"+people[j].core_id).editable();
		}
        
        if(people[j].tag_type == "face+speaker"){
			$("#mixedtimetable").append('<tr id=m_tr'+people[j].core_id+'><td style="width=2%;"><img title="Delete person" class="rmperson" id=m_rm-'+people[j].tag_id+' src="/static/navigator/icons/remove.png"/></td><td style="width=2%;"><img title="Show person" class="showperson" id=m_showp-'+people[j].core_id+' src="/static/navigator/icons/person.png"/></td><td id=mtdrow'+people[j].core_id+' width="13%" ><span title="Edit person" style="background-color:#90c695" class="person" id=m_editp-'+people[j].core_id+' data-type="text" data-pk=m_pk'+people[j].core_id+' data-title="Enter username">'+people[j].firstName+" "+people[j].lastName+'</span></td><td width="85%"><div class="timeline center" id=timeline'+j+'></div></td></tr>');
			$("#m_editp-"+people[j].core_id).editable();
			//~ $("#m_editp-"+people[j].core_id).on('save', function(e, params) {
				//~ mediaPlayer.pause();
				//~ var person = $(this);
				//~ updatePerson(e,params,person)
				//~ 
				//~ 
			//~ });
		}
		
		
		
		var count_istants = people[j].time.length;
		for(i=0;i<count_istants;i++){
			
			
			var ph_istant = (people[j].time[i]/mediaPlayer.duration);
			var ph_width = (people[j].duration[i]/mediaPlayer.duration);	
			var title = people[j].time[i]; 
			
			$("#timeline"+j).append('<div id=playhead'+j+"_"+i+' title='+title+'s></div>');		
			
			if(people[j].tag_type == "speaker"){			
				$("#playhead"+j+"_"+i).css({"left": (ph_istant*100)+"%","width": (ph_width*100)+"%", "background-color":"#aea8d3"});
			}
			else if(people[j].tag_type == "face") {
				$("#playhead"+j+"_"+i).css({"left": (ph_istant*100)+"%","width": (ph_width*100)+"%"});
			}
            else{
                $("#playhead"+j+"_"+i).css({"left": (ph_istant*100)+"%","width": (ph_width*100)+"%","background-color":"#90c695"});
            }
		}
	}
	
}



// Update the progress bar
function manage_movehead(){
	
    percentage = ((100 / mediaPlayer.duration) * mediaPlayer.currentTime);
	movehead.style.width = percentage+"%";
	$(time_label).text(mediaPlayer.currentTime.toFixed(1));
	time_label.style.left = percentage+"%";
}


function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}



function updatePerson(e,params,person){
	
	var reloaded = "false";
	var id_person = person.split('-')[1];
    var new_firstName = params.newValue.split(" ")[0];
    var new_lastName = params.newValue.split(" ")[1];
    var person_old;
    
    $.ajax({
        async: false,
        url: '/api/people/'+id_person,
        type: 'PUT',
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
            xhr.setRequestHeader("Authorization", "Bearer "+access_token);
        },
        data: {'first_name':new_firstName,'last_name': new_lastName},
        success: function(person_mod){
            
            
            if(id_person != person_mod.id){
                person_old = jQuery.grep(people, function(el) {			
		            return (el.core_id == id_person);
	            });
                
                
                $(person).remove();
                
                console.log("old person"+person_old);
                var tag_old_id = person_old[0].tag_id;
                
                $.ajax({
                    async: false,
                    url: '/api/tags/'+tag_old_id,
                    type: 'PUT',
                    dataType: 'json',
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                        xhr.setRequestHeader("Authorization", "Bearer "+access_token);
                    },
                    data: {'entity':person_mod.id},
                    success: function(tag){
                        item_id = tag.item;
                        
                        $.ajax({
                             async: false,
                             type: 'POST',
                             dataType: 'json',                             
                             url: "/api/dtags/merge/"+item_id+"/",
                             beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                                }
                             },
                             success: function(result) {
                                 console.log("update in");
                                 reload_data();
                                 reloaded = "true";
                             }
                        });
                            
                            
                    }
                });
                
                
            }
            if(reloaded == "false" ){
                console.log("update out");
                reload_data();
            }
            
            
        }
    });
   
	
	//~ $( "#edit-confirm" ).dialog({
		//~ resizable: false,
		//~ height:200,
		//~ height: 'auto',
		//~ modal: true,
		//~ buttons: {
			//~ "Ok": function() {
				//~ $( this ).dialog( "close" );
				//~ location.reload();
                //~ 
                //~ 
			//~ },
			//~ 
		//~ }
	//~ });
	
}

function reload_data(){
    console.log("reload");
    $('.tabs').remove();
    people = [];
    getData();
   
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



function checkError(request){
    
    request.error(function(httpObj, textStatus) {  
        if(httpObj.status==401){
            $("#error_id").text("Not authorized. Please login.")
        }
        if(httpObj.status==404){
            $("#error_id").text("Media not analyzed or not present.")
        }
        if(httpObj.status==500){
            $("#error_id").text("Media not avaible.")
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


function initTables(){
    
    //~ $("#videotimetable").fadeIn(1000);
    //~ $("#buttondiv").fadeIn(1000);
    //~ $("#progresstable").fadeIn(1000);
    $("#videoButton").css({"background":"#aea8d3"});
    $("#audioButton").css({"background":"#6C7A89"});
    $("#mixedButton").css({"background":"#6C7A89"});

    
}


//~ 
//~ function getEverything(){
           //~ 
    //~ $.when.apply($, getData()).then(function() {
         //~ console.log("DONE");
         //~ updateDOM();
         //~ 
    //~ }, function(e) {
         //~ console.log("My ajax failed");
//~ });
//~ 
//~ }

