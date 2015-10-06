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
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.Map.Entry;
import java.util.logging.Level;
import java.util.logging.Logger;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.Cluster;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libClusteringData.Segment;
import fr.lium.spkDiarization.libDecoder.FastDecoderWithDuration;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.libModel.gaussian.GMMArrayList;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.parameter.ParameterDecoder;
import fr.lium.spkDiarization.parameter.ParameterSegmentationFile.SegmentationFormat;
import fr.lium.spkDiarization.programs.MClust;
import fr.lium.spkDiarization.programs.MDecode;

/**
This class perform the decoding operation by Viterbi program.
* This class derived from the {@link MDecode} of Lium spkrdiarization framework.
*/
public class AMDecode extends fr.lium.spkDiarization.programs.MDecode{
	private Parameter parameter =null;
	private String parameter_path=null;
	private PropertiesReader propertiesReader=null;
	
	
	public PropertiesReader getPropertiesReader() {
		return propertiesReader;
	}

	public void setPropertiesReader(PropertiesReader propertiesReader) {
		this.propertiesReader = propertiesReader;
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

			
	public AMDecode(){};		
	/** The Constant logger. */
	private final static Logger logger = Logger.getLogger(AMDecode.class.getName());

	/**
	 * Make.
	 * 
	 * @param featureSet the feature set
	 * @param clusterSet the cluster set
	 * @param gmmList the gmm list
	 * @param parameter the parameter
	 * @return the cluster set
	 * @throws Exception the exception
	 */
	public static ClusterSet make(AudioFeatureSet featureSet, ClusterSet clusterSet, GMMArrayList gmmList, Parameter parameter) throws Exception {
		String message = "Number of GMM=" + gmmList.size();
		FastDecoderWithDuration decoder = null;
		if (parameter.getParameterTopGaussian().getScoreNTop() > 0) {
			message += " (use top)";
			decoder = new FastDecoderWithDuration(parameter.getParameterTopGaussian().getScoreNTop(), gmmList.get(0), parameter.getParameterDecoder().isComputeLLhR(), parameter.getParameterDecoder().getShift());
		} else {
			decoder = new FastDecoderWithDuration(parameter.getParameterDecoder().getShift());
		}
		
		decoder.setupHMM(gmmList, parameter);
		ClusterSet clusterSetToDecode = new ClusterSet();
		Cluster clusterToDecode = clusterSetToDecode.getOrCreateANewCluster("Init");
		TreeSet<Segment> segmentListToDecode = clusterSet.getSegments();

		for (Segment segment : segmentListToDecode) {
			clusterToDecode.addSegment(segment);
		}
		LinkedList<Integer> list = clusterSetToDecode.collapse(0);
		segmentListToDecode = clusterSetToDecode.getSegments();
		for (Segment segment : segmentListToDecode) {
			if (parameter.getParameterDecoder().getViterbiDurationConstraints().get(0) == ParameterDecoder.ViterbiDurationConstraint.VITERBI_JUMP_DURATION) {
				decoder.accumulate(featureSet, segment, list);
			} else {
				decoder.accumulate(featureSet, segment);
			}
		}

		ClusterSet res = decoder.getClusterSet();
		res.collapse();
		return res;
	}

	/**
	 * The main method.
	 * 
	 * @param args the arguments
	 * @throws Exception the exception  if (parameter==null){ parameter = MainTools.getParameters(args);};
	 */
	public static void main(String[] args) throws Exception {
		try {
			//System.out.println(args[1]);
			SpkDiarizationLogger.setup();
			Parameter parameter = MainTools.getParameters(args);
			//info(parameter, "AMDecode");
			System.out.println("parameter.show= "+parameter.show.toString());
			if (parameter.show.isEmpty() == false) {
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				GMMArrayList gmmList = MainTools.readGMMContainer(parameter);
				ClusterSet clusterSetResult = make(featureSet, clusterSet, gmmList, parameter);
				MainTools.writeClusterSet(parameter, clusterSetResult, false);
			}
		} catch (DiarizationException e) {
			logger.log(Level.SEVERE, "", e);
			e.printStackTrace();
		}
	}

	public ClusterSet run()  throws Exception{
		try {
			SpkDiarizationLogger.setup();
			if (parameter.show.isEmpty() == false) {
				System.out.println("inizio a clusterizzare");
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				GMMArrayList gmmList = MainTools.readGMMContainer(parameter);
				ClusterSet clusterSetResult = make(featureSet, clusterSet, gmmList, parameter);
				

				
				MainTools.writeClusterSet(parameter, clusterSetResult, false);
				return clusterSetResult;
			}
			
		} catch (DiarizationException e) {
			logger.log(Level.SEVERE, "", e);
			e.printStackTrace();
		}  
		return null;
	}

	
	/**
	 * Initialize the decoder.
	 * 
	 * @param parameter the parameter
	 * @param progam the progam
	 * @throws IllegalArgumentException the illegal argument exception
	 * @throws IllegalAccessException the illegal access exception
	 * @throws InvocationTargetException the invocation target exception
	 * --fInputDesc=audio2sphinx,1:3:2:0:0:0,13,0:0:0 --fInputMask=test_file/2sec.wav --sInputMask=./2sec/2sec.i.seg --sOutputMask=./2sec/2sec.pms.seg --dPenality=10,10,50 --tInputMask=./sms.gmms
	 * 
	 */



	public Parameter getParameter() {
		return parameter;
	}

	public void setParameter(Parameter parameter) {
		this.parameter = parameter;
	}

}
