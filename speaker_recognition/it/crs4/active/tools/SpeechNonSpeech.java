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

package it.crs4.active.tools;


import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.TreeMap;
import java.util.Vector;

import it.crs4.active.diarization.AMDecode;
import it.crs4.active.diarization.AMsegInit;
import it.crs4.util.PropertiesReader;
import fr.lium.spkDiarization.libClusteringData.Cluster;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libClusteringData.Segment;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.parameter.ParameterSegmentationFile.SegmentationFormat;
/**
 *  
 *  * */
public class SpeechNonSpeech {
	
	private String fInputMask=null; 
	
	/**the path of the wav audio file to be processed*/	
	public String fileName=null; 
	private String show=null; 
	private String baseName=null; 
	private String s_outputMaskRoot=null; 
	private String s_inputMaskRoot=null; 
	
	/**the location of intermediate build files*/
	public String outputRoot=null; 
	
	/**The path of the ubm.gmm file*/
	public String ubm_gmm="";
	
	/**The path of the sms_gmms file*/
	public String sms_gmms="";
	public Parameter parameter =null;
	public String parameter_path=null;
	public PropertiesReader propertiesReader=null;
	private ClusterSet clusterSetResult =null;
	
	/**
	 * Return the PropertiesReader with the configuration 
	 * */
	public PropertiesReader getPropertiesReader() {
		return propertiesReader;
	}
	/**
	 * Sets the PropertiesReader 
	 * 
	 *  @propertiesReader: the propertiesreader object
	 * */
	public void setPropertiesReader(PropertiesReader propertiesReader) {
		this.propertiesReader = propertiesReader;
	}


	/** 
	 * Return the path of the wav audio file to be processed 
	 * @return The pathname of file 
	 * */
	public String getFileName() {
		return fileName;
	}
	

	@Override
	public String toString() {
		return "Diarization [fInputMask=" + fInputMask + ", fileName="
				+ fileName + ", show=" + show + ", baseName=" + baseName
				+ ", s_outputMaskRoot=" + s_outputMaskRoot
				+ ", s_inputMaskRoot=" + s_inputMaskRoot + ", outputRoot="
				+ outputRoot + ", ubm_gmm=" + ubm_gmm + ", sms_gmms="
				+ sms_gmms + ", parameter=" + parameter + ", parameter_path="
				+ parameter_path + "]";
	}


	/**
	 * Return the parameter file
	 * @return parameter: the parameter object
	 * */	
	public Parameter getParameter() {
		return parameter;
	}

	/**
	 * Sets the parameter file
	 * @param parameter: the parameter object
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
	 * Construct a Diarization object with the propertiesReader object 
	 * @param propertiesReader
	 */
	public SpeechNonSpeech(PropertiesReader propertiesReader) {
		this.propertiesReader = propertiesReader;
		configureParameter(this.propertiesReader);
	}

	/**
	 * Construct a Diarization object with the configuration file
	 * @param configuration: the path of the configuration file
	 */
	public SpeechNonSpeech(String configuration) {
		String parameter_path=configuration;
		this.parameter_path = parameter_path;
		PropertiesReader pr=new PropertiesReader(this.parameter_path);
		this.setPropertiesReader(pr);
		configureParameter(this.propertiesReader);
	}

	/**
	 * Construct a Diarization object with the default configuration file
	 */
	public SpeechNonSpeech() {
	}	
	
	/** 
	 * Sets the wav audio file to be processed <br /> 
	 * For example: /Users/audio.wav <br /> 
	 * The wav file having these specs "RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz"
	 * @param The pathname of file 
	 * */	
	public void setFileName(String fileName) {
		this.fileName = fileName;
		baseName=fileName;
		baseName=baseName.split("/")[baseName.split("/").length-1];
		baseName=baseName.replaceFirst(".wav", "");
		show="show="+fileName;
		this.fInputMask="--fInputMask=/"+fileName;
	}
	
	/**
	 * Return the location of intermediate build files 
	 * @return the uri directory
	 * */	
	public String getOutputRoot() {
		return outputRoot;
	}
	
