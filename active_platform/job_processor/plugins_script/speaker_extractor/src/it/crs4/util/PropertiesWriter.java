package it.crs4.util;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;


public class PropertiesWriter {
    	private  String configProperties=null;

	    private  String fileProperties=null;


	      /**
	       * <br><b>public static synchronized String getString(String key) </b><br><hr>
	       * QUESTO METODO PERMETTE DI RECUPERARE UN VALORE DAL FILE CONFIG.PROPERTIES
	       *  
	       * <br><b>ReadOnly</b><br>
	       * @param pKey DI TIPO STRING
	     * @return VALORE DI KEY SE PRESENTE - ALTRIMENTI STRINGA VUOTA
	     * 
	     */
	      public  synchronized String getString(String pKey) {
	          String myReturn="";
	          Properties props = new Properties();

	          try {
	              props.load(new FileInputStream(fileProperties));
	              myReturn = props.getProperty(pKey);
	          } catch(IOException e) {
	          }
	          return myReturn ;

	      }
	      
	    /**
	     * <br><b>public static synchronized void  setProperty(String key, String value)</b><br><hr>
	     * QUESTO METODO PERMETTE DI SCRIVERE UN VALORE NEL FILE CONFIG.PROPERTIES
	     *  
	     * <br><b>WriteOnly</b><br>
	     * @param pKey DI TIPO STRING - RAPPRESENTA LA CHIAVE DA INSERIRE
	     * @param pValue DI TIPO STRING - RAPPRESENTA IL VALORE CHE SI VUOLE ATTRIBUIRE ALLA CHIAVE
	     * 
	     * 
	     */
	      public  synchronized void  setProperty(String pKey, String pValue)  {
	          Properties properties = new Properties();
	          try {
	              properties.load(new FileInputStream(configProperties));
	              properties.setProperty(pKey, pValue);
	            } catch (IOException e) {
	                System.out.println("ERRORE NELLA LETTURA DEL FILE: " + fileProperties + "\nERRORE: " + e.getMessage());
	            }
	            try {
	                properties.store(new FileOutputStream(fileProperties), null);
	            } catch (IOException e) {
	                 System.out.println("ERRORE NEL SALVATAGGIO DEL FILE " + fileProperties + "\nERRORE: " + e.getMessage());
	            }
	    }
	    
	    public void rewritePropertiesFrom(String settings){
			PropertiesReader pr=new PropertiesReader(settings);
			for(String p : pr.getAllPropertyNames() ){
				System.out.println(p +"="+pr.getProperty(p));
				setProperty(p, pr.getProperty(p));
			}
	    	
	    }  
	      
	  	public static void main(String[] args) {
	 
	  		PropertiesWriter pv=new PropertiesWriter();
	  		pv.setConfigProperties(args[0]);
	  		pv.setFileProperties(args[1]);
	  		//pv.rewritePropertiesFrom(pv.getConfigProperties());
	  		//
	  		String key_val=args[2];
	  		for (String listKV : key_val.split(";")){
	  			pv.setProperty(listKV.split("=")[0], listKV.split("=")[1]);
	  			
	  		}
	  	}

		public String getFileProperties() {
			return fileProperties;
		}

		public void setFileProperties(String fileProperties) {
			this.fileProperties = fileProperties;
		}

		public String getConfigProperties() {
			return configProperties;
		}

		public void setConfigProperties(String configProperties) {
			this.configProperties = configProperties;
		};
	}