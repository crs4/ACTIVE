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


package it.crs4.active.train;

import java.lang.reflect.InvocationTargetException;
import java.util.logging.Level;
import java.util.logging.Logger;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.Cluster;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.libModel.Distance;
import fr.lium.spkDiarization.libModel.gaussian.GMM;
import fr.lium.spkDiarization.libModel.gaussian.GMMArrayList;
import fr.lium.spkDiarization.libModel.gaussian.GMMFactory;
import fr.lium.spkDiarization.parameter.Parameter;

 
public class MTrainMAP {
	Parameter parameter =null;
	/** The Constant logger. */
	private final static Logger logger = Logger.getLogger(MTrainMAP.class.getName());

	/**
	 * .
	 * 
	 * @param featureSet the feature set
	 * @param clusterSet the cluster set
	 * @param initializationGmmList the initialization gmm list
	 * @param gmmList the gmm list
	 * @param parameter the parameter
	 * @param resetAccumulator the reset accumulator
	 * @throws Exception the exception
	 */
	public void make(AudioFeatureSet featureSet, ClusterSet clusterSet, GMMArrayList initializationGmmList, GMMArrayList gmmList, Parameter parameter, boolean resetAccumulator) throws Exception {
		logger.info("Train models using MAP");

		if (initializationGmmList.size() != clusterSet.clusterGetSize()) {
			throw new DiarizationException("error \t initial model number is not good ");
		}
		for (int i = 0; i < initializationGmmList.size(); i++) {
			logger.finer("info : " + i + "=" + initializationGmmList.get(i).getName());
		}

		boolean useSpeechDetector = (parameter.getParameterInputFeature().getSpeechThreshold() > 0);

		for (int i = 0; i < initializationGmmList.size(); i++) {
			GMM initializationGmm = initializationGmmList.get(i);
			GMM ubmGmm = initializationGmmList.get(i);
			String name = initializationGmm.getName();
			Cluster cluster = clusterSet.getCluster(name);
			if (cluster == null) {
				for (String clusterName : clusterSet) {
					logger.fine("cluster/gmm: " + clusterName + "/" + name + " levenshtein="
							+ Distance.levenshteinDistance(clusterName, name));
					byte tabC[] = clusterName.getBytes();
					byte tabN[] = name.getBytes();
					for (int j = 0; j < Math.min(tabC.length, tabN.length); j++) {
						logger.fine("cluster/gmm char " + j + " = " + tabC[j] + " " + tabN[j]);
					}
				}

				throw new DiarizationException("error \t can't find cluster for model " + name);
			}
			logger.fine("\t train MAP cluster=" + cluster.getName() + " size=" + cluster.getLength());

			gmmList.add(GMMFactory.getMAP(cluster, featureSet, initializationGmm, ubmGmm, parameter.getParameterEM(), parameter.getParameterMAP(), parameter.getParameterVarianceControl(), useSpeechDetector, resetAccumulator));
		}
	}

	/**
	 * The main method.
	 * 
	 * @param args the arguments
	 * @throws Exception the exception
	 */
	public static void main(String[] args) throws Exception {}
	public  void run() throws Exception {
		try {
			SpkDiarizationLogger.setup();
			info(parameter, "MTrainMAP");
			if (parameter.show.isEmpty() == false) {
				// clusters
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);

				// Features
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);

				// Compute Model
				GMMArrayList initializationGmmList = MainTools.readGMMContainer(parameter);
				GMMArrayList gmmList = new GMMArrayList();

				make(featureSet, clusterSet, initializationGmmList, gmmList, parameter, true);

				MainTools.writeGMMContainer(parameter, gmmList);
			}
		} catch (DiarizationException e) {
			logger.log(Level.SEVERE, "error \t exception ", e);
			e.printStackTrace();
		}
	}

	/**
	 * Info.
	 * 
	 * @param parameter the parameter
	 * @param progam the progam
	 * @throws IllegalArgumentException the illegal argument exception
	 * @throws IllegalAccessException the illegal access exception
	 * @throws InvocationTargetException the invocation target exception
	 */
	public static void info(Parameter parameter, String progam) throws IllegalArgumentException, IllegalAccessException, InvocationTargetException {
		if (parameter.help) {
			logger.config(parameter.getSeparator2());
			logger.config("program name = " + progam);
			logger.config(parameter.getSeparator());
			parameter.logShow();

			parameter.getParameterInputFeature().logAll(); // fInMask
			logger.config(parameter.getSeparator());
			parameter.getParameterSegmentationInputFile().logAll(); // sInMask
			logger.config(parameter.getSeparator());
			parameter.getParameterModelSetInputFile().logAll(); // tInMask
			parameter.getParameterModelSetOutputFile().logAll(); // tOutMask
			logger.config(parameter.getSeparator());
			parameter.getParameterEM().logAll(); // emCtl
			parameter.getParameterMAP().logAll(); // mapCtrl
			parameter.getParameterVarianceControl().logAll(); // varCtrl
			logger.config(parameter.getSeparator());
		}
	}
	public Parameter getParameter() {
		return parameter;
	}
	public void setParameter(Parameter parameter) {
		this.parameter = parameter;
	}
}
