from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from apps.product.views import CatalogView, CategoryView, ProductView, RecipeView, RecipesView
from apps.cart.views import CartView, NewOrder, print_order_view
from apps.userprofile.views import LoginView, RegistrationView, Logout
from django.conf import settings
from django.views.generic import TemplateView
from apps.product.admin_views import get_product
from apps.cart.s import sCart


urlpatterns = patterns('',
    (r'^admin_get_product/', get_product),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'', include('social_auth.urls')),
    (r'^$', CatalogView.as_view()),
    (r'search/', CatalogView.as_view()),
    (r'category/', CategoryView.as_view()),
    (r'product/', ProductView.as_view()),
    (r'recipe/', RecipeView.as_view()),
    (r'recipes/', RecipesView.as_view()),
    (r'cart/', CartView.as_view()),
    (r'login/', LoginView.as_view()),
    (r'logout/', Logout.as_view()),
    (r'registration/', RegistrationView.as_view()),
    (r'^new_order/', NewOrder.as_view()),
    url(r'^google2f5167f8caed758e.html', TemplateView.as_view(template_name='google2f5167f8caed758e.html')),
    url(r'^print_order/', print_order_view),

    url(r'^s/cart.html', sCart.as_view()),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
    url(r'^celiac/$', 'flatpage', {'url': '/celiac/'}, name='celiac'),
    url(r'^shipping/$', 'flatpage', {'url': '/shipping/'}, name='shipping'),
    url(r'^contacts/$', 'flatpage', {'url': '/contacts/'}, name='contacts'),
)

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns += patterns('',
    #     url(r'^__debug__/', include(debug_toolbar.urls)),
    # )
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
