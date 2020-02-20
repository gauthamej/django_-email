from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from users.forms import UserForm
from users.models import User
from users import authentication, serializers
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from antway_server import settings
from django.template.loader import render_to_string

def userlist(request):
    userlist=User.objects.values()
    print(userlist)
    return render(request,'userlist.html',{'userlist':userlist} )  

def delete(request, id):
    User.objects.filter(id=id).delete()
    return redirect('userlist')

def edit(request, id):
    post = User.objects.get(id=id)
    print(post)
    if request.method == "POST":
        form = UserForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return redirect('userlist')
    else:
        form = UserForm(instance=post)
    return render(request, 'registerform.html', {'form': form})
    
    
def register(request):
    if request.method == "POST":
        form = UserForm(request.POST or None, request.FILES or None)
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            print(form.errors)
        elif form.is_valid():
            form.save()
            phonenumber=form.cleaned_data['phone_number']
            usertype=form.cleaned_data['user_type']
            name=form.cleaned_data['name']
            password=form.password
            print(password)
            subject = "Antway: New user created"
            msg = "new user added"
            to = 'gauthamej76@gmail.com'
            html_content= render_to_string('emailform.html',{'form':form ,'name':name, 'form_headline':subject, 'password':password, 'phonenumber':phonenumber,'usertype':usertype})
            
            res = EmailMultiAlternatives(subject, msg, settings.EMAIL_HOST_USER,[to] )
            res.attach_alternative(html_content, "text/html")
            res.send()
            return redirect('userlist')
        else:
            print("Invalid")
            print(form.errors)

    else:        
        form = UserForm()
    return render(request, 'registerform.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        phone_number=request.POST['phone_number']
        password=request.POST['password']
        user=authenticate(request, phone_number=phone_number,password=password)
        if user is not None:
            login(request,user)
            print('valid')
            return redirect('userlist')
        else:
            print('invalid')
    return render(request, 'loginform.html')


def logout_user(request):
    logout(request)
    return redirect('login_form')

def login_form(request):
    return render(request,'loginform.html' )  

class LoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.save()
            return_data = serializers.TokenSerializer(instance=token).data
            return Response(data=return_data)
        return Response(data=serializer.errors, status=400)


class DesignerProfileView(APIView):

    authentication_classes = [authentication.DesignerAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.DesignerSerializer(instance=request.user.designer_set.first())
        return Response(data=serializer.data)

    def patch(self, request):
        designer = request.user.designer_set.first()
        serializer = serializers.DesignerSerializer(instance=designer, data=request.data,
                                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=400)
