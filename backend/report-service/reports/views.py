from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from reports.models import Report
from reports.serializers import ReportSerializer

CACHE_KEY = 'reports:list'


@api_view(['GET', 'POST'])
def report_list(request):
    if request.method == 'GET':
        cached = cache.get(CACHE_KEY)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        cache.set(CACHE_KEY, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def report_detail(request, pk):
    try:
        report = Report.objects.get(pk=pk)
    except Report.DoesNotExist:
        return Response({'message': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    if request.method == 'DELETE':
        report.delete()
        cache.delete(CACHE_KEY)
        return Response({'message': 'Report deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
