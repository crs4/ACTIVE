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

public interface VoiceModelInterface {

	/**
	Add new voice to the voice models and associate them with the given tag.
	No check is done on invalid or duplicated voices (it is responsibility of the caller to provide valid voices).
	
	@param filenames: a list of strings (path of audio file). Voices to be added to the face models data structure
	@param filenames tag: the tag associated to the voice to be added to the voice models data structure
	 */

	public abstract void addVoice(String filename, String tag);

	/**
	Add new voice to the voice models and associate them with the given tag.
	No check is done on invalid or duplicated voices (it is responsibility of the caller to provide valid faces).
	
	@param filenames: a list of strings (path of audio file). Voices to be added to the face models data structure
	@param filenames tag: the tag associated to the voice to be added to the voice models data structure
	 */

	public abstract void addVoice(String filename, String tag,
			String outputRoot, String sms_gmms, String ubm_gmm, String gmmRoot);

	/**
	Add new voices to the voice models and associate them with the given tag.
	No check is done on invalid or duplicated voices (it is responsibility of the caller to provide valid voices).
	
	@param filenames: a list of strings (path of audio file). Voices to be added to the face models data structure
	@param filenames tag: the tag associated to the voice to be added to the voice models data structure
	 */

	public abstract void addVoices(String[] filenames, String[] tags);

	/**
	Rename a tag in the face models data structure.
	Raise an exception if old_tag does not exist in face models data structure.
	Raise an exception if new_tag already exists in face models data structure.
	This method is asynchronous and is propagated to all workers.
	
	@param old_tag: a tag already present in the face models data structure
	@param new_tag: a tag not yet present in the face models data structure
	 */
	public abstract void renameTag(String old_tag, String new_tag);

}