package it.crs4.active.testsuite;

import static org.junit.Assert.*;

import java.io.FileNotFoundException;

import it.crs4.active.diarization.Diarization;
import it.crs4.util.PropertiesReader;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

public class DiarizationTest {

	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
	}

	@AfterClass
	public static void tearDownAfterClass() throws Exception {
	}

	@Before
	public void setUp() throws Exception {

	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public final void testGetPropertiesReader() {
		
		try {
			PropertiesReader pr=new PropertiesReader("/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Mameli-Lombardi-2minuti.properties");
			Diarization dia=new Diarization();
			dia.setPropertiesReader(pr);
			assertEquals(dia.getPropertiesReader(), pr);
		} catch (Exception e) {
			System.out.println(" properties file not foud");
			//e.printStackTrace();
		}
	}

	@Test
	public final void testSetPropertiesReader() {
		
		try {
			PropertiesReader pr=new PropertiesReader("/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/Mameli-Lombardi-2minuti.properties");
			Diarization dia=new Diarization();
			dia.setPropertiesReader(pr);
			assertEquals(dia.getPropertiesReader(), pr);
		} catch (Exception e) {
			System.out.println(" properties file not foud");
			//e.printStackTrace();
		}
	}

	@Test
	public final void testGetFileName() {	     
		Diarization dia=new Diarization();
		String filename="test";
		dia.setFileName(filename);
		assertEquals(dia.getFileName(), filename);
	}


	@Test
	public final void testGetParameter() {
		Diarization dia=new Diarization();
		String filename="test";
		dia.setFileName(filename);
		assertEquals(dia.getFileName(), filename);
	}

	@Test
	public final void testSetParameter() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testGetParameter_path() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testSetParameter_path() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testDiarizationPropertiesReader() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testDiarizationString() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testDiarization() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testSetFileName() {
		Diarization dia=new Diarization();
		String filename="test";
		dia.setFileName(filename);
		assertEquals(dia.getFileName(), filename);
	}

	@Test
	public final void testGetOutputRoot() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testSetOutputRoot() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testConfigureParameter() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testRunSegInit() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testRunAMCLust() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testRun() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testGetUbm_gmm() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testSetUbm_gmm() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testGetSms_gmms() {
		fail("Not yet implemented"); // TODO
	}

	@Test
	public final void testSetSms_gmms() {
		fail("Not yet implemented"); // TODO
	}

}
