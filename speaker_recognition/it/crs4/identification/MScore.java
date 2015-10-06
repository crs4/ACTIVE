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

package it.crs4.identification;

import it.crs4.active.diarization.AMScore;
import it.crs4.parameter.InputParameter;
import it.crs4.util.PropertiesReader;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.Vector;
import java.util.Map.Entry;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

import fr.lium.spkDiarization.lib.DiarizationException;
import fr.lium.spkDiarization.lib.IOFile;
import fr.lium.spkDiarization.lib.MainTools;
import fr.lium.spkDiarization.lib.SpkDiarizationLogger;
import fr.lium.spkDiarization.libClusteringData.Cluster;
import fr.lium.spkDiarization.libClusteringData.ClusterSet;
import fr.lium.spkDiarization.libClusteringData.Segment;
import fr.lium.spkDiarization.libFeature.AudioFeatureSet;
import fr.lium.spkDiarization.libModel.gaussian.GMM;
import fr.lium.spkDiarization.libModel.gaussian.GMMArrayList;
import fr.lium.spkDiarization.libModel.gaussian.ModelIO;
import fr.lium.spkDiarization.parameter.Parameter;
import fr.lium.spkDiarization.parameter.ParameterScore;

/**
 * This class perform log-likelihood scoring program 
 */
public class MScore {

	/** The Constant logger. */
	private Logger logger = Logger.getLogger(MScore.class.getName()); //Logger.getLogger("/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/mscore.log");//
	Parameter parameter =null;
	private String fInputMask=null; 
	private String fileName=null; 
	private String show=null; 
	private String baseName=null; 
	public String getBaseName() {
		return baseName;
	}
	public void setBaseName(String baseName) {
		this.baseName = baseName;
	}
	private String s_outputMaskRoot=null;
	private String s_inputMaskRoot=null;
	private String outputRoot=null;	
	private String ubm_gmm="";
	private String sms_gmms="";
	private String gmm_model=null;
	private ClusterSet clusterSetResult=null;
	private ClusterResultSet clusterResultSet=new ClusterResultSet();
	FileHandler fh;  

