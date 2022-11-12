from django.contrib.auth import get_user_model
from django.shortcuts import redirect

UserModel = get_user_model()


class UserOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.__class__.__name__ != 'AppUser':
            user = self.get_object().user
        else:
            user = obj

        if user != request.user:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)
