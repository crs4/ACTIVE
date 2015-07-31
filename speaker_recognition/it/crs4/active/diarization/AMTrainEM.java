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
package it.crs4.active.diarization;

import it.crs4.util.PropertiesReader;

import java.util.logging.Level;
import java.util.logging.Logger;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.libModel.gaussian.GMMArrayList;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.programs.MSegInit;
import fr.lium.spkDiarization.programs.MTrainEM;
/**
 * This class derived from the {@link MTrainEM} of Lium spkrdiarization framework.
 */
public class AMTrainEM extends MTrainEM {
	private Parameter parameter =null;
	private String parameter_path=null;
	private PropertiesReader propertiesReader=null;
	
	/**
	 * Return the properties file
	 * @return propertiesReader: a PropertiesReader object  
	 * */	
	public PropertiesReader getPropertiesReader() {
		return propertiesReader;
	}
	
	/**
	 * Sets the propertiesreader object
	 * @param propertiesReader
	 * */
	public void setPropertiesReader(PropertiesReader propertiesReader) {
		this.propertiesReader = propertiesReader;
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
	
	/**
	 * Return the path of parameter file
	 * @return parameter_path
	 * */
	public String getParameter_path() {
		return parameter_path;
	}
	
	/**
	 * Sets the path of properties file
	 * @param parameter_path
	 * */
	public void setParameter_path(String parameter_path) {
		this.parameter_path = parameter_path;
		this.propertiesReader=new PropertiesReader(parameter_path);
	}

	public void run() throws Exception {
		try {
			SpkDiarizationLogger.setup();
			if (parameter.show.isEmpty() == false) {
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				GMMArrayList initializationGmmList = MainTools.readGMMContainer(parameter);
				GMMArrayList gmmList = new GMMArrayList(clusterSet.clusterGetSize());
				make(featureSet, clusterSet, initializationGmmList, gmmList, parameter);
				MainTools.writeGMMContainer(parameter, gmmList);
			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		}
	}
	
}
