from django.http import request
from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View 
from django.views.generic.list import ListView
from django.db.models import Q
from main import models
from main import forms
from django.db.models.functions import Concat
import json
# Create your views here.

class Home(LoginRequiredMixin,ListView):
    model = models.Post
    template_name = 'main/home.html'
    context_object_name = 'posts'
    login_url = "/auth/login"
    
    def friends_details(self):
        friends = models.Friend.objects.filter(Q(personOne = self.request.user) | Q(personTwo = self.request.user))
        frndList = []
        
        for friend in friends:
            if friend.personOne.id == self.request.user.id and friend.personTwo.id != self.request.user.id:
               frndList.append(friend.personTwo.id)
            elif friend.personOne.id != self.request.user.id and friend.personTwo.id == self.request.user.id:
              frndList.append(friend.personOne.id)
        
        
        requestReceived =  models.FriendRequest.objects.filter(receiver = self.request.user)
        rclist =[]
        for request in requestReceived:
            rclist.append(request.sender.id)
        
        requestSent = models.FriendRequest.objects.filter(sender = self.request.user)
        rslist =[]
        for request in requestSent:
            rslist.append(request.receiver.id) 
        
        context = {
                    'friends':friends,
                    'frndidList':frndList,
                    'requestReceived':requestReceived,
                    'rclist':rclist,
                    'requestSent':requestSent,
                    'rslist':rslist
        }
        
        return context

    def get_queryset(self):
        friends = self.friends_details()
        frndidTuple = tuple(friends['frndidList'])
        posts = models.Post.objects.filter(Q(user=self.request.user) | Q(user_id__in = frndidTuple)).order_by('-date')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = forms.PostForm
        context['comment_form'] = forms.CommentForm
        return context


class CreateProfile(LoginRequiredMixin,CreateView):
    model = models.Profile
    form_class = forms.ProfileForm
    tempalte = 'main/user.html'
    
    def get_success_url(self):
        return '/user/'+str(self.request.user.id)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateProfile(LoginRequiredMixin,View):
    
    def post(self,request):
        image = self.request.FILES['image']
        profile = models.Profile.objects.get(user = self.request.user)
        profile.image = image
        profile.save()
        return redirect('/user/'+str(self.request.user.id))
       




class UserPost(LoginRequiredMixin,View):

    def get(self, request,pk):
        posts = models.Post.objects.filter(user_id = pk).order_by('-date')
        user = models.User.objects.get(id = pk)
        context = {'post_form':forms.PostForm,
                   'comment_form':forms.CommentForm,
                   'profile_form':forms.ProfileForm,
                   'posts':posts,
                   'user':user}
        
        if request.is_ajax():
            posts = json.loads(serialize('json',posts))
            return JsonResponse({'posts':posts})
        if pk != request.user.id:
            return render(request,'main/profile.html',context)
        else:
            return render(request,'main/user.html',context)
   

class ShowPost(LoginRequiredMixin,View):
    def get(self, request):
        post = models.Post.objects.filter(id = self.request.GET['postId'])
        post = json.loads(serialize('json', post))
        return JsonResponse({'post':post})


