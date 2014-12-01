BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'amqp://'
CELERY_MESSAGE_COMPRESSION = 'gzip'

APPS = (
	'jprocessor.jobs.commons', 
	'jprocessor.jobs.tasks',
	)
