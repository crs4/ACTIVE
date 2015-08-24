package it.crs4.identification;

 
import it.crs4.active.diarization.Diarization;
import it.crs4.util.PropertiesReader;
import java.io.File;
 import java.util.HashMap;
 import java.util.Hashtable;
import java.util.Iterator;
 import java.util.Map;
import java.util.Set;
 import java.util.Vector;
import java.io.*;

/**
 This class perform an identification of a person from characteristics of voices. 
* On the other hand, identification is the task of determining an unknown speaker's identity.
* This class perform a text-independet sistem: the text during enrollment and test is different 

 *<br> <strong> An example of properties file is:</strong> <br>
 *<br> the path of the wav audio file to be processed
 *             <br><i>fileName=/Users/example.wav</i>
 *             <br><br>the location of intermediate build files<br>
 *             <i>outputRoot=/Users/out/</i>
 *             <br><br>The path of the ubm.gmm file
 *             <br><i>ubm_gmm=/Users/ubm.gmm</i>
 *             <br><br>The location of the sms.gmms file<br><i>sms_gmms=/Users/sms.gmms</i>
 *             
 *             <br><br>The path of the models file<br><i>db_path=/Users/db_path/</i>  
 *             
 *             <br><br>The name of generated model<br>
 *             <i>gmmName=exampleName</i>
 *             
 *             <br><br> The location of generated model <br><br><i>modelDir=/Users/audio_model/</i>
* @author Felice Colucci
*
*/

public class Identification {
	
	public  Vector<String> getFiles(File pathFile, String estensione) {

		File listFile[] = pathFile.listFiles();
		Vector<String> vecFile=new Vector<String>();
		if (listFile != null) {
			for (int i = 0; i < listFile.length; i++) {
					if (estensione != null) {
						if (listFile[i].getName().endsWith(estensione)) {
							vecFile.add(listFile[i].getPath());
							//System.out.println("File di Import selezionato: [ "
							//		+ listFile[i].getPath() + " ]");
						}
					} 
			}
		}
		return vecFile;

	}
	
	
	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		
		Identification dbscore=new Identification();
		PropertiesReader pr=new PropertiesReader(args[0]);
		Diarization dia=new Diarization();
		boolean make_dia=true;
		System.out.println("------------"+ pr.getAllPropertyNames());
		
		String thr="0.1";
		if(pr.getProperty("thr")!=null){
			thr=pr.getProperty("thr");
		}
		
		if (args.length>1){
			if (args[1].equals("nodiarization")){
				make_dia=false;	
			}
		}	
		if(make_dia){
			dia.setFileName(pr.getProperty("fileName"));
			dia.setOutputRoot(pr.getProperty("outputRoot"));
			dia.setSms_gmms(pr.getProperty("sms_gmms"));
			dia.setUbm_gmm(pr.getProperty("ubm_gmm"));
			dia.run();
		}
		
		System.out.println("------ SCORING ------");
		dbscore.setDb_path(pr.getProperty("db_path"));
		dbscore.getMscore().setFileName(pr.getProperty("fileName"));
		dbscore.getMscore().setOutputRoot(pr.getProperty("outputRoot"));
		dbscore.getMscore().setUbm_gmm(pr.getProperty("ubm_gmm"));
		dbscore.getMscore().setSms_gmms(pr.getProperty("sms_gmms"));
		dbscore.run();

