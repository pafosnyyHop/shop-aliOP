from aliOP.celery import app
from django.core.mail import send_mail


@app.task
def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/activate/order/{code}/'
    send_mail(
        'Hello, please confirm your order!',
        f'To activate invite link: \n{full_link} \nIf this is not your order, please ignore this message!!!',
        'odecik30@gmail.com',
        [user],
        fail_silently=False
    )
