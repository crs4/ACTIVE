/**
 * 
 * <p>
 * MTrainInit
 * </p>
 * 
 * @author <a href="mailto:sylvain.meignier@lium.univ-lemans.fr">Sylvain Meignier</a>
 * @author <a href="mailto:gael.salaun@univ-lemans.fr">Gael Salaun</a>
 * @version v2.0
 * 
 *          Copyright (c) 2007-2009 Universite du Maine. All Rights Reserved. Use is subject to license terms.
 * 
 *          THIS SOFTWARE IS PROVIDED BY THE "UNIVERSITE DU MAINE" AND CONTRIBUTORS ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 *          DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
 *          USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 *          ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 *          Program for the initialization of the GMMs
 * 
 */

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