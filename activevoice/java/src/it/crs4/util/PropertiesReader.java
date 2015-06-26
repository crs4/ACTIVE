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