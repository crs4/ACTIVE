/**
 * 
 */
package it.crs4.active.api;

import it.crs4.util.PropertiesReader;

/**
 * @author Felice Colucci
 *
 */

	class Singleton{
		  
		private static Singleton singletonObject;
		
		/** A private Constructor prevents any other class from instantiating. */
		private Singleton(){
			  
		}
		public static synchronized PropertiesReader getProperties(){
			
			return new PropertiesReader("configuration.properties");
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

			// Your Business Logic
			System.out.println("Singleton object obtained");
			
		}
	}



