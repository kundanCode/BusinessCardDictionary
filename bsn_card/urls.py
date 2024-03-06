from django.urls import path
from . import views
from django.conf import settings
# from django.conf.urls.static import static
# from myapp.views import generate_pdf_report

app_name = 'bsn_card'
urlpatterns = [

    path('', views.home, name='bsn_card'),
    path('bsn_card_table',views.bsn_card_table, name="s"),
    # path('bsn_card_table_new', views.bsn_card_table_new, name="s"),
    # path("rt", views.generate_pdf_report ),

    path("saving_card", views.saving_card, name= "saving_Card"),
    path("report_gen", views.generate_csv_report, name="report")
    # path('pdf-report/', generate_pdf_report, name='pdf_report'),
    # path("testing", views.your_view)
    # path()
]


# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)