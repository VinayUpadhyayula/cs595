from django.shortcuts import render
import pickle
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from nltk.corpus import stopwords
import string
import re
import nltk
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))
PUNCTUATION = string.punctuation

with open('../sentiment_model.pkl', 'rb') as model_file:
    sentiment_model = pickle.load(model_file)

def preprocess_text(text):
    # Remove stopwords
    text = " ".join([word for word in text.split() if word not in STOPWORDS])
    # Remove punctuation
    text = text.translate(str.maketrans('', '', PUNCTUATION))
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    return text

# Create your views here.
class SentimentAPIView(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        data = request.data
        input_text = data.get('text', '')
        
        # Preprocess the text
        cleaned_text = preprocess_text(input_text)
        # Predict sentiment
        prediction = sentiment_model.predict([cleaned_text])
        
        # Convert prediction output (assuming model returns 0 for negative, 1 for positive)
        sentiment = 'Positive' if prediction[0] == 1 else 'Negative'
        
        # Return response
        return JsonResponse({'sentiment': sentiment}, status=200)