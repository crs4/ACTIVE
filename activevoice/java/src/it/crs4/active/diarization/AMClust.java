/**
 * 
 * <p>
 * MClust
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
 *          Hierarchical and linear clustering program based on CLR and BIC distances
 * 
 */

package it.crs4.active.diarization;

import it.crs4.util.PropertiesReader;

import java.io.IOException;

import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.parameter.ParameterClustering.*;
import fr.lium.spkDiarization.programs.MDecode;
import fr.lium.spkDiarization.programs.ivector.TrainIVectorOrTV;

import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.TreeSet;
import java.util.logging.Level;
import java.util.logging.Logger;

import fr.lium.spkDiarization.lib.*;
import fr.lium.spkDiarization.libClusteringData.*;
import fr.lium.spkDiarization.libClusteringMethod.*;
import fr.lium.spkDiarization.libDecoder.*;
import fr.lium.spkDiarization.libFeature.*;
import fr.lium.spkDiarization.libMatrix.*;
import fr.lium.spkDiarization.libModel.Distance;
import fr.lium.spkDiarization.libModel.gaussian.*;
import fr.lium.spkDiarization.libModel.ivector.*;
import fr.lium.spkDiarization.parameter.*;

import org.xml.sax.*;
import javax.xml.parsers.*;
import javax.xml.transform.*;
/**
 * The Class MClust.
 */
public class AMClust {

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

	/**
	 * save a step of the hierarchical clustering algorithm, clustering is duplicated form prevSuffix to suffix.
	 * 
	 * @param clustering the class of the hierarchical clustering
	 * @param previousSuffix save starting
	 * @param suffix save ending
	 * @param parameter root parameter class
	 * 
	 * @throws IOException Signals that an I/O exception has occurred.
	 * @throws ParserConfigurationException the parser configuration exception
	 * @throws SAXException the SAX exception
	 * @throws DiarizationException the diarization exception
	 * @throws TransformerException the transformer exception
	 */
	public static void saveClustering(HClustering clustering, long previousSuffix, long suffix, Parameter parameter) throws Exception {
		if (parameter.getParameterDiarization().isSaveAllStep()) {
			for (long i = previousSuffix; i < suffix; i++) {
				String segOutFilename = parameter.show + "." + String.valueOf(i);
				clustering.getClusterSet().write(segOutFilename, parameter.getParameterSegmentationOutputFile());
			}
		}
	}

	/**
	 * Save clustering.
	 * 
	 * @param clustering the clustering
	 * @param indexMerge the index merge
	 * @param parameter the parameter
	 * @throws IOException Signals that an I/O exception has occurred.
	 * @throws ParserConfigurationException the parser configuration exception
	 * @throws SAXException the sAX exception
	 * @throws DiarizationException the diarization exception
	 * @throws TransformerException the transformer exception
	 */
	public static void saveClustering(HClustering clustering, int indexMerge, Parameter parameter) throws IOException, ParserConfigurationException, SAXException, DiarizationException, TransformerException {
		String segOutFilename = parameter.show + "-" + String.format("%3d", indexMerge).replace(" ", "_");
		clustering.getClusterSet().write(segOutFilename, parameter.getParameterSegmentationOutputFile());
	}

