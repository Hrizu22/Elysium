from rest_framework.routers import DefaultRouter
from django.urls import path,include
from elysium_app.api.views import(StockListAV, StockDetailAV,
                                   PlatformInfoAV,PlatformInfoDetailAV,ReviewList,ReviewDetail,ReviewCreate,
                                   PlatformInfoVS, UserReview,StockListGV)
# from elysium_app.api.views import ReviewListVS

router = DefaultRouter()
router.register('stream',PlatformInfoVS,basename='PlatformInfo-list')

urlpatterns = [
    path('shares/',StockListAV.as_view(),name='Portfolio'),
    path('<int:pk>/',StockDetailAV.as_view(),name='portfolio-detail'),
    
    path('list2/', StockListGV.as_view(), name='stock-list'),
    # path('stream/',PlatformInfoAV.as_view(),name='client-info'),#client-info
    # path('stream/review/',ReviewList.as_view(),name='client-info-detail'),
    # path('stream/review/<int:pk>',ReviewDetail.as_view(),name='review-detail')
    # path('stream/<int:pk>/',PlatformInfoDetailAV.as_view (),name='client-info-detail'),
    
    path('', include(router.urls)),
    
    path('<int:pk>/review/',ReviewList.as_view(),name='platform-info-detail'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),
    
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    
    path('reviews/',UserReview.as_view(),name='review-detail'),
]
    
