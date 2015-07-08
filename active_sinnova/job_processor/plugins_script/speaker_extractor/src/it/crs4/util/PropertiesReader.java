package it.crs4.util;

import java.io.IOException;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.Properties;
import java.util.Set;
 

public class PropertiesReader {

	   private Properties configProp = null;
	    
	   public PropertiesReader(String propertiesFile)
	   {
		   try {
		   FileInputStream in = new FileInputStream(propertiesFile);// this.getClass().getClassLoader().getResourceAsStream(propertiesFile);
	      System.out.println(in);
	      configProp=new Properties();
	      System.out.println(configProp);
	      System.out.println("Read all properties from file");
	      
	          configProp.load(in);
	      } catch (IOException e) {
	          e.printStackTrace();
	      }
	   }
	   public static void main(String[] args)
	   {
		 PropertiesReader pr=new PropertiesReader("/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties/2sec.properties");
	     System.out.println(pr.getProperty("fileName"));
	     System.out.println(pr.getProperty("outputRoot"));
	      
	     //All property names
	     System.out.println(pr.getAllPropertyNames());
	   }
	 

	    
	   public String getProperty(String key){
	      return configProp.getProperty(key);
	   }
	    
	   public Set<String> getAllPropertyNames(){
	      return configProp.stringPropertyNames();
	   }
	    
	   public boolean containsKey(String key){
	      return configProp.containsKey(key);
	   }
	}