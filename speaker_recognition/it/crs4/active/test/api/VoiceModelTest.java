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

package it.crs4.active.test.api;

import static org.junit.Assert.*;

import java.io.File;

import it.crs4.active.api.VoiceModel;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

/**
 * Build a model by the file <i>filename</i> defined in the configuration file. 
 * The model is saved in <i>modelDir</i> directory defined in the configuration file.
 * The name of the model is <i>gmmName</i> defined in the configuration file.
 * @author Felice Colucci
 *
 */
public class VoiceModelTest {
	String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
	/**
	 * @throws java.lang.Exception
	 */
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
	}

	/**
	 * @throws java.lang.Exception
	 */
	@AfterClass
	public static void tearDownAfterClass() throws Exception {
	}

	/**
	 * @throws java.lang.Exception
	 */
	@Before
	public void setUp() throws Exception {
	}

	/**
	 * @throws java.lang.Exception
	 */
	@After
	public void tearDown() throws Exception {
	}



	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#VoiceModel()}.
	 */
	@Test
	public final void testVoiceModel() {
		VoiceModel vm=new VoiceModel();
		assertNotNull("", vm.propertiesReader);
	}

	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#VoiceModel(java.lang.String)}.
	 */
	@Test
	public final void testVoiceModelString() {
		VoiceModel vm=new VoiceModel(configuration);
		assertNotNull("", vm.propertiesReader);
	}

	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#init()}.
	 */
	@Test
	public final void testInit() {
		VoiceModel vm=new VoiceModel();
		vm.propertiesReader=null;
		vm.init();
		assertNotNull("", vm.propertiesReader);

	}

	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#addVoice(java.lang.String, java.lang.String)}.
	 */
	@Test
	public final void testAddVoiceStringString() {
		VoiceModel vm=new VoiceModel();
		vm.propertiesReader=null;
		vm.init(configuration);
		assertNotNull("", vm.propertiesReader);
	}

	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#addVoice(java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String)}.
	 */
	@Test
	public final void testAddVoiceStringStringStringStringStringString() {
		String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
		String tag="provaremo";
		VoiceModel voicemodel=new VoiceModel(configuration);
		String	filename=voicemodel.propertiesReader.getProperty("fileName");
		String	outputRoot=voicemodel.propertiesReader.getProperty("outputRoot");
		String	sms_gmms=voicemodel.propertiesReader.getProperty("sms_gmms");
		String	ubm_gmm=voicemodel.propertiesReader.getProperty("ubm_gmm");
		String	gmmRoot=voicemodel.propertiesReader.getProperty("gmmRoot");
		voicemodel.addVoice(filename, tag, outputRoot, sms_gmms, ubm_gmm, gmmRoot);
		File f=new File(gmmRoot+"/"+tag+".gmm");
		assertTrue(f.exists());
	}

	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#addVoice(java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String)}.
	 */
	@Test
	public final void testAddVoiceStringStringStringStringStringString4() {
		String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
		String tag="provaremo";
		VoiceModel voicemodel=new VoiceModel(configuration);
		String	filename=voicemodel.propertiesReader.getProperty("fileName");
		String	outputRoot=voicemodel.propertiesReader.getProperty("outputRoot");
		String	sms_gmms=voicemodel.propertiesReader.getProperty("sms_gmms");
		String	ubm_gmm=voicemodel.propertiesReader.getProperty("ubm_gmm");
		voicemodel.addVoice(filename, tag, outputRoot, sms_gmms, ubm_gmm, null);
		File f=new File(outputRoot+"/"+tag+".gmm");
		assertTrue(f.exists());
	}

	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#addVoice(java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String)}.
	 */
	@Test
	public final void testAddVoiceStringStringStringStringStringString3() {
		String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
		String tag="provaremo";
		VoiceModel voicemodel=new VoiceModel(configuration);
		String	filename=voicemodel.propertiesReader.getProperty("fileName");
		String	outputRoot=voicemodel.propertiesReader.getProperty("outputRoot");
		String	sms_gmms=voicemodel.propertiesReader.getProperty("sms_gmms");
		String	gmmRoot=voicemodel.propertiesReader.getProperty("gmmRoot");
		voicemodel.addVoice(filename, tag, outputRoot, sms_gmms, null, gmmRoot);
		File f=new File(gmmRoot+"/"+tag+".gmm");
		assertTrue(f.exists());
	}
	
	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#addVoice(java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String)}.
	 */
	@Test
	public final void testAddVoiceStringStringStringStringStringString2() {
		String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
		String tag="provaremo";
		VoiceModel voicemodel=new VoiceModel(configuration);
		String	filename=voicemodel.propertiesReader.getProperty("fileName");
		String	outputRoot=voicemodel.propertiesReader.getProperty("outputRoot");
		String	ubm_gmm=voicemodel.propertiesReader.getProperty("ubm_gmm");
		String	gmmRoot=voicemodel.propertiesReader.getProperty("gmmRoot");
		voicemodel.addVoice(filename, tag, outputRoot, null, ubm_gmm, gmmRoot);
		File f=new File(gmmRoot+"/"+tag+".gmm");
		assertTrue(f.exists());
	}
	
	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#addVoice(java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String)}.
	 */
	@Test
	public final void testAddVoiceStringStringStringStringStringString1() {
		String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
		String tag="provaremo";
		VoiceModel voicemodel=new VoiceModel(configuration);
		String	filename=voicemodel.propertiesReader.getProperty("fileName");
		String	sms_gmms=voicemodel.propertiesReader.getProperty("sms_gmms");
		String	ubm_gmm=voicemodel.propertiesReader.getProperty("ubm_gmm");
		String	gmmRoot=voicemodel.propertiesReader.getProperty("gmmRoot");
		voicemodel.addVoice(filename, tag, null, sms_gmms, ubm_gmm, gmmRoot);
		File f=new File(gmmRoot+"/"+tag+".gmm");
		assertTrue(f.exists());
	}
	
	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#addVoices(java.lang.String[], java.lang.String[])}.
	 */
	@Test
	public final void testAddVoices() {
		String configuration="/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Remo_Bodei##1min.properties";
		String filename="/Users/labcontenuti/Music/Bodei/Remo_Bodei##1min-2.wav";
		String[] filenames=new String[]{filename,filename};
		String[] tags=new String[]{"provaremo","provareo1"};
		VoiceModel voicemodel=new VoiceModel(configuration);
		voicemodel.addVoices(filenames, tags);
	}

	/**
	 * DiarizationExample method for {@link it.crs4.active.api.VoiceModel#renameTag(java.lang.String, java.lang.String)}.
	 */
	@Test
	public final void testRenameTag() {
		fail("Not yet implemented"); // TODO
	}

}
