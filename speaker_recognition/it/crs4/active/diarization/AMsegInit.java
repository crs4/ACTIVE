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

import java.lang.reflect.InvocationTargetException;
import java.util.logging.Level;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.Cluster;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libClusteringData.Segment;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.programs.MSeg;
import fr.lium.spkDiarization.programs.MSegInit;
/**
 * This class derived from the {@link MSegInit} of Lium spkrdiarization framework.
 */
public class AMsegInit extends MSegInit {
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

	public static void main(String[] args) throws Exception {
		try {
			SpkDiarizationLogger.setup();
			Parameter parameter = MainTools.getParameters(args);
			//info(parameter, "MSegInit");
			System.out.println(parameter.show.toString());
			if (parameter.show.isEmpty() == false) {
				ClusterSet clusterSet = null;
				Segment segment = null;
				if (parameter.getParameterSegmentationInputFile().getMask().equals("")) {
					clusterSet = new ClusterSet();
					Cluster cluster = clusterSet.createANewCluster("init");
					segment = new Segment(parameter.show, 0, 0, cluster, parameter.getParameterSegmentationInputFile().getRate());
					cluster.addSegment(segment);

				} else {
					// clusters
					clusterSet = MainTools.readClusterSet(parameter);
				}

				// Features
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				if (parameter.getParameterSegmentationInputFile().getMask().equals("")) {
					featureSet.setCurrentShow(segment.getShowName());
					segment.setLength(featureSet.getNumberOfFeatures());
				}

				ClusterSet clusterSetResult = new ClusterSet();

				make(featureSet, clusterSet, clusterSetResult, parameter);

				MainTools.writeClusterSet(parameter, clusterSetResult, true);
			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		}
	}
	
	public  void run( ) throws Exception {
		try {
			SpkDiarizationLogger.setup();
			//Parameter parameter = MainTools.getParameters(args);
			//info(parameter, "MSegInit");
			System.out.println(parameter.show.toString());
			if (parameter.show.isEmpty() == false) {
				ClusterSet clusterSet = null;
				Segment segment = null;
				if (parameter.getParameterSegmentationInputFile().getMask().equals("")) {
					clusterSet = new ClusterSet();
					Cluster cluster = clusterSet.createANewCluster("init");
					segment = new Segment(parameter.show, 0, 0, cluster, parameter.getParameterSegmentationInputFile().getRate());
					cluster.addSegment(segment);

				} else {
					// clusters
					clusterSet = MainTools.readClusterSet(parameter);
				}

				// Features
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				if (parameter.getParameterSegmentationInputFile().getMask().equals("")) {
					featureSet.setCurrentShow(segment.getShowName());
					segment.setLength(featureSet.getNumberOfFeatures());
				}

				ClusterSet clusterSetResult = new ClusterSet();

				make(featureSet, clusterSet, clusterSetResult, parameter);

				MainTools.writeClusterSet(parameter, clusterSetResult, true);
			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		}
	}	
	
	/**
	 * Returns info.
	 * 
	 * @param parameter the parameter
	 * @param program the program
	 * @throws IllegalArgumentException the illegal argument exception
	 * @throws IllegalAccessException the illegal access exception
	 * @throws InvocationTargetException the invocation target exception
	 */
	public static void info(Parameter parameter, String program) throws IllegalArgumentException, IllegalAccessException, InvocationTargetException {
		if (parameter.help) {
			parameter.logShow();
			parameter.getParameterInputFeature().logAll(); 
			parameter.getParameterSegmentationInputFile().logAll();  
			parameter.getParameterSegmentationOutputFile().logAll();  
		}
	}

}
