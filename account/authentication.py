from django.contrib.auth.models import User

class EmailAuthBackend:
    """
    Authenticate using an email address.
    
    la methode authenticate recois en parametre l'objet request et 2 autres parametres optionnels 
    en occurence username et password pour faire en sorte que le backend travail avec la vue du 
     framework d'authentification , la methode get_user recoit l'ID de l'utilisateur en parametre et return un 
     utilisateur la cle pk est un short de primary key 
    """
    def authenticate(self, request, username=None, password=None): 
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return  None
        except(User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None    