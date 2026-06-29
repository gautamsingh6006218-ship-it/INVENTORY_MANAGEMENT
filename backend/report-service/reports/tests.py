from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from reports.models import Report


class ReportListTests(TestCase):

    def setUp(self):
        # APIClient simulates HTTP requests without running a real server
        self.client = APIClient()
        self.url = '/api/reports/'

    def test_get_all_reports(self):
        # create two reports in test DB
        Report.objects.create(report_type='sales', status='completed', data={'total_sales': 5000}, created_by=1)
        Report.objects.create(report_type='inventory', status='completed', data={'total_items': 200}, created_by=2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should return both reports
        self.assertEqual(len(response.data), 2)

    def test_create_report(self):
        data = {
            'report_type': 'orders',
            'status': 'completed',
            'data': {'total_orders': 50, 'revenue': 10000},
            'created_by': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['report_type'], 'orders')
        # status should be what we sent
        self.assertEqual(response.data['status'], 'completed')

    def test_create_report_missing_fields(self):
        # report_type, data, created_by are required — should return 400
        data = {'report_type': 'sales'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReportDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create a report to use in all detail tests
        self.report = Report.objects.create(
            report_type='sales', status='completed',
            data={'total_sales': 5000, 'orders': 20}, created_by=1
        )
        self.url = f'/api/reports/{self.report.id}/'

    def test_get_single_report(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_type'], 'sales')

    def test_get_report_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.get('/api/reports/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_report(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # confirm it no longer exists in DB
        self.assertFalse(Report.objects.filter(id=self.report.id).exists())
