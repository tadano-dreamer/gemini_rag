from django.urls import path, include
from . import views

app_name = 'rag'
urlpatterns = [
    path('', views.index, name = 'index' ),
    # path('load/', views.load, name = 'load' ),
    path('llmquiz/', views.llm_quiz, name = 'llm_quiz' ),
    path('select/', views.select, name = 'select' )
]