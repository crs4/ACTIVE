package it.crs4.active.api.copy;

import it.crs4.active.diarization.Diarization;
import it.crs4.identification.DBScore;
import it.crs4.util.PropertiesReader;

import java.util.Set;
/**
 * The package it.crs4.active.api contains all of the classes for creating a user model and for identify a person from an audio file.
 *<br>
 * Using this class is possible:<br> 
 * <br> <li>add an audio segment spoken by a single speaker (and a tag identifying the speaker) to the training set of the speaker recognition tool
 * <br> <li>remove an audio segment from the training set of the speaker recognition tool
 * <br> <li>rebuild the models of the training set of the speaker recognition.
 * <br> <li>execute the speaker recognition on a set of items. 
 * The class VoiceExtractor is used for detecting and recognizing voices in an audio stream.
 * <br>
<strong>Voice Extractor: an example</strong>
		String configuration="example.properties";
		VoiceExtractor voiceExtractor=new VoiceExtractor(configuration);
		Set speakers= voiceExtractor.getSpeakers();
		Iterator  it =speakers.iterator(); 
		System.out.println("The speaker in the file defined in the configuration.properties file");
		while(it.hasNext()){
			System.out.println("Speaker name "+it.next());
		}

 */
public class VoiceExtractor implements VoiceExtractorInterface {
	public PropertiesReader propertiesReader=null;
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}
	/**
	 * Construct a VoiceExtractor object with default configuration
	 * */
	public VoiceExtractor(){
		init();
	}
	
	/**
	 * Construct a VoiceExtractor object with the defined configuration file
	 * @parameter configuration: the path of configuration file 
	 * */	
	public VoiceExtractor(String configuration){
		init(configuration);
	}	
	
	/* (non-Javadoc)
	 * @see it.crs4.active.api.VoiceExtractorInterface#init()
	 */
	@Override
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
	 * @see it.crs4.active.api.VoiceExtractorInterface#extractVoicesFromAudio(java.lang.String, java.lang.String)
	 */	
    @Override
	public String extractVoicesFromAudio(String resource_path, String save_as){
    	
    	return "";
    }
	private String threshold="0.21";
	/**
	 * @return the threshold
	 */
	public String getThreshold() {
		return threshold;
	}
	/**
	 * Force the threshold parameter to the new value 
	 * @param threshold The threshold to set
	 */
	public void setThreshold(String threshold) {
		this.threshold = threshold;
	}
	
	private boolean forceSetThreshold=false;

	/**
	 * 
	 * @return the forceSetThreshold
	 */
	public boolean isForceSetThreshold() {
		return forceSetThreshold;
	}
	
	
	/**
	 * Returns the speaker in the audio file
	 * @return A set of name of the detected speaker
	 * */
    public Set<String> getSpeakers(){
		DBScore dbscore=new DBScore();
		Diarization dia=new Diarization();
		boolean make_dia=true;
	
		dia.setFileName(propertiesReader.getProperty("fileName"));
		dia.setOutputRoot(propertiesReader.getProperty("outputRoot"));
		dia.setSms_gmms(propertiesReader.getProperty("sms_gmms"));
		dia.setUbm_gmm(propertiesReader.getProperty("ubm_gmm"));
		try {
			dia.run();
		} catch (Exception e1) {
			e1.printStackTrace();
		}

		String thr=getThreshold();
		if (!isForceSetThreshold()){
			if(propertiesReader.getProperty("thr")!=null){
				thr=propertiesReader.getProperty("thr");
			}
		}
		
		System.out.println("------ SCORING ------");
		dbscore.setDb_path(propertiesReader.getProperty("db_path"));
		dbscore.getMscore().setFileName(propertiesReader.getProperty("fileName"));
		dbscore.getMscore().setOutputRoot(propertiesReader.getProperty("outputRoot"));
		dbscore.getMscore().setUbm_gmm(propertiesReader.getProperty("ubm_gmm"));
		dbscore.getMscore().setSms_gmms(propertiesReader.getProperty("sms_gmms"));
		try {
			dbscore.run();
			dbscore.score(thr);
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		Set<String> speakers=dbscore.getSpeaker();
		return speakers;
    }
}
