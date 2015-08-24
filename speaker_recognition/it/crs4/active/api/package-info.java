/**
 * Contains all of the classes for creating a user model and for identify a person from an audio file.
 *<br>
 * Using this class is possible:<br> 
 * <br> <li>add an audio segment spoken by a single speaker (and a tag identifying the speaker) to the training set of the speaker recognition tool
 * <br> <li>remove an audio segment from the training set of the speaker recognition tool
 * <br> <li>rebuild the models of the training set of the speaker recognition.
   <br> <li>execute the speaker recognition on a set of items. 
   
   <br> <strong>An Example: build a model</strong>
   <code>
String configuration="example.properties";
String filename="example.wav";
String tag="model_name";
VoiceModel voicemodel=new VoiceModel(configuration);
voicemodel.addVoice(filename, tag);
</code>
<strong> An example of properties file </strong><br>
<code>fileName=/Users/example.wav <br>
outputRoot=/Users/example/ <br>
ubm_gmm=/Users/ubm.gmm <br>
sms_gmms=/Users/sms.gmms <br>
gmmName=example <br>

<strong>Voice Extractor: an example</strong>
<code>		String configuration="example.properties";
		VoiceExtractor voiceExtractor= new VoiceExtractor(configuration);
		Set speakers= voiceExtractor.getSpeakers();
		Iterator  it = speakers.iterator(); 
		System.out.println("The speaker in the file defined in the configuration.properties file");
		while(it.hasNext()){
			System.out.println("Speaker name "+it.next());
		}
</code>
 */
package it.crs4.active.api;

import java.util.Iterator;
import java.util.Set;
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
