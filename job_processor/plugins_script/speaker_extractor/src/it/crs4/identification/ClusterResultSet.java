package it.crs4.identification;

import java.util.Arrays;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;
import java.util.Vector;



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
	public void printTheBestBySpeaker(){
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
				speaker.put( (String) cr.getValue().get(db_arr[ln-1]), tmp);
			}else{
				Vector<String> tmp=new Vector<String>();
				tmp.add(cr_it);
				speaker.put( (String) cr.getValue().get(db_arr[ln-1]), tmp);				
			}
			//System.out.println("score="+db_arr[ln-1] +" name="+cr.getValue().get(db_arr[ln-1])  );
		}
		Iterator<String> sp_it=speaker.keySet().iterator();
		while(sp_it.hasNext()){
			String key=(String)sp_it.next();
			System.out.println("name="+key);
			for(int i=0; i< ( (Vector) speaker.get(key) ).size();i++){
				System.out.println(" cluster="+( (Vector) speaker.get(key) ).get(i));
			}
		}
		
	}
	public void printWithThr(Double thr){
		System.out.println("------");
		Iterator<String> it=cluster.keySet().iterator();
		while(it.hasNext()){
			String cr_it=(String)it.next();
			System.out.println(cr_it);
			ClusterResult cr=(ClusterResult)cluster.get(cr_it);
			Object[] db_arr=cr.getValue().keySet().toArray();
			Arrays.sort(db_arr);
			int ln=db_arr.length;
			Double best=(Double)db_arr[ln-1];
			System.out.println("score="+db_arr[ln-1] +" name="+cr.getValue().get(db_arr[ln-1]));
			for(int i=ln-2;i>0;i--) {
				boolean res=((best.longValue()-((Double)db_arr[i]).longValue()))<thr.longValue() ;
				//System.out.println( "best="+(best.longValue() +"  score="  +((Double)db_arr[i]).longValue()+ " res="+ res));
				if ( (best.longValue()-((Double)db_arr[i]).longValue())>thr.longValue()){
					System.out.println("***score="+db_arr[i] +" name="+cr.getValue().get(db_arr[i]));
				}else{
					break;
				}
			}
		}
		
	}

}
