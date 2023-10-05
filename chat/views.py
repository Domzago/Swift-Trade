from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from . models import Item, Conversation, ConversationMessage
from . forms import ItemForm, MessageForm


# Create your views here.
def home(request):
    p = Paginator(Item.objects.all(), 4)
    page = request.GET.get('page')
    items = p.get_page(page)

    search = request.GET.get('search')

    if search:
        items = Item.objects.filter(Q(name__icontains=search) | Q(description__icontains=search) | Q(price__icontains=search))

    return render(request, 'home.html', {'items':items, 'search':search})

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'detail.html', {'item':item})


@login_required
def createItem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created = request.user
            item.save()
            messages.success(request, 'Your Item was added successfully')
            return redirect('home')
        
    else:
        form = ItemForm()
    return render(request, 'create.html', {'form':form})

@login_required
def updateItem(request, pk):
    item = get_object_or_404(Item, pk=pk, created=request.user)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your Item was updated successfully')
            return redirect('detail', pk=pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'update.html', {'item':item, 'form':form})

@login_required
def deleteItem(request, pk):
    item = get_object_or_404(Item, pk=pk, created=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'The Item was deleted successfully')
        return redirect('home')
    return render(request, 'delete.html', {'item':item})

def signup(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'{username} you are highly welcomed to Swift Chat')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome Back {username}')
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'login.html', {})

@login_required
def newMessage(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if item.created == request.user:
        return redirect('home')
    

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('detailconvo', pk=conversations.first().id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created = request.user
            conversation_message.save()
            return redirect('detail', pk=pk)

    else:
        form = MessageForm()
    return render(request, 'message.html', {'form':form})

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    return render(request, 'inbox.html', {'conversations':conversations})

@login_required
def detailConvo(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created = request.user
            conversation_message.save()

            conversation.save()
            return redirect('detailconvo', pk=pk)
    else:
        form = MessageForm()

    return render(request, 'detailconvo.html', {'conversation':conversation, 'form':form})

