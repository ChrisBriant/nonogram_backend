from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import *
from .permissions import ValidApiKey
import random


#Supporting Functions

def random_string(range_max,string=None,unique=False):
    if not string:
        string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789?><.:;@#()'
    random_string = ''
    for i in range(0,range_max):
        new_char = random.choice(string)
        #If unique param is sent we want to remove the chosen character
        if unique:
            partitioned = string.rpartition(new_char)
            string = partitioned[0] + partitioned[2]
        random_string += new_char
    return random_string

def get_results_for_word_length(word_length,words,special,combos):
    #Get only one instance of each word
    unique_words = list(set(words))
    score = 0
    for word in unique_words:
        if word in combos:
            if word_length == 9:
                score = 150
            else:
                if word.find(special) != -1:
                    score += word_length*2
                else:
                    score += word_length
    return {
        'result': {
            'score' : score,
            'scoredWords' : [word for word in unique_words if word in combos],
            'unscoredWords' : [word for word in unique_words if word not in combos],
            'wordsChecked' : words,
        }
    }

#Returns a dictionary object with the scores for the actual solution
def score_solution(word_list,special):
    response_data = {
        'result' : {},
        'totalScore' : 0,
        'allPossibleWords' : word_list,
    }
    for i in range(3,10):
        result = get_results_for_word_length(i,[word for word in word_list if len(word) == i],special,word_list)
        response_data['result'][str(i)+'letter'] = result['result']
        response_data['totalScore'] += result['result']['score']
    return response_data
        



#Serializers

class NonogramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nonogram
        fields = ('id','word','combos')

#VIEWS
@api_view(['GET'])
def test(request):
    print('I am a test', random_string(128))    
    return Response("hello", status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([ValidApiKey])
def get_nonogram(request):
    words = Nonogram.objects.all().values('word','id')
    random_word = random.choice(words)
    #randomize the letters in the word
    random_word['word'] = random_string(9,random_word['word'],True)
    return Response(random_word, status=status.HTTP_200_OK)

############# SCORING RULES ##################
# must have 3 or more letters
# 1 point for letter
# If contains special character multiply by number of letters
# If nine letter words score 150

@api_view(['GET'])
@permission_classes([ValidApiKey])
def score_word(request):
    #Get the nonogram
    try:
        nonogram = Nonogram.objects.get(id=request.data['id'])
    except Exception as e:
        print(e)
        return Response({'message':'Word does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #Collect from payload
    word_list = request.data.get('word_list')
    special_letter = request.data.get('special')
    if not special_letter:
        return Response({'message':'Please provide the special character'}, status=status.HTTP_400_BAD_REQUEST)
    if word_list:
        #Setup dictionary result object
        payload = {
            'id' : nonogram.id,
            'solvedWord' : nonogram.word,
            'sentWord' : request.data['word'],
            'specialLetter' : special_letter,
            'result' : {},
            'totalScore' : 0,
            'scoredWords' : [word for word in word_list if word in nonogram.combos],
            'unscoredWords' : [word for word in word_list if word not in nonogram.combos],
            'sentWords' : word_list,
            'solution' : score_solution(nonogram.combos,special_letter),
        }
        for i in range(3,10):
            print(i)
            result = get_results_for_word_length(i,[word for word in word_list if len(word) == i],special_letter,nonogram.combos)
            payload['result'][str(i)+'letter'] = result['result']
            payload['totalScore'] += result['result']['score']
    else:
        return Response({'message':'Please provide a word list'}, status=status.HTTP_400_BAD_REQUEST)
    #words = Nonogram.objects.all().values('word')
    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([ValidApiKey])
def get_solution(request):
    try:
        nonogram = Nonogram.objects.get(id=request.data['id'])
    except Exception as e:
        print(e)
        return Response({'message':'Word does not exist'}, status=status.HTTP_404_NOT_FOUND)
    return Response(NonogramSerializer(nonogram).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([ValidApiKey])
def get_solution_with_score(request):
    try:
        nonogram = Nonogram.objects.get(id=request.data['id'])
    except Exception as e:
        print(e)
        return Response({'message':'Word does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.data.get('special'):
        special_letter = request.data['special']
    else:
        return Response({'message':'No speical letter has been sent.'}, status=status.HTTP_404_NOT_FOUND)
    response_data = {
        'id' : nonogram.id,
        'word' : nonogram.word,
        'solution' : score_solution(nonogram.combos,special_letter)
    }
    print(response_data)
    return Response(response_data, status=status.HTTP_200_OK)

