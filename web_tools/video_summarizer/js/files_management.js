//prova

var c;


function readTextFile(data){
	
	
	var durations = [];
	var starts = [];
	var title;
	var url;	
	var vid;
	
	
	var rows = data.split("\n");
	for(var i = 0; i< rows.length; i++){
		if(rows[i].indexOf("segment_start") > -1){
			var segment_start_split = rows[i].split(":");
			starts.push(segment_start_split[1]/1000); 							
		}
		if(rows[i].indexOf("segment_duration") > -1){
			var segment_duration_split = rows[i].split(":");
			durations.push(segment_duration_split[1]/1000);
		}
		if(rows[i].indexOf("video_url") > -1){
			var url_split = rows[i].split(":");
			url = url_split[1];
		}
		if(rows[i].indexOf("video_name") > -1){
			var name_split = rows[i].split(":");
			title = name_split[1];
		}
		if(rows[i].indexOf("ann_tag") > -1){
			var person_split = rows[i].split(":");
			person = person_split[1];
		}
		if(rows[i].indexOf("tot_segments_duration") > -1){
			var acc_split = rows[i].split(":");
			total_segments_duration = total_segments_duration + parseFloat(acc_split[1]/1000);
			
		}
	}
	
	vid = new Video(title, url, starts, durations);
	video_arr.push(vid);
	console.log(vid);

    
}

function getYamlFile(path,readTextFile) {
  
  $.ajax({
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

