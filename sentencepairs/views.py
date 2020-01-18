from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from google.cloud import translate

from sentencepairs.models import Sentencepairs
from sentencepairs.serializers import SentencepairsSerializer


@api_view(['GET', 'POST'])
def sentencepairs_list(request):
	if request.method == "GET":
		sp_list = Sentencepairs.objects.all()
		serializer = SentencepairsSerializer(sp_list, many=True)
		return Response(serializer.data)
	
	if request.method == "POST":
		serializer = SentencepairsSerializer(data=request.data)
		if serializer.is_valid():
			text = serializer.validated_data.get('text')
			sample_translate_text(text, 'ja', 'abhinavblog-1391d')
			# serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def sample_translate_text(text, target_language, project_id):
    """
    Translating Text

    Args:
      text The content to translate in string format
      target_language Required. The BCP-47 language code to use for translation.
    """

    client = translate.TranslationServiceClient.from_service_account_json('/Users/abhinavbhandari/Documents/Coursera/djangoprojects/highlation/AbhinavBlog-44581c15ad5e.json')

    # TODO(developer): Uncomment and set the following variables
    # text = 'Text you wish to translate'
    # target_language = 'fr'
    # project_id = '[Google Cloud Project ID]'
    contents = [text]
    parent = client.location_path(project_id, "global")

    response = client.translate_text(
        parent=parent,
        contents=contents,
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code='en-US',
        target_language_code=target_language)
    # Display the translation for each input text provided
    for translation in response.translations:
        print(u"Translated text: {}".format(translation.translated_text))
