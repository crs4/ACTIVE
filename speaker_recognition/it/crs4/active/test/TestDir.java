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
package it.crs4.active.test;

import java.io.File;
import java.io.FilenameFilter;
import java.util.Set;

public class TestDir {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		TestDir testdir=new TestDir();
		String folder = "/Users/labcontenuti/Documents/workspace/AudioActive/84/test_file/properties";
		testdir.listFilesForFolder(folder);
	}
	public Set<String> getAllPropertiesFiles(String dir){
		
		return null;
	}
	public void listFilesForFolder(String folder) {
        System.out.println("listFilesForFolder");
        File[] listFiles=findFiles(folder, "properties");
        
	    
	}
	private static File[] findFiles(String dir, String ext) {
        File file = new File(dir);
        if(!file.exists()) System.out.println(dir + " Directory doesn't exists");
        File[] listFiles = file.listFiles(new MyFileNameFilter(ext));
        if(listFiles.length ==0){
            System.out.println(dir + "doesn't have any file with extension "+ext);
        }else{
            for(File f : listFiles)
                System.out.println("File: "+dir+File.separator+f.getName());
        }
        return listFiles;
    }
 
    //FileNameFilter implementation
    public static class MyFileNameFilter implements FilenameFilter{
         
        private String ext;
         
        public MyFileNameFilter(String ext){
            this.ext = ext.toLowerCase();
        }
        @Override
        public boolean accept(File dir, String name) {
            return name.toLowerCase().endsWith(ext);
        }
         
    }
}
