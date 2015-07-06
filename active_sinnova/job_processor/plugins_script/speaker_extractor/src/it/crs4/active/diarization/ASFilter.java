package it.crs4.active.diarization;

import java.util.logging.Level;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.tools.SFilter;

public class ASFilter extends SFilter {
	Parameter parameter =null;
	/**
	 * @param args
	 */
	public  void run( ) throws Exception {
		try {
			SpkDiarizationLogger.setup();
			info(parameter, "ASFilter");
			if (parameter.show.isEmpty() == false) {
				// clusters
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);

				ClusterSet filterClusterSet = new ClusterSet();
				filterClusterSet.read(parameter.show, parameter.getParameterSegmentationFilterFile());

				ClusterSet clusterResult = make(clusterSet, filterClusterSet, parameter);

				MainTools.writeClusterSet(parameter, clusterResult, true);
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
