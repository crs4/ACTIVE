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
package it.crs4.identification;
 /**
  The package it.crs4.identification perform the identification of a person from characteristics of voices. 
 * On the other hand, identification is the task of determining an unknown speaker's identity.
 * 
 * This class is the entry point for the identification process <br>
 *<br> <strong> An example: </strong> <br>
 *<br> <i> java it.crs4.active.Main example.properties </i> <br>
 *				<br> <strong> An example of properties file is: </strong> <br>
 * 			   <br> the path of the wav audio file to be processed
 *             <br><i>fileName=/Users/example.wav</i>
 *             <br><br>the location of intermediate build file
 *             <br><i>outputRoot=/Users/out/</i>
 *             <br><br>The path of the ubm.gmm file
 *             <br><i>ubm_gmm=/Users/ubm.gmm</i>
 *             
 *             <br><br>The location of the sms.gmms file
 *             <br><i>sms_gmms=/Users/sms.gmms</i>
 *             
 *             <br><br>The path of the models file
 *             <br><i>db_path=/Users/db_path/</i>  
 *             
 *             <br><br>The name of generated model<br>
 *             <i>gmmName=RemoBodei</i>
 *             
 *             <br><br>The location of generated model <br><i>modelDir=/Users/audio_model/</i>
 *             
 * Entry point for the identification process<br>
 * <strong> Example </strong> <br>
 * <code>java -jar all_the_jar it.crs4.active.identification.Main example.properties </code>
 * 
 * @author Felice Colucci
 * 
 * */

import it.crs4.active.diarization.Diarization;
import it.crs4.util.PropertiesReader;
import java.io.File;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Vector;
import java.io.*;

/**
* Entry point for the identification process
* 
* <strong> Example </strong> <br>
* <code>java -jar all_the_jar it.crs4.active.identification.Main example.properties </code>
* 
* */
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
