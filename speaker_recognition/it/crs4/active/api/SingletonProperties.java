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

package it.crs4.active.api;

import it.crs4.util.PropertiesReader;

/**
 * This class is used to read the configuration stored in the configuration file and 
 * Converts the configuration encapsulate in a configuration file to the Properties-style format.
 The default configuration file is the <i>/var/configuration.properties</i>
 * <br> Refer the <i>it.crs4.util.PropertiesReader</i> for details.
 * 
 * <strong>Configuration file: an example</strong>
 * An example of configuration file is:
 * <code>
 * 			   <br><br> the path of the wav audio file to be processed
 *             <br>fileName=/Users/example.wav
 *             
 *             <br><br>the location of intermediate build files<br>
 *             outputRoot=/Users/out/
 *             
 *             <br><br>The path of the ubm.gmm file
 *             <br>ubm_gmm=/Users/ubm.gmm
 *             
 *             <br><br>The location of the sms.gmms file
 *             <br>sms_gmms=/Users/sms.gmms
 *             
 *             <br><br>The path of the models file
 *             <br>db_path=/Users/db_path/  
 *             
 *             <br><br>The name of generated model<br>
 *             gmmName=exampleName
 *             
 *             <br><br>The location of generated model <br>modelDir=/Users/audio_model/
 </code>
 * 
 * @author Felice Colucci
 *
 */
	class Singleton{
		  
		private static Singleton singletonObject;
		
		/** A private Constructor prevents any other class from instantiating. */
		private Singleton(){
			  
		}
		
		/**
		 * Default configuration encapsulated in <i>/var/configuration.properties</i>
		 * */
		public static synchronized PropertiesReader getProperties(){
			return new PropertiesReader("/var/configuration.properties");
		} 
		
		/**
		 * Sets the configuration encapsulated in <i>configuration</i> file
		 * @param the path of configuration file 
		 * */		
		public static synchronized PropertiesReader getProperties(String configuration){
			return new PropertiesReader(configuration);
		} 		
		
		public static synchronized Singleton getSingletonObject()
		{
		    if (singletonObject == null){
		    	singletonObject = new Singleton();
		    }
		    return singletonObject;
		}
		
		public Object clone() throws CloneNotSupportedException
		{
		    throw new CloneNotSupportedException(); 
		}
			  
	}
	/**
	 * Singleton class for properties
	 * */
	public class SingletonProperties {

		/* (non-Javadoc)
		 * @see java.lang.Object#toString()
		 */
		@Override
		public String toString() {
			return "SingletonProperties [getClass()=" + getClass()
					+ ", hashCode()=" + hashCode() + ", toString()="
					+ super.toString() + "]";
		}

		public static void main(String args[]){
			Singleton obj = Singleton.getSingletonObject();
			System.out.println("Singleton object obtained");
			
		}
	}



