package it.crs4.active.test;

import it.crs4.active.diarization.Diarization;
import it.crs4.active.train.Main;
import it.crs4.util.PropertiesReader;

import java.io.File;

public class DataSetManager {

	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		
		PropertiesReader pr=new PropertiesReader(args[0]);
		DataSetManager dsm=new DataSetManager();
		dsm.makeDataset(pr);

	}
	public void makeDataset(PropertiesReader pr) throws Exception{
		File pathFile=new File(pr.getProperty("modelDir"));
		File listFile[] = pathFile.listFiles();
		
		for(int i=0;i<listFile.length;i++){	 
			String gmmName=listFile[i].getName().split("##")[0].replace("_", "");			
			runTrain(pr, gmmName);
		}
	}
	

	public void runTrain(PropertiesReader pr, String gmmName) throws Exception{

		Diarization dia=new Diarization();
		dia.setFileName(pr.getProperty("fileName"));
		dia.setOutputRoot(pr.getProperty("outputRoot"));
		dia.setSms_gmms(pr.getProperty("sms_gmms"));
		dia.setUbm_gmm(pr.getProperty("ubm_gmm"));
		
		dia.run();
		
		Main ma=new Main();
		ma.setFileName(pr.getProperty("fileName"));
		ma.setOutputRoot(pr.getProperty("outputRoot"));
		ma.setSms_gmms(pr.getProperty("sms_gmms"));
		ma.setUbm_gmm(pr.getProperty("ubm_gmm"));
		
		if(pr.getProperty("gmmRoot")!=null){
			ma.setGmmRoot(pr.getProperty("gmmRoot"));
		}else{
			ma.setGmmRoot(pr.getProperty("outputRoot"));
		}
		

		ma.setGmmName(gmmName);

		ma.run();
	 	
	}
}