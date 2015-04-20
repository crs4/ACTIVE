package it.crs4.identification;

import java.io.File;
import java.util.Iterator;
import java.util.List;
import java.util.Vector;

public class DBScore {
	
	public  Vector getFiles(File pathFile, String estensione) {

		File listFile[] = pathFile.listFiles();
		Vector vecFile=new Vector();
		if (listFile != null) {
			for (int i = 0; i < listFile.length; i++) {
					if (estensione != null) {
						if (listFile[i].getName().endsWith(estensione)) {
							vecFile.add(listFile[i].getPath());
							System.out.println("File di Import selezionato: [ "
									+ listFile[i].getPath() + " ]");
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
		DBScore dbscore=new DBScore();
		dbscore.setDb_path("/Users/labcontenuti/Documents/workspace/AudioActive/84/gmm_db/");
		dbscore.run();
	}
	public void run() throws Exception{
		getMscore().setFileName("/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/angelina.wav");
		getMscore().setOutputRoot("/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/out/angelina/");
		Vector filesVec=this.getFiles(new File(this.db_path), "gmm");
		Iterator it=filesVec.iterator();
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