	/**
	 * Bootum-up Hierarchical clustering based on GMMs, metric could be CE (Cross Entropy) or CLR (Cross Likelihood ratio).
	 * 
	 * @param clusterSet the cluster set
	 * @param featureSet the feature set
	 * @param parameter the parameter
	 * @param ubm the ubm
	 * @return Clusters
	 * @throws IOException Signals that an I/O exception has occurred.
	 * @throws DiarizationException the diarization exception
	 * @throws ParserConfigurationException the parser configuration exception
	 * @throws SAXException the sAX exception
	 * @throws TransformerException the transformer exception
	 */
	public static ClusterSet gmmHAC(ClusterSet clusterSet, AudioFeatureSet featureSet, Parameter parameter, GMM ubm) throws Exception {

		CLRHClustering clustering = new CLRHClustering(clusterSet, featureSet, parameter, ubm);
		int nbCluster = clusterSet.clusterGetSize();

		int nbMerge = 0;
		double clustThr = parameter.getParameterClustering().getThreshold();
		int nbMaxMerge = parameter.getParameterClustering().getMaximumOfMerge();
		int nbMinClust = parameter.getParameterClustering().getMinimumOfCluster();
		long suffix = -1000;
		int mult = 100;
		clustering.initialize(0, 0); // Ci = 0; Cj = 0;
		logScore(clustering, parameter);
		saveClustering(clustering, suffix, suffix + 1, parameter);
		long previousSuffix = suffix;
		clustering.printDistance();

		double score = clustering.getScoreOfCandidatesForMerging();
		while (continuClustering(score, nbMerge, nbCluster, clusterSet, clustThr, nbMaxMerge, nbMinClust) == true) {
			nbMerge++;
			suffix = Math.round(score * mult);
			if (suffix > previousSuffix) {
				saveClustering(clustering, previousSuffix, suffix, parameter);
				previousSuffix = suffix;
			}
			clustering.mergeCandidates();
			score = clustering.getScoreOfCandidatesForMerging();
			nbCluster = clustering.getClusterSet().clusterGetSize();
		}
		if (!parameter.getParameterModelSetOutputFile().getMask().equals(ParameterModelSetOutputFile.getDefaultMask())) {
			MainTools.writeGMMContainer(parameter, clustering.getGmmList());
		}

		suffix = Math.round(clustThr * mult);
		saveClustering(clustering, previousSuffix, suffix + 1, parameter);
		return clustering.getClusterSet();
	}

	/**
	 * Bootum-up Hierarchical clustering based on GMMs, metric could be CE (Cross Entropy) or CLR (Cross Likelihood ratio) after each merge a decoding is performed.
	 * 
	 * @param clusterSet the cluster set
	 * @param featureSet the feature set
	 * @param parameter the parameter
	 * @param ubm the ubm
	 * @return Clusters
	 * @throws Exception the exception
	 */
	public static ClusterSet cdclust(ClusterSet clusterSet, AudioFeatureSet featureSet, Parameter parameter, GMM ubm) throws Exception {

		CLRHClustering clustering = new CLRHClustering(clusterSet, featureSet, parameter, ubm);
		int nbCluster = clusterSet.clusterGetSize();

		int nbMerge = 0;
		double clustThr = parameter.getParameterClustering().getThreshold();
		int nbMaxMerge = parameter.getParameterClustering().getMaximumOfMerge();
		int nbMinClust = parameter.getParameterClustering().getMinimumOfCluster();
		long suffix = -1000;
		int mult = 100;
		clustering.initialize(0, 0); // Ci = 0; Cj = 0;
		logScore(clustering, parameter);
		saveClustering(clustering, suffix, suffix + 1, parameter);
		long previousSuffix = suffix;

		double score = clustering.getScoreOfCandidatesForMerging();
		while (continuClustering(score, nbMerge, nbCluster, clusterSet, clustThr, nbMaxMerge, nbMinClust) == true) {
			nbMerge++;
			suffix = Math.round(score * mult);
			if (suffix > previousSuffix) {
				saveClustering(clustering, previousSuffix, suffix, parameter);
				previousSuffix = suffix;
			}
			ClusterSet decodeClusterSet = MDecode.make(featureSet, clustering.getClusterSet(), clustering.getGmmList(), parameter);
			clustering = new CLRHClustering(decodeClusterSet, featureSet, parameter, ubm);
			clustering.initialize(0, 0); // Ci = 0; Cj = 0;

			clustering.mergeCandidates();

			score = clustering.getScoreOfCandidatesForMerging();
			nbCluster = clustering.getClusterSet().clusterGetSize();
		}
		if (!parameter.getParameterModelSetOutputFile().getMask().equals(ParameterModelSetOutputFile.getDefaultMask())) {
			MainTools.writeGMMContainer(parameter, clustering.getGmmList());
		}
		suffix = Math.round(clustThr * mult);
		saveClustering(clustering, previousSuffix, suffix, parameter);
		return clustering.getClusterSet();
	}

