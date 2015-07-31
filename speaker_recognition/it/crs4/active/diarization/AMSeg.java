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

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;

import fr.lium.experimental.spkDiarization.programs.SegmentationMeeting;
import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.Cluster;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libClusteringData.Segment;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.libModel.Distance;
import fr.lium.spkDiarization.libModel.gaussian.DiagGaussian;
import fr.lium.spkDiarization.libModel.gaussian.FullGaussian;
import fr.lium.spkDiarization.libModel.gaussian.GMMFactory;
import fr.lium.spkDiarization.libModel.gaussian.Gaussian;
import fr.lium.spkDiarization.libSegmentationMethod.BorderSet;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.parameter.ParameterSegmentation;
import fr.lium.spkDiarization.programs.MScore;
import fr.lium.spkDiarization.programs.MSeg;
/**
 * This class perform the segmentation operation
 * * This class derived from the {@link MSeg} of Lium spkrdiarization framework.
  */
public class AMSeg extends fr.lium.spkDiarization.programs.MSeg {

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
	 * Sets the PropertiesReader object
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
	
	
	
	/**
	 * Check max.
	 * 
	 * @param segment the segment
	 * @param max the max
	 * @param parameter the parameter
	 * @param featureSet the feature set
	 * @return true, if successful
	 * @throws DiarizationException the diarization exception
	 */
	public static boolean checkMax(Segment segment, int max, Parameter parameter, AudioFeatureSet featureSet) throws DiarizationException {
		int length = segment.getLength();
		int start = segment.getStart();
		int end = start + length;
		Gaussian g1;
		if (parameter.getParameterModel().getModelKind() == Gaussian.FULL) {
			g1 = new FullGaussian(featureSet.getFeatureSize());
		} else {
			g1 = new DiagGaussian(featureSet.getFeatureSize());
		}
		Segment leftSegment = (segment.clone());
		int leftResult = -1;
		leftSegment.setLength(max - start);
		leftResult = GMMFactory.initializeGaussian(featureSet, g1, leftSegment.getStart(), leftSegment.getLength());

		Segment rightSegment = (segment.clone());
		int rightResult = -1;
		rightSegment.setStart(max);
		rightSegment.setLength(end - max);
		g1.statistic_reset();
		rightResult = GMMFactory.initializeGaussian(featureSet, g1, rightSegment.getStart(), rightSegment.getLength());
		if ((rightResult >= 0) && (leftResult >= 0)) {
			return true;
		}
		return false;
	}

	/**
	 * select the true border from the array of similarities.
	 * 
	 * @param measures the measures
	 * @param parameter the parameter
	 * @return the borders
	 */
	public static BorderSet doBorders(double[] measures, Parameter parameter) {
		int size = measures.length;
		BorderSet borders = new BorderSet();
		borders.put(0, 0.0);
		int j = 0;
		borders.put(measures.length - 1, 0.0);
		double thr = parameter.getParameterSegmentation().getThreshold();
		if (parameter.getParameterSegmentation().getMethod() == ParameterSegmentation.SegmentationMethod.SEG_BIC) {
			thr = 0;
		}

		int i = parameter.getParameterSegmentation().getMinimimWindowSize() - 1;

		while (i < size) {
			double curr = measures[i];
			int start = Math.max(0, i - parameter.getParameterSegmentation().getMinimimWindowSize());
			int end = Math.min(size, i + parameter.getParameterSegmentation().getMinimimWindowSize());
			double max = measures[start];
			for (int m = start + 1; m < end; m++) {
				double v = measures[m];
				if ((i != m) && (v > max)) {
					max = v;
				}
			}
			if ((curr > max) && (curr > thr)) {
				//logger.finest(" nb=" + j + " i=" + i + " " + curr);

				borders.put(i, curr);
				i += parameter.getParameterSegmentation().getMinimimWindowSize();
				j++;
			} else {
				i++;
			}
		}
		return borders;
	}

