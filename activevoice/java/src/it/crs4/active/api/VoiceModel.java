/**
 * 
 */
package it.crs4.active.api;
import java.io.File;

import it.crs4.active.train.Main;
import it.crs4.util.PropertiesReader;

/**
 *  
 *  The persistent data structure containing the voice models used by the 
 *  voice recognition algorithm and replicated on each worker.<br />
 *  This class ensures that the voice models are replicated and updated on each worker.
 */
/**
 * @author Felice Colucci
 *
 */
public class VoiceModel implements VoiceModelInterface {
	public PropertiesReader propertiesReader=null;

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}
	

	/**
	 * @param args
	 */
	public void init(){ 
		
		propertiesReader= Singleton.getSingletonObject().getProperties();
		
	}

	/* (non-Javadoc)
	 * @see it.crs4.active.api.VoiceModelInterface#addVoice(java.lang.String, java.lang.String)
	 */
	
	@Override
	public void addVoice(String filename, String tag){
		
		it.crs4.active.train.Main train=new it.crs4.active.train.Main();
		train.setFileName(filename);
		train.setOutputRoot(propertiesReader.getProperty("outputRoot"));
		train.setSms_gmms(propertiesReader.getProperty("sms_gmms"));
		train.setUbm_gmm(propertiesReader.getProperty("ubm_gmm"));
		
		if(propertiesReader.getProperty("gmmRoot")!=null){
			train.setGmmRoot(propertiesReader.getProperty("gmmRoot"));
		}else{
			train.setGmmRoot(propertiesReader.getProperty("outputRoot"));
		}
		
		train.setGmmName(tag);
		try {
			train.run();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/* (non-Javadoc)
	 * @see it.crs4.active.api.VoiceModelInterface#addVoice(java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String)
	 */
	
	@Override
	public void addVoice(String filename, String tag, String outputRoot, String sms_gmms,String ubm_gmm, String gmmRoot){
		
		it.crs4.active.train.Main train=new it.crs4.active.train.Main();
		
		train.setFileName(filename);
		
		if(outputRoot==null){
			train.setOutputRoot(propertiesReader.getProperty("outputRoot"));
		}
		
		if(sms_gmms==null){
			train.setSms_gmms(propertiesReader.getProperty("sms_gmms"));
		}
		
		if(ubm_gmm==null){
		train.setUbm_gmm(propertiesReader.getProperty("ubm_gmm"));
		}
		
		if(gmmRoot==null){
			if(propertiesReader.getProperty("gmmRoot")!=null){
				train.setGmmRoot(propertiesReader.getProperty("gmmRoot"));
			}else{
				train.setGmmRoot(propertiesReader.getProperty("outputRoot"));
			}
		}

		train.setGmmName(tag);

		try {
			train.run();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}	
	
	
	/* (non-Javadoc)
	 * @see it.crs4.active.api.VoiceModelInterface#addVoices(java.lang.String[], java.lang.String[])
	 */
	
	@Override
	public void addVoices(String[] filenames, String[] tags){
		for (int i=0;i<filenames.length;i++){
			addVoice(filenames[i], tags[i]);
		}
	}

    /* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "VoiceModel [propertiesReader=" + propertiesReader
				+ ", getClass()=" + getClass() + ", hashCode()=" + hashCode()
				+ ", toString()=" + super.toString() + "]";
	}


	/* (non-Javadoc)
	 * @see it.crs4.active.api.VoiceModelInterface#renameTag(java.lang.String, java.lang.String)
	 */	
    @Override
	public void renameTag(String old_tag, String new_tag){
    	
    	String db=propertiesReader.getProperty("gmmRoot");
    	String model_path=db+old_tag;
    	File file = new File(old_tag);
        File file2 = new File(new_tag);
        //if(file2.exists()) throw new java.io.IOException("file exists");
        boolean success = file.renameTo(file2);
        System.out.print("renameTag "+old_tag+ " to "+new_tag +"---> "+success);
    }
}
