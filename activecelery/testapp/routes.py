import sys

class CustomRouter:
	
	def __init__(self):
		sys.stdout = open('/home/federico/workspace-python/activecelery/queues.txt','w')
	
	def route_for_task(self, task, args=None, kwargs=None):
		
		media = self.getTaskMedia(task)
		
		if media == 'video':
			print(media)
			return 'video'
		elif media == 'sound':
			print(media)
			return 'sound'
		elif media == 'image':
			print(media)
			return 'image'
		print('default')
		return None
		
	def getTaskMedia(self, string):
		#taskPath --> appName.tasks.taskName
		#taskName --> taskMedia_action_task --> videos_recognition_task
		print(string)
		if string.split('.')[0] == 'celery':
			return None
		taskName  = string.split('.')[2]
		taskMedia = taskName.split('_')[0]
		return taskMedia.lower()
