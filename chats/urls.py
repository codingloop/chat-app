from rest_framework.routers import DefaultRouter

from chats.views import ChatGroupViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register('chat-group', ChatGroupViewSet, 'ChatGroupViewSet')
router.register('chat-message', ChatMessageViewSet, 'ChatMessageViewSet')

urlpatterns = router.urls
