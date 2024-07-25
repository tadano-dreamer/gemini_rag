# Gemini RAG APP

## Demo 
![切り抜きデモ](https://github.com/user-attachments/assets/cec67e16-d0fc-4955-bfd5-497d2a2480ae)

## How to Launch

### 1．Launch Qdrant
```
docker run -p 6333:6333 -p 6334:6334 -v ${pwd}/qdrant_storage:/qdrant/storage qdrant/qdrant
```
### 2. Launch Server
```
python manage.py runserver
```
