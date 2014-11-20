//prova

var c;


function readTextFile(file)
{
	var allText;
	var durations = [];
	var starts = [];
	var firstName = "";
	var lastName = "";
	
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                allText = rawFile.responseText;
                
            }
        }
    }
    rawFile.send(null);
   
    var segments = allText.split("-");
    for(var i = 0; i<segments.length; i++){
		
		var segments_lines = segments[i].split("\n");
		for(var j = 0; j<segments_lines.length; j++ ){
			
			if(segments_lines[j].indexOf("ann_tag") > -1 && firstName == "" && lastName == ""){
				var ann_tag_split = segments_lines[j].split(":");
				var first_last_name = ann_tag_split[1].split("_");
				firstName = first_last_name[1];
				lastName = first_last_name[0];
							
			}
			
			if(segments_lines[j].indexOf("segment_start") > -1){
				var segment_start_split = segments_lines[j].split(":");
				starts.push(segment_start_split[1]); 
							
			}
			if(segments_lines[j].indexOf("segment_duration") > -1){
				var segment_duration_split = segments_lines[j].split(":");
				durations.push(segment_duration_split[1]); 
							
			}
		}
	}
	var person = new Person(firstName, lastName, starts, durations);
	return person; 
    
}


function Person(firstName, lastName, starts, durations){

   this.firstName = firstName;
   this.lastName = lastName;
   this.time = starts;
   this.duration = durations;
}

