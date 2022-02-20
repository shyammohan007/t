from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Max

from bank_app.serializers import *
from datetime import datetime


class TransactionListAPI(APIView):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self,request, date):
        transaction_date = datetime.strptime(date,'%d-%m-%y')
        qs = self.queryset.filter(date__date=transaction_date)
        serializer = self.serializer_class(qs, many=True)

        return Response({'data': serializer.data, 'message':'Transactions listed successfully' },
                            status=status.HTTP_200_OK)

    def post(self,request):

        print(request.data)

        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            trans = serializer.save()
        return Response(
                {"data": TransactionSerializer(trans).data , "message": "Successfully created transaction"},
                status=status.HTTP_200_OK)


class BalanceAPI(APIView):

    serializer_class = BalanceSerializer

    def get(self,request,date):
        transaction_date = datetime.strptime(date,'%d-%m-%y')
        queryset = Account.objects.all()
        trans_id = []
        for account in queryset:
            try:
                t_id = Transaction.objects.filter(date__date=transaction_date,account=account).order_by('date').last()
                if t_id:
                    trans_id.append(t_id.id)
            except Exception as e:
                continue
        trans = Transaction.objects.filter(id__in=trans_id)
        serializer = self.serializer_class(trans, many=True)

        return Response({'data': serializer.data, 'message':'Balance shown successfully' },
                            status=status.HTTP_200_OK)


class TransactionDetailAPI(APIView):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, pk):
        try:
            transaction = self.queryset.get(id=pk)
        except Transaction.DoesNotExist:
            return Response({"message": "Transaction details not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(transaction)

        return Response({'data': serializer.data, 'message':'Transaction details listed successfully' },
                            status=status.HTTP_200_OK)