		System.out.println("------ DECISION ------");
		String listaNomiPresenti=null;
		//dbscore.getMscore().getClusterResultSet().printAll();
		System.out.println("------ printWithThr1e2 ------");
		//dbscore.getMscore().getClusterResultSet().printTheBest();
		listaNomiPresenti=dbscore.getMscore().getClusterResultSet().printWithThr1e2(Double.parseDouble(thr));
		
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
	}

	/**
	 * @param args
	 * @throws Exception 
	 */
	public void exec(String[] args) throws Exception {
		
		PropertiesReader pr=new PropertiesReader(args[0]);
		Diarization dia=new Diarization();
		boolean make_dia=true;
		System.out.println("------------"+ pr.getAllPropertyNames());
		
		String thr="0.1";
		if(pr.getProperty("thr")!=null){
			thr=pr.getProperty("thr");
		}
		
		if (args.length>1){
			if (args[1].equals("nodiarization")){
				make_dia=false;	
			}
		}	
		if(make_dia){
			dia.setFileName(pr.getProperty("fileName"));
			dia.setOutputRoot(pr.getProperty("outputRoot"));
			dia.setSms_gmms(pr.getProperty("sms_gmms"));
			dia.setUbm_gmm(pr.getProperty("ubm_gmm"));
			dia.run();
		}
		
		System.out.println("------ SCORING ------");
		setDb_path(pr.getProperty("db_path"));
		getMscore().setFileName(pr.getProperty("fileName"));
		getMscore().setOutputRoot(pr.getProperty("outputRoot"));
		getMscore().setUbm_gmm(pr.getProperty("ubm_gmm"));
		getMscore().setSms_gmms(pr.getProperty("sms_gmms"));
		run();

		System.out.println("------ DECISION ------");
		String listaNomiPresenti=null;
		//dbscore.getMscore().getClusterResultSet().printAll();
		System.out.println("------ printWithThr1e2 ------");
		//dbscore.getMscore().getClusterResultSet().printTheBest();
		listaNomiPresenti=getMscore().getClusterResultSet().printWithThr1e2(Double.parseDouble(thr));
		
		//listaNomiPresenti=dbscore.getMscore().getClusterResultSet().printTheBestBySpeaker();
		//dbscore.getMscore().printTheBestBySpeaker();
		if (listaNomiPresenti!= null){
			try {
					OutputStreamWriter nomi_pres= new OutputStreamWriter(new FileOutputStream(getMscore().getOutputRoot()+"/"+getMscore().getBaseName()+".nomi.txt"));
					System.out.println("NOMI PRESENTI "+listaNomiPresenti);
					nomi_pres.write(listaNomiPresenti);
					nomi_pres.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
		}	
	}
	private Hashtable<String, String> result=null;
	
	private void processResult(String result){
		this.result=new Hashtable<String, String>();
		String[] nomi=result.split("\n");
		for(int i=0;i<nomi.length;i++){
			String rig=nomi[i];
			if (rig.length()>3){
				this.result.put(rig.split(" ")[0], rig.split(" ")[1]);		
			}
		}
	}
	public void score(String thr){
		String listaNomiPresenti=null;
		listaNomiPresenti= getMscore().getClusterResultSet().printWithThr1e2(Double.parseDouble(thr));	
		processResult(listaNomiPresenti);
	}
	public Set<String> getSpeaker(){
		return result.keySet();
	}
	
	public Hashtable<String, String> getResult(){
		return result;
	}
	
	public void run() throws Exception{
		//getMscore().setFileName("/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/angelina.wav");
		//getMscore().setOutputRoot("/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/angelina/");
		Vector<String> filesVec=this.getFiles(new File(this.db_path), "gmm");
		Iterator<String> it=filesVec.iterator();
		 
		Map<String, Ratio> clusterRatioSet=new HashMap<String, Ratio>();
		while(it.hasNext()){
			 
			String fl_gmm = (String) it.next();
			System.out.println("gmm ---> "+fl_gmm);
			mscore.setGmm_model(fl_gmm);
			mscore.run();
		}
		
	}
	private String db_path=null;
	private MScore mscore=new MScore();
	public String getDb_path() {
		return db_path;
	}
	public void setDb_path(String db_path) {
		this.db_path = db_path;
	}
	public MScore getMscore() {
		return mscore;
	}
	public void setMscore(MScore mscore) {
		this.mscore = mscore;
	}
}
