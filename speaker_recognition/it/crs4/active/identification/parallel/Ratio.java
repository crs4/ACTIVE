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
package it.crs4.active.identification.parallel;

import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

public class Ratio {
	private Map<Double, Object> unsortMap=new HashMap<Double, Object>();
	private Map<Double, Object> ascSortedMap =null;
	/**
	 * The main method.
	 *
	 * @param args the arguments
	 */
	public static void main(String[] args) {
		Ratio ratio=new Ratio();
		//creating unsorted map of employee id as a key and employee name as a value
		Map<Double, Object> unsortMap= ratio.getUnsortMap();//new HashMap<Double, String>();
		unsortMap.put(-33.7202646529298, "Ashraf");
		unsortMap.put(-33.72024, "Sara");
		unsortMap.put(-32.720, "Mohamed");
		unsortMap.put(-30.7202646529298, "Esraa");
		unsortMap.put(-33.72026462, "Bahaa");
		unsortMap.put(-35.7202646529298, "Dalia");
		unsortMap.put(-36.7202646529298, "Amira");

		System.out.println("Unsort Map......");
		ratio.printMap(ratio.getUnsortMap() );
		ratio.run();
	};
	
	public void run(){
		try{
		// Using the default natural ordering of sorted map Integer key which implement Comparable interface
		
		ascSortedMap = new TreeMap<Double, Object>();
		ascSortedMap.putAll(unsortMap);
		//printMap(ascSortedMap);

		// Forcing the descending order by creating our own comparator then passing it to the sorted map at creation time
		
		Map<Double, Object> desSortedMap = new TreeMap<Double, Object>(
				new Comparator<Double>() {

					@Override
					public int compare(Double o1, Double o2) {
						return o2.compareTo(o1);
					}

				});
		desSortedMap.putAll(unsortMap);
		//System.out.println(" --- all map---" );
		//printMap(desSortedMap);
		}catch(Exception ex){
			ex.printStackTrace();
		}
	}

	/**
	 * Prints the map.
	 *
	 * @param map the map
	 */
	public void printMap(Map<Double, Object> map) {
		for (Map.Entry<Double, Object> entry : map.entrySet()) {
			System.out.println("Key : " + entry.getKey() + " Value : "
					+ entry.getValue());
		}
	}
	public void printMapStringArray(Map<Double, String[]> map) {
		for (Map.Entry<Double, String[]> entry : map.entrySet()) {
			System.out.println("Key : " + entry.getKey() + " Value : "
					+ entry.getValue()[0]+"|"+entry.getValue()[1]+"|"+entry.getValue()[2]);
		}
	}	
	/**
	 * Prints the best
	 *
	 * @param map the map
	 */
	public void printBest(Map<Double, String> map, int best) {
		int index=0;
		for (Map.Entry<Double, String> entry : map.entrySet()) {
			System.out.println("Key : " + entry.getKey() + " Value : "
					+ entry.getValue());
			index=index+1;
			if (index>best) return;
		}
	}	

	public Map<Double, Object> getUnsortMap() {
		return unsortMap;
	}

	public void setUnsortMap(Map<Double, Object> unsortMap) {
		this.unsortMap = unsortMap;
	}

}