	/**
	 * add Borders to Clusters.
	 * 
	 * @param idx the idx
	 * @param borderSet the border set
	 * @param inputSegment the input segment
	 * @param clusterSet the cluster set
	 * @param parameter the parameter
	 * @return the int
	 */
	public static int doClusters(int idx, BorderSet borderSet, Segment inputSegment, ClusterSet clusterSet, Parameter parameter) {
		Iterator<Integer> it = borderSet.getSortedKeys();
		//logger.finer("maxIdxName=" + idx);

		String show = inputSegment.getShowName();
		int start = inputSegment.getStart();
		int previousBorder = 0;
		float rate = parameter.getParameterSegmentationInputFile().getRate();
		it.next();
		while (it.hasNext()) {
			int currentBorder = it.next();
			StringBuffer name = new StringBuffer();
			name.append("S" + idx);
			Cluster cluster = clusterSet.createANewCluster(name.toString());
			idx++;
			int segmentStart = start + previousBorder;
			int segmentLength = currentBorder - previousBorder;
			Segment segment = new Segment(show, segmentStart, segmentLength, cluster, rate);
			cluster.addSegment(segment);
			//logger.finer("name=" + name.toString() + " start=" + segmentStart + " len=" + segmentLength);

			previousBorder = currentBorder;
		}
		return idx;
	}

	/**
	 * Compute all the similarity.
	 * 
	 * @param featureSet the feature set
	 * @param segment the segment
	 * @param parameter the parameter
	 * @return a array of similarity
	 * @throws DiarizationException the diarization exception
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	public static double[] doMeasures(AudioFeatureSet featureSet, Segment segment, Parameter parameter) throws DiarizationException, IOException {
		featureSet.setCurrentShow(segment.getShowName());
		int start = segment.getStart();
		int nbOfFeatures = Math.min(segment.getLength(), featureSet.getNumberOfFeatures());

		double[] measures = new double[nbOfFeatures];
		int idxMeasures = 0;
		//logger.finer("start=" + start + " len=" + nbOfFeatures);

		if (nbOfFeatures < (2 * parameter.getParameterSegmentation().getModelWindowSize())) {
			for (long i = 0; i < nbOfFeatures; i++) {
				measures[idxMeasures++] = Double.MIN_VALUE;
			}
		} else {
			int dim = featureSet.getFeatureSize();
			Gaussian leftGaussian;
			Gaussian rightGaussian;
			if (parameter.getParameterModel().getModelKind() == Gaussian.FULL) {
				leftGaussian = new FullGaussian(dim);
				rightGaussian = new FullGaussian(dim);
			} else {
				leftGaussian = new DiagGaussian(dim);
				rightGaussian = new DiagGaussian(dim);
			}
			GMMFactory.initializeGaussian(featureSet, leftGaussian, start + 0, parameter.getParameterSegmentation().getModelWindowSize());
			GMMFactory.initializeGaussian(featureSet, rightGaussian, start
					+ parameter.getParameterSegmentation().getModelWindowSize(), parameter.getParameterSegmentation().getModelWindowSize());
			// start
			double cst = Distance.BICGaussianConstant(parameter.getParameterModel().getModelKind(), dim, parameter.getParameterSegmentation().getThreshold());
			double score = AMSeg.getSimilarity(leftGaussian, rightGaussian, parameter, cst);
			for (int i = 0; i < parameter.getParameterSegmentation().getModelWindowSize(); i++) {
				measures[idxMeasures++] = score;
			}
			// compute borders
			for (int i = parameter.getParameterSegmentation().getModelWindowSize(); i < (nbOfFeatures - parameter.getParameterSegmentation().getModelWindowSize()); i++) {
				leftGaussian.statistic_removeFeature(featureSet, (start + i)
						- parameter.getParameterSegmentation().getModelWindowSize());
				leftGaussian.statistic_addFeature(featureSet, start + i);
				rightGaussian.statistic_removeFeature(featureSet, start + i);
				rightGaussian.statistic_addFeature(featureSet, start + i
						+ parameter.getParameterSegmentation().getModelWindowSize());

				leftGaussian.setModel();
				rightGaussian.setModel();
				score = AMSeg.getSimilarity(leftGaussian, rightGaussian, parameter, cst);
				//logger.finer("idx=" + i + " score=" + score);

				measures[idxMeasures++] = score;
			}
			// end
			for (int i = nbOfFeatures - parameter.getParameterSegmentation().getModelWindowSize(); i < nbOfFeatures; i++) {
				measures[idxMeasures++] = score;
			}
		}
		return measures;
	}

	/**
	 * Do split.
	 * 
	 * @param measureVector the measure vector
	 * @param segment the segment
	 * @param startMeasures the start measures
	 * @param minLength the min length
	 * @param segmentList the segment list
	 */
	public static void doSplit(double[] measureVector, Segment segment, int startMeasures, int minLength, ArrayList<Segment> segmentList) {
		int length = segment.getLength();
		if (length > (minLength + minLength + 1)) {
			int start = segment.getStart();
			int end = start + length;
			int max = -1;
			double maxValue = Double.MIN_VALUE;

			for (int i = start + minLength; i < (end - minLength); i++) {
				double value = measureVector[i];
				if (value > maxValue) {
					maxValue = value;
					max = i;
				}
			}
			//logger.finer("split max=" + max + " start=" + start + " lenght=" + length);

			Segment leftSegment = (segment.clone());
			leftSegment.setLength(max - start);

			//logger.finer("left =" + leftSegment.getStart() + " len=" + leftSegment.getLength());

			doSplit(measureVector, leftSegment, startMeasures, minLength, segmentList);

			Segment rightSegment = (segment.clone());
			rightSegment.setStart(max);
			rightSegment.setLength(end - max);
			//logger.finer("right =" + rightSegment.getStart() + " len=" + rightSegment.getLength());
			doSplit(measureVector, rightSegment, startMeasures, minLength, segmentList);
		} else {
			//logger.finer(" add =" + segment.getStart() + " len=" + segment.getLength());

			segmentList.add(segment);
		}
	}

