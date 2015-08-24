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

package it.crs4.active.api.copy;
import java.io.File;

import it.crs4.active.train.Main;
import it.crs4.util.PropertiesReader;
 
public class VoiceModel implements VoiceModelInterface {
	
	/**
	 * Encapsulate configuration parameter. <br>
	 * Refer <i>SingletonParameter</i> class for details. 
	 * */	
	public PropertiesReader propertiesReader=null;

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		 

	}
	
	/**
	 * Construct a VoiceModel object with default configuration
	 * */
	public VoiceModel(){
		init();
	}
	
	/**
	 * Construct a VoiceModel object with the defined configuration file
	 * @parameter configuration: the path of configuration file 
	 * */	
	public VoiceModel(String configuration){
		init(configuration);
	}

	/**
	 * Default initialization routine. 
	 * */
	public void init(){ 
		propertiesReader= Singleton.getSingletonObject().getProperties();
	}

	
	/**
	 * Initialization routine using the configuration file 
	 * @param configuration: the path of configuration file 
	 * */	
	public void init(String configuration){ 
		propertiesReader= Singleton.getSingletonObject().getProperties(configuration);		
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
		}else{
			train.setOutputRoot(outputRoot);
		}
		
		if(sms_gmms==null){
			train.setSms_gmms(propertiesReader.getProperty("sms_gmms"));
		}else{
			train.setSms_gmms(sms_gmms);
		}
		
		if(ubm_gmm==null){
			train.setUbm_gmm(propertiesReader.getProperty("ubm_gmm"));
		}else{
			train.setUbm_gmm(ubm_gmm);
		}
		
		if(gmmRoot==null){
			if(propertiesReader.getProperty("gmmRoot")!=null){
				train.setGmmRoot(propertiesReader.getProperty("gmmRoot"));
			}else{
				train.setGmmRoot(propertiesReader.getProperty("outputRoot"));
			}
		}else{
			train.setGmmRoot(gmmRoot);
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
