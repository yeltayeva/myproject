from django.urls import path
from .views import document_list, home, upload_document, login_view, sign_document, download_document, incoming_documents, outgoing_documents, delete_document
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  # Добавляем пустой путь
    path('upload_document/', views.upload_document, name='upload_document'),
    path('login/', views.login_view, name='login'),
    path('document_list/<str:category>/', views.document_list, name='document_list'),
    path('delete_document/<int:document_id>/', views.delete_document, name='delete_document'),
    path('sign_document/<int:document_id>/', sign_document, name='sign_document'),
    path('download_document/<int:document_id>/', download_document, name='download_document'),
    path('outgoing_documents/', views.outgoing_documents, name='outgoing_documents'),
    path('incoming_documents/', views.incoming_documents, name='incoming_documents'),
]

if settings.DEBUG:
    # Добавляем обработчик для медиафайлов только в режиме DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)