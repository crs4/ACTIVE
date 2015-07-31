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
package it.crs4.util;

import java.io.IOException;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.Properties;
import java.util.Set;


/**
 * An utility class for read and process a properties file 
 * */
public final class PropertiesReader {
	
	/**the path of the wav audio file to be processed*/
	public final static String FILENAME="fileName";
	
	/**the location of intermediate build files*/
	public final static String OUTPUTROOT="outputRoot";
	
	/**The path of the ubm.gmm file*/
	public final static String UBMGMM="ubm_gmm";
	
	/**The path of the sms_gmms file*/
	public final static String SMSGMMS="sms_gmms";
	
	/**The location of model (used in training fase)*/
	public final static String GMMROOT="gmmRoot";
	
	/**The name of generated model*/
	public final static String GMMNAME="gmmName";
	
	/**The location of generated model*/
	public final static String MODELDIR="modelDir";

	private Properties configProp = null;

	/**
	 * @return the configProp
	 */
	public Properties getConfigProp() {
		return configProp;
	}

	/**
	 * @param configProp
	 *            the configProp to set
	 */
	public void setConfigProp(Properties configProp) {
		this.configProp = configProp;
		
	}
	/**
	 * @param configProp
	 *            the file path of configProp to set
	 */
	public void setConfigProp(String configProp) {
		init(configProp);
		
	}

	public static int sanityCeckDiarization = 0;
	public static int sanityCeckIdentification = 1;
	public static int sanityCeckTraining = 2;

	public PropertiesReader(String propertiesFile) {
		init(propertiesFile);
	}

	public void init(String propertiesFile){
		try {
			FileInputStream in = new FileInputStream(propertiesFile);
			System.out.println(in);
			configProp = new Properties();
			System.out.println(configProp);
			System.out.println("Read all properties from file");

			configProp.load(in);
		} catch (IOException e) {
			e.printStackTrace();
		}

	}
	@Override
	public String toString() {
		return "PropertiesReader [configProp=" + configProp + "]";
	}

	public static void main(String[] args) {
		PropertiesReader pr = new PropertiesReader(
				"/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/2sec.properties");

		System.out.println(pr.getProperty("fileName"));
		System.out.println(pr.getProperty("outputRoot"));
		if (pr.sanityCeck(1)) {
			System.out.print("Properties file is ok");

		} else {
			System.out.print("Properties file is NOT ok");
		}
		// All property names
		System.out.println(pr.getAllPropertyNames());
	}

	public String getProperty(String key) {
		return configProp.getProperty(key);
	}

	public Set<String> getAllPropertyNames() {
		return configProp.stringPropertyNames();
	}

	public boolean containsKey(String key) {
		return configProp.containsKey(key);
	}

	public boolean sanityCeck(int type) {
		boolean sanity = true;
		String[] keys = null;
		if (type == sanityCeckDiarization) {

			keys = new String[] { "fileName", "outputRoot", "ubm_gmm",
					"sms_gmms" };
		}

		if (type == sanityCeckIdentification) {
			keys = new String[] { "fileName", "outputRoot", "ubm_gmm",
					"sms_gmms", "db_path" };
		}
		if (type == sanityCeckTraining) {
			keys = new String[] { "fileName", "outputRoot", "ubm_gmm",
					"sms_gmms", "gmmRoot", "gmmName" };
		}

		for (int i = 0; i < keys.length; i++) {
			if (!containsKey(keys[i])) {
				sanity = false;
			}
		}
		return sanity;
	}
}