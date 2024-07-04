from django.urls import path, include

from . import views

app_name = 'djit_ripd'

urlpatterns = [
    path('<str:item>/list/',            views.index,    name='ripd'),
    path('<str:item>/read/<int:id>',    views.read,     name='ripd_read'),
    path('<str:item>/insert/',          views.insert,   name='ripd_insert'),
    path('<str:item>/patch/<int:id>',   views.patch,    name='ripd_patch'),
    path('<str:item>/put/<int:id>',     views.put,      name='ripd_put'),
    path('<str:item>/delete/<int:id>',  views.delete,   name='ripd_delete'),
]
