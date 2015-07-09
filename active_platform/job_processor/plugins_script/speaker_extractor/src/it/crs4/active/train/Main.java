package it.crs4.active.train;

import fr.lium.spkDiarization.parameter.Parameter;

import it.crs4.active.diarization.Diarization;
import it.crs4.util.PropertiesReader;

public class Main {
	private String fInputMask=null;//"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav";
	private String fileName=null;//"/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav";
	private String show=null;//"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav";
	private String baseName=null;//"2sec";
	private String s_outputMaskRoot=null;//"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/";
	private String s_inputMaskRoot=null;//"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/";
	private String outputRoot=null;//"/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/";	
	private String gmmRoot=null;
	private String gmmName=null;

	public String getGmmName() {
		return gmmName;
	}
	public void setGmmName(String gmmName) {
		this.gmmName = gmmName;
	}
	public String getGmmRoot() {
		return gmmRoot;
	}
	public void setGmmRoot(String gmmRoot) {
		this.gmmRoot = gmmRoot;
	}
	private String ubm_gmm="/Users/labcontenuti/Documents/workspace/AudioActive/84/ubm.gmm";
	private String sms_gmms="/Users/labcontenuti/Documents/workspace/AudioActive/84/sms.gmms";
	public String getFileName() {
		return fileName;
	}
	public void setFileName(String fileName) {
		this.fileName = fileName;
		baseName=fileName;
		baseName=baseName.split("/")[baseName.split("/").length-1];
		baseName=baseName.replaceFirst(".wav", "");
		show="show="+fileName;
		this.fInputMask="--fInputMask=/"+fileName;
		setGmmName(baseName);
	}
	public String getOutputRoot() {
		return outputRoot;
	}
	public void setOutputRoot(String outputRoot) {
		this.outputRoot = outputRoot;
		this.s_inputMaskRoot="--sInputMask="+this.outputRoot;
		this.s_outputMaskRoot="--sOutputMask="+this.outputRoot;
	}
	
	
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception{ 
		
		//System.out.println(args[0]);
		PropertiesReader pr=new PropertiesReader(args[0]);
		boolean make_dia=true;
		
		if (args.length>1){
			if (args[1].equals("nodiarization")){
				make_dia=false;	
			}
		}	
		if(make_dia){
			Diarization dia=new Diarization();
			dia.setFileName(pr.getProperty("fileName"));
			dia.setOutputRoot(pr.getProperty("outputRoot"));
			dia.setSms_gmms(pr.getProperty("sms_gmms"));
			dia.setUbm_gmm(pr.getProperty("ubm_gmm"));
			dia.run();
		}
		Main ma=new Main();
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
	// --tOutputMask=%s.init.gmm speakers

	public void run() throws Exception{
		Parameter parameter = new Parameter();
		
		
		/*

	def _train_init(filebasename):
    """Train the initial speaker gmm model."""
    utils.start_subprocess(JAVA_EXE +' -Xmx256m -cp ' + CONFIGURATION.LIUM_JAR
        + ' fr.lium.spkDiarization.programs.MTrainInit '
        + '--sInputMask=%s.ident.seg --fInputMask=%s.wav '
        + '--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4 '
        + '--emInitMethod=copy --tInputMask=' + CONFIGURATION.UBM_PATH
        + ' --tOutputMask=%s.init.gmm ' + filebasename)
    utils.ensure_file_exists(filebasename + '.init.gmm')

*/

		String[] parameterSeg ={"","--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,1:1:300:4","--emInitMethod=copy",
				fInputMask,
				s_inputMaskRoot+baseName+".s.seg",
				s_outputMaskRoot+baseName+".i.seg",
				"--tInputMask="+this.getUbm_gmm(),
				"--tOutputMask="+this.outputRoot+baseName+".init.gmm",
				show };
		MTrainInit mti= new MTrainInit();
		parameter.readParameters(parameterSeg);
		mti.setParameter(parameter);
		mti.run();
/*
 * def _train_map(filebasename):
    """Train the speaker model using a MAP adaptation method."""
    utils.start_subprocess(JAVA_EXE +' -Xmx256m -cp ' + CONFIGURATION.LIUM_JAR
        + ' fr.lium.spkDiarization.programs.MTrainMAP --sInputMask=%s.ident.seg'
        + ' --fInputMask=%s.wav '
        + '--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4 '
        + '--tInputMask=%s.init.gmm --emCtrl=1,5,0.01 --varCtrl=0.01,10.0 '
        + '--tOutputMask=%s.gmm ' + filebasename)
    	 * 
		 * */

		// --sInputMask=%s.seg --fInputMask=%s.wav --fInputDesc="audio16kHz2sphinx,1:3:2:0:0:0,13,1:1:300:4"  --tInputMask=%s.init.gmm --emCtrl=1,5,0.01 --varCtrl=0.01,10.0 --tOutputMask=%s.gmm speakers
		System.out.println("M TRAIN MAP   "+s_inputMaskRoot+baseName+".s.seg");	
		String[] parameterMap ={""," --emCtrl=1,5,0.01"," --varCtrl=0.01,10.0", "--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,1:1:300:4",
				fInputMask,
				s_inputMaskRoot+baseName+".ident.seg",
				s_outputMaskRoot+baseName+".i.seg",
				
				"--tInputMask="+this.outputRoot+baseName+".init.gmm",
				"--tOutputMask="+this.gmmRoot+gmmName+".gmm",
				show
				//"nomediprova"
				};
		System.out.println("\n ------------------INIZIO parameterMap\n\n---------------");
		System.out.println(" --emCtrl=1,5,0.01  --varCtrl=0.01,10.--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,1:1:300:4 "+  fInputMask + "      "+s_inputMaskRoot+baseName+".s.seg" + s_outputMaskRoot+baseName+".i.seg"+ "--tInputMask="+this.outputRoot+baseName+".init.gmm"+ "--tOutputMask="+this.gmmRoot+gmmName+".gmm"+  show);
		System.out.println("\n ------------------FINITO parameterMap\n\n--------------------------");
		MTrainMAP mtiMap= new MTrainMAP();
		parameter.readParameters(parameterMap);
		mtiMap.setParameter(parameter);
		mtiMap.run();
	
		
	}
	public String getUbm_gmm() {
		return ubm_gmm;
	}
	public void setUbm_gmm(String ubm_gmm) {
		this.ubm_gmm = ubm_gmm;
	}
	public String getSms_gmms() {
		return sms_gmms;
	}
	public void setSms_gmms(String sms_gmms) {
		this.sms_gmms = sms_gmms;
	}
}
