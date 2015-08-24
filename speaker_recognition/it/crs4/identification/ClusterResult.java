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

import java.util.Hashtable;
/**
 * This class encapsulate the result of a single cluster
 * */
public class ClusterResult {
	
	
	private String name=null;
	private Hashtable value=new Hashtable();
	
	
	/**
	 * Returns the name of the cluster
	 * */
	public String getName() {
		return name;
	}

	
	/**
	 * Sets the name of the cluster
	 * @param name: the identification of the cluster
	 * */	
	public void setName(String name) {
		this.name = name;
	}

	
	/**
	 * Returns the result of the identification process for this cluster
	 * */
	public Hashtable getValue() {
		return value;
	}
	
	/**
	 * Sets the result of the identification process for this cluster
	 * */
	public void setValue(Hashtable value) {
		this.value = value;
	}

	
	/**
	 * Sets the result of the identification process for this cluster
	 * 
	 * @param key: the key
	 * @param value: the value
	 * */
	public void setValueIstance(Object key, Object value) {
		this.value.put(key, value);
	}	
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
