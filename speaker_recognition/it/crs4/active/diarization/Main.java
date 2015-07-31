/**
 *  Speaker Recognition for Active (C) Sardegna Ricerche.
 *  Email felice@crs4.it 
 *  All Rights Reserved. Use is subject to license terms. 
 *  This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * */

package it.crs4.active.diarization;

import it.crs4.util.PropertiesReader;
 
/**
 The package it.crs4.active.diarization perform the speaker diarization task, which  is the process of partitioning an input audio stream into homogeneous segments
* <br>This task consists of two steps: speaker turn detection and speaker clustering.<br/> 
* This class is an entry point for the Diarization process. You can use the jar file directly by this class. For example:
 * <code> java -classpath the_jar it.crs4.active.diarization.Main example.properties </code>
* 
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
*             <code>gmmName=gmmName</code>
*             
*             <br><br>The location of generated model <br><code>modelDir=/Users/audio_model/</code>
*<br> 
*The class Main is the entry point for the Diarization process
@author Felice Colucci
*/

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		PropertiesReader pr=new PropertiesReader(args[0]);
		try {
			Diarization dia=new Diarization();
			dia.setFileName(pr.getProperty("fileName"));
			dia.setOutputRoot(pr.getProperty("outputRoot"));
			dia.setSms_gmms(pr.getProperty("sms_gmms"));
			dia.setUbm_gmm(pr.getProperty("ubm_gmm"));		
			dia.run();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
