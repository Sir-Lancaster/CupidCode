from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Dater, Cupid, User, Message, Gig, Quest, Date, Feedback


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.password = make_password(user.password)
        user.save()
        return user


class DaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dater
        fields = '__all__'

    def create(self, validated_data):
        dater = Dater(**validated_data)
        dater.is_suspended = False
        dater.save()
        return dater


class CupidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupid
        fields = '__all__'

    def create(self, validated_data):
        cupid = Cupid(**validated_data)
        cupid.is_suspended = False
        cupid.save()
        return cupid


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = '__all__'


class GigSerializer(serializers.ModelSerializer):
    quest = QuestSerializer(many=False, read_only=True)

    class Meta:
        model = Gig
        fields = '__all__'


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'