	/**
	 * Sets the location where stored the intermediate build files
	 * @param  the path of directory
	 * */		
	public void setOutputRoot(String outputRoot) {
		this.outputRoot = outputRoot;
		this.s_inputMaskRoot="--sInputMask="+this.outputRoot;
		this.s_outputMaskRoot="--sOutputMask="+this.outputRoot;
	}
	
	
	/**
	 * Usage example <i> java it.crs4.active.diarization.Diarization example.properties </i>
	 * 
	 * <br />The <strong>properties</strong> file:<br /><br /> the path of the wav audio file to be processed<br />
	 * fileName=/Users/mio_file.wav <br /><br />the location of intermediate build files<br />
	 * outputRoot=/Users/out<br />
	 * <br />The path of the ubm.gmm file<br />ubm_gmm=/Users/ubm.gmm<br />
	 * <br />The path of the sms.gmms file<br />sms_gmms=/Users/sms.gmms<br />
	 * <br />The location of the models file<br />modelDir=/Users/audio_model/
	 * 
	 * @param args
	 * @exception Exception
	 */
	public static void main(String[] args) throws Exception{ 
		
		PropertiesReader pr=new PropertiesReader(args[0]);
		SpeechNonSpeech dia=new SpeechNonSpeech();
		dia.setFileName(pr.getProperty("fileName"));
		dia.setOutputRoot(pr.getProperty("outputRoot"));
		dia.setSms_gmms(pr.getProperty("sms_gmms"));
		dia.setUbm_gmm(pr.getProperty("ubm_gmm"));
		dia.run();
		dia.computeSpeechNonSpeech();
		//dia.printSpeech();
		dia.printAll(0);

		for (Object elm: dia.getSpeech()){
			System.out.println("type="+((Object[])elm)[0]+" start="+((Object[])elm)[1]+" stop="+((Object[])elm)[2]+" duration="+((Object[])elm)[3]);
		};
		/*
		for (Object elm: dia.getSilence()){
			System.out.println( ((Object[])elm)[0]);
			System.out.println( ((Object[])elm)[1]);
			System.out.println( ((Object[])elm)[2]);
			System.out.println( ((Object[])elm)[3]);
			
		};
		*/
	}

	public void printSpeech(){
		for (Object elm: getSpeech()){
			System.out.println("type="+((Object[])elm)[0]+" start="+((Object[])elm)[1]+" stop="+((Object[])elm)[2]+" duration="+((Object[])elm)[3]);
			/*System.out.print( ((Object[])elm)[0]  );
			System.out.print( ((Object[])elm)[1] );
			System.out.print( ((Object[])elm)[2] );
			System.out.print( ((Object[])elm)[3] );
		*/	
		};
	}	
	public void printAll(float mindur){
		
		System.out.println("@@@ speech");
		float totalSpeech=0;
		for (Object elm: getSpeech()){
			String tmpdur= ((Object[])elm)[3]+"";
			if ( Float.parseFloat(tmpdur) >mindur ){
			 System.out.println("type="+((Object[])elm)[0]+" start="+((Object[])elm)[1]+" stop="+((Object[])elm)[2]+" duration="+((Object[])elm)[3]);
			 totalSpeech=totalSpeech+Float.parseFloat(""+((Object[])elm)[3]);
			}
		};
		System.out.println("@@@ total speech="+totalSpeech);
		System.out.println("---");
		for (Object elm: this.getNonSpeech()){
			String tmpdur= ((Object[])elm)[3]+"";
			if ( Float.parseFloat(tmpdur) >mindur ){
			 System.out.println("type="+((Object[])elm)[0]+" start="+((Object[])elm)[1]+" stop="+((Object[])elm)[2]+" duration="+((Object[])elm)[3]);
			}
		};
		System.out.println("±±±± other");
		for (Object elm: this.getOther()){
			String tmpdur= ((Object[])elm)[3]+"";
			if ( Float.parseFloat(tmpdur) >mindur ){
			 System.out.println("type="+((Object[])elm)[0]+" start="+((Object[])elm)[1]+" stop="+((Object[])elm)[2]+" duration="+((Object[])elm)[3]);
			}
		};
	  }	
	
