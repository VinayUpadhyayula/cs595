from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json

class SentimentAnalysisTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('predict-sentiment')  #URL name from urlpatterns
        self.valid_text = {'text': 'This is a great day!'}

    def test_sentiment_analysis_text(self):
        """Test sentiment prediction with valid input text."""
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_text),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('prediction', response.json())  # Ensure 'prediction' is in the response