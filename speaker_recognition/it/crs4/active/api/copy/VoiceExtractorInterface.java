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
package it.crs4.active.api.copy;

import java.util.List;
import java.util.Set;

public interface VoiceExtractorInterface {

	/**
	 * Initialize the voice extractor.
	    The configuration parameters define and customize the voice extraction algorithm.
	    If any of the configuration parameters is not provided a default value is used.
	
	    @param voice_models: the voice models data structure
	    @param params: configuration parameters 
	 * 
	 * */
	public abstract void init();

	/**
	    Launch the voice extractor on one audio resource.
		@return file_name_path: the path of the file of the resulting name
	    @param resource_path: resource file path
	 * */
	public abstract String extractVoicesFromAudio(String resource_path,
			String save_as);
	
	/**
	 * Returns the speakers extracted from the audio
	 * */
	public abstract Set<String> getSpeakers();
	
}