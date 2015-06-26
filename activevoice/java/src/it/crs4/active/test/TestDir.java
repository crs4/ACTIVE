package it.crs4.active.test;

import fr.lium.experimental.spkDiarization.libClusteringData.speakerName.SpeakerName;
import fr.lium.spkDiarization.libClusteringData.Cluster;
import it.crs4.active.diarization.Diarization;
import it.crs4.util.PropertiesReader;
import it.crs4.identification.DBScore;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
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


public class TestDir {
	
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
	public boolean verify(String nomeCalcolato, String nomeAtteso){
		
		return true;
	}
	public String getTrueName(String filename){
		String tmp=filename.split("/")[-1];
		return tmp.split(".wav")[0];
	}	
	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		
		TestDir testdir=new TestDir();
		testdir.run(args);
		
	}
	
		public void run(String[] args) throws Exception {
		DBScore dbscore=new DBScore();
		PropertiesReader pr=new PropertiesReader(args[0]);
		Diarization dia=new Diarization();
		boolean make_dia=true;
		
		String thr="0.21";
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
		listaNomiPresenti=dbscore.getMscore().getClusterResultSet().printWithThr1e2(Double.parseDouble(thr));
		String[] nomi=listaNomiPresenti.split("\n");
		boolean verify_ok=true;
		String trueName=getTrueName(pr.getProperty("fileName"));
		for (int i=0;i<nomi.length&&verify_ok;i++){
			verify_ok=(nomi[i]==trueName);
		}
		System.out.println("Test: "+pr.toString());
		if(verify_ok){
			System.out.println("*********************  OK ***** "+ trueName );
		}else{ 
			System.out.println("-----------------  ERROR " );
			for (int i=0;i<nomi.length;i++){
				System.out.println("+"+ nomi[i] );
			}			
		}
	}
}
