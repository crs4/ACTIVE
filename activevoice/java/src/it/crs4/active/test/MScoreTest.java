/**
 * 
 */
package it.crs4.active.test;

import static org.junit.Assert.*;
import it.crs4.identification.ClusterResultSet;
import it.crs4.identification.MScore;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

/**
 * @author labcontenuti
 *
 */
public class MScoreTest {
	MScore mscore=new MScore();
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
	 * Test method for {@link it.crs4.identification.MScore#getBaseName()}.
	 */
	@Test
	public final void testGetBaseName() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#setBaseName(java.lang.String)}.
	 */
	@Test
	public final void testSetBaseName() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#writeIdentSegFile()}.
	 */
	@Test
	public final void testWriteIdentSegFile() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#MScore()}.
	 */
	@Test
	public final void testMScore() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#printTheBestBySpeaker()}.
	 */
	@Test
	public final void testPrintTheBestBySpeaker() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#printTheBestByThr(long)}.
	 */
	@Test
	public final void testPrintTheBestByThr() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#getFileName()}.
	 */
	@Test
	public final void testGetFileName() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#setFileName(java.lang.String)}.
	 */
	@Test
	public final void testSetFileName() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#getOutputRoot()}.
	 */
	@Test
	public final void testGetOutputRoot() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#setOutputRoot(java.lang.String)}.
	 */
	@Test
	public final void testSetOutputRoot() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#getUbm_gmm()}.
	 */
	@Test
	public final void testGetUbm_gmm() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#setUbm_gmm(java.lang.String)}.
	 */
	@Test
	public final void testSetUbm_gmm() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#getSms_gmms()}.
	 */
	@Test
	public final void testGetSms_gmms() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#setSms_gmms(java.lang.String)}.
	 */
	@Test
	public final void testSetSms_gmms() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#make(fr.lium.spkDiarization.libFeature.AudioFeatureSet, fr.lium.spkDiarization.libClusteringData.ClusterSet, fr.lium.spkDiarization.libModel.gaussian.GMMArrayList, fr.lium.spkDiarization.libModel.gaussian.GMMArrayList, fr.lium.spkDiarization.parameter.Parameter)}.
	 */
	@Test
	public final void testMake() {
		fail("Not yet implemented"); // TODO
	}
	
	/**
	 * Test method for {@link it.crs4.identification.MScore#isName(java.lang.String)}.
	 */
	@Test
	public final void testIsName() {
		//fail("Not yet implemented"); // TODO
		assertFalse(mscore.isName("s1"));
	}
	@Test
	public final void testIsName_2() {
		//fail("Not yet implemented"); // TODO
		assertFalse(mscore.isName("s11111"));
	}
	@Test
	public final void testIsName_3() {
		//fail("Not yet implemented"); // TODO
		assertFalse(mscore.isName("S11111"));
	}
	@Test
	public final void testIsName_4() {
		//fail("Not yet implemented"); // TODO
		assertTrue(mscore.isName("SandroLombardi"));
	}
	public final void testIsName_5() {
		//fail("Not yet implemented"); // TODO
		assertTrue(mscore.isName("SandroLombardi1"));
	}
	/**
	 * Test method for {@link it.crs4.identification.MScore#main(java.lang.String[])}.
	 */
	@Test
	public final void testMain() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#getClusterResultSet()}.
	 */
	@Test
	public final void testGetClusterResultSet() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#setClusterResultSet(it.crs4.identification.ClusterResultSet)}.
	 */
	@Test
	public final void testSetClusterResultSet() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#run()}.
	 */
	@Test
	public final void testRun() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#info(fr.lium.spkDiarization.parameter.Parameter, java.lang.String)}.
	 */
	@Test
	public final void testInfo() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#getParameter()}.
	 */
	@Test
	public final void testGetParameter() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#setParameter(fr.lium.spkDiarization.parameter.Parameter)}.
	 */
	@Test
	public final void testSetParameter() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#getGmm_model()}.
	 */
	@Test
	public final void testGetGmm_model() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#setGmm_model(java.lang.String)}.
	 */
	@Test
	public final void testSetGmm_model() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#getClusterSetResult()}.
	 */
	@Test
	public final void testGetClusterSetResult() {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link it.crs4.identification.MScore#setClusterSetResult(fr.lium.spkDiarization.libClusteringData.ClusterSet)}.
	 */
	@Test
	public final void testSetClusterSetResult() {
		fail("Not yet implemented"); // TODO
	}

}
