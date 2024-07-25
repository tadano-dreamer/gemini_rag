from django.shortcuts import render

import os

# from langchain import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain_google_genai import ChatGoogleGenerativeAI

def index(request):
    context = {}
    return render(request, 'rag/index.html', context)


def llm_quiz(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        
        rag_ans = ask_rag(question_text)
        simplellm_ans = ask_simple_llm(question_text)      
            
        context = {
            "rag_ans": rag_ans,
            "simplellm_ans":simplellm_ans,
            "question_text":question_text,
                }
        return render(request, "rag/qa.html", context) 
    else:
        rag_ans=""
        simplellm_ans=""
        question_text = ""
        
        context = {
            "rag_ans": rag_ans,
            "simplellm_ans":simplellm_ans,
            "question_text":question_text,
                }
        return render(request, "rag/qa.html", context)
    

def ask_simple_llm(question_text):
    os.environ["GOOGLE_API_KEY"] = "" #Your Google API Key

    llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.7, top_p=0.85)
    llm_prompt_template = """
以下の入力されたキャラクター（若しくは質問文）について説明（若しくは回答）をしてください。
内容の真偽は曖昧でも良いので何かしら文章を生成してください。
キャラクター（若しくは質問文）: {question} 
回答:"""
    llm_prompt = PromptTemplate.from_template(llm_prompt_template)

    rag_chain = (
        {"question": RunnablePassthrough()}
        | llm_prompt
        | llm
        | StrOutputParser()
        )
    
    simplellm_ans = rag_chain.invoke(question_text)
    
    return simplellm_ans

def ask_rag(question_text):
    
    #RAGの処理
    # Qdrantのベクトルストアを設定
    # 初期化
    os.environ["GOOGLE_API_KEY"] = "" #Your Google API Key

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    client = QdrantClient("localhost", port=6333)

    vector_store = Qdrant(
        client=client,
        collection_name="anpanman_characters",
        embeddings=embeddings
    )

    # リトリーバーの設定
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.7, top_p=0.85)
    llm_prompt_template = """
コンテクストに基づいて以下のキャラクター（若しくは質問文）について説明（若しくは回答）をしてください。
キャラクター（若しくは質問文）: {question} 
コンテクスト: {context} 
回答:"""
    llm_prompt = PromptTemplate.from_template(llm_prompt_template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | llm_prompt
        | llm
        | StrOutputParser()
        )
    
    rag_ans = rag_chain.invoke(question_text)
    
    references = retriever.get_relevant_documents(question_text)
    print("\n==========RAGの該当部分==========\n")
    for doc in references:
        print(doc.page_content,"\n=============\n")
    
    return rag_ans


def select(request):
    if request.method == 'POST':
        choice = request.POST.get('choice') #選択肢に応じてAI-1 かAI-2を取得する
        if choice == "AI-1":
            message = "Correct !!"
        else:
            message = "Not Correct ..."
        
        context = {
            "your_select": choice,
            "message":message

            }
    else:
        context={

        }
    return render(request, "rag/select.html", context)