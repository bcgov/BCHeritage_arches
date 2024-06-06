from django.contrib.auth.backends import RemoteUserBackend


class BCGovRemoteUserBackend(RemoteUserBackend):
    create_unknown_user = False

    def clean_username(self, username):
        """
        Force username to lowercase and remove optional idir prefix
        """
        cleaned_username = username.lower().replace('idir\\', '')

        # print("Replacing "+username+" with "+cleaned_username)
        return cleaned_username