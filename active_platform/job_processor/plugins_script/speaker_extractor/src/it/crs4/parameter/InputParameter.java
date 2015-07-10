package it.crs4.parameter;

public class InputParameter {
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

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
