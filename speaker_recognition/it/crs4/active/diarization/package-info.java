/**
  This package perform the speaker diarization task, which  is the process of partitioning an input audio stream into homogeneous segments
 * <br>This task consists of two steps: speaker turn detection and speaker clustering.<br> 
 * <br>
 * <strong> Usage Example</strong>: <br>
 * As command line:<br>
 * 
 * <code> java -classpath the_path_jar it.crs4.active.diarization.Main example.properties </code>
 *  <br>
 * <br>
 * <strong> Usage Example</strong>:<br>
 * As java program<br>
 *  <code>
 *  PropertiesReader pr=new PropertiesReader(args[0]);<br>
	Diarization dia=new Diarization();<br>
	dia.setFileName(pr.getProperty("fileName"));<br>
	dia.setOutputRoot(pr.getProperty("outputRoot"));<br>
	dia.setSms_gmms(pr.getProperty("sms_gmms"));<br>
	dia.setUbm_gmm(pr.getProperty("ubm_gmm"));<br>
	dia.run();<br>
</code> <br>

 * <strong> An example of properties file</strong>:
 * 			   <br> the path of the wav audio file to be processed
 *             <br><code>fileName=/Users/example.wav</code>
 *             
 *             <br><br>the location of intermediate build files<br>
 *             <code>outputRoot=/Users/out/</code>
 *             
 *             <br><br>The path of the ubm.gmm file
 *             <br><code>ubm_gmm=/Users/ubm.gmm</code>
 *             
 *             <br><br>The location of the sms.gmms file
 *             <br><code>sms_gmms=/Users/sms.gmms</code>
 *             
 *             <br><br>The path of the models file
 *             <br><code>db_path=/Users/db_path/</code>  
 *             
 *             <br><br>The name of generated model<br>
 *             <code>gmmName=RemoBodei</code>
 *             
 *             <br><br>The location of generated model <br><code>modelDir=/Users/audio_model/</code>
@author Felice Colucci
 */

package it.crs4.active.diarization;