	/**
	 * BIC Hierarchical clustering.
	 * 
	 * @param clusterSet the cluster set
	 * @param featureSet the feature set
	 * @param parameter the parameter
	 * @return Clusters
	 * @throws DiarizationException the diarization exception
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	public static ClusterSet gaussianHAC(ClusterSet clusterSet, AudioFeatureSet featureSet, Parameter parameter) throws DiarizationException, IOException {
		BICHClustering clustering = new BICHClustering(clusterSet.clone(), featureSet, parameter);
		int nbMerge = 0;
		int clustMaxMerge = parameter.getParameterClustering().getMaximumOfMerge();
		int clustMinSpk = parameter.getParameterClustering().getMinimumOfCluster();
		int nbCluster = clusterSet.clusterGetSize();

		double score = 0;
		clustering.initialize(0, 0); // Ci = 0; Cj = 0;
		score = clustering.getScoreOfCandidatesForMerging();

		while (continuClustering(score, nbMerge, nbCluster, clusterSet, 0.0, clustMaxMerge, clustMinSpk) == true) {
			clustering.mergeCandidates();
			score = clustering.getScoreOfCandidatesForMerging();
			nbMerge++;
			nbCluster = clustering.getClusterSet().clusterGetSize();
		}
		if (!parameter.getParameterModelSetOutputFile().getMask().equals(ParameterModelSetOutputFile.getDefaultMask())) {
			MainTools.writeGMMContainer(parameter, clustering.getGmmList());
		}
		return clustering.getClusterSet();
	}

	/**
	 * BIC Hierarchical clustering only diagonal merge.
	 * 
	 * @param clusterSet the cluster set
	 * @param featureSet the feature set
	 * @param parameter the parameter
	 * @return Clusters
	 * @throws DiarizationException the diarization exception
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	public static ClusterSet gaussianHACDiagonal(ClusterSet clusterSet, AudioFeatureSet featureSet, Parameter parameter) throws DiarizationException, IOException {
		BICDClustering clustering = new BICDClustering(clusterSet.clone(), featureSet, parameter);
		int nbMerge = 0;
		int clustMaxMerge = parameter.getParameterClustering().getMaximumOfMerge();
		int clustMinSpk = parameter.getParameterClustering().getMinimumOfCluster();
		int nbCluster = clusterSet.clusterGetSize();

		double score = 0;
		clustering.initialize(0, 0); // Ci = 0; Cj = 0;
		score = clustering.getScoreOfCandidatesForMerging();

		while (continuClustering(score, nbMerge, nbCluster, clusterSet, 0.0, clustMaxMerge, clustMinSpk) == true) {
			clustering.mergeCandidates();
			score = clustering.getScoreOfCandidatesForMerging();
			nbMerge++;
			nbCluster = clustering.getClusterSet().clusterGetSize();
		}
		if (!parameter.getParameterModelSetOutputFile().getMask().equals(ParameterModelSetOutputFile.getDefaultMask())) {
			MainTools.writeGMMContainer(parameter, clustering.getGmmList());
		}
		return clustering.getClusterSet();
	}

	/**
	 * BIC linear left to right clustering.
	 * 
	 * @param clusterSet the cluster set
	 * @param featureSet the feature set
	 * @param parameter the parameter
	 * @return Clusters
	 * @throws DiarizationException the diarization exception
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	public static ClusterSet gaussianHACRightToLeft(ClusterSet clusterSet, AudioFeatureSet featureSet, Parameter parameter) throws DiarizationException, IOException {
		BICLClustering clustering = new BICLClustering(clusterSet.clone(), featureSet, parameter);
		double score = 0;
		clustering.initialize(0, 1); // Ci = 0; Cj = 1;
		score = clustering.getScoreOfCandidatesForMerging();
		while (score < Double.MAX_VALUE) {
			String message = "score = " + score + " ci = " + clustering.getIndexOfFirstCandidate() + "("
					+ clustering.getFirstCandidate().getName() + ")" + " cj = "
					+ clustering.getIndexOfSecondCandidate() + "(" + clustering.getSecondCandidate().getName() + ")";
			if (score < 0.0) {
				clustering.mergeCandidates();
			} else {
				clustering.incrementIndexOfFirstCandidate();
				clustering.incrementIndexOfSecondCandidate();
			}
			score = clustering.getScoreOfCandidatesForMerging();
		}
		if (!parameter.getParameterModelSetOutputFile().getMask().equals(ParameterModelSetOutputFile.getDefaultMask())) {
			MainTools.writeGMMContainer(parameter, clustering.getGmmList());
		}
		return clustering.getClusterSet();
	}

	/**
	 * BIC linear right to left clustering.
	 * 
	 * @param clusterSet the cluster set
	 * @param featureSet the feature set
	 * @param parameter the parameter
	 * @return Clusters
	 * @throws DiarizationException the diarization exception
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	public static ClusterSet gaussianHACLeftToRight(ClusterSet clusterSet, AudioFeatureSet featureSet, Parameter parameter) throws DiarizationException, IOException {
		BICLClustering clustering = new BICLClustering(clusterSet.clone(), featureSet, parameter);
		double score = 0;
		int lastIndex = clustering.getIndexOfLastCandidate();
		clustering.initialize(lastIndex - 1, lastIndex);
		score = clustering.getScoreOfCandidatesForMerging();
		while (score < Double.MAX_VALUE) {
			String message = "score = " + score + " ci = " + clustering.getIndexOfFirstCandidate() + "("
					+ clustering.getFirstCandidate().getName() + ")" + " cj = "
					+ clustering.getIndexOfSecondCandidate() + "(" + clustering.getSecondCandidate().getName() + ")";
			if (score < 0.0) {
				clustering.mergeCandidates();
				message = "merge " + message;
			}
			clustering.decrementIndexOfFirstCandidate();
			clustering.decrementIndexOfSecondCandidate();
			score = clustering.getScoreOfCandidatesForMerging();
		}
		if (!parameter.getParameterModelSetOutputFile().getMask().equals(ParameterModelSetOutputFile.getDefaultMask())) {
			MainTools.writeGMMContainer(parameter, clustering.getGmmList());
		}
		return clustering.getClusterSet();
	}

	/**
	 * Make.
	 * 
	 * @param featureSet the feature set
	 * @param clusterSet the cluster set
	 * @param parameter the parameter
	 * @param ubm the ubm
	 * @return the cluster set
	 * @throws Exception the exception
	 */
	public static ClusterSet make(AudioFeatureSet featureSet, ClusterSet clusterSet, Parameter parameter, GMM ubm) throws Exception {
		Date date = new Date();
		ClusterSet clusterSetResult = new ClusterSet();
		if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_BIC)) {
			clusterSetResult = AMClust.gaussianHAC(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_ES_IV)) {
			clusterSetResult = AMClust.iVectorExhaustiveSearch(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_ICR)) {
			clusterSetResult = AMClust.gaussianHAC(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_GLR)) {
			clusterSetResult = AMClust.gaussianHAC(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_GD)) {
			clusterSetResult = AMClust.gaussianHAC(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_BIC_SR)) {
			clusterSetResult = AMClust.gaussianHAC(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_L_BIC)) {
			clusterSetResult = AMClust.gaussianHACRightToLeft(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_L_BIC_SR)) {
			clusterSetResult = AMClust.gaussianHACRightToLeft(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_D_BIC)) {
			clusterSetResult = AMClust.gaussianHACDiagonal(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_R_BIC)) {
			clusterSetResult = AMClust.gaussianHACLeftToRight(clusterSet, featureSet, parameter);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_TScore)) {
			clusterSetResult = AMClust.gmmHAC(clusterSet, featureSet, parameter, ubm);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_CLR)) {
			clusterSetResult = AMClust.gmmHAC(clusterSet, featureSet, parameter, ubm);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_CE)) {
			clusterSetResult = AMClust.gmmHAC(clusterSet, featureSet, parameter, ubm);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_CE_D)) {
			clusterSetResult = AMClust.cdclust(clusterSet, featureSet, parameter, ubm);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_C_D)) {
			clusterSetResult = AMClust.cdclust(clusterSet, featureSet, parameter, ubm);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_GDGMM)) {
			clusterSetResult = AMClust.gmmHAC(clusterSet, featureSet, parameter, ubm);
		} else if (parameter.getParameterClustering().getMethod().equals(ParameterClustering.ClusteringMethod.CLUST_H_BIC_GMM_MAP)) {
			clusterSetResult = AMClust.gmmHAC(clusterSet, featureSet, parameter, ubm);
		} else {
			System.exit(-1);
		}
		return clusterSetResult;
	}

	/**
	 * I vector exhaustive search.
	 * 
	 * @param clusterSet the cluster set
	 * @param featureSet the feature set
	 * @param parameter the parameter
	 * @return the cluster set
	 * @throws DiarizationException the diarization exception
	 * @throws IOException Signals that an I/O exception has occurred.
	 * @throws SAXException the sAX exception
	 * @throws ParserConfigurationException the parser configuration exception
	 * @throws ClassNotFoundException the class not found exception
	 */
	public static ClusterSet iVectorExhaustiveSearch(ClusterSet clusterSet, AudioFeatureSet featureSet, Parameter parameter) throws DiarizationException, IOException, SAXException, ParserConfigurationException, ClassNotFoundException {
		ClusterSet clusterSetResult = new ClusterSet();
		featureSet.setCurrentShow(clusterSet.getFirstCluster().firstSegment().getShowName());
	
		Date date1 = new Date();
		IVectorArrayList iVectorList = TrainIVectorOrTV.make(clusterSet, featureSet, parameter);
		EigenFactorRadialList normalization = MainTools.readEigenFactorRadialNormalization(parameter);
		IVectorArrayList normalizedIVectorList = EigenFactorRadialNormalizationFactory.applied(iVectorList, normalization);
		MatrixSymmetric covarianceInvert = MainTools.readMahanalonisCovarianceMatrix(parameter).invert();

		Date date2 = new Date();

		MatrixSymmetric distance = new MatrixSymmetric(iVectorList.size());
		distance.fill(0.0);
		//TreeMap<Double, String> ds = new TreeMap<Double, String>();
		double min = Double.MAX_VALUE;
		double max = Double.MIN_VALUE;
		for (int i = 0; i < distance.getSize(); i++) {
			//String ch = iVectorList.get(i).getName() + " " + i + " [ ";
			for (int j = i; j < distance.getSize(); j++) {
				double d = Distance.iVectorMahalanobis(normalizedIVectorList.get(i), normalizedIVectorList.get(j), covarianceInvert);
				if (d < min) min = d;
				if (d > max) max = d;
				distance.set(i, j, d);
			}
		}
		Date date3 = new Date();

		double threshold = parameter.getParameterClustering().getThreshold();
		ConnectedGraph connectedGraph = new ConnectedGraph(distance, threshold);
		int[] subGraph = connectedGraph.getSubGraph();
		int nbSubGraph = connectedGraph.getNbSubGraph();
		ArrayList<ArrayList<Integer>> subGraphList = new ArrayList<ArrayList<Integer>>(nbSubGraph);
		for (int i = 0; i < nbSubGraph; i++) {
			subGraphList.add(new ArrayList<Integer>());
		}
		for (int j = 0; j < iVectorList.size(); j++) {
			subGraphList.get(subGraph[j]).add(j);
		}
		
		for (int i = 0; i < nbSubGraph; i++) {
			
			ArrayList<Integer> nodes = subGraphList.get(i);
			String nodesString = "";
			for (int j = 0; j < iVectorList.size(); j++) {
				if (subGraph[j] == i) {
					nodesString += " " + j;
				}
			}

			ExhaustiveClustering exhaustiveClustering = new ExhaustiveClustering(distance, threshold, nodes);
			int[] partition = exhaustiveClustering.backtrack();

			String ch = "partition :";
			for (int c : nodes) {
				if (partition[c] == c) {
					ch += " " + c;
					String clusterName = iVectorList.get(c).getName();
					Cluster cloneCluster = clusterSet.getCluster(clusterName).clone();
					clusterSetResult.addCluster(cloneCluster);
				} else {
					String centerName = iVectorList.get(partition[c]).getName();
					String clusterName = iVectorList.get(c).getName();
					Iterator<Segment> it = clusterSet.getCluster(clusterName).iterator();
					clusterSetResult.getCluster(centerName).addSegments(it);
				}
			}
		}
		Date date4 = new Date();
		long d = date2.getTime() - date1.getTime();
		 d = date3.getTime() - date2.getTime();
		 d = date4.getTime() - date3.getTime();

		return clusterSetResult;
	}

	/**
	 * The main method.
	 * 
	 * @param args the arguments
	 * @throws Exception the exception
	 */
	public static void main(String[] args) throws Exception {
		try {
			SpkDiarizationLogger.setup();
			Parameter parameter = MainTools.getParameters(args);

			if (parameter.show.isEmpty() == false) {
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				GMMArrayList GMMList = MainTools.readGMMContainer(parameter);
				GMM ubm = null;
				if (GMMList != null) {
					ubm = GMMList.get(0);
				}
				ClusterSet clustersetResult = make(featureSet, clusterSet, parameter, ubm);
				MainTools.writeClusterSet(parameter, clustersetResult, false);

			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		}
	}
	public  void run() throws Exception {
		try {
			SpkDiarizationLogger.setup();
			//Parameter parameter = MainTools.getParameters(args);
			//info(parameter, "MClust");
			if (parameter.show.isEmpty() == false) {
				// clusters
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);

				// Features
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);

				// methods
				GMMArrayList GMMList = MainTools.readGMMContainer(parameter);
				GMM ubm = null;
				if (GMMList != null) {
					ubm = GMMList.get(0);
				}
				
				ClusterSet clustersetResult = make(featureSet, clusterSet, parameter, ubm);
				

				MainTools.writeClusterSet(parameter, clustersetResult, false);

			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Log score.
	 * 
	 * @param clustering the clustering
	 * @param parameter the parameter
	 */
	public static void logScore(CLRHClustering clustering, Parameter parameter) {
		MatrixSquare distances = clustering.getDistances(); // Matrix of distances.
		GMMArrayList models = clustering.getGmmList(); // List of models
		int size = distances.getSize();
		for (int i = 0; i < size; i++) {
			String spk1 = models.get(i).getName();
			for (int j = i + 1; j < size; j++) {
				String spk2 = models.get(j).getName();
				double score = distances.get(i, j);
			}
		}

	}

	/**
	 * Continu clustering.
	 * 
	 * @param score the score
	 * @param nbMerge the nb merge
	 * @param nbCluster the nb cluster
	 * @param clusters the clusters
	 * @param clustThr the clust thr
	 * @param nbMaxMerge the nb max merge
	 * @param nbMinCluster the nb min cluster
	 * @return true, if successful
	 */
	public static boolean continuClustering(double score, int nbMerge, int nbCluster, ClusterSet clusters, double clustThr, int nbMaxMerge, int nbMinCluster) {

		if (score == Double.MAX_VALUE) {
			return false;
		}
		boolean res = ((score < clustThr) && (nbMerge < nbMaxMerge) && (nbCluster > nbMinCluster));
		return res;
	}


	 

}