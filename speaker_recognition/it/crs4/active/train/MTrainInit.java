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
import fr.lium.spkDiarization.libModel.gaussian.GMMArrayList;
import fr.lium.spkDiarization.libModel.gaussian.GMMFactory;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.parameter.ParameterInitializationEM.ModelInitializeMethod;

/**
 * The Class MTrainInit.
 */
public class MTrainInit {
	
	Parameter parameter =null;
	String parameter_path=null;
	
	public MTrainInit() {
		super();
	}
	
	/**
	 * Return the path of parameter file
	 * @return parameter_path
	 * */
	public String getParameter_path() {
		return parameter_path;
	}
	
	/**
	 * Sets the path of parameter file
	 * @param parameter_path
	 * */
	public void setParameter_path(String parameter_path) {
		this.parameter_path = parameter_path;
	}

	public MTrainInit(Parameter parameter) {
		super();
		this.parameter = parameter;
	}
	
	/**
	 * Make.
	 * 
	 * @param featureSet the feature set
	 * @param clusterSet the cluster set
	 * @param gmmList the gmm list
	 * @param parameter the parameter
	 * @throws Exception the exception
	 */
	private void make(AudioFeatureSet featureSet, ClusterSet clusterSet, GMMArrayList gmmList, Parameter parameter) throws Exception {

		GMMArrayList ubmGmmList = new GMMArrayList();
		if (parameter.getParameterInitializationEM().getModelInitMethod().equals(ModelInitializeMethod.TRAININIT_COPY)) {
			ubmGmmList = MainTools.readGMMContainer(parameter);
			if (ubmGmmList.size() > 1) {
				throw new DiarizationException("error \t UBM input model is not unique ");
			}
		}
		int nbGmm = 0;
		for (String name : clusterSet) {
			Cluster cluster = clusterSet.getCluster(name);
			if (!parameter.getParameterInitializationEM().getModelInitMethod().equals(ModelInitializeMethod.TRAININIT_COPY)) {
				gmmList.add(GMMFactory.initializeGMM(name, cluster, featureSet, parameter.getParameterModel().getModelKind(), parameter.getParameterModel().getNumberOfComponents(), parameter.getParameterInitializationEM().getModelInitMethod(), parameter.getParameterEM(), parameter.getParameterVarianceControl(), parameter.getParameterInputFeature().useSpeechDetection()));
			} else {
				gmmList.add(ubmGmmList.get(0).clone());
				gmmList.get(nbGmm).setName(name);
			}
			nbGmm++;
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
			
			if (parameter.show.isEmpty() == false) {
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				GMMArrayList gmmList = new GMMArrayList(clusterSet.clusterGetSize());
				make(featureSet, clusterSet, gmmList, parameter);
				MainTools.writeGMMContainer(parameter, gmmList);
			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		}
	}

	@Override
	public String toString() {
		return "MTrainInit [parameter=" + parameter + ", parameter_path="
				+ parameter_path + "]";
	}
	
	/**
	 * Return the parameter file
	 * @return parameter
	 * */
	public Parameter getParameter() {
		return parameter;
	}
	
	/**
	 * Sets the parameter file
	 * @param parameter
	 * */
	public void setParameter(Parameter parameter) {
		this.parameter = parameter;
	}

}