/**
 * 
 * <p>
 * MDecode
 * </p>
 * 
 * @author <a href="mailto:sylvain.meignier@lium.univ-lemans.fr">Sylvain Meignier</a>
 * @author <a href="mailto:gael.salaun@univ-lemans.fr">Gael Salaun</a>
 * @author <a href="mailto:teva.merlin@lium.univ-lemans.fr">Teva Merlin</a>
 * @version v2.0
 * 
 *          Copyright (c) 2007-2009 Universite du Maine. All Rights Reserved. Use is subject to license terms.
 * 
 *          THIS SOFTWARE IS PROVIDED BY THE "UNIVERSITE DU MAINE" AND CONTRIBUTORS ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 *          DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
 *          USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 *          ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 *          Viterbi decoding program
 * 
 */

package it.crs4.active.diarization;

import it.crs4.util.PropertiesReader;

import java.lang.reflect.InvocationTargetException;
import java.util.LinkedList;
import java.util.TreeSet;
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

/**
 * The Class AMDecode.
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

	public void run()  throws Exception{
		try {
			SpkDiarizationLogger.setup();
			if (parameter.show.isEmpty() == false) {
				System.out.println("inizio a clusterizzare");
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
