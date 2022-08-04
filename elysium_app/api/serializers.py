from rest_framework import serializers
from elysium_app.models import  Stock,ClientInfo,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user=  serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('holder',)

class StocksSerializer(serializers.ModelSerializer):
    # reviews= ReviewSerializer(many=True,read_only=True)
    platform = serializers.CharField(source = 'platform.name')
    
    stopLoss_stock=serializers.SerializerMethodField()
    class Meta:
        model = Stock
        fields = "__all__"
        #fields = ['id,'name']
        #exclude=['hold']
    
    def get_stopLoss_stock(self,object):
        stopLoss= 0.2 * (object.boughtFor)
        return stopLoss
    
    def validate_price(self,data):
        if data['boughtFor']==0:
            raise serializers.ValidationError("Stock price cannot be zero")    
        else:
            return data
        
    def validated_data(self,value):
        if len(value)<2:
            raise serializers.ValidationError("The name of the stock is too short")
        else:
            return value

class ClientInfoSerializer(serializers.ModelSerializer):
    holder = StocksSerializer(many=True,read_only=True)
    class Meta:
        model = ClientInfo
        fields ="__all__"



        