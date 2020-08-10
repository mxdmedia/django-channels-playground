from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # Basic json and text consumers- no user auth required.
    re_path(r'ws/widgets/json/$', consumers.WidgetJsonConsumer),
    re_path(r'ws/widgets/text/$', consumers.WidgetTextConsumer),

    # Json consumer that requires a logged in user to connect.
    re_path(r'ws/widgets/django-auth/json/$', consumers.WidgetJsonDjangoAuthConsumer),

]
