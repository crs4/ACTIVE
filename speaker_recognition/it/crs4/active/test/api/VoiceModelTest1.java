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

import it.crs4.active.api.VoiceModel;

/**
 * Build a model by the file <i>filename</i>  
 * The model is saved in <i>modelDir</i> directory defined in the configuration file.
 * */
public class VoiceModelTest1 {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
		String filename="/Users/labcontenuti/Music/Bodei/Remo_Bodei##1min-2.wav";
		String gmmName="provaremo";
		VoiceModel voicemodel=new VoiceModel(configuration);
		voicemodel.addVoice(filename, gmmName);
	}

}
