//~ 
//~ $.ajax({
	//~ url: "Caredda_Giorgio.YAML",
//~ 
	//~ success: ciao()
//~ });
//~ 
//~ 
//~ function ciao(){
	//~ alert("ciao zio");
//~ }



function readTextFile(file)
{
	var allText;
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
    return allText;
}
