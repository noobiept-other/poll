from django.conf.urls import url


urlpatterns = [

    url( r'^new_account$', 'accounts.views.new_account', name= 'new_account' ),
    url( r'^login$', 'accounts.views.login', name= 'login' ),
    url( r'^logout$', 'django.contrib.auth.views.logout', name= 'logout' ),
    url( r'^user/(?P<username>\w+)$', 'accounts.views.user_page', name= 'user_page' ),

        # Add/Remove Moderator Rights
    url( r'^set_moderator/confirm/(?P<username>\w+)$', 'accounts.views.set_moderator_confirm', name= 'set_moderator_confirm' ),
    url( r'^set_moderator/(?P<username>\w+)$', 'accounts.views.set_moderator', name= 'set_moderator' ),

        # Remove Account
    url( r'^remove/confirm/(?P<username>\w+)$', 'accounts.views.remove_user_confirm', name= 'remove_confirm' ),
    url( r'^remove/(?P<username>\w+)$', 'accounts.views.remove_user', name= 'remove' ),

        # Disable Account
    url( r'^disable/confirm/(?P<username>\w+)$', 'accounts.views.disable_user_confirm', name= 'disable_confirm' ),
    url( r'^disable/(?P<username>\w+)$', 'accounts.views.disable_user', name= 'disable' ),

        # Change Password
    url( r'^change_password$', 'django.contrib.auth.views.password_change', { 'template_name': 'accounts/change_password.html', 'post_change_redirect': 'accounts:password_changed' }, name= 'change_password' ),
    url( r'^password_changed$', 'accounts.views.password_changed', name= 'password_changed' ),

       # Private Messages
    url( r'^message/send/(?P<username>\w+)$', 'accounts.views.message_send', name= 'message_send' ),
    url( r'^message/all/$', 'accounts.views.message_all', name='message_all' ),
    url( r'^message/open/(?P<messageId>\w+)$', 'accounts.views.message_open', name= 'message_open' ),
    url( r'^message/remove_confirm/(?P<messageId>\w+)$', 'accounts.views.message_remove_confirm', name= 'message_remove_confirm' ),
    url( r'^message/remove/(?P<messageId>\w+)$', 'accounts.views.message_remove', name= 'message_remove' ),
]
