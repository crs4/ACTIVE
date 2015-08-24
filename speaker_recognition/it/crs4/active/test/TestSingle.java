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


public class TestSingle {
	public TestSingle(){}
	private String configurationProperties="";
	public TestSingle(String config){
		this.configurationProperties=config;
		
	}
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
		String res="";
		try{
			String[] a=filename.split("/");
			String basename=a[a.length-1];
			String tmp=basename.split("##")[0];
			String[] nc=tmp.split("_");
			return nc[0]+nc[1];
		}catch(Exception ex){
			ex.printStackTrace();
		}
		return res;
	}	
	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		
		TestSingle test=new TestSingle();
		String tn= test.getTrueName("/Users/labcontenuti/Music/Bodei/Remo_Bodei##1min-2.wav");
		System.out.println(tn);
		test.run(args);
		
	}
	private String threshold="0.21";
	/**
	 * @return the threshold
	 */
	public String getThreshold() {
		return threshold;
	}
	/**
	 * @param threshold the threshold to set
	 */
	public void setThreshold(String threshold) {
		this.threshold = threshold;
	}
	private boolean forceSetThreshold=false;

	public void runPrpperties(String properties){
		try {
			run(new String[]{properties});
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	public void run() throws Exception {
		runPrpperties(this.configurationProperties);
	}
	public void run(String[] args) throws Exception {
		DBScore dbscore=new DBScore();
		PropertiesReader pr=new PropertiesReader(args[0]);
		Diarization dia=new Diarization();
		boolean make_dia=true;
		
		String thr=getThreshold();
		if (!isForceSetThreshold()){
			if(pr.getProperty("thr")!=null){
				thr=pr.getProperty("thr");
			}
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
		dbscore.score(thr);
		
		Set<String> speakers=dbscore.getSpeaker();
		boolean verify_ok=true;
		String trueName=getTrueName(pr.getProperty("fileName"));
		Iterator<String> sp= speakers.iterator();
		while(sp.hasNext()){
			if(!trueName.equals(sp.next())){
				verify_ok=false;
			}
		}
		System.out.println("DiarizationExample: "+pr.toString());
		info.put(PROPERTIES, args[0]);
		info.put(SPEAKERS, speakers);
		if(verify_ok){
			System.out.println("*********************  OK ***** "+ trueName );
			info.put(VERIFY, VERIFYOK);
		}else{ 
			System.out.println("-----------------  ERROR " );
			info.put(VERIFY, VERIFYERROR);
			while(sp.hasNext()){
				System.out.println(sp.next());
				
			}		
		}
	}
	/**
	 * @return the forceSetThreshold
	 */
	public boolean isForceSetThreshold() {
		return forceSetThreshold;
	}
	/**
	 * @param forceSetThreshold the forceSetThreshold to set
	 */
	public void setForceSetThreshold(boolean forceSetThreshold) {
		this.forceSetThreshold = forceSetThreshold;
	}
	private Hashtable<String, Object> info=new Hashtable<String, Object>();
	/**
	 * @return the info
	 */
	public Hashtable<String, Object> getInfo() {
		return info;
	}
	public static String PROPERTIES="properties";
	public static String VERIFY="verify";
	public static String VERIFYOK="verify_ok";
	public static String VERIFYERROR="verify_error";
	public static String SPEAKERS="speakers";
}
