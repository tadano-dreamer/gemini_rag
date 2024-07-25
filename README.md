# Gemini RAG APP

Which is better AI (mitigate hallucinations) ?

## Demo 
![切り抜きデモ](https://github.com/user-attachments/assets/cec67e16-d0fc-4955-bfd5-497d2a2480ae)

## How to Play

### 1．Launch Qdrant
```
docker run -p 6333:6333 -p 6334:6334 -v ${pwd}/qdrant_storage:/qdrant/storage qdrant/qdrant
```

### 2. exe rag/qdrant_web_load.py
chunked data will be set in the vector store

### 3. Launch Server
```
python manage.py runserver
```
