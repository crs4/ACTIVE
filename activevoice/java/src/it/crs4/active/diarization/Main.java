/**
 * 
 */
package it.crs4.active.diarization;

import it.crs4.util.PropertiesReader;

/**
 * @author labcontenuti
 *
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
