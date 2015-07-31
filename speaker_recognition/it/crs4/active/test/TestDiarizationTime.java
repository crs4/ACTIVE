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
import it.crs4.util.PropertiesReader;

import java.io.File;
import java.util.*;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

public class TestDiarizationTime {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
	      try {
	    	  long durata_totale=(long)0; 
	    	  String tmp_arg=args[0];//"/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties";
	    	  Logger logger = Logger.getLogger("logger"); 
	    	  
	    	  FileHandler fh=new FileHandler(tmp_arg+"/"+"log.log");  
	          logger.addHandler(fh);
	          SimpleFormatter formatter = new SimpleFormatter();  
	          fh.setFormatter(formatter);  
	          
	    	  File dir = new File(tmp_arg);
	    	  String[] files = dir.list();
	    	  for (int i = 0; i < files.length; i++) {
	    		  if (files[i].endsWith("properties")){
		    		System.out.println(files[i]);
	    	        long start = System.currentTimeMillis( );
	    	        PropertiesReader pr=new PropertiesReader(tmp_arg+"/"+files[i]);
    	    		System.out.println(pr.getProperty("fileName"));
    	    		System.out.println(pr.getProperty("outputRoot"));
    	    		System.out.println(pr.getProperty("sms_gmms"));
    	    		System.out.println(pr.getProperty("ubm_gmm"));
	    	        Diarization dia=new Diarization();
		    		dia.setFileName(pr.getProperty("fileName"));
		    		dia.setOutputRoot(pr.getProperty("outputRoot"));
		    		dia.setSms_gmms(pr.getProperty("sms_gmms"));
		    		dia.setUbm_gmm(pr.getProperty("ubm_gmm"));
		    		dia.run();
		    		
		    		long end = System.currentTimeMillis();
		    		long diff = end - start;
		    		logger.info(files[i] +" diarization time= "+diff);
	    			durata_totale=durata_totale+diff;  
	    		  }
	    	  }
	    	  logger.info("DURATA TOTALE="+durata_totale);
	       } catch (Exception e) {
	          e.printStackTrace();
	       }

	}
}
