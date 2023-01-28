<<<<<<< HEAD
from django.core.mail import send_mail


def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
    send_mail(
        'Hello activate your account!',
        f'To activate invite link: \n{full_link} ',
        'baialinovsultan@gmail.com',
        [user],
        fail_silently= False
    )
    
def send_confirmation_email_for_new(user, code):
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
    send_mail(
        'Hello activate your account!',
        f'To activate invite link: \n{full_link} ',
        'baialinovsultan@gmail.com',
        [user],
        fail_silently= False
    )



=======
# from django.core.mail import send_mail
#
#
# def send_confirmation_email(user, code):
#     full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
#     send_mail(
#         'Hello activate your account!',
#         f'To activate invite link: \n{full_link} ',
#         'baialinovsultan@gmail.com',
#         [user],
#         fail_silently=False
#     )
>>>>>>> b1d2dfd7fb67a7f24f4490d67b409dce320fa7c3
