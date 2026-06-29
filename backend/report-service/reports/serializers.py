from rest_framework import serializers
from reports.models import Report


# converts Report model to JSON and validates incoming report data from request
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        # tells serializer which model to work with
        model = Report
        # id and generated_at are auto generated — returned in response but not required in request
        fields = ['id', 'report_type', 'status', 'data', 'created_by', 'generated_at']
        