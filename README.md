#Gemini RAG APP

##How to Launch

###1．Launch Qdrant
```
docker run -p 6333:6333 -p 6334:6334 -v ${pwd}/qdrant_storage:/qdrant/storage qdrant/qdrant
```
###2. Launch Server
'''
python manage.py runserver
'''
