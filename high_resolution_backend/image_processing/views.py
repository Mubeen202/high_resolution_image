from .serializers import ImageSerializer
from .models import Images
from rest_framework import viewsets, status, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
# Create AI code.
import torch
from PIL import Image
import numpy as np
from RealESRGAN import RealESRGAN
import io
import base64
import os
import uuid
import shutil

import spacy
import random
import nltk
from nltk.corpus import wordnet as wn
from django.http import HttpResponse

# Ensure NLTK resources are downloaded
nltk.download('wordnet')

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

def get_synonym(word):
    """
    Get a synonym for a given word using WordNet with the same part of speech.

    Args:
    - word (str): The input word for which a synonym is desired.

    Returns:
    - str: A synonym for the input word with the same part of speech, or the original word if no synonym is found.
    """
    # Process the word with spaCy to get its part of speech
    pos = nlp(word)[0].pos_
    print("POS from spaCy:", pos)

    # Get synsets (sets of synonyms) for the word
    synsets = wn.synsets(word)

    # If there are synsets available
    if synsets:
        # Filter synsets by part of speech
        synsets = [synset for synset in synsets if synset.pos() == pos]

        if synsets:
            # Get synonyms from all synsets
            synonyms = [synonym for synset in synsets for synonym in synset.lemma_names() if synonym != word]

            # Choose a random synonym
            if synonyms:
                synonym = random.choice(synonyms)
                print("Selected synonym:", synonym)
                return synonym.replace("_", " ")  # Replace underscores with spaces in multi-word synonyms

    # If no synonym is found, return the original word
    print('no word changes')
    return word




def enhance(img_path, scale):
    generated_uuid = uuid.uuid4()
    print(generated_uuid)
    assert scale in [2, 4], f"Scale should be 2 or 4"
    weight_path = f"./weights/x{scale}.pth"
    device = torch.device('cpu')
    model = RealESRGAN(device, scale=scale)
    model.load_weights(weight_path)
    image = Image.open(img_path).convert('RGB')
    save_dir = f"media/output/{generated_uuid}.png"
    sr_image = model.predict(image)
    sr_image.save(save_dir)    
    return save_dir


class ImageView(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def image_to_base64(self, image):
        # Convert the image to a byte stream
        with io.BytesIO() as buffer:
            image.save(buffer, format="JPEG")
            byte_stream = buffer.getvalue()
        
        # Encode the byte stream using base64
        encoded_image = base64.b64encode(byte_stream).decode('utf-8')
        
        return encoded_image

    
    
    
    def get(self, request, *args, **kwargs):
            posts = Images.objects.all()
            serializer = ImageSerializer(posts, many=True)
            return Response(serializer.data)


    def rephrase(self, request, *args, **kwargs):
        original_sentence = "TThe speedy brown fox jumps over the lazy dog<br>The speedy brown fox jumps over the lazy dog"

        # Generate four rephrased sentences
        rephrased_sentences = []

        for _ in range(4):
            # Tokenize the original sentence
            doc = nlp(original_sentence)

            # Choose a random word to replace
            replace_index = random.randint(0, len(doc) - 1)
            replace_word = doc[replace_index].text

            # Generate a new word (synonym) to replace with
            new_word = get_synonym(replace_word)

            # Replace the word in the sentence
            rephrased_tokens = [new_word if i == replace_index else token.text for i, token in enumerate(doc)]
            rephrased_sentence = " ".join(rephrased_tokens)
            rephrased_sentences.append(rephrased_sentence)
        return Response({
                'data': "<br>".join(rephrased_sentences),
            }, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
         # Serialize the image data
        image_serializer = ImageSerializer(data=request.data)
        
        if image_serializer.is_valid():
            # Save the image data
            image_serializer.save()
            
            # Get the uploaded image file
            
            imagee = request.FILES['image']
            file_name = str(imagee)
            print(f'[INFO] File Name: {file_name}')

            # Define the directory where you want to save the image
            save_dir = "media/images/"

            # Ensure that the directory exists, create it if it doesn't
            os.makedirs(save_dir, exist_ok=True)

            # Define the path where the image will be saved
            file_path = os.path.join(save_dir, file_name)

            # Call the enhance function
            result_img = enhance(file_path, int(image_serializer.data['model_number']))
            
            # Convert the enhanced image to base64
            print('result', result_img)
            
            
            # Return success response
            # Return the serialized data along with the enhanced image
            return Response({
                'data': image_serializer.data,
                "High_resolution_image": result_img
            }, status=status.HTTP_201_CREATED)

        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        # image_serializer = ImageSerializer(data=request.data)
        # if image_serializer.is_valid():
        #     image_serializer.save()
        #     #  array = np.array([1, 2, 3], dtype=np.int32)
        #     imagee = request.FILES['image']
        #     # file_name = str(imagee)
        #     # print(f'[INFO] File Name: {file_name}')
        #     # with open("media/images/"+file_name, 'wb+') as f:
        #     #     for chunk in imagee.chunks():
        #     #         f.write(chunk)
        #     # img = Image.open(imagee)
        #     # print('jjjjjj', imagee)

        #     result_img=enhance(imagee, int(image_serializer.data['model_number']))
        #     print('*****************************************break************************', image_serializer.data['model_number'])
        #     return Response({'data':image_serializer.data,
        #      "High Resolution Image": result_img
        #      }, status=status.HTTP_201_CREATED)
        # else:
        #     print('error', image_serializer.errors)
        #     return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)