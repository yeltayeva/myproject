from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseForbidden, HttpResponse, FileResponse
from django.contrib import messages
from .forms import DocumentForm, UserRegistrationForm
from .models import Document
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Перенаправление на страницу списка документов после успешного входа
            return redirect('document_list', category='all')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def document_list(request, category=None):
    username = request.user.username
    print("Current user:", username)
    if category == 'incoming':
        documents = Document.objects.filter(recipient=request.user)
        title = 'Входящие документы'
    elif category == 'outgoing':
        documents = Document.objects.filter(author=request.user)
        title = 'Исходящие документы'
    else:
        documents = Document.objects.filter(Q(author=request.user) | Q(recipient=request.user))
        title = 'Все документы'
    print("Filtered documents:", documents)
    return render(request, 'document_list.html', {'documents': documents, 'title': title, 'username': username, 'current_category': category})


def home(request):
    # Логика для представления home
    return render(request, 'home.html')  

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.author = request.user
            document.is_sent = True  # Устанавливаем флаг is_sent в True, так как документ отправлен
            document.save()
            return redirect('document_list', category='all')
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})

    
@login_required
def download_document(request, document_id):
    document = Document.objects.get(pk=document_id)

    # Обновление статуса is_viewed
    document.is_viewed = True
    document.viewed_at = timezone.now()  # Добавляем дату и время просмотра
    document.save()

    # Получаем документ отправителя
    sender_document = Document.objects.get(recipient=request.user, title=document.title)  # Проверьте условие нахождения документа отправителя
    if sender_document:
        sender_document.is_viewed = True
        sender_document.viewed_at = timezone.now()  # Добавляем дату и время просмотра
        sender_document.save()

    # Получите путь к файлу документа или объект файла, который будет отправлен пользователю
    file_path = document.file.path
    
    # Отправляем файл пользователю
    try:
        return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)

@login_required
def sign_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    
    # Проверяем, имеет ли текущий пользователь право подписывать этот документ
    if request.user == document.recipient:
        # Подписываем документ
        document.is_signed = True
        document.signed_by = request.user
        document.signed_at = timezone.now()
        document.save()
        return redirect('document_list', category='all')
    else:
        # Если текущий пользователь не является получателем документа, возвращаем ошибку 403 Forbidden
        return HttpResponseForbidden("Вы не можете подписать этот документ.")
    
def send_signed_notification(sender_email, recipient_email, document_title):
    subject = 'Document Signed Notification'
    message = f'The document "{document_title}" has been signed.'
    send_mail(subject, message, sender_email, [recipient_email])

def outgoing_documents(request):
    # Получаем список отправленных документов текущего пользователя
    outgoing_documents = Document.objects.filter(author=request.user)
    return render(request, 'outgoing_documents.html', {'documents': outgoing_documents})

def incoming_documents(request):
    # Получаем список полученных документов текущего пользователя
    incoming_documents = Document.objects.filter(recipient=request.user)
    return render(request, 'incoming_documents.html', {'documents': incoming_documents})

def delete_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document.delete()
    return redirect(request.POST.get('next', '/'))