from datetime import datetime
from rest_framework import serializers
from django.core.exceptions import ValidationError

from bank_app.models import *


class TransactionSerializer(serializers.ModelSerializer):

    account_number = serializers.IntegerField(source="account.account_number")
    date = serializers.SerializerMethodField()
    value_date = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'date','account_number', 'transaction_detail', 'value_date', 'currency',
            'transaction_type', 'transaction_amount', 'balance_amount'
        ]

    def get_date(self,obj):
        return obj.date.date()

    def get_value_date(self,obj):
        try:
            return obj.value_date.date()
        except:
            return obj.value_date
        

class BalanceSerializer(serializers.ModelSerializer):

    account_number = serializers.IntegerField(source="account.account_number")
    date = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'date', 'account_number', 'balance_amount'
        ]

    def get_date(self,obj):
        return obj.date.date()

class TransactionCreateSerializer(serializers.ModelSerializer):

    account_number = serializers.IntegerField(source="account.account_number",allow_null=False)
    transaction_detail = serializers.CharField(allow_null=False)
    transaction_type = serializers.CharField(allow_null=False)
    transaction_amount = serializers.FloatField(allow_null=False)
    value_date = serializers.DateField(allow_null=False)

    class Meta:
        model = Transaction
        fields = [
            'account_number','transaction_detail','transaction_type','transaction_amount',
            'value_date'
        ]

    def validate_transaction_type(self,transaction_type):
        trans_type = ['CR','DR']
        if transaction_type in ['CR','DR']:
            return transaction_type
        else:
            raise ValidationError('Incorrect transaction type')
    
    def validate_account_number(self,account_number):
        try:
            account = Account.objects.get(account_number=account_number)
            return account_number
        except Account.DoesNotExist:
            raise ValidationError('Account number does not exist')
    
    def create(self, validated_data):
        account_num = validated_data['account'].get('account_number')
        account = Account.objects.get(account_number=account_num)
        trans = Transaction.objects.create(
            account = account,
            date = datetime.now(),
            transaction_detail = validated_data['transaction_detail'],
            value_date = validated_data['value_date'],
            transaction_type = validated_data['transaction_type'],
            transaction_amount = validated_data['transaction_amount']
        )
        if trans.transaction_type == 'CR':
            trans.balance_amount = account.account_balance + trans.transaction_amount
        else:
            trans.balance_amount = account.account_balance - trans.transaction_amount
        trans.save()
        account.account_balance = trans.balance_amount
        account.save()

        return trans