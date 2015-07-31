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

import it.crs4.active.diarization.Diarization;
import it.crs4.active.train.Main;
import it.crs4.util.PropertiesReader;

import java.io.File;

public class DataSetManager {

	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		
		PropertiesReader pr=new PropertiesReader(args[0]);
		DataSetManager dsm=new DataSetManager();
		dsm.makeDataset(pr);

	}
	public void makeDataset(PropertiesReader pr) throws Exception{
		File pathFile=new File(pr.getProperty("modelDir"));
		File listFile[] = pathFile.listFiles();
		
		for(int i=0;i<listFile.length;i++){	 
			String gmmName=listFile[i].getName().split("##")[0].replace("_", "");			
			runTrain(pr, gmmName);
		}
	}
	

	public void runTrain(PropertiesReader pr, String gmmName) throws Exception{

		Diarization dia=new Diarization();
		dia.setFileName(pr.getProperty("fileName"));
		dia.setOutputRoot(pr.getProperty("outputRoot"));
		dia.setSms_gmms(pr.getProperty("sms_gmms"));
		dia.setUbm_gmm(pr.getProperty("ubm_gmm"));
		
		dia.run();
		
		Main ma=new Main();
		ma.setFileName(pr.getProperty("fileName"));
		ma.setOutputRoot(pr.getProperty("outputRoot"));
		ma.setSms_gmms(pr.getProperty("sms_gmms"));
		ma.setUbm_gmm(pr.getProperty("ubm_gmm"));
		
		if(pr.getProperty("gmmRoot")!=null){
			ma.setGmmRoot(pr.getProperty("gmmRoot"));
		}else{
			ma.setGmmRoot(pr.getProperty("outputRoot"));
		}
		

		ma.setGmmName(gmmName);

		ma.run();
	 	
	}
}