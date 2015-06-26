package it.crs4.active.api;

public interface VoiceModelInterface {

	/**
	Add new voice to the voice models and associate them with the given tag.
	No check is done on invalid or duplicated voices (it is resposibility of the caller to provide valid faces).
	This method is asynchronous and is propagated to all workers.
	
	@param filenames: a list of strings (path of audio file). Voices to be added to the face models data structure
	@param filenames tag: the tag associated to the voice to be added to the voice models data structure
	 */

	public abstract void addVoice(String filename, String tag);

	/**
	Add new voice to the voice models and associate them with the given tag.
	No check is done on invalid or duplicated voices (it is resposibility of the caller to provide valid faces).
	This method is asynchronous and is propagated to all workers.
	
	@param filenames: a list of strings (path of audio file). Voices to be added to the face models data structure
	@param filenames tag: the tag associated to the voice to be added to the voice models data structure
	 */

	public abstract void addVoice(String filename, String tag,
			String outputRoot, String sms_gmms, String ubm_gmm, String gmmRoot);

	/**
	Add new voices to the voice models and associate them with the given tag.
	No check is done on invalid or duplicated voices (it is resposibility of the caller to provide valid faces).
	This method is asynchronous and is propagated to all workers.
	
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