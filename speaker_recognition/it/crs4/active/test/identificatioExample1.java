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
import it.crs4.identification.Main;
import it.crs4.util.PropertiesReader;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

public class identificatioExample1 {

	/**
	 * @param args
	 * @throws Exception
	 *             An example of properties file is: <br />
	 *             <br />fileName=example.wav
	 *             <br />outputRoot=/Users/out/
	 *             <br />ubm_gmm
	 *             =/Users/ubm.gmm
	 *             <br />sms_gmms=/Users/sms.gmms
	 *             <br />db_path=/Users/2el/ 
	 *             # gmmName= serve soltanto in fase di treining
	 *             <br />gmmRoot
	 *             =/Users/2el/
	 *             <br />modelDir=/Users/audio_model/
	 */
	public static void main(String[] args) throws Exception {
		Main dbscore = new Main();
		PropertiesReader pr = new PropertiesReader(args[0]);
		Diarization dia = new Diarization();
		boolean make_dia = true;
		System.out.println("------------" + pr.getAllPropertyNames());

		if (args.length > 1) {
			if (args[1].equals("nodiarization")) {
				make_dia = false;
			}
		}
		if (make_dia) {
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
		String listaNomiPresenti = null;
		// dbscore.getMscore().getClusterResultSet().printAll();
		System.out.println("------ printWithThr1e2 ------");
		// dbscore.getMscore().getClusterResultSet().printTheBest();
		listaNomiPresenti = dbscore.getMscore().getClusterResultSet()
				.printWithThr1e2(Double.parseDouble("0.5"));
		System.out.println("------ printTheBestBySpeaker ------");

		// listaNomiPresenti=dbscore.getMscore().getClusterResultSet().printTheBestBySpeaker();
		// dbscore.getMscore().printTheBestBySpeaker();
		if (listaNomiPresenti != null) {
			try {
				OutputStreamWriter nomi_pres = new OutputStreamWriter(
						new FileOutputStream(dbscore.getMscore()
								.getOutputRoot()
								+ "/"
								+ dbscore.getMscore().getBaseName()
								+ ".nomi.txt"));
				System.out.println("NOMI PRESENTI " + listaNomiPresenti);
				nomi_pres.write(listaNomiPresenti);
				nomi_pres.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}

	}

}
