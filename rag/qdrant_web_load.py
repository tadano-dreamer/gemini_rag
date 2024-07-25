import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_qdrant import Qdrant

import requests
from bs4 import BeautifulSoup

def qdrant_load():
    os.environ['GOOGLE_API_KEY'] = "" #Your Google API Key

    # アンパンマン
    url = "https://ja.wikipedia.org/wiki/%E3%82%A2%E3%83%B3%E3%83%91%E3%83%B3%E3%83%9E%E3%83%B3%E3%81%AE%E7%99%BB%E5%A0%B4%E4%BA%BA%E7%89%A9%E4%B8%80%E8%A6%A7"
    # HTTPリクエストを送信
    response = requests.get(url)
    # レスポンスの内容をHTMLパーサーで解析
    soup = BeautifulSoup(response.content, 'html.parser')
    # 指定された<div>要素を取得
    content4 = soup.find('div', {'class': 'mw-body-content'})
    content4_text = content4.get_text()
    text_all = content4_text.replace('\n', '')
    documents = text_all


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True
    )

    # テキストの分割
    docs = text_splitter.create_documents([documents])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    url = "http://localhost:6333"
    Qdrant.from_documents(
        docs,
        embeddings,
        url=url,
        prefer_grpc=True,
        collection_name="anpanman_characters",
    )


qdrant_load()
print("======================\n読み込みが完了しました！\n===================")