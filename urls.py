from django.urls import path, include

from . import views

app_name = 'djit_ripd'

urlpatterns = [

    path('<str:item_name>/',                views.htmx_handler,     name='htmx_handler'),
    path('<str:item_name>/items',           views.list_items,       name='htmx_handler_list_items'),
    path('<str:item_name>/item/<int:id>',   views.htmx_handler,     name='htmx_handler_id'),

]
