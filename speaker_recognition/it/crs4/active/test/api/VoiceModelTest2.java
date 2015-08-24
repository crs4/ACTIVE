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

public class VoiceModelTest2 {

	/**
	 * Build a model
	 * @param args
	 */
	public static void main(String[] args) {
		String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
		String gmmName="provaremo";
		VoiceModel voicemodel=new VoiceModel(configuration);
		String	filename=voicemodel.propertiesReader.getProperty("fileName");
		String	outputRoot=voicemodel.propertiesReader.getProperty("outputRoot");
		String	sms_gmms=voicemodel.propertiesReader.getProperty("sms_gmms");
		String	ubm_gmm=voicemodel.propertiesReader.getProperty("ubm_gmm");
		String	gmmRoot=voicemodel.propertiesReader.getProperty("gmmRoot");
		voicemodel.addVoice(filename, gmmName, outputRoot, sms_gmms, ubm_gmm, gmmRoot);
	}

}
