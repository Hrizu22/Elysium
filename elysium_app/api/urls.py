
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from elysium_app.api.views import(StockListAV, StockDetailAV,
                                   ClientInfoAV,ClientInfoDetailAV,ReviewList,ReviewDetail,ReviewCreate,
                                   ClientInfoVS, UserReview,StockListGV)
# from elysium_app.api.views import ReviewListVS

router = DefaultRouter()
router.register('stream',ClientInfoVS,basename='clientInfo-list')

urlpatterns = [
    path('shares/',StockListAV.as_view(),name='Portfolio'),
    path('shares/<int:pk>/',StockDetailAV.as_view(),name='portfolio-detail'),
    # path('stream/',ClientInfoAV.as_view(),name='client-info'),
    # path('stream/<int:pk>/',ClientInfoDetailAV.as_view (),name='client-info-detail'),
    path('list2/', StockListGV.as_view(), name='stock-list'),
    
    path('', include(router.urls)),
    path('<int:pk>/review/',ReviewList.as_view(),name='client-info-detail'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),
    
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    # path('stream/review/',ReviewList.as_view(),name='client-info-detail'),
    # path('stream/review/<int:pk>',ReviewDetail.as_view(),name='review-detail')
    path('reviews/',UserReview.as_view(),name='review-detail'),
]
    
