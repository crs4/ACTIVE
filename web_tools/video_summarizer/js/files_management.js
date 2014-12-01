//prova

var c;


function readTextFile(data){
	
	
	var durations = [];
	var starts = [];
	var title;
	var url;
	//~ var firstName = "";
	//~ var lastName = "";
	var vid;
	
	
	var segments = data.split("-");
	
	for(var i = 0; i<segments.length; i++){
		var segments_lines = segments[i].split("\n");
		for(var j = 0; j<segments_lines.length; j++ ){
				
			//~ if(segments_lines[j].indexOf("ann_tag") > -1 && firstName == "" && lastName == ""){
				//~ var ann_tag_split = segments_lines[j].split(":");
				//~ var first_last_name = ann_tag_split[1].split("_");
				//~ firstName = first_last_name[1];
				//~ lastName = first_last_name[0];
								//~ 
			//~ }
				
			if(segments_lines[j].indexOf("segment_start") > -1){
				var segment_start_split = segments_lines[j].split(":");
				starts.push(segment_start_split[1]/1000); 
								
			}
			if(segments_lines[j].indexOf("segment_duration") > -1){
				var segment_duration_split = segments_lines[j].split(":");
				durations.push(segment_duration_split[1]/1000); 
								
			}
		}		
			
	}	
	
	vid = new Video(title, url, starts, durations);
	video_arr.push(vid);
	console.log(vid);
    
   
    
    
}

function getYamlFile(path,readTextFile) {
  
  return $.ajax({
      url: path,
      success: readTextFile
  });
}


function Video(title, url, starts, durations){

   this.title = title;
   this.url = url;
   this.time = starts;
   this.duration = durations;
}

