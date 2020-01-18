from rest_framework import serializers
from sentencepairs.models import Sentencepairs 

class SentencepairsSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	text = serializers.CharField(required=False, allow_blank=True)

	def create(self, validated_data):
		"""
		"""
		return Sentencepairs.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		"""
		instance.text = validated_data.get('text', instance.text)
		return instance
