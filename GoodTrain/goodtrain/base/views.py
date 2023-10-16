from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import User, Train, RoomStatus, Room, MatchType, Match, ReviewType, Review, Message, UserLikes, UserFlags, UserData
from .forms import RoomForm, UserForm, MyUserCreationForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def get_customer(room):
    customer_id = Match.objects.filter(room=room, type=MatchType.objects.get_or_create(name='Customer')[0]).values('user')[0]
    return User.objects.get(id=customer_id['user'])

def get_room_to_customer(rooms):
    room_to_customer = {}  # Создаем пустой словарь

    for room in rooms:
        customer = get_customer(room)
        if customer:
            room_to_customer[room] = customer
    
    return room_to_customer
import numpy as np
import pandas as pd

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(train__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    trains = Train.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__train__name__icontains=q))[0:3]

    room_to_customer = get_room_to_customer(rooms)  

    participants_ids = [Match.objects.filter(room=room).values('user') for room in rooms]
    participants_groups = [User.objects.filter(id__in=[user_id['user'] for user_id in participants_id]) for participants_id in participants_ids]
    users_datas_groups = [UserData.objects.filter(user__in=[user for user in participants_group]) for participants_group in participants_groups]
    
    agreeableness_rooms = [np.mean(np.array([user_data.agreeableness for user_data in users_data])) for users_data in users_datas_groups]
    conscientiousness_rooms = [np.mean(np.array([user_data.conscientiousness for user_data in users_data])) for users_data in users_datas_groups]
    extraversion_rooms = [np.mean(np.array([user_data.extraversion for user_data in users_data])) for users_data in users_datas_groups]
    openness_rooms = [np.mean(np.array([user_data.openness for user_data in users_data])) for users_data in users_datas_groups]
    emotional_stability_rooms = [np.mean(np.array([user_data.emotional_stability for user_data in users_data])) for users_data in users_datas_groups]

    interest_economic_rooms = [np.mean(np.array([user_data.interest_economic for user_data in users_data])) for users_data in users_datas_groups]
    interest_social_rooms = [np.mean(np.array([user_data.interest_social for user_data in users_data])) for users_data in users_datas_groups]
    interest_spiritual_rooms = [np.mean(np.array([user_data.interest_spiritual for user_data in users_data])) for users_data in users_datas_groups]
    interest_political_rooms = [np.mean(np.array([user_data.interest_political for user_data in users_data])) for users_data in users_datas_groups]

    social_level_rooms = [np.mean(np.array([user_data.social_level for user_data in users_data])) for users_data in users_datas_groups]

    current_user = User.objects.all()[0]
    user_data = UserData.objects.filter(user=current_user)[0]
    user_df = np.array([user_data.agreeableness, user_data.conscientiousness, user_data.extraversion, user_data.openness, user_data.emotional_stability, user_data.interest_economic, user_data.interest_social, user_data.interest_spiritual, user_data.interest_political,  user_data.social_level], dtype='float64')
    vectors = np.array([          agreeableness_rooms,     conscientiousness_rooms,     extraversion_rooms,     openness_rooms,      emotional_stability_rooms,    interest_economic_rooms,     interest_social_rooms,     interest_spiritual_rooms,     interest_political_rooms, social_level_rooms], dtype='float64').T
    corrs = [np.corrcoef(user_df, v1)[0, 1] for v1 in vectors]
    # messages.error(request, str(corrs))
    corrs_dict = {}
    i = 0
    for room in rooms:
        corrs_dict[room] = corrs[i]
        i += 1

    context = {'rooms': rooms, 
               'room_to_customer': room_to_customer, 
               'trains': trains,
               'room_count': room_count, 
               'room_messages': room_messages,
               'corrs': corrs_dict}
    

    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants_id = Match.objects.filter(room=room).values('user')
    participants = User.objects.filter(id__in=[user_id['user'] for user_id in participants_id])

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        message.save()
        if Match.objects.filter(user=request.user).count() == 0:
            match = Match.objects.create(
                room = room,
                user = request.user,
                type = MatchType.objects.get_or_create(name='Participant')[0]
            )
            match.save()
        return redirect('room', pk=room.id)
    
    customer_id = Match.objects.filter(room=room, type=MatchType.objects.get_or_create(name='Customer')[0]).values('user')
    room_customer = User.objects.filter(id=customer_id[0]['user'])[0]
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants,
               'room_customer': room_customer}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = Room.objects.filter(id__in=[x['room'] for x in 
        Match.objects.filter(user=user, type=MatchType.objects.get_or_create(name='Customer')[0].id).values('room')
    ])
    room_messages = user.message_set.all()
    trains = Train.objects.all()
    room_to_customer = get_room_to_customer(rooms)
    context = {'user': user, 'room_to_customer': room_to_customer,
               'room_messages': room_messages, 'trains': trains}
    return render(request, 'base/profile.html', context)

def userBalance(request, pk): # TODO:
    user = User.objects.get(id=pk)
    transaction_karmas = user.transaction_karma_set.all()
    context = {
        'user': user,
        'transaction_karmas': transaction_karmas
    }
    return render(request, f'base/balance.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    trains = Train.objects.all()
    if request.method == 'POST':
        train_name = request.POST.get('train')
        train, created = Train.objects.get_or_create(name=train_name)

        room = Room.objects.create(
            train=train,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            status = RoomStatus.objects.get_or_create(name='Find performer')[0],
            cost=request.POST.get('cost'),
        )
        room.save()
        match = Match.objects.create(
            room = room,
            user = request.user,
            type = MatchType.objects.get_or_create(name='Customer')[0],
        )
        match.save()
        return redirect('home')

    context = {'form': form, 'trains': trains}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    trains = Train.objects.all()
    customer_id = Match.objects.filter(room=room, type=MatchType.objects.get_or_create(name='Customer')[0]).values('user')
    room_customer = User.objects.filter(id=customer_id[0]['user'])[0]
    if request.user != room_customer:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        train_name = request.POST.get('train')
        train, created = Train.objects.get_or_create(name=train_name)
        room.name = request.POST.get('name')
        room.train = train
        room.description = request.POST.get('description')
        room.cost = request.POST.get('cost')
        room.save()
        return redirect('home')

    context = {'form': form, 'trains': trains, 'room': room}
    
    return render(request, 'base/room_form.html', context)

def get_customer(room):
    customer_id = Match.objects.filter(room=room, type=MatchType.objects.get_or_create(name='Customer')[0]).values('user')
    room_customer = User.objects.filter(id=customer_id[0]['user'])[0]
    return room_customer

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    room_customer = get_customer(room)

    if request.user != room_customer:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', {})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def trainsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    trains = Train.objects.filter(name__icontains=q)
    return render(request, 'base/trains.html', {'trains': trains})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