	/**
	 * Do split2.
	 * 
	 * @param measureVector the measure vector
	 * @param segment the segment
	 * @param startMeasures the start measures
	 * @param minLength the min length
	 * @param segmentList the segment list
	 * @param parameter the parameter
	 * @param featureSet the feature set
	 * @return true, if successful
	 * @throws DiarizationException the diarization exception
	 */
	public static boolean doSplit2(double[] measureVector, Segment segment, int startMeasures, int minLength, ArrayList<Segment> segmentList, Parameter parameter, AudioFeatureSet featureSet) throws DiarizationException {
		int length = segment.getLength();
		int start = segment.getStart();
		int end = start + length;
		int max = -1;
		double maxValue = Double.MIN_VALUE;

		for (int i = start + minLength; i < (end - minLength); i++) {
			double value = measureVector[i];
			if (value > maxValue) {
				if (checkMax(segment, i, parameter, featureSet)) {
					maxValue = value;
					max = i;
				//} else {
				//	logger.finer("max=" + i + " reject");
				}
			}
		}
		if (max == -1) {
			return false;
		}
		//logger.finer("split max=" + max + " start=" + start + " lenght=" + length);

		Segment leftSegment = (segment.clone());
		leftSegment.setLength(max - start);
		//logger.finer("left =" + leftSegment.getStart() + " len=" + leftSegment.getLength());
		if (doSplit2(measureVector, leftSegment, startMeasures, minLength, segmentList, parameter, featureSet) == false) {
			segmentList.add(leftSegment);
		}

		Segment rightSegment = (segment.clone());
		rightSegment.setStart(max);
		rightSegment.setLength(end - max);
		//logger.finer("right =" + rightSegment.getStart() + " len=" + rightSegment.getLength());
		if (doSplit2(measureVector, rightSegment, startMeasures, minLength, segmentList, parameter, featureSet) == false) {
			segmentList.add(rightSegment);
		}

		return true;
	}

