package it.crs4.active.diarization;

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
import fr.lium.spkDiarization.programs.MSegInit;

public class AMsegInit extends MSegInit {
	Parameter parameter =null;
	/**
	 * @param args
	 * @throws Exception 
	 * Esempio di parametri
	 --fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav 
	 --fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0 
	 --sInputMask= 
	 --sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/%s.i.seg
	 *
	 */
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
	 * Info.
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
			parameter.getParameterInputFeature().logAll(); // fInMask
			parameter.getParameterSegmentationInputFile().logAll(); // sInMask
			parameter.getParameterSegmentationOutputFile().logAll(); // sOutMask
		}
	}

	public Parameter getParameter() {
		return parameter;
	}

	public void setParameter(Parameter parameter) {
		this.parameter = parameter;
	}
	
}
