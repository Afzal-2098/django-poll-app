from django.shortcuts import render, get_object_or_404
from .forms import CreatePollForm, UserRegistraionForm
from .models import Question, Choice, User, Vote
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# View, for rendering polls and handling voting requests.
@login_required
def ViewPoll(request):
    if request.method == "POST":
        questid = request.POST.get("questid")
        optval = request.POST.get("optval")
        requestuser = User.objects.get(username=request.user)
        quest = Question.objects.get(uid=questid)
        # option = Choice.objects.get(choice_text=optval)
        optionlist = Choice.objects.filter(question=questid)
        for option in optionlist:
            if optval == option.choice_text:
                optval = option.choice_text
                break
        try:
            votequery = Vote.objects.filter(user=request.user).get(question=quest)
            msg = "You Already Voted in this Poll."
            return JsonResponse({"message":msg, "status_code":200})
        except Vote.DoesNotExist:
            votequery = None
            if votequery is None:
                vote = Vote(user=requestuser, question=quest, choice=option)
                vote.save()
                def vote_percentage():
                    '''calculating voting percentage'''
                    votequeryset = Vote.objects.filter(question=quest)
                    totalvotes = votequeryset.count()
                    list_choice = list(Choice.objects.filter(question=quest))
                    percentage_list = []
                    for choice in list_choice:
                        this_count = votequeryset.filter(choice=choice).count()
                        percentage = int((this_count/totalvotes)*100)
                        percentage_list.append(percentage)
                    return percentage_list
                prcnt = vote_percentage()
                return JsonResponse({"percentage":prcnt, "status_code":201})

    try:
        polls = Question.objects.all()
        dict = {}
        for poll in polls:
            ques_choice = []
            choices = []
            choice_queryset = Choice.objects.filter(question=poll.uid)
            for obj in choice_queryset:
                choices.append(obj.choice_text)
            ques_choice.append(poll.text)
            ques_choice.append(choices)
            dict[poll.uid] = ques_choice
        context = {"dict":dict}
        return render(request, "App/home.html", context)
    except Exception as e:
        print(e)
        messages.error(request, "No Polls available right now.")
        return render(request, "App/home.html")
    

# View, For registering the new users. 
class UserRegistrationFormView(View):
    def get(self, request):
        form = UserRegistraionForm()
        return render(request, 'App/userregistration.html', {'form':form})
    def post(self, request):
        form = UserRegistraionForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations!!! Registered Successfully")
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    email=form.cleaned_data['email'])
            login(request, new_user)
            # return redirect("viewpoll")
            return render(request, 'App/userregistration.html', {'form':form})
        messages.error(request, "Invalid Form Request! (: username and password should not be similar. and at least 8 characters required.")
        return render(request, "App/userregistration.html", {'form':form})


# This view renders the user profile.
@login_required
def UserProfile(request):
    if request.user.is_authenticated:
        userdata = User.objects.filter(username=request.user)
        created_polls = Question.objects.filter(owner=userdata[0])
        context = {"userdata":userdata, "created_polls":created_polls}
        return render(request, "App/userprofile.html", context)


# handles requests for creating the new polls.
def CreatePoll(request):
    if request.user.is_authenticated:
        fm = CreatePollForm()
        allpolldata = Question.objects.filter(owner=request.user)
        size = len(allpolldata)
        print(size)
        if size < 5:
            if request.method == "POST":
                fm = CreatePollForm(request.POST)
                if fm.is_valid():
                    questionobj = Question()
                    user = get_object_or_404(User, id=request.user.id)
                    questionobj.owner = user
                    questionobj.text = fm.cleaned_data['text']
                    questionobj.save()
                
                    choice1 = request.POST.get("option1")
                    choice2 = request.POST.get("option2")
                    choice3 = request.POST.get("option3")
                    choice4 = request.POST.get("option4")
                    ques = get_object_or_404(Question, text=fm.cleaned_data['text'])
                    choicelist = [choice1, choice2, choice3, choice4]
                    for choice in choicelist:
                        choiceobj = Choice.objects.create(question=ques, choice_text=choice)
                        choiceobj.save()

                    createdpolldata = list(Question.objects.values().filter(owner=user))
                    return JsonResponse({"createdpolldata":createdpolldata, "status_code":201})
                else:
                    JsonResponse({"msg":"Invalid Form!", "status_code":400})
        else:
            messages.info(request, "You already Posted 5 Polls. You Can Only Post 5 Polls/day(try after 24 hours after the poll is Posted.)")
        context = {"form":fm, "allpolldata":allpolldata}
        return render(request, "App/createpoll.html", context)
