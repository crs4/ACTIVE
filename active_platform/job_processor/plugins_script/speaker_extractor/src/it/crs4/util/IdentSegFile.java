package it.crs4.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Map.Entry;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;

import org.xml.sax.SAXException;

import fr.lium.experimental.EPAC.xml.XmlEPACInputOutput;
import fr.lium.experimental.MEDIA.xml.XmlMEDIAInputOutput;
import fr.lium.experimental.REPERE.xml.XmlREPEREInputOutput;
import fr.lium.experimental.spkDiarization.libClusteringData.speakerName.SpeakerName;
import fr.lium.experimental.spkDiarization.libClusteringData.transcription.Entity;
import fr.lium.experimental.spkDiarization.libClusteringData.transcription.EntitySet;
import fr.lium.experimental.spkDiarization.libClusteringData.transcription.Link;
import fr.lium.experimental.spkDiarization.libClusteringData.transcription.LinkSet;
import fr.lium.experimental.spkDiarization.libClusteringData.turnRepresentation.Turn;
import fr.lium.experimental.spkDiarization.libClusteringData.turnRepresentation.TurnSet;
import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.IOFile;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.Cluster;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libClusteringData.Segment;
import fr.lium.spkDiarization.libModel.ModelScores;
import fr.lium.spkDiarization.parameter.ParameterSegmentationFile;
import fr.lium.spkDiarization.parameter.ParameterSegmentationFile.SegmentationFormat;

public class IdentSegFile {
	/** The Constant logger. */
	private final static Logger logger = Logger.getLogger(ClusterSet.class.getName());

	/** container of the clusters. */
	protected TreeMap<String, Cluster> clusterMap;

	/** The head cluster set. */
	protected ClusterSet headClusterSet;

	/** The writing. */
	protected Cluster writing;

	public Cluster getWriting() {
		return writing;
	}
	public void setWriting(Cluster writing) {
		this.writing = writing;
	}

	/** The type. */
	protected String type = "speaker";

	/** Universal information storage Map. */
	private TreeMap<String, Object> informationMap;
	
	public ClusterSet clusterSet=null;
	
	public IdentSegFile() {
		clusterMap = new TreeMap<String, Cluster>();
		informationMap = new TreeMap<String, Object>();
		writing = null;
		headClusterSet = null;
	}
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

	public void write(String showName, ParameterSegmentationFile param) throws IOException, ParserConfigurationException, SAXException, DiarizationException, TransformerException {
		String segOutFilename = IOFile.getFilename(param.getMask(), showName);
		logger.info("--> write ClusterSet : " + segOutFilename + " / " + showName);
		File f = new File(segOutFilename);
		SegmentationFormat format = param.getFormat();
		
		if (format.equals(ParameterSegmentationFile.SegmentationFormat.FILE_XML_EPAC)) {
			XmlEPACInputOutput xmlEPAC = new XmlEPACInputOutput();
			//xmlEPAC.writeXML(this, f, param.getEncoding());
		} else if (format.equals(ParameterSegmentationFile.SegmentationFormat.FILE_XML_MEDIA)) {
			XmlMEDIAInputOutput xmlMEDIA = new XmlMEDIAInputOutput();
			//xmlMEDIA.writeXML(this, f, param.getEncoding());
		} else if (param.getFormat().equals(ParameterSegmentationFile.SegmentationFormat.FILE_EGER_HYP)) {
			OutputStreamWriter dos = new OutputStreamWriter(new FileOutputStream(f), param.getEncoding());
			for (Cluster cluster : clusterMap.values()) {
				cluster.writeAsEGER(dos, type);
			}
			if (headClusterSet != null) {
				logger.info("save HEAD !");
				for (Cluster cluster : headClusterSet.getClusterMap().values()) {
					cluster.writeAsEGER(dos, headClusterSet.getType());
				}
			}
			// if (writing != null) {
			// writing.writeAsEGER(dos, "writing");
			// }
			dos.close();

			segOutFilename = IOFile.getFilename(param.getMask(), showName) + ".seg";
			f = new File(segOutFilename);
			dos = new OutputStreamWriter(new FileOutputStream(f), param.getEncoding());
			for (Cluster cluster : clusterMap.values()) {
				Set<Entry<String, Object>> set = clusterSet.getInformation().entrySet();
				for (Entry<String, Object> entry : set) {
					dos.write(";; clusterSet " + entry.getKey() + " " + entry.getValue().toString() + "\n");
				}
				cluster.writeAsSeg(dos);
			}
			dos.close();

		} else if (param.getFormat().equals(ParameterSegmentationFile.SegmentationFormat.FILE_CTL)) {
			OutputStreamWriter dos = new OutputStreamWriter(new FileOutputStream(f), param.getEncoding());
			for (Cluster cluster : clusterMap.values()) {
				cluster.writeAsCTL(dos);
			}
		} else {
			if (headClusterSet != null) {
				logger.info("save HEAD !");
				OutputStreamWriter dos = new OutputStreamWriter(new FileOutputStream(f), param.getEncoding());
				for (Cluster cluster : clusterMap.values()) {
					for (Segment segment : cluster) {
						segment.setChannel("speaker");
					}
					Set<Entry<String, Object>> set = clusterSet.getInformation().entrySet();
					for (Entry<String, Object> entry : set) {
						dos.write(";; clusterSet SPEAKER " + entry.getKey() + " " + entry.getValue().toString() + "\n");
					}
					cluster.writeAsSeg(dos);
				}

				for (Cluster cluster : headClusterSet.getClusterMap().values()) {
					for (Segment segment : cluster) {
						segment.setChannel("head");
					}
					if (param.getFormat().equals(ParameterSegmentationFile.SegmentationFormat.FILE_CTL)) {
						cluster.writeAsCTL(dos);
					} else {
						Set<Entry<String, Object>> set = clusterSet.getInformation().entrySet();
						for (Entry<String, Object> entry : set) {
							dos.write(";; clusterSet HEAD " + entry.getKey() + " " + entry.getValue().toString() + "\n");
						}
						cluster.writeAsSeg(dos);
					}
				}
				if (getWriting() != null) {
					for (Segment segment : getWriting()) {
						segment.setChannel("writting");
					}
					getWriting().writeAsSeg(dos);
				}
				dos.close();
			} else {
				OutputStreamWriter dos = new OutputStreamWriter(new FileOutputStream(f), param.getEncoding());
				for (Cluster cluster : clusterMap.values()) {
					Set<Entry<String, Object>> set = clusterSet.getInformation().entrySet();
					for (Entry<String, Object> entry : set) {
						dos.write(";; clusterSet	 " + entry.getKey() + " " + entry.getValue().toString() + "\n");
					}
					cluster.writeAsSeg(dos);
				}
				dos.close();
			}
		}
	}

}
