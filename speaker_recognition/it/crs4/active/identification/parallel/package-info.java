 
/**
  This package perform the identification of a person from characteristics of voices. 
This package is similar to the package it.crs4.identification; 
<br> the identification process is performed in an distributed computing environment
 <br> <strong> An example: </strong> <br>
 *<br> <i> java it.crs4.active.identification.Main example.properties </i> <br>
 *				<br> <strong> An example of properties file is: </strong> <br>
 * 			   <br> the path of the wav audio file to be processed
 *             <br><i>fileName=/Users/example.wav</i>
 *             <br><br>the location of intermediate build file
 *             <br><i>outputRoot=/Users/out/</i>
 *             <br><br>The path of the ubm.gmm file
 *             <br><i>ubm_gmm=/Users/ubm.gmm</i>
 *             
 *             <br><br>The location of the sms.gmms file
 *             <br><i>sms_gmms=/Users/sms.gmms</i>
 *             
 *             <br><br>The path of the models file
 *             <br><i>db_path=/Users/db_path/</i>  
 *             
 *             <br><br>The name of generated model<br>
 *             <i>gmmName=RemoBodei</i>
 *             
 *             <br><br>The location of generated model <br><i>modelDir=/Users/audio_model/</i>
 * @author Felice Colucci
 * 
 */

package it.crs4.active.identification.parallel;