	public void writeIdentSegFile(){
		
		try{
			
		}catch(Exception e ){
			e.printStackTrace();
		}
		
	}
	public MScore(){
	}
	public void printTheBestBySpeaker(){
		System.out.println("------THE BEST BY SPEAKERil------");
		Hashtable cluster=clusterResultSet.getCluster();
		Iterator<String> it=cluster.keySet().iterator();
		Hashtable<String, Vector> speaker=new Hashtable<String, Vector>();
		while(it.hasNext()){
			String cr_it=(String)it.next();
			//System.out.println(cr_it);
			ClusterResult cr=(ClusterResult)cluster.get(cr_it);
			Object[] db_arr=cr.getValue().keySet().toArray();
			Arrays.sort(db_arr);
			int ln=db_arr.length;
			if ( speaker.keySet().contains( (String) cr.getValue().get(db_arr[ln-1]))  ){
				Vector<String> tmp= speaker.get(cr.getValue().get(db_arr[ln-1]));
				tmp.add( cr_it );
				speaker.put( (String) cr.getValue().get(db_arr[ln-1]), tmp);
			}else{
				Vector<String> tmp=new Vector<String>();
				tmp.add(cr_it);
				speaker.put( (String) cr.getValue().get(db_arr[ln-1]), tmp);				
			}
			
		}
		Iterator<String> sp_it=speaker.keySet().iterator();

		OutputStreamWriter dos;
		try {
			dos = new OutputStreamWriter(new FileOutputStream(outputRoot+"/"+baseName+"_ident.txt"));
			OutputStreamWriter nomi_pres= new OutputStreamWriter(new FileOutputStream(outputRoot+"/"+"nomi.txt"));
			
			String tmp_name="\n";
			while(sp_it.hasNext()){
				String key=(String)sp_it.next();
				System.out.println("name="+key);
				nomi_pres.write(key+"\n");
				tmp_name=tmp_name+key+"\n";
				for(int i=0; i< ( (Vector) speaker.get(key) ).size();i++){
					TreeMap<Integer,Segment> map=clusterSetResult.getCluster((String)( (Vector) speaker.get(key) ).get(i)).clusterToFrames();
					System.out.println(" cluster="+((Vector) speaker.get(key) ).get(i)+" lenght="+clusterSetResult.getCluster((String)( (Vector) speaker.get(key) ).get(i)).getLength());
					dos.write(((Vector) speaker.get(key) ).get(i)+"="+key+"\n");
					
				}
			}
			
		 
			dos.close();
			System.out.println("NOMI PRESENTI "+tmp_name);
			nomi_pres.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public void printTheBestByThr(long thr){
		System.out.println("------THE BEST BY SPEAKERil------");
		Hashtable cluster=clusterResultSet.getCluster();
		Iterator<String> it=cluster.keySet().iterator();
		Hashtable<String, Vector> speaker=new Hashtable<String, Vector>();
		while(it.hasNext()){
			String cr_it=(String)it.next();
			//System.out.println(cr_it);
			ClusterResult cr=(ClusterResult)cluster.get(cr_it);
			Object[] db_arr=cr.getValue().keySet().toArray();
			Arrays.sort(db_arr);
			int ln=db_arr.length;
			if ( speaker.keySet().contains( (String) cr.getValue().get(db_arr[ln-1]))  ){
				Vector<String> tmp= speaker.get(cr.getValue().get(db_arr[ln-1]));
				tmp.add( cr_it );
				speaker.put( (String) cr.getValue().get(db_arr[ln-1]), tmp);
			}else{
				Vector<String> tmp=new Vector<String>();
				tmp.add(cr_it);
				speaker.put( (String) cr.getValue().get(db_arr[ln-1]), tmp);				
			}
			//System.out.println("score="+db_arr[ln-1] +" name="+cr.getValue().get(db_arr[ln-1])  );
		}
		Iterator<String> sp_it=speaker.keySet().iterator();
		//String f ="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/testindent.txt";

		OutputStreamWriter dos;
		try {
			dos = new OutputStreamWriter(new FileOutputStream(outputRoot+"/"+baseName+"_ident.txt"));
			
			while(sp_it.hasNext()){
				String key=(String)sp_it.next();
				System.out.println("name="+key);
				for(int i=0; i< ( (Vector) speaker.get(key) ).size();i++){
					TreeMap<Integer,Segment> map=clusterSetResult.getCluster((String)( (Vector) speaker.get(key) ).get(i)).clusterToFrames();
					System.out.println(" cluster="+((Vector) speaker.get(key) ).get(i)+" lenght="+clusterSetResult.getCluster((String)( (Vector) speaker.get(key) ).get(i)).getLength());
					dos.write(((Vector) speaker.get(key) ).get(i)+"="+key+"\n");
				}
			}
			
		 
			dos.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	
	
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
	    try {  
	        // This block configure the logger with handler and formatter  
	        fh = new FileHandler(this.outputRoot+"/mscore.log");  
	        logger.addHandler(fh);
	        SimpleFormatter formatter = new SimpleFormatter();  
	        fh.setFormatter(formatter); 
	    } catch (SecurityException e) {  
	        e.printStackTrace();  
	    } catch (IOException e) {  
	        e.printStackTrace();  
	    }  

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
	
	public ClusterSet make(AudioFeatureSet featureSet, ClusterSet clusterSet, GMMArrayList gmmList, GMMArrayList gmmTopList, Parameter parameter) throws DiarizationException, IOException {
		logger.info("Compute Score");
		int size = gmmList.size();
		logger.finer("GMM size:" + size);
		ArrayList<String> genderString = new ArrayList<String>();
		ArrayList<String> bandwidthString = new ArrayList<String>();
		for (int i = 0; i < size; i++) {
			String gmmName = gmmList.get(i).getName();
			if (parameter.getParameterScore().isGender() == true) {
				if (gmmName.equals("MS")) {
					genderString.add(Cluster.genderStrings[1]);
					bandwidthString.add(Segment.bandwidthStrings[2]);
				} else if (gmmName.equals("FS")) {
					genderString.add(Cluster.genderStrings[2]);
					bandwidthString.add(Segment.bandwidthStrings[2]);
				} else if (gmmName.equals("MT")) {
					genderString.add(Cluster.genderStrings[1]);
					bandwidthString.add(Segment.bandwidthStrings[1]);
				} else if (gmmName.equals("FT")) {
					genderString.add(Cluster.genderStrings[2]);
					bandwidthString.add(Segment.bandwidthStrings[1]);
				} else {
					genderString.add(Cluster.genderStrings[0]);
					bandwidthString.add(Segment.bandwidthStrings[0]);
				}
			} else {
				genderString.add(Cluster.genderStrings[0]);
				bandwidthString.add(Segment.bandwidthStrings[0]);
			}
		}

		ClusterSet clusterSetResult = new ClusterSet();
		for (Cluster cluster : clusterSet.clusterSetValue()) {
			double[] sumScoreVector = new double[size];
			int[] sumLenghtVector = new int[size];
			double ubmScore = 0.0;
			GMM gmmTop = null;
			if (parameter.getParameterTopGaussian().getScoreNTop() >= 0) {
				gmmTop = gmmTopList.get(0);
			}
			Arrays.fill(sumScoreVector, 0.0);
			Arrays.fill(sumLenghtVector, 0);
			for (Segment currantSegment : cluster) {
				Segment segment = (currantSegment.clone());
				int end = segment.getStart() + segment.getLength();
				featureSet.setCurrentShow(segment.getShowName());
				double[] scoreVector = new double[size];
				double maxScore = 0.0;
				int idxMaxScore = 0;
				for (int i = 0; i < size; i++) {
					gmmList.get(i).score_initialize();
				}
				for (int start = segment.getStart(); start < end; start++) {
					for (int i = 0; i < size; i++) {
						GMM gmm = gmmList.get(i);
						if (parameter.getParameterTopGaussian().getScoreNTop() >= 0) {
							if (i == 0) {
								gmmTop.score_getAndAccumulateAndFindTopComponents(featureSet, start, parameter.getParameterTopGaussian().getScoreNTop());
							}
							gmm.score_getAndAccumulateForComponentSubset(featureSet, start, gmmTop.getTopGaussianVector());
						} else {
							gmm.score_getAndAccumulate(featureSet, start);
						}
					}
				}

				if (parameter.getParameterTopGaussian().getScoreNTop() >= 0) {
					ubmScore = gmmTop.score_getMeanLog();
					gmmTop.score_getSumLog();
					gmmTop.score_getCount();
					gmmTop.score_reset();
				}
				for (int i = 0; i < size; i++) {
					GMM gmm = gmmList.get(i);
					scoreVector[i] = gmm.score_getMeanLog();
					sumLenghtVector[i] += gmm.score_getCount();
					sumScoreVector[i] += gmm.score_getSumLog();
					if (i == 0) {
						maxScore = scoreVector[0];
						idxMaxScore = 0;
					} else {
						double value = scoreVector[i];
						if (maxScore < value) {
							maxScore = value;
							idxMaxScore = i;
						}
					}
					gmm.score_reset();
				}
				if (parameter.getParameterScore().isTNorm()) {
					double sumScore = 0;
					double sum2Score = 0;
					for (int i = 0; i < size; i++) {
						sumScore += scoreVector[i];
						sum2Score += (scoreVector[i] * scoreVector[i]);
					}
					for (int i = 0; i < size; i++) {
						double value = scoreVector[i];
						double mean = (sumScore - value) / (size - 1);
						double et = Math.sqrt(((sum2Score - (value * value)) / (size - 1)) - (mean * mean));
						scoreVector[i] = (value - mean) / et;
					}
				}
				if (parameter.getParameterScore().isGender() == true) {
					segment.setBandwidth(bandwidthString.get(idxMaxScore));
					segment.setInformation("segmentGender", genderString.get(idxMaxScore));
				}
				if (parameter.getParameterScore().isBySegment()) {
					for (int k = 0; k < size; k++) {
						double score = scoreVector[k];
						GMM gmm = gmmList.get(k);
						segment.setInformation("score:" + gmm.getName(), score);
						currantSegment.setInformation("score:" + gmm.getName(), score);
					}
					if (parameter.getParameterTopGaussian().getScoreNTop() >= 0) {
						segment.setInformation("score:" + "UBM", ubmScore);
						currantSegment.setInformation("score:" + "UBM", ubmScore);
					}
				}
				String newName = cluster.getName();
				if (parameter.getParameterScore().isByCluster() == false) {
					if ((scoreVector[idxMaxScore] > parameter.getParameterSegmentation().getThreshold())
							&& (parameter.getParameterScore().getLabel() != ParameterScore.LabelType.LABEL_TYPE_NONE.ordinal())) {
						if (parameter.getParameterScore().getLabel() == ParameterScore.LabelType.LABEL_TYPE_ADD.ordinal()) {
							newName += "_";
							newName += gmmList.get(idxMaxScore).getName();
						} else {
							newName = gmmList.get(idxMaxScore).getName();
						}
					}

					Cluster temporaryCluster = clusterSetResult.getOrCreateANewCluster(newName);
					temporaryCluster.setGender(cluster.getGender());
					if (parameter.getParameterScore().isGender() == true) {
						temporaryCluster.setGender(genderString.get(idxMaxScore));
					}
					temporaryCluster.addSegment(segment);
				}
			}
			if (parameter.getParameterScore().isByCluster()) {
				for (int i = 0; i < size; i++) {
					sumScoreVector[i] /= sumLenghtVector[i];
				}
				if (parameter.getParameterScore().isTNorm()) {
					double sumScore = 0;
					double sum2Score = 0;
					for (int i = 0; i < size; i++) {
						sumScore += sumScoreVector[i];
						sum2Score += (sumScoreVector[i] * sumScoreVector[i]);
					}
					for (int i = 0; i < size; i++) {
						double value = sumScoreVector[i];
						double mean = (sumScore - value) / (size - 1);
						double et = Math.sqrt(((sum2Score - (value * value)) / (size - 1)) - (mean * mean));
						sumScoreVector[i] = (value - mean) / et;
					}
				}
				double maxScore = sumScoreVector[0];
				int idxMaxScore = 0;
				for (int i = 1; i < size; i++) {
					double s = sumScoreVector[i];
					if (maxScore < s) {
						maxScore = s;
						idxMaxScore = i;
					}
				}
				String newName = cluster.getName();
				if ((sumScoreVector[idxMaxScore] > parameter.getParameterSegmentation().getThreshold())
						&& (parameter.getParameterScore().getLabel() != ParameterScore.LabelType.LABEL_TYPE_NONE.ordinal())) {
					if (parameter.getParameterScore().getLabel() == ParameterScore.LabelType.LABEL_TYPE_ADD.ordinal()) {
						newName += "_";
						newName += gmmList.get(idxMaxScore).getName();
					} else {
						newName = gmmList.get(idxMaxScore).getName();
					}
					//logger.finer("cluster name=" + cluster.getName() + " new_name=" + newName);
				}
				Cluster tempororaryCluster = clusterSetResult.getOrCreateANewCluster(newName);
				tempororaryCluster.setGender(cluster.getGender());
				if (parameter.getParameterScore().isGender() == true) {
					tempororaryCluster.setGender(genderString.get(idxMaxScore));
				}
				tempororaryCluster.setName(newName);
				for (Segment currantSegment : cluster) {
					Segment segment = (currantSegment.clone());
					if (parameter.getParameterScore().isGender() == true) {
						segment.setBandwidth(bandwidthString.get(idxMaxScore));
					}
					tempororaryCluster.addSegment(segment);
				}
				for (int k = 0; k < size; k++) {
					double score = sumScoreVector[k];
					GMM gmm = gmmList.get(k);
					//logger.finer("****clustername = " + newName + " name=" + gmm.getName() + " =" + score+" k="+k);
					//logger.log(Level.SEVERE, "****clustername = " + newName + " name=" + gmm.getName() + " =" + score);
					tempororaryCluster.setInformation("score:" + gmm.getName(), score);
					ClusterResult cr=new ClusterResult();
					cr.setName(newName);
					cr.getValue().put(score, gmm.getName());
					System.out.println("------ clusterResultSet.putValue(newName, gmm.getName(), score)=----------------");
					System.out.println(newName+ "  "+ gmm.getName()+"  "+ score);
					if (isName(gmm.getName())){
						clusterResultSet.putValue(newName, gmm.getName(), score);
					}else{
						System.out.println("*****************"+gmm.getName()+" Non nome valido  ");
						
					}
				}
				
				if (parameter.getParameterTopGaussian().getScoreNTop() >= 0) {
					// tempororaryCluster.putInformation("score:" + "length", ubmSumLen);
					// tempororaryCluster.putInformation("score:" + "UBM", ubmSumScore / ubmSumLen);
				}
			}
		}
		this.clusterSetResult=clusterSetResult;
		return clusterSetResult;
	}
	public boolean isName(String name){
		boolean result=true;
		name=name.trim();
		name=name.toLowerCase();
		if(name.startsWith("s")){
			name=name.replaceFirst("s", "");
			if(name.matches("-?\\d+(\\.\\d+)?")){
				result=false;
			}
		}
		return result;
	}
	/**
	 * The main method.
	 * 
	 * @param args the arguments
	 * @throws Exception the exception
	 */
	public static void main(String[] args) throws Exception {
		
		PropertiesReader pr=new PropertiesReader(args[0]);
		MScore mscore=new MScore();
		mscore.setFileName(pr.getProperty("fileName"));
		mscore.setOutputRoot(pr.getProperty("outputRoot"));
		mscore.setGmm_model("/Users/labcontenuti/Documents/workspace/AudioActive/84/gmm_db/GiacomoMameli.gmm");
		mscore.run();

		mscore.setGmm_model("/Users/labcontenuti/Documents/workspace/AudioActive/84/gmm_db/DanielaPieri.gmm");
		mscore.run();
		System.out.println("______________________________");
		mscore.getClusterResultSet().printAll();
	}
	public ClusterResultSet getClusterResultSet() {
		return clusterResultSet;
	}
	public void setClusterResultSet(ClusterResultSet clusterResultSet) {
		this.clusterResultSet = clusterResultSet;
	}
	public void run() throws Exception {
		try {
			SpkDiarizationLogger.setup();
			parameter =new Parameter();
			String[] parameterScoreIdent ={"","--sGender","--sByCluster","--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4","--sOutputFormat=seg,UTF8", 
	 				fInputMask, "--sTop=8,"+this.ubm_gmm,
	 				s_inputMaskRoot+baseName+".spl.3.seg", 
	 				s_outputMaskRoot+baseName+".g.3.seg",
	 				"--tInputMask="+gmm_model,
	 				"--sOutputMask="+outputRoot+"/"+baseName+".ident.M.GiacomoMameli.gmm.seg",
	 				show}; 		
	 		parameter.readParameters(parameterScoreIdent);
			if (parameter.show.isEmpty() == false) {
				// clusters
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				
				for(Cluster cluster: clusterSet.clusterSetValue()) {
		            //Iterate over segment of the cluster
		            for(Segment segment: cluster) {
		                // Iterate over feature of the segment
		                for(int i = 0; i < segment.getLength(); i++) {
		                    // Get a feature, ie a array of float
		                    float[] feature =   featureSet.getFeature(segment.getShowName(), segment.getStart()+i);
		                    for(int j = 0; j < feature.length; j++) {
		                        System.out.println(feature[j]);
		                    }
		                }
		            }
		        }
				
				GMMArrayList gmmTopGaussianList = MainTools.readGMMForTopGaussian(parameter, featureSet);
				GMMArrayList gmmList = MainTools.readGMMContainer(parameter);
				System.out.println("parameter.getParameterModelSetInputFile().getMask()" +parameter.getParameterModelSetInputFile().getMask());
				
				/*
				GMMArrayList gmmList = new GMMArrayList();
				String inputFilename = IOFile.getFilename(parameter.getParameterModelSetInputFile().getMask(), parameter.show);
				File inputFile = new File(inputFilename);
				IOFile inputFileReader = new IOFile(inputFilename, "rb");
				ModelIO.readerGMMContainer(inputFileReader, gmmList);
				inputFileReader.close();
				if (gmmList.size() > 0) {
					parameter.getParameterModel().setKind(gmmList.get(0).getGaussianKind());
					parameter.getParameterModel().setNumberOfComponents(gmmList.get(0).getNbOfComponents());
				}
				
				*/
				
				clusterSetResult = make(featureSet, clusterSet, gmmList, gmmTopGaussianList, parameter);
				MainTools.writeClusterSet(parameter, clusterSetResult, false);
			}
		} catch (DiarizationException e) {
			logger.log(Level.SEVERE, "error \t exception ", e);
			e.printStackTrace();
		}

	}
	public void run1() throws Exception {
		try {
			SpkDiarizationLogger.setup();
			parameter =new Parameter();
			String[] parameterScoreIdent ={"","--sGender","--sByCluster","--fInputDesc=audio2sphinx,1:3:2:0:0:0,13,1:1:300:4","--sOutputFormat=seg,UTF8", 
	 				fInputMask, "--sTop=8,"+this.ubm_gmm,
	 				s_inputMaskRoot+baseName+".spl.3.seg", 
	 				s_outputMaskRoot+baseName+".g.3.seg",
	 				"--tInputMask="+gmm_model+"/rb/",
	 				"--sOutputMask="+outputRoot+"/"+baseName+".ident.M.GiacomoMameli.gmm.seg",
	 				show}; 		
	 		parameter.readParameters(parameterScoreIdent);
			if (parameter.show.isEmpty() == false) {
				// clusters
				ClusterSet clusterSet = MainTools.readClusterSet(parameter);
				AudioFeatureSet featureSet = MainTools.readFeatureSet(parameter, clusterSet);
				GMMArrayList gmmTopGaussianList = MainTools.readGMMForTopGaussian(parameter, featureSet);
				GMMArrayList gmmList = MainTools.readGMMContainer(parameter);
				System.out.println("parameter.getParameterModelSetInputFile().getMask()" +parameter.getParameterModelSetInputFile().getMask());
				
				/*
				GMMArrayList gmmList = new GMMArrayList();
				String inputFilename = IOFile.getFilename(parameter.getParameterModelSetInputFile().getMask(), parameter.show);
				File inputFile = new File(inputFilename);
				IOFile inputFileReader = new IOFile(inputFilename, "rb");
				ModelIO.readerGMMContainer(inputFileReader, gmmList);
				inputFileReader.close();
				if (gmmList.size() > 0) {
					parameter.getParameterModel().setKind(gmmList.get(0).getGaussianKind());
					parameter.getParameterModel().setNumberOfComponents(gmmList.get(0).getNbOfComponents());
				}
				
				*/
				
				clusterSetResult = make(featureSet, clusterSet, gmmList, gmmTopGaussianList, parameter);
				MainTools.writeClusterSet(parameter, clusterSetResult, false);
			}
		} catch (DiarizationException e) {
			logger.log(Level.SEVERE, "error \t exception ", e);
			e.printStackTrace();
		}

	}


	/**
	 * Info.
	 * 
	 * @param parameter the parameter
	 * @param program the program
	 * @throws IllegalArgumentException the illegal argument exception
	 * @throws IllegalAccessException the illegal access exception
	 * @throws InvocationTargetException the invocation target exception
	 */
	public static void info(Parameter parameter, String program) throws IllegalArgumentException, IllegalAccessException, InvocationTargetException {
	}

	public Parameter getParameter() {
		return parameter;
	}

	public void setParameter(Parameter parameter) {
		this.parameter = parameter;
	}
	public String getGmm_model() {
		return gmm_model;
	}
	public void setGmm_model(String gmm_model) {
		this.gmm_model = gmm_model;
	}
	public ClusterSet getClusterSetResult() {
		return clusterSetResult;
	}
	public void setClusterSetResult(ClusterSet clusterSetResult) {
		this.clusterSetResult = clusterSetResult;
	}

}
