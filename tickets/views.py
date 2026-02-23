from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Ticket
from .serializers import TicketSerializer
from rest_framework import status
from django.core.cache import cache
from django_redis import get_redis_connection


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ticket_list(request):

    # GET → LIST TICKETS
    if request.method == 'GET':
        cache_key = f"ticket_list_{request.get_full_path()}"
        cached_data = cache.get(cache_key)

        if cached_data:
            print("CACHE HIT (Redis used)")
            return Response(cached_data)

        ordering = request.query_params.get('ordering')
        search = request.query_params.get('search')
        category = request.query_params.get('category')
        status_param = request.query_params.get('status')

        tickets = Ticket.objects.all()

        # Filtering
        if category:
            tickets = tickets.filter(category=category)

        if status_param:
            tickets = tickets.filter(status=status_param)

        # Searching
        if search:
            tickets = tickets.filter(title__icontains=search)

        # Ordering
        if ordering:
            tickets = tickets.order_by(ordering)

        # Pagination (same as professor)
        paginator = PageNumberPagination()
        #page_size = 2
        paginated_tickets = paginator.paginate_queryset(tickets, request)

        serializer = TicketSerializer(paginated_tickets, many=True)
        response = paginator.get_paginated_response(serializer.data)

        cache.set(cache_key, response.data, timeout=60*5)

        print("CACHE MISS (Saved to Redis)")

        return response
    # POST → CREATE TICKET
    elif request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("ticket_list")
            return Response(serializer.data, status=201)
        return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def ticket_detail(request, pk):

    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=404)

    # GET ONE
    if request.method == 'GET':
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    # PUT UPDATE
    if request.method == 'PUT':
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            redis_conn = get_redis_connection("default")
            redis_conn.delete_pattern("ticket_list_*")
            return Response(serializer.data)
        return Response(serializer.errors)

    # PATCH (update status mainly)
    if request.method == 'PATCH':
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            redis_conn = get_redis_connection("default")

            redis_conn.delete_pattern("ticket_list_*")
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # DELETE
    if request.method == 'DELETE':
        ticket.delete()
        redis_conn = get_redis_connection("default")
        redis_conn.delete_pattern("ticket_list_*")  
        return Response({"message": "Ticket deleted successfully"}, status=204)
