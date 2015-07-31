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
package it.crs4.active.train;

import fr.lium.spkDiarization.parameter.Parameter;

import it.crs4.util.PropertiesReader;


/**
 * This class perform a train speaker models using a MAP adaptation method. 
 * First, the UBM is copied for each speaker given the initial model. Last, the MAP adaptation is performed. Only means are adapted.
 * The initial model contains one gaussian learned over the training data. 
 * Iteratively, the gaussians are split and trained (up to 5 iterations of EM algorithm) until the number of components is reached. 
 * The second call trains the GMM using the EM algorithm. After 1 to 20 iterations, 
 * the algorithm stops if the gain of likelihood between 2 iterations is less than a given threshold.
 * 
 *  * <strong> Example </strong>
 * <code>
 * <br>  PropertiesReader pr=new PropertiesReader("properties file");
 * 	<br>	Train train=new Train();
	<br>	train.setFileName(pr.getProperty("fileName"));
	<br> train.setOutputRoot(pr.getProperty("outputRoot"));
	<br>	train.setSms_gmms(pr.getProperty("sms_gmms"));
	<br>	train.setUbm_gmm(pr.getProperty("ubm_gmm"));
	<br>	train.run();
	</code>
<br><br>
<strong> An example of properties file </strong><br>
<code>fileName=/Users/example.wav <br>
outputRoot=/Users/example/ <br>
ubm_gmm=/Users/ubm.gmm <br>
sms_gmms=/Users/sms.gmms <br>
gmmName=example <br>
</code>
 * <br> <strong> Expected result </strong><br>
 * The expected result is the <i>example.gmm</i> 
 * */
public class Train {
	 
	private String fInputMask=null;
	private String fileName=null;
	private String show=null;
	private String baseName=null;
	private String s_outputMaskRoot=null;
	private String s_inputMaskRoot=null;
	private String outputRoot=null;
	
	/**
	 * The location of gmm (models) file
	 * */
	private String gmmRoot=null;
	
	/**
	 * The name of generated model
	 * */	
	private String gmmName=null;
	
	/**
	 * Return the name of generated model
	 * @return the name of model
	 * */	
	public String getGmmName() {
		return gmmName;
	}
	
	/**
	 * Set the name of generated model
	 * @param the name of model
	 * */	
	public void setGmmName(String gmmName) {
		this.gmmName = gmmName;
	}

	/**
	 * Return the path where are stored the models
	 * @return the path of directory
	 * */	
	public String getGmmRoot() {
		return gmmRoot;
	}
	

	/**
	 * Sets the path where are stored the models
	 * @param the path of directory
	 * */		
	public void setGmmRoot(String gmmRoot) {
		this.gmmRoot = gmmRoot;
	}
	
	private String ubm_gmm="";
	private String sms_gmms="";

	/** 
	 * Return the path of the wav audio file to be processed 
	 * @return The pathname of file. 
	 * */	
	public String getFileName() {
		return fileName;
	}
	
	/** 
	 * Sets the wav audio file to be processed <br /> 
	 * For example: /Users/labcontenuti/Documents/audio.wav <br /> 
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
		setGmmName(baseName);
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
	 * Usage example <i> java it.crs4.active.train.Main example.properties </i>
	 * 
	 * <br />The <strong>properties</strong> file:<br />
	 * fileName=/Users/mio_file.wav <br />
	 * outputRoot=/Users/out<br />
	 * ubm_gmm=/Users/ubm.gmm<br />
	 * sms_gmms=/Users/sms.gmms<br />
	 * gmmRoot=/Users/gmm_db<br />
	 * 
	 * @param args
	 * @exception Exception
	 */
	public static void main(String[] args) throws Exception{ 
		
		PropertiesReader pr=new PropertiesReader(args[0]);
		boolean make_dia=true;
		/** */
		if (args.length>1){
			if (args[1].equals("nodiarization")){
				make_dia=false;	
			}
		}	
		if(make_dia){
			it.crs4.active.diarization.Diarization dia=new it.crs4.active.diarization.Diarization();
			dia.setFileName(pr.getProperty("fileName"));
			dia.setOutputRoot(pr.getProperty("outputRoot"));
			dia.setSms_gmms(pr.getProperty("sms_gmms"));
			dia.setUbm_gmm(pr.getProperty("ubm_gmm"));
			dia.run();
		}
		
		Train ma=new Train();
		ma.setFileName(pr.getProperty("fileName"));
		ma.setOutputRoot(pr.getProperty("outputRoot"));
		ma.setSms_gmms(pr.getProperty("sms_gmms"));
		ma.setUbm_gmm(pr.getProperty("ubm_gmm"));
		
		if(pr.getProperty("gmmRoot")!=null){
			ma.setGmmRoot(pr.getProperty("gmmRoot"));
		}else{
			ma.setGmmRoot(pr.getProperty("outputRoot"));
		}
		
		if(pr.getProperty("gmmName")!=null){
			ma.setGmmName(pr.getProperty("gmmName"));
		}
		ma.run();
	     

	}

