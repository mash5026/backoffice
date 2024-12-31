from django.contrib.auth.backends import BaseBackend
from backoffice.models import Profile
import bcrypt


class ProfileBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            profile = Profile.objects.get(username=username)
            if (
                profile.DJANGO_IS_ACTIVE and
                bcrypt.checkpw(password.encode('utf-8'), profile.password.encode('utf-8'))
            ):
                has_admin_role = profile.profileroles.filter(role__enkey='province_admin').exists()
                if has_admin_role:
                    if profile.usertype and profile.usertype.id == 2 and profile.usertype.code == "03":
                        return profile
                    else:
                        return None
                else:
                    return None
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            profile = Profile.objects.get(pk=user_id)
            profile.is_authenticated = True
            profile.is_staff = profile.DJANGO_IS_STAFF
            profile.is_superuser = profile.DJANGO_IS_SUPERUSER
            return profile
        except Profile.DoesNotExist:
            return None