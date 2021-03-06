from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from google.cloud import translate
import os
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
			translated_text = sample_translate_text(text, 'ja', 'abhinavblog-1391d')
			# serializer.save()
			response_data = create_sentence_pair_json(text, translated_text)
			
			# response_data = { 'translated_text': translated_text }
			return Response(response_data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_sentence_pair_json(text_en, text_jp):
	split_jp = text_jp.split("。")
	split_en = text_en.split(".")
	
	json_jp = {i: t.strip() for i, t in enumerate(split_jp) if t.strip() != ""}
	json_en = {i: t.strip() for i, t in enumerate(split_en) if t.strip() != ""}
	
	jp_to_en_map = {j: e for j, e in zip(json_jp.keys(), json_en.keys())}
	
	return {"json_jp": json_jp, "json_en": json_en, "jp_to_en_map": jp_to_en_map}


def sample_translate_text(text, target_language, project_id):
    """
    Translating Text

    Args:
      text The content to translate in string format
      target_language Required. The BCP-47 language code to use for translation.
    """
    cred_full_path = os.path.join(os.getcwd(), 'AbhinavBlog-44581c15ad5e.json') 
    client = translate.TranslationServiceClient.from_service_account_json(cred_full_path)

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
    return response.translations[0].translated_text
    # for translation in response.translations:
    #     print(u"Translated text: {}".format(translation.translated_text))
