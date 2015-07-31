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

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.Arrays;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;
import java.util.Vector;


/**
 * This class encapsulate the results of a cluster process
 * */
public class ClusterResultSet {
@Override
protected Object clone() throws CloneNotSupportedException {
	// TODO Auto-generated method stub
	return super.clone();
}
	private Hashtable cluster=new Hashtable();
	public Hashtable getCluster() {
		return cluster;
	}
	private void setCluster(Hashtable cluster) {
		this.cluster = cluster;
		
	}
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}
	public void put(ClusterResult cr){
		if (cluster.containsKey( cr.getName() )){
			ClusterResult tmp=(ClusterResult)cluster.get(cr.getName());
			tmp.getValue().put(cr.getName(), cr);
			cluster.put(cr.getName(), tmp);
		}else{
			cluster.put(cr.getName(), cr);
		}
	}
	public void putValue(String clusterName, String gmmName, Double score){
		if(cluster.containsKey(clusterName)){
			ClusterResult tmp=(ClusterResult)cluster.get(clusterName);
			tmp.getValue().put(score, gmmName);
			cluster.put(clusterName, tmp);
		}else{
			ClusterResult cs=new ClusterResult();
			cs.getValue().put(score, gmmName);
			cluster.put(clusterName, cs);
		}
		
	}
	public void printAll(){
		System.out.println("------");
		Iterator<String> it=cluster.keySet().iterator();
		while(it.hasNext()){
			String cr_it=(String)it.next();
			System.out.println(cr_it);
			
			ClusterResult cr=(ClusterResult)cluster.get(cr_it);
			Object[] db_arr=cr.getValue().keySet().toArray();
			Arrays.sort(db_arr);
			//for(Object t : cr.getValue().keySet().toArray()) {
			for(Object t : db_arr) {
				System.out.println("score="+t +" name="+cr.getValue().get(t));
			}
			Iterator cr_key=cr.getValue().keySet().iterator();
			//System.out.println(cr.getValue());
			/*
			while(cr_key.hasNext()){
				Double db=(Double)cr_key.next();
				System.out.println(db+" "+cr.getValue().get(db));
				
			}
			*/
		}
		
	}
	public void printTheBest(){
		System.out.println("------THE BEST------");
		Iterator<String> it=cluster.keySet().iterator();
		while(it.hasNext()){
			String cr_it=(String)it.next();
			System.out.println(cr_it);
			ClusterResult cr=(ClusterResult)cluster.get(cr_it);
			Object[] db_arr=cr.getValue().keySet().toArray();
			Arrays.sort(db_arr);
			int ln=db_arr.length;
			System.out.println("score="+db_arr[ln-1] +" name="+cr.getValue().get(db_arr[ln-1]));
		}
		
	}
	public boolean isName(String name){
		boolean result=true;
		name=name.trim();
		name=name.toLowerCase();
		if(name.startsWith("s")){
			name=name.replaceFirst("s", "");
			if(name.matches("-?\\d+(\\.\\d+)?")){
				result=false;
			}
		}
		return result;
	}
	public String printTheBestBySpeaker(){
		System.out.println("------THE BEST BY SPEAKERil------");
		
		Iterator<String> it=cluster.keySet().iterator();
		Hashtable<String, Vector> speaker=new Hashtable<String, Vector>();
		while(it.hasNext()){
			String cr_it=(String)it.next();
			//System.out.println(cr_it);
			ClusterResult cr=(ClusterResult)cluster.get(cr_it);
			Object[] db_arr=cr.getValue().keySet().toArray();
			Arrays.sort(db_arr);
			int ln=db_arr.length;
			if ( speaker.keySet().contains( (String) cr.getValue().get(db_arr[ln-1]))  ){
				Vector<String> tmp= speaker.get(cr.getValue().get(db_arr[ln-1]));
				
				tmp.add( cr_it );
				
				System.out.println("Cluster RESULT SET adding "+cr_it+" with score "+db_arr[ln-1]);
				speaker.put( (String) cr.getValue().get(db_arr[ln-1]), tmp);
				
			}else{
				Vector<String> tmp=new Vector<String>();
				tmp.add(cr_it);
				
				System.out.println("Cluster RESULT SET adding "+cr_it);
				speaker.put( (String) cr.getValue().get(db_arr[ln-1]), tmp);
				
			}
			//System.out.println("score="+db_arr[ln-1] +" name="+cr.getValue().get(db_arr[ln-1])  );
		}
		Iterator<String> sp_it=speaker.keySet().iterator();
		String nomiPresenti="\n";
		while(sp_it.hasNext()){
			String key=(String)sp_it.next();
			System.out.println("name="+key);
			if(1==1){//isName(key)){
				nomiPresenti=nomiPresenti+key;
				for(int i=0; i< ( (Vector) speaker.get(key) ).size();i++){
					System.out.println(" cluster="+( (Vector) speaker.get(key) ).get(i) );
					nomiPresenti=nomiPresenti+" "+((Vector) speaker.get(key) ).get(i);
				}
				nomiPresenti=nomiPresenti+"\n";
			}
		}
		return nomiPresenti;
		
	}
	public void printWithThr(Double thr){
		System.out.println("------");
		Iterator<String> it=cluster.keySet().iterator();
		while(it.hasNext()){
			String cr_it=(String)it.next();
			System.out.println("\n\n"+cr_it);
			ClusterResult cr=(ClusterResult)cluster.get(cr_it);
			Object[] db_arr=cr.getValue().keySet().toArray();
			Arrays.sort(db_arr);
			int ln=db_arr.length;
			Double best=(Double)db_arr[ln-1];
			System.out.println("score="+db_arr[ln-1] +" name="+cr.getValue().get(db_arr[ln-1]));
			for(int i=ln-2;i>0;i--) {
				double diff=best.doubleValue()-((Double)db_arr[i]).doubleValue();
				System.out.println("diff "+diff) ;
				boolean res=diff>thr.doubleValue() ;
				System.out.println( "best="+best+"--db_arr[i]="+(Double)db_arr[i]+"--- diff="+diff) ;
				//System.out.println( "best="+(best.longValue() +"  score="  +((Double)db_arr[i]).longValue()+ " res="+ res));
				//if ( (best.longValue()-((Double)db_arr[i]).longValue())>thr.longValue()){
				if(res){
					System.out.println("***score="+db_arr[i] +" name="+cr.getValue().get(db_arr[i]));
				}else{
					System.out.println(".");
					break;
				}
			}
		}
		
	}

	public void printWithThr1e2(Double thr){
		System.out.println("------");
		Iterator<String> it=cluster.keySet().iterator();
		while(it.hasNext()){
			String cr_it=(String)it.next();
			System.out.println("\n\n"+cr_it);
			ClusterResult cr=(ClusterResult)cluster.get(cr_it);
			Object[] db_arr=cr.getValue().keySet().toArray();
			Arrays.sort(db_arr);
			int ln=db_arr.length;
			if (ln>2){
				Double best=(Double)db_arr[ln-1];
				Double best2=(Double)db_arr[ln-2];
				System.out.println("score best="+db_arr[ln-1] +" name="+cr.getValue().get(db_arr[ln-1]));
				System.out.println("score second="+db_arr[ln-2] +" name="+cr.getValue().get(db_arr[ln-2]));
				double diff=best.doubleValue()-best2.doubleValue();
				System.out.println("diff "+diff);
				boolean res=diff<thr.doubleValue() ;
				System.out.println( "best="+best+"--second="+best2+"--- diff="+diff) ;
				if(res){
						System.out.println("*** vicino="+cr.getValue().get(db_arr[ln-2]));
				}
			}
		}
	}	
	
}
