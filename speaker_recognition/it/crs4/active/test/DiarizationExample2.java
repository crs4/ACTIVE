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
package it.crs4.active.test;

import it.crs4.active.diarization.Diarization;
import it.crs4.util.PropertiesReader;

/**
 * Entry point for the Diarization process. You can use the jar file directly by this class. For example
 * <code> java it.crs4.active.diarization.Main example.propertties </code>
 * 
 * <br>@author Felice Colucci
 */
public class DiarizationExample2 {

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
