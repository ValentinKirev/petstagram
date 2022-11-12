from django.urls import path

from petstagram.common.views import like_functionality, share_functionality, add_comment_functionality, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('like/<int:photo_id>/', like_functionality, name='like'),
    path('share/<int:photo_id>/', share_functionality, name='share'),
    path('comment/<int:photo_id>/', add_comment_functionality, name='comment')
]
