from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from reports.models import Report
from reports.serializers import ReportSerializer

# Create your views here.

@api_view(['GET', 'POST'])

def report_list(request):
    if request.method == 'GET':
        # fetch all reports from DB
        reports = Report.objects.all()
        # many=True tells serializer multiple objects are being converted to JSON
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # pass incoming JSON data to serializer for validation
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # saves new report to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'DELETE'])

def report_detail(request, pk):
    try:
        # pk comes from the URL — e.g. /api/reports/1/ → pk=1
        report = Report.objects.get(pk=pk)
    except Report.DoesNotExist:
        # return 404 if no report with that ID exists in DB
        return Response({'message': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # no data= argument — just reading, not updating
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    if request.method == 'DELETE':
        report.delete()  # removes the row from DB
        return Response({'message': 'Report deleted successfully'}, status=status.HTTP_204_NO_CONTENT)  
    