	/**
	 * Performs the computation.
	 * @exception Exception
	 * */
	public void run() throws Exception{
		Parameter parameter = new Parameter();
		String[] parameterDia ={"","--doCEClustering",
				fInputMask,
				//s_outputMaskRoot+baseName+".seg",
				"--sOutputMask="+this.outputRoot+baseName+".seg",
				show };
		
		/*it.crs4.active.train.Diarization dia =new it.crs4.active.train.Diarization();
		parameter.readParameters(parameterDia);
		dia.setParameter(parameter);
		dia.exec(parameterDia);
		dia.runParameter(parameter);
		*/
	    //--sOutputMask="+base_name+".seg --fInputMask="+base_name+".wav --doCEClustering " +base_name;
		fr.lium.spkDiarization.system.Diarization.main(parameterDia);
		
		System.out.println("*********************M TRAIN INIT   ");	
		String[] parameterSeg ={"","--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,1:1:300:4","--emInitMethod=copy",
				fInputMask,
				s_inputMaskRoot+baseName+".s.ident.seg",
				"--sInputMask="+this.outputRoot+baseName+".seg",
				s_outputMaskRoot+baseName+".i.seg",
				"--tInputMask="+this.getUbm_gmm(),
				"--tOutputMask="+this.outputRoot+baseName+".init.gmm",
				show };

		MTrainInit mti= new MTrainInit();
		parameter.readParameters(parameterSeg);
		mti.setParameter(parameter);
		//mti.run();
		fr.lium.spkDiarization.programs.MTrainInit.main(parameterSeg);
		System.out.println("FINEEEEEEEE  *********************M TRAIN INIT   ");	

		System.out.println("M TRAIN MAP   "+s_inputMaskRoot+baseName+".s.seg");	
		String[] parameterMap ={" "," --emCtrl=1,5,0.01"," --varCtrl=0.01,10.0", "--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,1:1:300:4",
				fInputMask,
				"--sInputMask="+this.outputRoot+baseName+".seg",
				"--tInputMask="+this.outputRoot+baseName+".init.gmm",
				"--tOutputMask="+this.gmmRoot+gmmName+".gmm",
				show
				};
		
	    // --sInputMask="+base_name+".seg --fInputMask="+base_name+".wav " 
	    //	    command=command +" --fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4  --tInputMask="+base_name + ".init.gmm 
		//--emCtrl=1,5,0.01 --varCtrl=0.01,10.0 --tOutputMask="+base_name+".gmm "+base_name 


		System.out.println("\n ------------------INIZIO parameterMap\n\n---------------");
		System.out.println(" --emCtrl=1,5,0.01  --varCtrl=0.01,10 --fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,1:1:300:4 "+  fInputMask + "      "+s_inputMaskRoot+baseName+".s.seg" + s_outputMaskRoot+baseName+".i.seg"+ "--tInputMask="+this.outputRoot+baseName+".init.gmm"+ "--tOutputMask="+this.gmmRoot+gmmName+".gmm"+  show);
		System.out.println("\n ------------------FINITO parameterMap\n\n--------------------------");
		MTrainMAP mtiMap= new MTrainMAP();
		parameter.readParameters(parameterMap);
		mtiMap.setParameter(parameter);
		//mtiMap.run();
		fr.lium.spkDiarization.programs.MTrainMAP.main(parameterMap);
		System.out.println("---- END---");
	}
	
	/**
	 * Returns the path of ubm.gmm file
	 * @return the path of file
	 * */	
	public String getUbm_gmm() {
		return ubm_gmm;
	}

	/**
	 * Sets the path of ubm.gmm file
	 * @param the path of file
	 * */
	public void setUbm_gmm(String ubm_gmm) {
		this.ubm_gmm = ubm_gmm;
	}
	
	/**
	 * Returns the path of sms.gmms file
	 * @return the path of file
	 * */	
	public String getSms_gmms() {
		return sms_gmms;
	}
	
	/**
	 * Sets the path of sms.gmms file
	 * @param the path of file
	 * */
	public void setSms_gmms(String sms_gmms) {
		this.sms_gmms = sms_gmms;
	}

	@Override
	public String toString() {
		return "Opencv [fInputMask=" + fInputMask + ", fileName=" + fileName
				+ ", show=" + show + ", baseName=" + baseName
				+ ", s_outputMaskRoot=" + s_outputMaskRoot
				+ ", s_inputMaskRoot=" + s_inputMaskRoot + ", outputRoot="
				+ outputRoot + ", gmmRoot=" + gmmRoot + ", gmmName=" + gmmName
				+ ", ubm_gmm=" + ubm_gmm + ", sms_gmms=" + sms_gmms + "]";
	}
}
