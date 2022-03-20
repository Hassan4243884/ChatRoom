from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Messages, Room, Topic, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.
# rooms = [
#     {"id":1,"name":"Fuck You"},
#     {"id":2,"name":"What Ever"},
# ]


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        print(email+"\n"+password)
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User Does Not Exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            messages.error(request, "email or Password does not match")

    context = {"page": page}
    return render(request, "accounting/login.html", context)


def logoutPage(request):
    logout(request)
    return redirect("home")


def registerUser(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An Error has Occured")

    context = {"form": form}
    return render(request, "accounting/register_form.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(disc__icontains=q)
    )
    topics = Topic.objects.all()

    room_messages = Messages.objects.filter(
        Q(room__topic__name__icontains=q))
    room_count = rooms.count()
    context = {"rooms": rooms, "topics": topics[:5],
               "room_count": room_count, "room_messages": room_messages[:4]}
    return render(request, "accounting/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.messages_set.all().order_by('-created')
    particepents = room.particepent.all()
    user = request.user
    if request.method == 'POST':
        message = Messages.objects.create(
            user=user,
            room=room,
            body=request.POST.get("body")
        )
        room.particepent.add(user)
        return redirect("room", pk=room.id)
    context = {"room": room, "room_messages": room_messages,
               "particepents": particepents,"user":user}
    return render(request, "accounting/rooms.html", context)


def userProfile(request, pk):
    q = request.GET.get("q") if request.GET.get("q") != None else ''

    topics = Topic.objects.all()[:5]
    user = User.objects.get(id=pk)
    room_messages = user.messages_set.all()

    rooms = user.room_set.all()
    context = {"user": user, "rooms": rooms,
               "topics": topics, "room_messages": room_messages}
    return render(request, "accounting/profile.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            disc=request.POST.get("disc"),
        )
        return redirect("home")

    context = {'form': form, "topics": topics}
    return render(request, "accounting/create-room.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You Are Not Fucking Allowed Here")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.disc = request.POST.get("disc")
        room.topic = topic
        room.save()

        return redirect("home")

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "accounting/create-room.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You Are Not Fucking Allowed Here")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "accounting/delete.html", {"obj": room})


@login_required(login_url="login")
def deleteMessage(request, pk):
    Message = Messages.objects.get(id=pk)
    if request.method == "POST":
        Message.delete()
        return redirect("home")
    return render(request, "accounting/delete.html", {"obj": Message})


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect("user-profile", pk=user.id)
    return render(request, "accounting/edit-user.html", {"form": form})


@login_required(login_url="login")
def topicPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "accounting/topic.html", {"topics": topics})


@login_required(login_url="login")
def activityPage(request):
    messages = Messages.objects.all()
    return render(request, "accounting/activityPage.html", {"room_messages": messages})

# 6978
# KJ_kjkljlyufyjyui8yi
# KJ_kjkljlyufyjyui8yi
