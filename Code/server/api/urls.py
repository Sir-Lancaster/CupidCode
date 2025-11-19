from django.urls import path
from . import views

urlpatterns = [
    path('user/create/', views.create_user, name='create_user'), 
    path('user/sign_in/', views.sign_in, name='sign_in'),
    path('user/<int:pk>', views.get_user, name='get_user'), 
    path('chat/', views.send_chat_message, name='send_chat_message'),
    path('chat/<int:pk>/<int:count>', views.get_messages, name='get_messages'), 
    path('dater/calendar/<int:pk>/', views.calendar, name='calendar'), 
    path('dater/rate/', views.rate_dater, name='rate_dater'), 
    path('dater/ratings/<int:pk>/', views.get_dater_ratings, name='get_dater_ratings'),
    path('dater/transfer/', views.dater_transfer, name='dater_transfer'), #unused
    path('dater/balance/<int:pk>/', views.get_dater_balance, name='get_dater_balance'),
    path('dater/profile/<int:pk>/', views.get_dater_profile, name='get_dater_profile'), #unused
    path('dater/profile/', views.set_dater_profile, name='set_dater_profile'), 
    path('dater/gigs/<int:pk>', views.get_dater_gigs, name='get_dater_gigs'), 
    path('dater/save_card/', views.save_card, name='save_card'), #unused
    path('dater/get_cards/<int:pk>', views.get_cards, name='get_cards'), #unused
    path('cupid/rate/', views.rate_cupid, name='rate_cupid'),
    path('cupid/ratings/<int:pk>/', views.get_cupid_ratings, name='get_cupid_ratings'),
    path('cupid/profile/', views.set_cupid_profile, name='set_cupid_profile'),
    path('cupid/gigs/<int:pk>/', views.get_cupid_gigs, name='get_cupid_gigs'),
    path('gig/create/', views.create_gig, name='create_gig'), 
    path('gig/accept/', views.accept_gig, name='accept_gig'), 
    path('gig/complete/', views.complete_gig, name='complete_gig'), 
    path('gig/drop/', views.drop_gig, name='drop_gig'), 
    path('gig/cancel/', views.cancel_gig, name='cancel_gig'), 
    path('gig/<int:pk>/<int:count>/', views.get_gigs, name='get_gigs'),
    path('manager/cupids/', views.get_cupids, name='get_cupids'),
    path('manager/daters/', views.get_daters, name='get_daters'),
    path('manager/dater_count/', views.get_dater_count, name='get_dater_count'),
    path('manager/cupid_count/', views.get_cupid_count, name='get_cupid_count'),
    path('manager/active_cupids/', views.get_active_cupids, name='get_active_cupids'),
    path('manager/active_daters/', views.get_active_daters, name='get_active_daters'),
    path('manager/gig_rate/', views.get_gig_rate, name='get_gig_rate'),
    path('manager/gig_count/', views.get_gig_count, name='get_gig_count'),
    path('manager/gig_drop_rate/', views.get_gig_drop_rate, name='get_gig_drop_rate'),
    path('manager/gig_complete_rate/', views.get_gig_complete_rate, name='get_gig_complete_rate'),
    path('manager/suspend/', views.suspend, name='suspend'),
    path('manager/unsuspend/', views.unsuspend, name='unsuspend'),
    path('notifications/<int:pk>/', views.get_notifications, name='get_notifications'),
    path('google-maps-config/', views.get_google_maps_config, name='get_google_maps_config'),
    path('paypal/config/', views.paypal_config, name='paypal_config'),
    path('check-speech-for-word/', views.check_speech_for_word, name='check_speech_for_word'),
    path('ai-gig/create/', views.create_ai_gig, name='create_ai_gig'),
]
