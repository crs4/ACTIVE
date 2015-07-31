/**
 * This package perform these phases: feature extraction and model creation
 * The goal of this package is to create a model (a gmm file) of a given person.
 * <br />
 * <strong> Example </strong>
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
 *  */

package it.crs4.active.train;
