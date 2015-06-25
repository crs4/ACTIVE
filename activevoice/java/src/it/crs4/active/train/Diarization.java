/**
 * 
 */
package it.crs4.active.train;

import java.io.IOException;
import java.util.logging.Level;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;

import org.xml.sax.SAXException;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.parameter.ParameterBNDiarization;

/**
 * @author Felice Colucci
 *The class perform the diarization task in the training process 
 */
public class Diarization extends fr.lium.spkDiarization.system.Diarization {
	
	Parameter parameter =null;
	String parameter_path=null;

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

	@Override
	public ClusterSet sanityCheck(ClusterSet clusterSet,
			AudioFeatureSet featureSet, Parameter parameter)
			throws DiarizationException, IOException,
			ParserConfigurationException, SAXException, TransformerException {
		 
		return super.sanityCheck(clusterSet, featureSet, parameter);
	}

	
	/*
	 * (non-Javadoc)
	 * @see java.lang.Thread#run()
	 */
	@Override
	public void run() {
		ClusterSet clusterSet = getNextClusterSet();
		while (clusterSet != null) {
			parameter.show = clusterSet.getShowNames().first();
			try {
				ester2Diarization(parameter, clusterSet);
				System.gc();
			} catch (DiarizationException e) {
				e.printStackTrace();
			} catch (Exception e) {
				e.printStackTrace();
			}
			clusterSet = getNextClusterSet();
		}
	}

	public void exec(String[] args) {
		try {
			SpkDiarizationLogger.setup();
			Parameter parameter = getParameter(args);
			parameter.logCmdLine(args);

			if (parameter.show.isEmpty() == false) {
				Diarization2 diarization = new Diarization2();
				if (parameter.getParameterDiarization().getSystem() == ParameterBNDiarization.SystemString[1]) {
					parameter.getParameterSegmentationSplit().setSegmentMaximumLength((10 * parameter.getParameterSegmentationInputFile().getRate()));
				}
				diarization.ester2DiarizationCorpus(parameter);
			}
		} catch (DiarizationException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}

	}


	public void runParameter(Parameter parameter) {
		ClusterSet clusterSet = getNextClusterSet();
		while (clusterSet != null) {
			parameter.show = clusterSet.getShowNames().first();
			try {
				ester2Diarization(parameter, clusterSet);
				System.gc();
			} catch (DiarizationException e) {
				e.printStackTrace();
			} catch (Exception e) {
				e.printStackTrace();
			}
			clusterSet = getNextClusterSet();
		}
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

	
	public Diarization() {
		super();
	}

	public Diarization(Parameter parameter) {
		super();
		this.parameter = parameter;
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
