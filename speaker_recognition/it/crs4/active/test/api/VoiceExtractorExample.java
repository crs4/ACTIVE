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

package it.crs4.active.test.api;

import java.util.Iterator;
import java.util.Set;

import it.crs4.active.api.VoiceExtractor;
import it.crs4.active.api.VoiceModel;

/**
 * Extract all the speaker in the file <i>filename</i> defined in the configuration file. 
 * The model are in the path <i>modelDir</i> defined in the configuration file. 
 * @author Felice Colucci
 *
 */
public class VoiceExtractorExample {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
		VoiceExtractor voiceExtractor=new VoiceExtractor(configuration);
		Set<String> speakers= voiceExtractor.getSpeakers();
		Iterator<String> it =speakers.iterator(); 
		System.out.println("The speaker in the file defined in the configuration.properties file");
		while(it.hasNext()){
			System.out.println("Speaker name "+it.next());
		}
	}

}
