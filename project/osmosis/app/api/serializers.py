from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import App
from osmosis.utils import encrypt_val, decrypt_val

import logging
logger = logging.getLogger(__name__)


class VerificationSerializer(serializers.ModelSerializer):


    class Meta:
        model = App
        fields = ('api_key',)
        write_only_fields = ()
        read_only_fields = ()

class TokenSerializer(serializers.ModelSerializer):


    class Meta:
        model = App
        fields = ('api_key', 'api_secret')
        write_only_fields = ()
        read_only_fields = ()

class AppSerializer(serializers.ModelSerializer):

    #user = serializers.CharField(default='')
    #name = serializers.CharField(required=False)

    class Meta:
        model = App
        fields = ('id','name', 'url', 'css_url', 'owner', 'api_key', 'api_secret', 'stripe_id', 'stripe_account')
        write_only_fields = ()
        read_only_fields = ('api_secret', 'api_key')
"""
    def create(self):
    	logger.info('c')
    	return

    def is_valid(self):
    	logger.info('valid')
    	return

    def validate_api_secret(self, password1):
    	logger.info("val")
        if password1 != self.initial_data['password2']:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
    def initialize(self, parent, field_name):
    	logger.info('init')
    	return

    def to_native(self, obj):
    	logger.info('native')
    	super().to_native(obj)
    	return

    def get_field(self, model_field):
    	logger.info("get")
    	super().get_field(model_field)
    	return
"""
'''
	
	def to_internal_value(self, instance):
		"""Convert `username` to lowercase."""
		logger.info("here")
		ret = super().to_internal_value(instance)
		ret['api_secret'] = decrypt_val(ret['api_secret'])
		return ret

	def to_representation(self, instance):
		"""Convert `username` to lowercase."""
		logger.info("here rep")
		ret = super().to_representation(instance)
		ret['api_secret'] = ""#decrypt_val(ret['api_secret'])
		return ret

	def get_created(self, obj):
		logger.info("gt c")
		return encrypt_val(obj.api_secret)
	
	logger.info("test2")

	@property
	def data(self):
		loggr.info('data')
		data = super().data
		data['phone_numbers'].sort(key=lambda p: p['id'])
		
		return data

	def create(self, validated_data):
		logger.info('create')
		
		app = App(
		name=validated_data['name'],
		url=validated_data['url'],
		css_url=validated_data['css_url'],
		owner=validated_data['owner'],
		api_key=validated_data['api_key'],
		api_secret=encrypt_val(validated_data['name']),
		stripe_account=validated_data['name'],
		stripe_id=validated_data['name'],
		)
		user.set_password(validated_data['password'])
		user.save()
		return user
'''
    


