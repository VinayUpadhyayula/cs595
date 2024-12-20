from django.shortcuts import render
import pickle
from django.http import JsonResponse
import nltk
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
st = PorterStemmer()
lm = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))
PUNCTUATION = string.punctuation

with open('../sentiment_model.pkl', 'rb') as model_file:
    sentiment_model = pickle.load(model_file)

with open('../vectorizer.pkl', 'rb') as model_file:
    vectorizer = pickle.load(model_file)

# vectoriser = TfidfVectorizer(ngram_range=(1,2), max_features=500000)

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"  # other symbols
        u"\U000024C2-\U0001F251"  # enclosed characters
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def preprocess_text(text):
    # Remove stopwords
    text = " ".join([word for word in text.split() if word not in STOPWORDS])
    # Remove punctuation
    text = text.translate(str.maketrans('', '', PUNCTUATION))
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    #Emoji removal
    text = remove_emojis(text)
    return text

def stemming_on_text(data):
    stemmed_text = [st.stem(word) for word in data]
    return stemmed_text

def lemmatizer_on_text(data):
    lemmatized_text =  [lm.lemmatize(word) for word in data]
    return lemmatized_text

def tokenize_tweet(cleanedTweet):
    tokens = word_tokenize(cleanedTweet)
    return tokens

class SentimentAPIView(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        data = request.data
        input_text = data.get('text', '')
        
        # Preprocess the text
        cleaned_text = preprocess_text(input_text)

        tokens = word_tokenize(cleaned_text)

        stemmed_text = stemming_on_text(tokens)

        lemmatized_text = lemmatizer_on_text(stemmed_text)

        # vectoriser.fit(lemmatized_text)
        
        transformed_text = vectorizer.transform(lemmatized_text)
        #Faced a lot of issues to match the features, googled and understaood how to use the same vectorizer so used the same one loaded as pickel file
        #Below 3 indicates that that the same vectorizer has been used for transforming data before(during model training)
        #Also to undesrand that transformed single tweet text and the model also accepts same number of features.
        print(len(vectorizer.get_feature_names_out()))
        print(transformed_text.shape)
        print(sentiment_model.coef_.shape[1])

        #shape the clean text by transforming to be able to input it to the model - Done
        #Predict sentiment and classify based on prediction output - Done
        prediction = sentiment_model.predict(transformed_text)
        print(prediction)
        
        # # Return response
        # return JsonResponse({'sentiment': sentiment}, status=200)
        return JsonResponse({'prediction':prediction[0]},status =200)