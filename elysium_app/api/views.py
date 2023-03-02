from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import generics 
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import viewsets
# from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from elysium_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle


from elysium_app.models import Stock,PlatformInfo,Review
from elysium_app.api.serializers import StocksSerializer,PlatformInfoSerializer,ReviewSerializer
from elysium_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from elysium_app.api.pagination import StockListPagination,StockListLOPagination,StockListCPagination


    
class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes=[IsAuthenticated]
    # throttle_classes = [ReviewListThrottle]
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)



class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_class = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        holder = Stock.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(holder=holder, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if holder.number_rating == 0:
            holder.avg_rating = serializer.validated_data['rating']
        else:
            holder.avg_rating = (holder.avg_rating + serializer.validated_data['rating'])/2

        holder.number_rating = holder.number_rating + 1
        holder.save()

        serializer.save(holder=holder, review_user=review_user)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes=[IsAuthenticated]
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['review_user__username', 'active']
    
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(holder=pk)
        
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class= ReviewSerializer
    permission_class =[IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'

class PlatformInfoVS(viewsets.ModelViewSet):
    queryset = PlatformInfo.objects.all()
    serializer_class = PlatformInfoSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

class PlatformInfoAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    def get(self,request):
        info = PlatformInfo.objects.all()
        serializer = PlatformInfoSerializer(
            info, many=True, context={'request': request})
        
        return Response(serializer.data)
    def post(self,request):
        serializer = PlatformInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.data)
        
class PlatformInfoDetailAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    def get(self,request,pk):
        try:
            info=PlatformInfo.objects.get(pk=pk)
        except PlatformInfo.DoesNotExist:
            return Response({'Error':'Client not found'},status=status.HTTP_404_NOT_FOUND)
        
        serializer= PlatformInfoSerializer(
            info,context={'request':request})
        return Response(serializer.data)
        
    def put(self,request,pk):
        platform = PlatformInfo.objects.get(pk=pk)
        serializer=PlatformInfoSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        info = PlatformInfo.objects.get(pk=pk)
        info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StockListGV(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StocksSerializer
    pagination_class = StockListCPagination
    

class StockListAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    def get(self,request):
        stocks =Stock.objects.all()
        serializer = StocksSerializer(stocks,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StocksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StockDetailAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]
    
    def get(self,request,pk):
        try:
            stock=Stock.objects.get(pk=pk)
        except Stock.DoesNotExist:
            return Response({'Error':'Stock not found'},status=status.HTTP_404_NOT_FOUND)  
        
        serializer = StocksSerializer(stock)
        return Response(serializer.data)
    
    def put(self,request,pk):
        holding = Stock.objects.get(pk=pk)
        serializer=StocksSerializer(holding,data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        stocks = Stock.objects.get(pk=pk)
        stocks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

