from django.shortcuts import render
from rest_framework import generics
from api.serializers import * 
from main.models import *
from user.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import sys
from io import StringIO
from rest_framework.status import *
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect, get_object_or_404

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserView(generics.CreateAPIView):
#     renderer_classes = [TemplateHTMLRenderer] 
#     permission_classes = [AllowAny,]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer  
#     template_name = 'onlineCoding/authorization.html'


#     def get(self, request, *args, **kwargs):
#         return Response(status=HTTP_200_OK)
    
#     def post(self, request):
#         user = User.objects.create_user(**request.data)
#         user.set_password(request.data['password'])
#         user.save()
#         serializer = UserSerializer(user, data=request.data)
#         if not serializer.is_valid():
#             return Response({'serializer': serializer, 'user': user})
#         serializer.save()
#         return redirect('profile-list')




class ProgrammingTaskDetail(generics.RetrieveAPIView):
    queryset = ProgrammingTask.objects.all()
    serializer_class = ProgrammingTaskSerializer


class ProgrammingTaskSolutionDetail(generics.RetrieveAPIView):
    queryset = ProgrammingTaskSolution.objects.all()
    serializer_class = ProgrammingTaskSolutionSerializer


class ProgrammingTaskSolutionView(generics.CreateAPIView):
    queryset = ProgrammingTaskSolution.objects.all()
    serializer_class = ProgrammingTaskSolutionSerializer

    def create(self, request, *args, **kwargs):     
        try:
            old_stdout = sys.stdout 
            x = StringIO() 
            mystdout = sys.stdout = x 
            exec(request.data['code']) 
            sys.stdout = old_stdout
        except Exception as e: 
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
        serializer = ProgrammingTaskSolutionSerializer(data=request.data)
        mystdout.getvalue().replace("\n", "")
        if serializer.is_valid():
            
            task = ProgrammingTask.objects.get(id=request.data['task'])
            print(task.output_example + " " + mystdout.getvalue())

            if task.output_example.strip() == mystdout.getvalue().strip():
                print(1)
                return Response({"answer" : "you are right!", "programming_solution": serializer.data,"execute" : mystdout.getvalue().replace('\n', "")}, status=HTTP_200_OK)
            else:
                return Response({"answer" : "you are not right!", "programming_solution": serializer.data,"execute" : mystdout.getvalue().replace('\n', "")}, status=HTTP_400_BAD_REQUEST)
        return Response({"error" : serializer.errors}, status=HTTP_400_BAD_REQUEST) 
    

class ProgrammingTaskView(generics.ListCreateAPIView):
    queryset = ProgrammingTask.objects.all()
    serializer_class = ProgrammingTaskSerializer



# view for textEditor.html
class TextEditorView(generics.ListCreateAPIView):
    queryset = ProgrammingTaskSolution.objects.all()
    serializer_class = ProgrammingTaskSolutionSerializer
    template_name = 'onlineCoding/textEditor.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    def create(self, request, *args, **kwargs):
        serializer = ProgrammingTaskSolutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
def index(request):
    return render(request, 'onlineCoding/welcome.html')

def auth(request):
    if request.method == 'GET':
        return render(request, 'onlineCoding/authorization.html')
    elif request.method == 'POST':
        return redirect('base')
def base(request):
    return render(request, 'onlineCoding/base.html')
def problems(request):
    tasks = ProgrammingTask.objects.all()
    return render(request, 'onlineCoding/problems.html', {'tasks': tasks})

def textEditor(request, slug):
    task = get_object_or_404(ProgrammingTask, slug=slug)
    return render(request, 'onlineCoding/textEditor.html', {'task': task})



def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'onlineCoding/profile.html')
        else:
            return render(request, 'onlineCoding/problempage.html')
    
def leaderboard(request):
    users = User.objects.all()
    return render(request, 'onlineCoding/leaderboard.html', {'users': users})