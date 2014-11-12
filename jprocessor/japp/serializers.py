from rest_framework import serializers

from japp.models import Job

class JobSerializer(serializers.ModelSerializer):
	
	class Meta:
		model  = Job
		fields = ('id', 'created', 'resource', 'data')
