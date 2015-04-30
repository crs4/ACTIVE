package it.crs4.active.diarization;

import fr.lium.spkDiarization.parameter.Parameter;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception{
		Parameter parameter = new Parameter();
		String[] parameterSeg ={"","--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=",
				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.i.seg",
				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
		AMsegInit seg= new AMsegInit();
		parameter.readParameters(parameterSeg);
		seg.setParameter(parameter);
		seg.run();
		
		
		
		String[] parameterDecode ={"","--fInputDesc=audio16kHz2sphinx,1:3:2:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.i.seg",
				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.pms.seg",
				"--dPenality=10,10,50" ,
				"--tInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/sms.gmms",
				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
		parameter.readParameters(parameterDecode);
		AMDecode amdecode=new AMDecode();
		amdecode.setParameter(parameter);
		amdecode.run();
		

		String[] parameterSeg2 ={"","--kind=FULL", "--sMethod=GLR", 
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.i.seg",
				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.s.seg",
				"--dPenality=10,10,50" ,
				"--tInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/sms.gmms",
				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
		parameter.readParameters(parameterSeg2);
		AMSeg amseg2=new AMSeg();
		amseg2.setParameter(parameter);
		amseg2.run();
		
		
		String[] parameterClust ={"", "--cMethod=l", "--cThr=2",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.s.seg",
				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.l.seg",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
 		parameter.readParameters(parameterClust);
		AMClust clust=new AMClust();
		clust.setParameter(parameter);
		clust.run();

		
		String[] parameterClustH3 ={"", "--cMethod=h", "--cThr=3",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.l.seg",
				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.h.3.seg",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
 		parameter.readParameters(parameterClustH3);
		clust.setParameter(parameter);
		clust.run();
		
		String[] parameterTrain ={"", "--nbComp=8", "--kind=DIAG",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.h.3.seg",
				"--tOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.init.gmms",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
 		parameter.readParameters(parameterTrain);
 		AMTrainInit train=new AMTrainInit();
		train.setParameter(parameter);
		train.run();		

		String[] parameterTrainEM ={"", "--nbComp=8", "--kind=DIAG",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.h.3.seg",
				"--tOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.gmms",
				"--tInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.init.gmms",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
 		parameter.readParameters(parameterTrainEM);
 		AMTrainEM trainEM=new AMTrainEM();
		trainEM.setParameter(parameter);
		trainEM.run();		
	
		String[] parameterDecodeViterbi ={"", "--dPenality=250",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.h.3.seg",
				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.d.3.seg",
				"--tInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.init.gmms",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
 		parameter.readParameters(parameterDecodeViterbi);
		amdecode.setParameter(parameter);
		amdecode.run();		
		
		
		String[] parameterSadjSeg ={"", "--dPenality=250",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.d.3.seg",
				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.adj.3.seg",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
		ASAdjSeg asadjSeg=new ASAdjSeg();
 		parameter.readParameters(parameterSadjSeg);
 		asadjSeg.setParameter(parameter);
 		asadjSeg.run();		
		
		String[] parameterFilter ={"", "--fltSegMinLenSpeech=150", "--fltSegMinLenSil=25", "--sFilterClusterName=j", "--fltSegPadding=25",
				"--fInputDesc=audio16kHz2sphinx,1:1:0:0:0:0,13,0:0:0",
				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
				"--sFilterMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.pms.seg",
				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.adj.3.seg",
				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.flt.3.seg",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav" };
 		parameter.readParameters(parameterFilter);
 		ASFilter asfilter=new ASFilter();
 		asfilter.setParameter(parameter);
 		asfilter.run();		
 		
 		
 		String[] parameterSSplit ={"","--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,0:0:0", 
 				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav", 
 				"--fltSegMinLenSpeech=150", 
 				"--fltSegMinLenSil=25", 
 				"--sFilterClusterName=j", 
 				"--fltSegPadding=25", 
 				"--sFilterMask=/Users/labcontenuti/Documents/workspace/AudioActive/84//2sec/2sec.pms.seg", 
 				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84//2sec/2sec.adj.3.seg", 
 				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84//2sec/2sec.spl.3.seg",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav"};
 		ASSplitSeg ass=new ASSplitSeg();
 		parameter.readParameters(parameterSSplit);
 		ass.setParameter(parameter);
 		ass.run();		
 		
 
 		String[] parameterScore ={"","--sGender","--sByCluster","--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4", 
 				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav", 
 				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.spl.3.seg", 
 				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.g.3.seg",
 				"--tInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/ubm.gmm",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav"}; 		
 		AMScore amscore=new AMScore();
 		parameter.readParameters(parameterScore);
 		amscore.setParameter(parameter);
 		amscore.run();		
 		
		String[] parameterClustFinale ={"","--cMethod=ce","--cThr=1.7","--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4", 
 				"--fInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav", 
 				"--sInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.g.3.seg", 
 				"--sOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.g.3.seg",
 				"--tInputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/ubm.gmm",
 				"show=/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/2sec.wav",
 				"--tOutputMask=/Users/labcontenuti/Documents/workspace/AudioActive/84/2sec/2sec.c.gmm",
 				"--emCtrl=1,5,0.01","--sTop=5,/Users/labcontenuti/Documents/workspace/AudioActive/84/ubm.gmm"}; 		
 		parameter.readParameters(parameterClustFinale);
 		clust.setParameter(parameter);
 		clust.run();		
 		
	
	}

}
