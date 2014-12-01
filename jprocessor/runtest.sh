#! /bin/bash

for i in {1..500}
do
curl -X POST http://localhost:5555/api/task/send-task/jprocessor.jobs.tasks.tasks.task_extract_xmp -d '{"kwargs":{"resource_path":"/home/federico/Scaricati/image.jpg"}}'
#curl -i -H "Content-Type:application/json" -X POST http://localhost:5555/api/task/send-task/task_embed_xmp -d '{"kwargs":{"component_id":1,"component_path":"/home/federico/Scaricati/dreamcar.png","changes":{}}}'
done