	/**
	 * select and compute the similarity method.
	 * 
	 * @param leftGaussian the first Gaussien
	 * @param rightGaussian the second Gaussien
	 * @param parameter the parameter structure
	 * @param BICCst the constant need in BIC similarity
	 * @return the similarity
	 * @throws DiarizationException the diarization exception
	 */
	public static double getSimilarity(Gaussian leftGaussian, Gaussian rightGaussian, Parameter parameter, double BICCst) throws DiarizationException {
		if (parameter.getParameterSegmentation().getMethod().equals(ParameterSegmentation.SegmentationMethod.SEG_GLR)) {
			return Distance.GLR(leftGaussian, rightGaussian);
		} else {
			if (parameter.getParameterSegmentation().getMethod().equals(ParameterSegmentation.SegmentationMethod.SEG_BIC)) {
				int len = leftGaussian.getCount() + rightGaussian.getCount();
				// double cst = Distance.BICConstant(param.kind, dim,
				// param.segThr);
				return Distance.BIC(leftGaussian, rightGaussian, BICCst, len);
			} else {
				if (parameter.getParameterSegmentation().getMethod().equals(ParameterSegmentation.SegmentationMethod.SEG_KL2)) {
					return Distance.KL2(leftGaussian, rightGaussian);
				} else {
					if (parameter.getParameterSegmentation().getMethod().equals(ParameterSegmentation.SegmentationMethod.SEG_GD)) {
						return Distance.GD(leftGaussian, rightGaussian);
					} else {
						if (parameter.getParameterSegmentation().getMethod().equals(ParameterSegmentation.SegmentationMethod.SEG_H2)) {
							return Distance.H2(leftGaussian, rightGaussian);
						} else {
							throw new DiarizationException("mSeg unknown similarity "
									+ parameter.getParameterSegmentation().getMethod());
						}
					}
				}
			}
		}
	}

	/**
	 * Resegment.
	 * 
	 * @param featureSet the feature set
	 * @param borderSet the border set
	 * @param parameter the parameter
	 * @return the border set
	 * @throws DiarizationException the diarization exception
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	static public BorderSet resegment(AudioFeatureSet featureSet, BorderSet borderSet, Parameter parameter) throws DiarizationException, IOException {
		BorderSet result = new BorderSet();
		Cluster empty = new Cluster("empty");
		float rate = parameter.getParameterSegmentationInputFile().getRate();
		ArrayList<Integer> borderList = new ArrayList<Integer>();
		Iterator<Integer> iterator = borderSet.getSortedKeys();
		while (iterator.hasNext()) {
			borderList.add(iterator.next());
		}
		int i = 0;
		int left = 0;
		int middle = 0;
		int right = borderList.get(i);
		i++;
		while (i < borderList.size()) {
			left = middle;
			middle = right;
			right = borderList.get(i);
			Segment segment = new Segment(featureSet.getCurrentShowName(), left, (right - left) + 1, empty, rate);
			double[] measures = doMeasures(featureSet, segment, parameter);
			double max = -Double.MAX_VALUE;
			int index = 0;
			for (int j = 0; j < measures.length; j++) {
				if (measures[j] > max) {
					max = measures[j];
					index = j;
				}
			}
			index += left;
			//logger.info("left=" + left + " middle=" + middle + "/" + index + " right=" + right);
			borderList.set(i - 1, index);
			i++;
		}

		// borderList.add(featureSet.getNumberOfFeatures());
		for (i = 0; i < borderList.size(); i++) {
			result.put(borderList.get(i), 0.0);
		}

		return result;
	}

	/**
	 * Valide.
	 * 
	 * @param featureSet the feature set
	 * @param clusterSet the cluster set
	 * @param parameter the parameter
	 * @return the cluster set
	 * @throws DiarizationException the diarization exception
	 */
	static public ClusterSet valide(AudioFeatureSet featureSet, ClusterSet clusterSet, Parameter parameter) throws DiarizationException {
		ClusterSet result = new ClusterSet();

		Iterator<Segment> itSegment = clusterSet.getSegments().iterator();
		Segment previous = itSegment.next();
		Segment current = itSegment.next();

		Gaussian gPrevious, gCurrent, gNext = null;
		int dim = featureSet.getFeatureSize();
		if (parameter.getParameterModel().getModelKind() == Gaussian.FULL) {
			gPrevious = new FullGaussian(dim);
			gCurrent = new FullGaussian(dim);
		} else {
			gPrevious = new DiagGaussian(dim);
			gCurrent = new DiagGaussian(dim);
		}
		GMMFactory.initializeGaussian(featureSet, gPrevious, previous.getStart(), previous.getLength());
		GMMFactory.initializeGaussian(featureSet, gCurrent, current.getStart(), current.getLength());
		double cst = Distance.BICGaussianConstant(parameter.getParameterModel().getModelKind(), dim, 1);

		while (itSegment.hasNext()) {
			Segment next = itSegment.next();

			if (parameter.getParameterModel().getModelKind() == Gaussian.FULL) {
				gNext = new FullGaussian(dim);
			} else {
				gNext = new DiagGaussian(dim);
			}
			GMMFactory.initializeGaussian(featureSet, gNext, next.getStart(), next.getLength());

			double dpc = Distance.BICLocal(gPrevious, gCurrent, cst);
			double dcn = Distance.BICLocal(gCurrent, gNext, cst);
			double dpn = Distance.BICLocal(gPrevious, gNext, cst);

			current.setInformation("Prev/Cur", dpc);
			current.setInformation("Cur/Next", dcn);
			current.setInformation("Prev/Next", dpn);

			if ((dpn > 0) && (dpc < 0) && (dcn < 0)) {
				//logger.finer("sup distance: Prev/Cur=" + dpc + " Cur/Next=" + dcn + " Prev/Next=" + dpn + " prev="
				//		+ previous.getStart() + " cur=" + current.getStart() + " next=" + next.getStart());
				current.setInformation("sup", "0");
			}

			// move
			previous = current;
			gPrevious = gCurrent;
			current = next;
			gCurrent = gNext;
		}

		return result;
	}

