package it.crs4.identification;

import java.util.Hashtable;

public class ClusterResult {
	
	private String name=null;
	private Hashtable value=new Hashtable();
	
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Hashtable getValue() {
//		clusterResultSet		
		return value;
	}

	public void setValue(Hashtable value) {
		this.value = value;
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
