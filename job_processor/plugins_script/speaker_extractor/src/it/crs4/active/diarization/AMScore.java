package it.crs4.active.diarization;

import java.util.logging.Level;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.libModel.gaussian.GMMArrayList;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.programs.MScore;

public class AMScore extends MScore {
	Parameter parameter =null;

	/**
	 * @param args
	 */
	public  void run() throws Exception {
		try {
			SpkDiarizationLogger.setup();
			info(parameter, "MScore");
			if (parameter.show.isEmpty() == false) {
				// clusters
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);
				// FeatureSet featureSet2 = Diarization.loadFeature(parameter, clusterSetBase, parameter.getParameterInputFeature().getFeaturesDescription().getFeaturesFormat()
				// + ",1:1:0:0:0:0,13,0:0:0:0");
				// ClusterSet clusterSet = new ClusterSet();
				// MSegInit.make(featureSet2, clusterSetBase, clusterSet, parameter);
				// clusterSet.collapse();
				// Features
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				// Top Gaussian model
				GMMArrayList gmmTopGaussianList = MainTools.readGMMForTopGaussian(parameter, featureSet);

				// Compute Model
				GMMArrayList gmmList = MainTools.readGMMContainer(parameter);

				ClusterSet clusterSetResult = make(featureSet, clusterSet, gmmList, gmmTopGaussianList, parameter);

				// Seg outPut
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
