from rest_framework import serializers
from elysium_app.models import  Stock,PlatformInfo,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user=  serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('holder',)

class StocksSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = Stock
        fields = "__all__"

    def create(self, validated_data):
        platform_data = validated_data.pop('platform')
        platform, created = PlatformInfo.objects.get_or_create(name=platform_data['name'])
        validated_data['platform'] = platform
        stock = Stock.objects.create(**validated_data)
        return stock


class PlatformInfoSerializer(serializers.ModelSerializer):
    holder = StocksSerializer(many=True,read_only=True)
    class Meta:
        model = PlatformInfo
        fields ="__all__"



        