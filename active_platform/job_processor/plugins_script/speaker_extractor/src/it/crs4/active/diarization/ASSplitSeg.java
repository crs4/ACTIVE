package it.crs4.active.diarization;

import java.util.logging.Level;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.libModel.gaussian.GMMArrayList;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.tools.SSplitSeg;

public class ASSplitSeg extends SSplitSeg {
	Parameter parameter =null;
	/**
	 * @param args
	 */
	public  void run( ) throws Exception {
		try {
			SpkDiarizationLogger.setup();
			info(parameter, "ASSplitSeg");
			if (parameter.show.isEmpty() == false) {
				// clusters
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);

				// Features
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				// Compute Model
				GMMArrayList gmmList = MainTools.readGMMContainer(parameter);

				ClusterSet filterClusterSet = new ClusterSet();
				filterClusterSet.read(parameter.show, parameter.getParameterSegmentationFilterFile());

				ClusterSet clusterSetResult = make(featureSet, clusterSet, gmmList, filterClusterSet, parameter);

				MainTools.writeClusterSet(parameter, clusterSetResult, false);

			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		}
	}
	public Parameter getParameter() {
		return parameter;
	}
	public void setParameter(Parameter parameter) {
		this.parameter = parameter;
	}

}
