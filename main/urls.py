from django.urls import path
from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

                path('',views.Home.as_view(), name="home"),
                path('user/<int:pk>',views.UserPost.as_view(), name="user_post"),
                path('create_profile/',views.CreateProfile.as_view(), name="create_profile"),
                path('update_profile/<int:pk>',views.UpdateProfile.as_view(), name="update_profile"),
                path('show_post/',views.ShowPost.as_view(), name="show_post"), 
                path('create_post/',views.CreatePost.as_view(), name="create_post"),
                path('update_post/',views.UpdatePost.as_view(), name="update_post"),
                path('delete_post/<int:pk>',views.DeletePost.as_view(), name="delete_post"),
                path('create_like/',views.CreateLike.as_view(), name="create_post"),
                path('comment/',views.Comment.as_view(), name="create_comment"),
                path('delete_comment/',views.DeleteComment.as_view(), name="delete_comment"),
                path('friends/',views.ShowFriends.as_view(), name="friend_request"),
                path('remove_frnd/<int:pk>',views.RemoveFriend.as_view(), name="remove_frnd"),
                path('send_request/<int:pk>',views.SendRequest.as_view(), name="send_request"),
                path('accept_req/<int:pk>',views.AcceptRequest.as_view(), name="acccept_req"),
                path('remove_req/<int:pk>',views.RemoveRequest.as_view(), name="acccept_req"),
                path('cancel_req/<int:pk>',views.CancelRequest.as_view(), name="cancel_req"),
                path('search/',views.SearchFriend.as_view(), name="search"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