	/**
	 * Configure the parameter used in the diarization process by the file stored in properties file
	 * @param propertiesReader
	 * */
	public	void configureParameter(PropertiesReader pr){
		if (pr!=null){
				setPropertiesReader(pr);		
		}
        setFileName(propertiesReader.getProperty("fileName"));
		setOutputRoot(propertiesReader.getProperty("outputRoot"));
		setSms_gmms(propertiesReader.getProperty("sms_gmms"));
		setUbm_gmm(propertiesReader.getProperty("ubm_gmm"));
	}
	

	
	/**
	 * Performs the computation.
	 * @exception Exception
	 * */
	public void run() throws Exception{
		parameter = new Parameter();
		String[] parameterSeg ={"","--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,0:0:0"," --doCEClustering ",
				fInputMask,
				"--sInputMask=",
				s_outputMaskRoot+baseName+".i.seg",
				show };
		AMsegInit seg= new AMsegInit();
		parameter.readParameters(parameterSeg);
		seg.setParameter(parameter);
		seg.run();
		
		
		
		String[] parameterDecode ={"","--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,0:0:0"," --doCEClustering ",
				fInputMask,
				s_inputMaskRoot+baseName+".i.seg",
				s_outputMaskRoot+baseName+".pms.seg",
				"--dPenality=10,10,50" ,
				"--tInputMask="+this.sms_gmms,
				show };
		parameter.readParameters(parameterDecode);
		AMDecode amdecode=new AMDecode();
		amdecode.setParameter(parameter);
		this.clusterSetResult=amdecode.run();
		
	}
	private Set speech=new HashSet(); // example [ ["speech",start in second (float),"end in second","duration in second" ]]
	private Set music=new HashSet();
	private Set silence=new HashSet();
	private Set jingle=new HashSet();
	private Set other=new HashSet();
	

	
	public Set getSpeech() {
		return speech;
	}
	public Set getMusic() {
		return music;
	}
	public Set getSilence() {
		return silence;
	}
	public Set getJingle() {
		return jingle;
	}
	public Set getOther() {
		return other;
	}
	public Set  getNonSpeech(){
		Set tmp=new HashSet();
		tmp.addAll(music);
		tmp.addAll(silence);
		tmp.addAll(jingle);
		return tmp;
	}
	
	
	public void computeSpeechNonSpeech(){

		
		clusterSetResult.collapse();
		SegmentationFormat format = parameter.getParameterSegmentationOutputFile().getFormat();
		System.out.println(format);
		TreeMap<String,Cluster> clusterMap=clusterSetResult.getClusterMap();
		Iterator itCluster=clusterMap.entrySet().iterator(); 

		for (Cluster cluster : clusterMap.values()) {
			Iterator<Segment> itseg=cluster.iterator();
			while(itseg.hasNext()) {
						boolean otherTmp=true;
				         Segment seg = itseg.next();
				         System.out.println(seg.getClusterName() + " start="+seg.getStartInSecond()+ " end="+seg.getEndInSecond()+" lenght="+seg.getLengthInSecond());
				         if(seg.getClusterName().equals("f3")){				        	  
				        	 silence.add(new Object[]{"silence",seg.getStartInSecond(),seg.getEndInSecond(),seg.getLengthInSecond()});
				        	 otherTmp=false;
				         }
				         if(seg.getClusterName().equals("fx")){				        	  
				        	 music.add(new Object[]{"music",seg.getStartInSecond(),seg.getEndInSecond(),seg.getLengthInSecond()});
				        	 otherTmp=false;
				        }
				         if(seg.getClusterName().equals("p")){				        	  
				        	 speech.add(new Object[]{"speech",seg.getStartInSecond(),seg.getEndInSecond(),seg.getLengthInSecond()});
				        	 otherTmp=false;
				        }
				         if(seg.getClusterName().equals("j")){				        	  
				        	 jingle.add(new Object[]{"jingle",seg.getStartInSecond(),seg.getEndInSecond(),seg.getLengthInSecond()});
				        	 otherTmp=false;
				        }
				         if(otherTmp){
				        	 other.add(new Object[]{seg.getClusterName(),seg.getStartInSecond(),seg.getEndInSecond(),seg.getLengthInSecond()});
	 
				         }
			}					
		}

		
	}
	
	/**
	 * 
	 * @return The path of the ubm.gmm file
	 */
	public String getUbm_gmm() {
		return ubm_gmm;
	}
	
	/**
	 * Sets the path of the ubm.gmm file
	 * @param ubm_gmm
	 */
	public void setUbm_gmm(String ubm_gmm) {
		this.ubm_gmm = ubm_gmm;
	}
	
	/**
	 * Return the location of the sms.gmms file
	 * @return the location of sms file
	 */
	public String getSms_gmms() {
		return sms_gmms;
	}
	
	/**
	 * Sets the location of the sms.gmms file
	 * @param sms_gmms
	 */
	public void setSms_gmms(String sms_gmms) {
		this.sms_gmms = sms_gmms;
	}

}
