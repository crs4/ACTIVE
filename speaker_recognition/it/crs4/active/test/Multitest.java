
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
 * */package it.crs4.active.test;

import it.crs4.util.PropertiesReader;

import java.io.File;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Set;

/**
 * @author Felice Colucci
 *
 */
public class Multitest {
	private Set<Hashtable> info=new HashSet();
	/**
	 * @return the info
	 */
	public Set<Hashtable> getInfo() {
		return info;
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		Multitest multitest=new Multitest();
		PropertiesReader pr=new PropertiesReader(args[0]);
		Set<String> setProp=pr.getAllPropertyNames();
		Iterator<String> setPropIt=setProp.iterator();
		while(setPropIt.hasNext()){
			TestSingle testSingle=new TestSingle();
			testSingle.runPrpperties(setPropIt.next());
			multitest.getInfo().add(testSingle.getInfo());
		}
	}
	public void run1(File[] listProperties) {
		String[] listS=new String[listProperties.length];
		for(int i=0;i<listProperties.length;i++){
			listS[i]=listProperties[i].getAbsolutePath();
		}
		run1(listS);
	}
	public void run1(String[] listProperties) {
		for(int i=0;i<listProperties.length;i++){
			PropertiesReader pr=new PropertiesReader(listProperties[i]);
			Set<String> setProp=pr.getAllPropertyNames();
			Iterator<String> setPropIt=setProp.iterator();
			while(setPropIt.hasNext()){
				TestSingle testSingle=new TestSingle();
				testSingle.runPrpperties(setPropIt.next());
				getInfo().add(testSingle.getInfo());
			}
		}
	}
	
	public void report(){
		int ok=0;
		int error=0;
		Iterator<Hashtable> infoIt=info.iterator();
		while(infoIt.hasNext()){
			Hashtable<String, Object> info=(Hashtable<String, Object>)infoIt.next();
			System.out.println("------------\n\n");
			System.out.println(info.get(TestSingle.PROPERTIES));
			System.out.println(info.get(TestSingle.VERIFY));
			if(info.get(TestSingle.VERIFY).equals(TestSingle.VERIFYOK)){
				ok=ok+1;
			}else{
				error=error+1;
			}
			System.out.println("------------\n\n-------------- TOTAL --------------");
			System.out.println(" OK "+ok );
			System.out.println(" ERROR "+error );
		}
		
	}

}
