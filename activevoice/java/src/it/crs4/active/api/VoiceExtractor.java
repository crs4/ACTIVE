/**
 * 
 */
package it.crs4.active.api;

import it.crs4.active.diarization.Diarization;
import it.crs4.identification.DBScore;
import it.crs4.util.PropertiesReader;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

/**
 * Tool for detecting and recognizing voices in audio and video.
 * @author Felice Colucci
 *
 */
public class VoiceExtractor {
	public PropertiesReader propertiesReader=null;
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

	/**
	 *  Initialize the voice extractor.
        The configuration parameters define and customize the voice extraction algorithm.
        If any of the configuration parameters is not provided a default value is used.

        @param voice_models: the voice models data structure
        @param params: configuration parameters (see table)

	 * 
	 * */
	public void init(){
		propertiesReader= Singleton.getSingletonObject().getProperties();

    }

	/**
        Launch the voice extractor on one audio resource.
        This method is asynchronous and returns a task handle.
		@return file_name_path: the path of the file of the resulting name
        @param resource_path: resource file path
	 * */	
    public String extractVoicesFromAudio(String resource_path, String save_as){
		DBScore dbscore=new DBScore();
		Diarization dia=new Diarization();
		boolean make_dia=true;
	
		dia.setFileName(resource_path);
		dia.setOutputRoot(propertiesReader.getProperty("outputRoot"));
		dia.setSms_gmms(propertiesReader.getProperty("sms_gmms"));
		dia.setUbm_gmm(propertiesReader.getProperty("ubm_gmm"));
		try {
			dia.run();
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		
		System.out.println("------ SCORING ------");
		dbscore.setDb_path(propertiesReader.getProperty("db_path"));
		dbscore.getMscore().setFileName(propertiesReader.getProperty("fileName"));
		dbscore.getMscore().setOutputRoot(propertiesReader.getProperty("outputRoot"));
		dbscore.getMscore().setUbm_gmm(propertiesReader.getProperty("ubm_gmm"));
		dbscore.getMscore().setSms_gmms(propertiesReader.getProperty("sms_gmms"));
		try {
			dbscore.run();
		} catch (Exception e1) {
			e1.printStackTrace();
		}

		System.out.println("------ DECISION ------");
		String listaNomiPresenti=null;
		//dbscore.getMscore().getClusterResultSet().printAll();
		System.out.println("------ printWithThr1e2 ------");
		//dbscore.getMscore().getClusterResultSet().printTheBest();
		listaNomiPresenti=dbscore.getMscore().getClusterResultSet().printWithThr1e2(Double.parseDouble("0.5"));
		System.out.println("------ printTheBestBySpeaker ------");
		
		//listaNomiPresenti=dbscore.getMscore().getClusterResultSet().printTheBestBySpeaker();
		//dbscore.getMscore().printTheBestBySpeaker();
		if (listaNomiPresenti!= null){
			try {
					OutputStreamWriter nomi_pres= new OutputStreamWriter(new FileOutputStream(dbscore.getMscore().getOutputRoot()+"/"+dbscore.getMscore().getBaseName()+".nomi.txt"));
					System.out.println("NOMI PRESENTI "+listaNomiPresenti);
					nomi_pres.write(listaNomiPresenti);
					nomi_pres.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
		}	

    	return dbscore.getMscore().getOutputRoot()+"/"+dbscore.getMscore().getBaseName()+".nomi.txt";
    }

}