class CreatePost(LoginRequiredMixin,CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'main/home.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin,View):

    def post(self,request):
        postId = self.request.POST['postId']
        updatedPost = self.request.POST['updatedPost']
        updated = models.Post.objects.filter(id= postId).update(post = updatedPost)
        if updated:
            return HttpResponse('ok')
        return HttpResponse('Unable to update')


class DeletePost(LoginRequiredMixin,View):
    def get(self, request,pk):
        postId = pk
        deleted = models.Post.objects.filter(id = postId).delete()
        if deleted:
            return redirect('/user/'+str(self.request.user.id))
        return HttpResponse('unable to delete')




class CreateLike(LoginRequiredMixin,View):
   
    def post(self, request):
        like = models.Like.objects.filter(user = self.request.user, like = True, post =models.Post.objects.get(id = self.request.POST['post_id'] ))

        if like :
            like.delete()
            likes = models.Like.objects.filter(post =self.request.POST['post_id'] ).count()
            return JsonResponse({'likes':likes})
        else:
            models.Like.objects.create(user = self.request.user, like = True, post =models.Post.objects.get(id = self.request.POST['post_id'] ))
            likes = models.Like.objects.filter(post =self.request.POST['post_id'] ).count()
            return JsonResponse({'likes':likes})
   
class Comment(LoginRequiredMixin,View):

    def post(self,request):
        post =  models.Post.objects.get(id = self.request.POST['post_id'])
        models.Comment.objects.create(user = self.request.user,
                                      post = post,
                                      comment = self.request.POST['commentData'])
        return HttpResponse('ok')
    

    def get(self, request):
        post =  models.Post.objects.get(id = self.request.GET['post_id'])
        comments = models.Comment.objects.filter(post = post)
        commentCount = comments.count()
        name = []
        for comment in comments:
            name.append({'first_name':comment.user.first_name,'last_name':comment.user.last_name})
           
        commentsData = json.loads(serialize('json',comments)) 
        return JsonResponse({'commentCount':commentCount,'comments':commentsData,'name':name})

class DeleteComment(LoginRequiredMixin,View):
    
    def post(self,request):
        comments = models.Comment.objects.filter(id = self.request.POST['id']).delete()
        if comments:
             return HttpResponse('ok')
        
        return HttpResponse('unable to delete')


class ShowFriends(Home,LoginRequiredMixin,ListView,):
    model = models.Friend
    template_name = 'main/friends.html'
   
    def get_context_data(self, **kwargs):
        friends = Home.friends_details(self)
        rcTuple = tuple(friends['rclist'])
        rsTuple = tuple(friends['rslist'])
      
        frndidTuple = tuple(friends['frndidList'])
        
        people = models.User.objects.exclude(Q(id = self.request.user.id) | Q(id__in= frndidTuple) | Q(id__in = rsTuple) | Q(id__in = rcTuple))

        context = {'friends':friends['friends'],
                   'requestReceived':friends['requestReceived'],
                   'requestSent':friends['requestSent'],
                   'people':people}
        return context


class SendRequest(ShowFriends,LoginRequiredMixin, View):
    
    def get(self, request, pk):
        requestSent = models.FriendRequest.objects.filter(sender = self.request.user,receiver_id=pk)
        if not requestSent:
            sender = models.User.objects.get(id= self.request.user.id)
            receiver =  models.User.objects.get(id=pk)
            sent = models.FriendRequest.objects.create(sender = sender, receiver = receiver)
            if sent:
                return redirect('/friends/')
            else:
                return HttpResponse('unable to send')

class AcceptRequest(LoginRequiredMixin,View):
    def get(self, request,pk):
        personOne_id = self.request.user.id
        personTwo_id = pk
        
        accepted = models.Friend.objects.create(personOne_id = personOne_id, personTwo_id = personTwo_id)
        if accepted:
            models.FriendRequest.objects.filter(sender = pk).delete()
            return redirect('/friends/')
        else:
            return HttpResponse('unable to accept')


class RemoveRequest(LoginRequiredMixin,View):
    def get(self, request,pk):
            models.FriendRequest.objects.filter(sender_id = pk).delete()
            return redirect('/friends/')

class CancelRequest(LoginRequiredMixin,View):
    def get(self, request,pk):
            models.FriendRequest.objects.filter(receiver_id = pk).delete()
            return redirect('/friends/')

class RemoveFriend(LoginRequiredMixin,View):
    def get(self, request,pk):
        unfriend = models.Friend.objects.filter(id = pk).delete()
        if unfriend:
            return redirect('/friends')
        return HttpResponse('unable to delete')
  
class SearchFriend(LoginRequiredMixin,View):
    
    def post(self, request):
        value = self.request.POST['search_friend'].split()
        if len(value)-1 == 1:
            value = value[0]+value[1]
        else:
            value = value[0]
        
        search_frnd = models.User.objects.annotate(search_name = Concat('first_name','last_name')).filter(
                                            Q(search_name__contains = value)).exclude(id = self.request.user.id)
        
        friends = Home.friends_details(self)
        
        context = {'people':search_frnd,
                    'idList':friends['frndidList'],
                    'rsList':friends['rslist']
                  }
        
        return render(request,'main/search.html',context)