from .models import Notification, UserRegister

def notification_count(request):

    count = 0

    user_id = request.session.get('user_id')

    if user_id:

        # get user role from DB
        user = UserRegister.objects.filter(id=user_id).first()

        if user and user.role == 'seller':

            count = Notification.objects.filter(
                user_id=user_id,
                target_role='seller',
                is_read=False
            ).count()

        elif user and user.role == 'buyer':

            count = Notification.objects.filter(
                user_id=user_id,
                target_role='buyer',
                is_read=False
            ).count()

    return {
        'notification_count': count
    }