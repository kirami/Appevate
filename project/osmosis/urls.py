"""osmosis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from osmosis.app.api import views as app_api_views
from osmosis.owner.api import views as owner_api_views
from osmosis.invite.api import views as invite_api_views
from osmosis.event.api import views as event_api_views
from osmosis.program.api import views as program_api_views
from osmosis.action.api import views as action_api_views
from osmosis.action_type.api import views as action_type_api_views
from osmosis.metric.api import views as metric_api_views
from osmosis.account.api import views as account_api_views
from osmosis.account.ledger.api import views as ledger_api_views
from osmosis.customauth.api import views as customauth_api_views
from osmosis.subscription.api import views as subscription_api_views
from osmosis.payment.api import views as payment_api_views

from osmosis.onboarding import views as onboarding_views
from osmosis.customauth import views as customauth_views
from osmosis.dashboard import views as dashboard_views
from osmosis.app import views as app_views
from osmosis.payment import views as payment_views
from osmosis.action_type import views as action_type_views
from osmosis.custom_admin import views as admin_views
#from osmosis.subscription import views as subscription_views

from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls),
    
    #url(r'^accounts/', include('registration.backends.default.urls')),

    #APIs
    url(r'^api/app/$', app_api_views.AppList.as_view(), name="app-list"),
    url(r'^api/app/(?P<pk>[0-9]+)/$', app_api_views.AppDetail.as_view(), name="app-detail"),
    url(r'^api/owner/$', owner_api_views.OwnerList.as_view(), name="owner-list"),
    url(r'^api/owner/(?P<pk>[0-9]+)/$', owner_api_views.OwnerDetail.as_view(), name="owner-detail"),
    #url(r'^api/invite/$', invite_api_views.InviteList.as_view(), name="invite-list"),
    #url(r'^api/invite/(?P<pk>[0-9]+)/$', invite_api_views.InviteDetail.as_view(), name="invite-detail"),
    url(r'^api/event/$', event_api_views.EventList.as_view(), name="event-list"),
    url(r'^api/event/(?P<pk>[0-9]+)/$', event_api_views.EventDetail.as_view(), name="event-detail"),
    
    url(r'^api/program/$', program_api_views.ProgramList.as_view(), name="program-list"),
    url(r'^api/program/(?P<pk>[0-9]+)/$', program_api_views.ProgramDetail.as_view(), name="program-detail"),
    url(r'^api/action/$', action_api_views.ActionList.as_view(), name="action-list"),
    url(r'^api/action/(?P<pk>[0-9]+)/$', action_api_views.ActionDetail.as_view(), name="action-detail"),
    url(r'^api/action-type/$', action_type_api_views.ActionTypeList.as_view(), name="action-type-list"),
    url(r'^api/action-type/(?P<pk>[0-9]+)/$', action_type_api_views.ActionTypeDetail.as_view(), name="action-type-detail"),
    
    url(r'^api/metric/$', metric_api_views.MetricList.as_view(), name="metric-list"),
    url(r'^api/metric/(?P<pk>[0-9]+)/$', metric_api_views.MetricDetail.as_view(), name="metric-detail"),

    url(r'^api/account/$', account_api_views.AccountList.as_view(), name="account-list"),
    url(r'^api/account/(?P<pk>[0-9]+)/$', account_api_views.AccountDetail.as_view(), name="account-detail"),
    
    url(r'^api/account/ledger$', ledger_api_views.LedgerList.as_view(), name="ledger-list"),
    url(r'^api/account/ledger/(?P<pk>[0-9]+)/$', ledger_api_views.LedgerDetail.as_view(), name="ledger-detail"),

    url(r'^api/user/$', customauth_api_views.UserList.as_view(), name="user-list"),
    url(r'^api/user/(?P<pk>[0-9]+)/$', customauth_api_views.UserDetail.as_view(), name="user-detail"),
    
    url(r'^api/payment/send-payment/$', payment_views.paypal_payment_api, name="send_payment"),
   
    url(r'^api/payment/$', payment_api_views.PaymentList.as_view(), name="payment-list"),
    url(r'^api/payment/(?P<pk>[0-9]+)/$', payment_api_views.PaymentDetail.as_view(), name="payment-detail"),
    

    #url(r'^api/subscription/$', subscription_api_views.SubscriptionList.as_view(), name="subscription-list"),
    #url(r'^api/subscription/(?P<pk>[0-9]+)/$', subscription_api_views.SubscriptionDetail.as_view(), name="subscription-detail"),
    

    #Onboarding
    #url(r'^register/$', onboarding_views.signup.as_view(), name="signup"),
    url(r'^register/$', onboarding_views.signup, name="signup"),
    url(r'^integrate/$', onboarding_views.integrate, name="integrate"),
    url(r'^dashboard/$', dashboard_views.dashboard_main, name="dashboard_main"),

    url(r'^dashboard/settings/$',  dashboard_views.dashboard_settings, name="dashboard_settings"),
    
    #url(r'^webframe/settings/$',  TemplateView.as_view(template_name='webframe/settings.html'), name="wf-settings"),
    #url(r'^webframe/form/$',  TemplateView.as_view(template_name='webframe/form.html'), name="wf-form"),
    
    url(r'^user-dashboard/(?P<user_id>[0-9]+)/$', dashboard_views.user_dashboard, name="user_dashboard"),
    url(r'^user-dashboard/payments/(?P<user_id>[0-9]+)/$', dashboard_views.user_payments, name="user_payments"),
    url(r'^user-dashboard/rewards/(?P<user_id>[0-9]+)/$', dashboard_views.user_rewards, name="user_rewards"),


    url(r'^webframe/settings/(?P<user_id>[0-9]+)/$',  TemplateView.as_view(template_name='webframe/settings.html'), name="wf-settings"),
    url(r'^webframe/form/(?P<user_id>[0-9]+)/$',  dashboard_views.webframe_user_form, name="wf-form"),
    url(r'^webframe/dashboard/(?P<user_id>[0-9]+)/$',  dashboard_views.webframe_dashboard, name="wf-form"),
    url(r'^webframe/TOS/$', TemplateView.as_view(template_name='webframe/TOS.html'), name="wf-TOS"),
    url(r'^webframe/activeProgramDetail/$', dashboard_views.webframe_active_program_detail, name="wf-activePD"),
    url(r'^webframe/dashboard/sample/(?P<style>[0-9]+)/$',  dashboard_views.webframe_dashboard_template, name="wf-form_template"),
        

    url(r'^program/(?P<app_id>[0-9]+)/$', dashboard_views.programs_by_app, name="programs-by-app"),
    url(r'^program-detail/(?P<program_id>[0-9]+)/$', dashboard_views.program_info, name="program-info"),
    url(r'^delete/program/(?P<program_id>[0-9]+)/$', dashboard_views.delete_program, name="delete-program"),
    url(r'^app-detail/(?P<app_id>[0-9]+)/$', dashboard_views.app_info, name="app-info"),
    url(r'^custom-metrics/(?P<program_id>[0-9]+)/$', dashboard_views.custom_metrics, name="custom_metrics"),
    url(r'^edit-metric/(?P<metric_id>[0-9]+)/$', dashboard_views.edit_metric, name="edit_metric"),
    url(r'^delete/metric/(?P<metric_id>[0-9]+)/$', dashboard_views.delete_metric, name="delete_metric"),
    url(r'^program-metrics/(?P<program_id>[0-9]+)/$', dashboard_views.program_metrics_detail, name="program_metrics_detail"),
    url(r'^user-metrics/(?P<program_id>[0-9]+)/(?P<user_id>[0-9]+)/$', dashboard_views.user_metrics_detail, name="user_metrics_detail"),
    
    url(r'^edit-action-type/(?P<action_type_id>[0-9]+)/$', dashboard_views.edit_action_type, name="edit_action_type"),
    url(r'^delete/action-type/(?P<action_type_id>[0-9]+)/$', dashboard_views.delete_action_type, name="delete_action_type"),
    url(r'^edit-app/(?P<app_id>[0-9]+)/$', dashboard_views.edit_app, name="edit_app"),
    url(r'^delete/app/(?P<app_id>[0-9]+)/$', dashboard_views.delete_app, name="delete_app"),

    url(r'^accounts/login/$', auth_views.LoginView, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView, {'next_page': 'login'}, name='logout'),
    url(r'^accounts/verifyEmail/$', customauth_views.verifyEmail,  name='verifyEmail'),
    url(r'^accounts/reset-password/$', customauth_views.resetEmail,  name='resetEmail'),
    
    url(r'^integrations/$', TemplateView.as_view(template_name='integrations.html'), name="integrations"),
    url(r'^api-docs/$', TemplateView.as_view(template_name='api-docs.html'), name="api-docs"),

    url(r'^$', TemplateView.as_view(template_name='landing.html'), name='landing_page'),
    url(r'^profile/$', customauth_views.ProfileView, name="profile"),
    url(r'^profile/css-submit/$', customauth_views.Change_CSS_URL, name="change_css"),
    url(r'^profile/image-upload/$', customauth_views.Image_Upload, name="image_upload"),
    url(r'^css-test/(?P<app_id>[0-9]+)/$', app_views.CSSView, name="css-view"),
    
    url(r'^payment/paypal-test/$', payment_views.paypal_payment, name="paypal_payment"),
    url(r'^payment/view-payments/(?P<app_id>[0-9]+)/$', dashboard_views.dashboard_payments, name="dashboard_payments"),
    url(r'^payment/filter-payments/(?P<app_id>[0-9]+)/$', dashboard_views.dashboard_filter_payments, name="dashboard_filter_payments"),
    url(r'^payment/ledgers-by-payments/(?P<payment_id>[0-9]+)/$', dashboard_views.ledgers_by_payment, name="ledgers_by_payment"),
    
    #url(r'^payout/paypal-test/$', payment_views.paypal_payment, name="paypal_payment"),
    url(r'^payout/view-payouts/(?P<app_id>[0-9]+)/$', dashboard_views.dashboard_payouts, name="dashboard_payouts"),
    url(r'^payout/filter-payouts/(?P<app_id>[0-9]+)/$', dashboard_views.dashboard_filter_payouts, name="dashboard_filter_payouts"),
    #url(r'^payment/ledgers-by-payments/(?P<payment_id>[0-9]+)/$', dashboard_views.ledgers_by_payment, name="ledgers_by_payment"),
    

    #url(r'^payment/dwolla-test/$', payment_views.dwolla_payment, name="dwolla_payment"),
    url(r'^test-payments/$', TemplateView.as_view(template_name='test-payments.html'), name="test_payments"),
    #url(r'^subscription/$', subscription_views.SubscriptionCreateView.as_view(), name="create"),

    url(r'^action-type/create/$', action_type_views.CreateActionType, name="create_AT"),
    
    url(r'^filterMetrics/$', dashboard_views.filterMetrics, name="filterMetrics"),

    url(r'^testApp/$', TemplateView.as_view(template_name='testApp.html'), name="testApp"),

    url(r'^docs/', include_docs_urls(title='Appevate API')),

    #url(r'^fabrics/$',  onboarding_views.fabrics, name="create"),

    url(r'^subscription/(?P<app_id>[0-9]+)/$', TemplateView.as_view(template_name='subscription.html'), name='subscription'),
    url(r'^payout/(?P<app_id>[0-9]+)/$', dashboard_views.payouts, name='payouts'),
    url(r'^charge/(?P<app_id>[0-9]+)/$', dashboard_views.stripe_charge, name='stripe_charge'),
    
    url(r'^api/api-token-auth/', customauth_api_views.CustomAuthToken.as_view()),
    url(r'^api/verify-integration/', customauth_api_views.VerifyIntegration.as_view()),
    
    #url(r'^payments/', include('djstripe.urls', namespace="djstripe")),

    url(r'^custom_admin/manual-payout/', admin_views.admin_payouts, name="admin_payouts"),
    url(r'^custom_admin/manual-payments/', admin_views.admin_payments, name="admin_payments"),
     
    url(r'^custom_admin/payout_report/', admin_views.admin_payout_report, name="admin_payout_report"),
    url(r'^custom_admin/payout/filter-payouts/$', admin_views.admin_filter_payouts, name="admin_filter_payouts"),
    url(r'^custom_admin/payment_report/', admin_views.admin_payment_report, name="admin_payment_report"),
    url(r'^custom_admin/payment/filter-payments/$', admin_views.admin_filter_payments, name="admin_filter_payments"),
    url(r'^custom_admin/user-report/$', admin_views.admin_user_report, name="admin_user_report"),
    url(r'^custom_admin/revenue-report/$', admin_views.admin_revenue_report, name="admin_revenue_report"),
    url(r'^payment/admin-pay/$', payment_views.admin_pay, name="admin_pay"),
    url(r'^custom_admin/unit-tests/$', admin_views.admin_unit_tests, name="admin_unit_tests"),
    url(r'^custom_admin/send-app-report/$', admin_views.send_app_report, name="send_app_report"),
    url(r'^custom_admin/erase-test-data/$', admin_views.erase_test_data, name="eraseTestData"),
  
    url(r'^custom_admin/run-test/$', admin_views.run_test, name="run_test"),
    url(r'^custom_admin/send-test-emails/$', admin_views.send_test_emails, name="send_test_emails"),

    url(r'^about-us/$', TemplateView.as_view(template_name='about-us.html'), name="about-us"),
    url(r'^learn-more/$', TemplateView.as_view(template_name='learn-more.html'), name="learn-more"),
    url(r'^terms-of-service/$', TemplateView.as_view(template_name='TOS.html'), name="tos"),
    url(r'^privacy-policy/$', TemplateView.as_view(template_name='privacy-policy.html'), name="privacy-policy"),
    url(r'^contact-us/$', admin_views.contact_us, name="contact_us"),
    url(r'^our-mission/$', TemplateView.as_view(template_name='our-mission.html'), name="how-it-works"),  
    url(r'^blog/$', TemplateView.as_view(template_name='blog.html'), name="blog"),  
    url(r'^market-research/$', TemplateView.as_view(template_name='market-research.html'), name="case-studies"),  
    url(r'^support/$', TemplateView.as_view(template_name='support.html'), name="support"),  
    url(r'^feature-list/(?P<plan_type>[\w]+)/$', onboarding_views.plan_view, name="plan_view"),
    url(r'^company-history/$', TemplateView.as_view(template_name='company-history.html'), name="case-studies"),  
    
    url(r'^FAQ/$', TemplateView.as_view(template_name='faq.html'), name="faq"),  
    

    url(r'^resetTestApp/$', app_views.reset_test_app, name="reset_test_app"),


    url(r'^dashboard/program/(?P<app_id>[0-9]+)/$', dashboard_views.programs_by_app, name="programs-by-app"),
    url(r'^dashboard/create-program/wizard/1/$', dashboard_views.create_program_1, name="create_program_1"),
    url(r'^dashboard/create-program/wizard/2/$', dashboard_views.create_program_2, name="create_program_2"),
    url(r'^dashboard/create-program/wizard/3/$', dashboard_views.create_program_3, name="create_program_3"),
         

    url(r'^dashboard/active-program/(?P<app_id>[0-9]+)/$', dashboard_views.active_program, name="active_program"),
    url(r'^dashboard/inactive-programs/(?P<app_id>[0-9]+)/$', dashboard_views.inactive_programs, name="inactive_programs"),
    url(r'^dashboard/webhooks/(?P<app_id>[0-9]+)/$', dashboard_views.webhooks, name="webhooks"),
    url(r'^dashboard/event-tracking/(?P<app_id>[0-9]+)/$', dashboard_views.event_tracking, name="event_tracking"),
    url(r'^dashboard/rewards-tracking/(?P<app_id>[0-9]+)/$', dashboard_views.rewards_tracking, name="rewards_tracking"),
    
    url(r'^dashboard/user-interface/(?P<app_id>[0-9]+)/$', dashboard_views.user_interface, name="user_interface"),
    url(r'^dashboard/custom-css/(?P<app_id>[0-9]+)/$', dashboard_views.custom_css, name="custom_css"),
    url(r'^dashboard/sample-templates/(?P<app_id>[0-9]+)/$', dashboard_views.sample_templates, name="sample_templates"),
    url(r'^dashboard/edit-program/(?P<program_id>[0-9]+)/$', dashboard_views.edit_program, name="edit_program"),
    
    url(r'^dashboard/integration-information/$', dashboard_views.integration_info, name="integration_info"),
    url(r'^dashboard/edit-password/$', dashboard_views.edit_password, name="edit_password"),
    url(r'^dashboard/delete-program/(?P<program_id>[0-9]+)/$', dashboard_views.delete_program, name="delete_program"),
    url(r'^dashboard/app-profile/$', dashboard_views.app_profile, name="app_profile"),
        

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
