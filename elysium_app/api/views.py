# from django.shortcuts import get_object_or_404
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


from elysium_app.models import Stock,ClientInfo,Review
from elysium_app.api.serializers import StocksSerializer,ClientInfoSerializer,ReviewSerializer
from elysium_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from elysium_app.api.pagination import StockListPagination,StockListLOPagination,StockListCPagination

# class ReviewListVS(viewsets.ViewSet):
#     def list(self,request):
#         queryset = ClientInfo.objects.all()
#         serializer = ClientInfoSerializer(queryset,many=True)
#         return Response(serializer.data)
#     def retrieve(self,request,pk=None):
#         queryset = ClientInfo.objects.all()
#         holder = get_object_or_404(queryset,pk=pk)
#         serializer = ClientInfoSerializer(holder)
#         return Response(serializer.data)
    
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

# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin,
#                     mixins.CreateModelMixin,
#                     generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     # def delete(self, request, *args, **kwargs):
#     #     return self.destroy(request, *args, **kwargs)

class ClientInfoVS(viewsets.ModelViewSet):
    queryset = ClientInfo.objects.all()
    serializer_class = ClientInfoSerializer
    permission_classes = [IsAdminOrReadOnly]

class ClientInfoAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    def get(self,request):
        info = ClientInfo.objects.all()
        serializer = ClientInfoSerializer(info,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = ClientInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.data)
        
class ClientInfoDetailAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            info=ClientInfo.objects.get(pk=pk)
        except ClientInfo.DoesNotExist:
            return Response({'Error':'Client not found'},status=status.HTTP_404_NOT_FOUND)
        serializer= ClientInfoSerializer(
            info,context={'request':request})
        return Response(serializer.data)
        
    def put(self,request):
        
        serializer=ClientInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        info = ClientInfo.objects.get(pk=pk)
        info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StockListGV(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StocksSerializer
    pagination_class = StockListCPagination
    

class StockListAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    def get(self,request):
        stocks =Stock.objects.all()
        serializer = StocksSerializer(stocks,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=StocksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StockDetailAV(APIView):
    permission_class = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            stock=Stock.objects.get(pk=pk)
        except Stock.DoesNotExist:
            return Response({'Error':'Stock not found'},status=status.HTTP_404_NOT_FOUND)  
        serializer = StocksSerializer(stock)
        return Response(serializer.data)
    
    def put(self,request,pk):
        serializer=StocksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        stocks = Stock.objects.get(pk=pk)
        stocks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

