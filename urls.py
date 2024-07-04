from django.urls import path, include

from . import views

app_name = 'djit_ripd'

urlpatterns = [
    path('<str:item>/list',             views.basic_list,     name='list'),
    path('<str:item>/read/<int:id>',    views.basic_read,     name='read'),
    path('<str:item>/insert/',          views.basic_insert,   name='insert'),
    path('<str:item>/patch/<int:id>',   views.basic_patch,    name='patch'),
    path('<str:item>/put/<int:id>',     views.basic_put,      name='put'),
    path('<str:item>/delete/<int:id>',  views.basic_delete,   name='delete'),

    path('<str:item_name>/',            views.all_in_one,   name='all_in_one'),
    path('<str:item_name>/<int:id>',    views.all_in_one,   name='all_in_one_id'),
]
