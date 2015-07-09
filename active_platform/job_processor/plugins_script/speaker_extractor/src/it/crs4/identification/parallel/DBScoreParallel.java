package it.crs4.identification.parallel;

import fr.lium.experimental.spkDiarization.libClusteringData.speakerName.SpeakerName;
import fr.lium.spkDiarization.libClusteringData.Cluster;
import it.crs4.active.diarization.Diarization;
import it.crs4.util.PropertiesReader;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.Vector;

import java.io.*;
public class DBScoreParallel {
	
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
		
		DBScoreParallel dbscore=new DBScoreParallel();
		PropertiesReader pr=new PropertiesReader(args[0]);
		Diarization dia=new Diarization();
		boolean make_dia=false;

		if (args.length>1){
			if (args[1].equals("diarization")){
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

		dbscore.setDb_path(pr.getProperty("db_path"));
		
		dbscore.getMscore().setFileName(pr.getProperty("fileName"));
		dbscore.getMscore().setOutputRoot(pr.getProperty("outputRoot"));
		dbscore.getMscore().setUbm_gmm(pr.getProperty("ubm_gmm"));
		dbscore.getMscore().setSms_gmms(pr.getProperty("sms_gmms"));

		System.out.println("s_inputMaskRoot "+pr.getProperty("s_inputMaskRoot"));
		dbscore.getMscore().setS_inputMaskRoot(pr.getProperty("s_inputMaskRoot"));
		
		System.out.println("s_outputMaskRoot "+pr.getProperty("s_outputMaskRoot"));		
		dbscore.getMscore().setS_outputMaskRoot(pr.getProperty("s_outputMaskRoot"));

		dbscore.run();

		System.out.println("------ DECISION ------");
		//dbscore.getMscore().getClusterResultSet().printAll();
		
		//dbscore.getMscore().getClusterResultSet().printTheBest();
		//dbscore.getMscore().getClusterResultSet().printWithThr1e2(Double.parseDouble("0.1"));

		String listaNomiPresenti=null;
		listaNomiPresenti=dbscore.getMscore().getClusterResultSet().printTheBestBySpeaker();
		//dbscore.getMscore().printTheBestBySpeaker();
		if (listaNomiPresenti != null){
			try {
					OutputStreamWriter nomi_pres= new OutputStreamWriter(new FileOutputStream(dbscore.getMscore().getOutputRoot()+"/"+dbscore.getMscore().getBaseName()+".nomi.txt",true));
					System.out.println("NOMI PRESENTI "+listaNomiPresenti);
					nomi_pres.write(listaNomiPresenti);
					nomi_pres.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
		}	
	}
	public void run() throws Exception{
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
	private MScoreParallel mscore=new MScoreParallel();
	public String getDb_path() {
		return db_path;
	}
	public void setDb_path(String db_path) {
		this.db_path = db_path;
	}
	public MScoreParallel getMscore() {
		return mscore;
	}
	public void setMscore(MScoreParallel mscore) {
		this.mscore = mscore;
	}
}
