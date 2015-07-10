package it.crs4.active.diarization;

import it.crs4.util.PropertiesReader;
import fr.lium.spkDiarization.parameter.Parameter;

public class Diarization {
	
	private String fInputMask=null;//"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav";
	private String fileName=null;//"/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav";
	private String show=null;//"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav";
	private String baseName=null;//"2sec";
	private String s_outputMaskRoot=null;//"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/";
	private String s_inputMaskRoot=null;//"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/";
	private String outputRoot=null;//"/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/";	
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
	    System.out.println(pr.getProperty("fileName"));
	    System.out.println(pr.getProperty("outputRoot"));
	     
		Diarization dia=new Diarization();
		dia.setFileName(pr.getProperty("fileName"));
		dia.setOutputRoot(pr.getProperty("outputRoot"));
		dia.setSms_gmms(pr.getProperty("sms_gmms"));
		dia.setUbm_gmm(pr.getProperty("ubm_gmm"));
		dia.run();
		//dia.runSegInit();
		//dia.runAMCLust();
	}

	public void runSegInit() throws Exception{
		Parameter parameter = new Parameter();
		String[] parameterSeg ={"","--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,0:0:0",
				fInputMask,
				"--sInputMask=",
				s_outputMaskRoot+baseName+".i.seg",
				show };
		AMsegInit seg= new AMsegInit();
		parameter.readParameters(parameterSeg);
		seg.setParameter(parameter);
		seg.run();
	};
	public void runAMCLust() throws Exception{
		Parameter parameter = new Parameter();
		String[] parameterClust ={"", "--cMethod=l", "--cThr=2",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				fInputMask,
				s_inputMaskRoot+baseName+".s.seg",
				s_outputMaskRoot+baseName+".l.seg",
					show };
			parameter.readParameters(parameterClust);
		AMClust clust=new AMClust();
		clust.setParameter(parameter);
		clust.run();
}
	
	public void run() throws Exception{
		Parameter parameter = new Parameter();
		String[] parameterSeg ={"","--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,0:0:0",
				fInputMask,
				"--sInputMask=",
				s_outputMaskRoot+baseName+".i.seg",
				show };
		AMsegInit seg= new AMsegInit();
		parameter.readParameters(parameterSeg);
		seg.setParameter(parameter);
		seg.run();
		
		
		
		String[] parameterDecode ={"","--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,0:0:0",
				fInputMask,
				s_inputMaskRoot+baseName+".i.seg",
				s_outputMaskRoot+baseName+".pms.seg",
				"--dPenality=10,10,50" ,
				"--tInputMask="+this.sms_gmms,
				show };
		parameter.readParameters(parameterDecode);
		AMDecode amdecode=new AMDecode();
		amdecode.setParameter(parameter);
		amdecode.run();
		

		String[] parameterSeg2 ={"","--kind=FULL", "--sMethod=GLR", 
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				fInputMask,
				s_inputMaskRoot+baseName+".i.seg",
				s_outputMaskRoot+baseName+".s.seg",
				"--dPenality=10,10,50" ,
				"--tInputMask="+this.sms_gmms,
				show };
		parameter.readParameters(parameterSeg2);
		AMSeg amseg2=new AMSeg();
		amseg2.setParameter(parameter);
		amseg2.run();
		
		
		String[] parameterClust ={"", "--cMethod=l", "--cThr=2",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				fInputMask,
				s_inputMaskRoot+baseName+".s.seg",
				s_outputMaskRoot+baseName+".l.seg",
 				show };
 		parameter.readParameters(parameterClust);
		AMClust clust=new AMClust();
		clust.setParameter(parameter);
		clust.run();

		
		String[] parameterClustH3 ={"", "--cMethod=h", "--cThr=3",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				fInputMask,
				s_inputMaskRoot+baseName+".l.seg",
				s_outputMaskRoot+baseName+".h.3.seg",
 				show };
 		parameter.readParameters(parameterClustH3);
		clust.setParameter(parameter);
		clust.run();

		
/*
 *		
		String[] parameterTrain ={"", "--nbComp=8", "--kind=DIAG",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.h.3.seg",
				"--tOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.init.gmms",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
 
 * */		
		System.out.println("show ="+show);
		String[] parameterTrain ={"", "--nbComp=8", "--kind=DIAG",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				fInputMask,
				s_inputMaskRoot+baseName+".h.3.seg",
				"--tOutputMask="+this.outputRoot+baseName+".init.gmms",
 				show };
 		parameter.readParameters(parameterTrain);
 		AMTrainInit train=new AMTrainInit();
		train.setParameter(parameter);
		train.run();		

		String[] parameterTrainEM ={"", "--nbComp=8", "--kind=DIAG",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				fInputMask,
				s_inputMaskRoot+baseName+".h.3.seg",
				s_outputMaskRoot+baseName+".gmms",//--tOutputMask=./2sec/%s.gmms
				"--tInputMask="+this.outputRoot+baseName+".init.gmms",
 				show };
 		parameter.readParameters(parameterTrainEM);
 		AMTrainEM trainEM=new AMTrainEM();
		trainEM.setParameter(parameter);
		trainEM.run();		

		
		
/*
 		String[] parameterDecodeViterbi ={"", "--dPenality=250",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.h.3.seg",
				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.d.3.seg",
				"--tInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.init.gmms",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };

 * 
 * */		
		String[] parameterDecodeViterbi ={"", "--dPenality=250",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				fInputMask,
				s_inputMaskRoot+baseName+".h.3.seg",
				s_outputMaskRoot+baseName+".d.3.seg",
				"--tInputMask="+this.outputRoot+baseName+".init.gmms",
 				show };
 		parameter.readParameters(parameterDecodeViterbi);
		amdecode.setParameter(parameter);
		amdecode.run();		
		
		
		String[] parameterSadjSeg ={"", "--dPenality=250",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				fInputMask,
				s_inputMaskRoot+baseName+".d.3.seg",
				s_outputMaskRoot+baseName+".adj.3.seg",
 				show };
		ASAdjSeg asadjSeg=new ASAdjSeg();
 		parameter.readParameters(parameterSadjSeg);
 		asadjSeg.setParameter(parameter);
 		asadjSeg.run();		
		
		String[] parameterFilter ={"", "--fltSegMinLenSpeech=150", "--fltSegMinLenSil=25", "--sFilterClusterName=j", "--fltSegPadding=25",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				fInputMask,
				"--sFilterMask="+this.outputRoot+this.baseName+".pms.seg",
				s_inputMaskRoot+baseName+".adj.3.seg",
				s_outputMaskRoot+baseName+".flt.3.seg",
 				show };
 		parameter.readParameters(parameterFilter);
 		ASFilter asfilter=new ASFilter();
 		asfilter.setParameter(parameter);
 		asfilter.run();		
 		
 		
 		String[] parameterSSplit ={"","--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,0:0:0", 
 				fInputMask, 
 				"--fltSegMinLenSpeech=150", 
 				"--fltSegMinLenSil=25", 
 				"--sFilterClusterName=j", 
 				"--fltSegPadding=25", 
 				"--sFilterMask="+this.outputRoot+this.baseName+".pms.seg", 
 				s_inputMaskRoot+baseName+".adj.3.seg", 
 				s_outputMaskRoot+baseName+".spl.3.seg",
 				show};
 		ASSplitSeg ass=new ASSplitSeg();
 		parameter.readParameters(parameterSSplit);
 		ass.setParameter(parameter);
 		ass.run();		
 		
 
 		String[] parameterScore ={"","--sGender","--sByCluster","--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4", 
 				fInputMask, 
 				s_inputMaskRoot+baseName+".spl.3.seg", 
 				s_outputMaskRoot+baseName+".g.3.seg",
 				"--tInputMask="+this.ubm_gmm,
 				show}; 		
 		AMScore amscore=new AMScore();
 		parameter.readParameters(parameterScore);
 		amscore.setParameter(parameter);
 		amscore.run();		
 		
		String[] parameterClustFinale ={"","--cMethod=ce","--cThr=1.7","--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4", 
 				fInputMask, 
 				s_inputMaskRoot+baseName+".g.3.seg", 
 				s_outputMaskRoot+baseName+".g.3.seg",
 				"--tInputMask="+this.ubm_gmm,
 				show,
 				"--tOutputMask"+this.outputRoot+baseName+".c.gmm",
 				"--emCtrl=1,5,0.01","--sTop=5,"+this.ubm_gmm}; 		
 		parameter.readParameters(parameterClustFinale);
 		clust.setParameter(parameter);
 		clust.run();		
 		
 		System.out.println("-------------------------\n ---------FINITO DIARIZATION\n ------------------");
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