	/**
	 * Make.
	 * 
	 * @param featureSet the feature set
	 * @param clusterSet the cluster set
	 * @param clusterSetResult the cluster set result
	 * @param parameter the parameter
	 * @throws Exception the exception
	 */
	public static void make(AudioFeatureSet featureSet, ClusterSet clusterSet, ClusterSet clusterSetResult, Parameter parameter) throws Exception {
		if (parameter.getParameterSegmentation().isRecursion()) {
			ArrayList<Segment> segmentList = new ArrayList<Segment>();
			for (Cluster cluster : clusterSet.clusterSetValue()) {
				for (Segment segment : cluster) {
					double[] m = AMSeg.doMeasures(featureSet, segment, parameter);
					// doSplit(m, seg, seg.getStartFrameIndex(),
					// param.segMinWSize, arraySegment);
					if (doSplit2(m, segment, segment.getStart(), parameter.getParameterSegmentation().getMinimimWindowSize(), segmentList, parameter, featureSet) == false) {
						segmentList.add(segment);
					}
				}
			}
			for (int i = 0; i < segmentList.size(); i++) {
				String name = new String("S" + Integer.toString(i));
				Cluster cluster = clusterSetResult.createANewCluster(name);
				cluster.addSegment(segmentList.get(i));
			}
		} else {
			if (parameter.getParameterSegmentation().getMethod() == ParameterSegmentation.SegmentationMethod.SEG_GLR_IT) {
				SegmentationMeeting.make(clusterSet, clusterSetResult, featureSet, parameter);
			} else {
				int idx = 0;
				for (Cluster cluster : clusterSet.clusterSetValue()) {
					for (Segment segment : cluster) {
						double[] measureVector = doMeasures(featureSet, segment, parameter);
						BorderSet borderSet = doBorders(measureVector, parameter);
						idx = doClusters(idx, borderSet, segment, clusterSetResult, parameter);
					}
				}
			}
		}
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
				clusterSet.collapse();
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				ClusterSet clusterSetResult = new ClusterSet();
				make(featureSet, clusterSet, clusterSetResult, parameter);
				MainTools.writeClusterSet(parameter, clusterSetResult, false);
			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		}

	}
	public  void run() throws Exception {

		try {
			SpkDiarizationLogger.setup();
			if (parameter.show.isEmpty() == false) {
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);
				clusterSet.collapse();
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				ClusterSet clusterSetResult = new ClusterSet();
				make(featureSet, clusterSet, clusterSetResult, parameter);
				MainTools.writeClusterSet(parameter, clusterSetResult, false);
			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		}

	}


}