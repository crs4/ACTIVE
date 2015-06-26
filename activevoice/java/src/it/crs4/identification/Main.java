package it.crs4.identification;

import it.crs4.active.diarization.Diarization;
import it.crs4.util.PropertiesReader;

import java.io.File;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Vector;

import java.io.*;
public class Main {
	
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
		
		Main dbscore=new Main();
		PropertiesReader pr=new PropertiesReader(args[0]);
		Diarization dia=new Diarization();
		boolean make_dia=true;
		System.out.println("------------"+ pr.getAllPropertyNames());
		
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
			/*
			Iterator<String> iter = mscore.getClusterSetResult().iterator(); 
			while (iter.hasNext ())
				{
				    String s = iter.next();
				    //Ratio r =new Ratio();
				    //String info_all=mscore.getClusterSetResult().getCluster(s).getInformations();
				    Cluster spe= mscore.getClusterSetResult().getCluster(s);
				    TreeMap<String, Object> info=mscore.getClusterSetResult().getCluster(s).getInformation();
				    Iterator<String> info_it=info.keySet().iterator();
				    while(info_it.hasNext()){
				    	String k = info_it.next();
				    	System.out.println ("clustername="+s+"name="+k+"****"+info.get(k));
				    	Ratio r=null;
				    	if(clusterRatioSet.containsKey("clustername="+s+"name="+k)){
				    		r=clusterRatioSet.get("clustername="+s+"name="+k);
				    	}else{
				    		r =new Ratio();
				    	}
				    	String[] value= {"clustername="+s,"name="+k,"info="+info.get(k).toString()};
				    	System.out.println ("@@@@"+info.get(k).toString()+"***"+value[0]+"!"+value[1]+"!"+value[2] );
				    	r.getUnsortMap().put(Double.parseDouble(info.get(k).toString()),value);
				    	System.out.println("clustername="+s+"name="+k);
				    	
				    	clusterRatioSet.put("clustername="+s+"name="+k, r);
				    }
				};
				 
			}
		Iterator<String> it_set=clusterRatioSet.keySet().iterator();
		while(it_set.hasNext()){
			
			String key=(String)it_set.next();
			System.out.println("----++++--------"+ key+"------------");
			Ratio r =(Ratio)clusterRatioSet.get(key);
			Iterator keyit=r.getUnsortMap().keySet().iterator();
			while(keyit.hasNext()){
				Double kk=(Double)keyit.next();
				System.out.println("****"+((String[])r.getUnsortMap().get(kk))[0]+"****"+((String[])r.getUnsortMap().get(kk))[1]+"****"+((String[])r.getUnsortMap().get(kk))[2]);
				
			}
			*/
			//r.run();
			//r.printMap(r.getUnsortMap());
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
