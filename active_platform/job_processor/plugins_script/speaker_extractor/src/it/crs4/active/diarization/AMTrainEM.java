package it.crs4.active.diarization;

import java.util.logging.Level;
import java.util.logging.Logger;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.libModel.gaussian.GMMArrayList;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.programs.MTrainEM;

public class AMTrainEM extends MTrainEM {

	/**
	 * @param args
	 */
	Parameter parameter =null;
	private final static Logger logger = Logger.getLogger(AMClust.class.getName());

	public void run() throws Exception {
		try {
			SpkDiarizationLogger.setup();
			info(parameter, "AMTrainEM");
			if (parameter.show.isEmpty() == false) {
				// clusters
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);

				// Features
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);

				// Compute Model
				GMMArrayList initializationGmmList = MainTools.readGMMContainer(parameter);
				// Compute Model
				GMMArrayList gmmList = new GMMArrayList(clusterSet.clusterGetSize());

				make(featureSet, clusterSet, initializationGmmList, gmmList, parameter);

				MainTools.writeGMMContainer(parameter, gmmList);
			}
		} catch (DiarizationException e) {
			logger.log(Level.SEVERE, "error \t exception ", e);
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
