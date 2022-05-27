from django.core.management.base import BaseCommand, CommandError
from api.models import Nonogram
from django.conf import settings
from datetime import datetime
import random, os

def load_words():
    word_file_path = os.path.join(settings.BASE_DIR, 'words_alpha.txt')
    with open(word_file_path) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

def get_word_combos(masterword):
    result = []
    #result = set()
    def nextLetter(a,l,key,used):
        if len(key) == l:
            return
        for i in range(0,l):
            print(used)
            if not ''+str(i) in used:
            #if not used.startswith(''+str(i)):
                result.append(key+a[i])
                nextLetter(a,l,key+a[i],used + str(i))
    a=masterword
    l=len(a)
    for i in range(0,len(a)):
        result.append(a[i])
        nextLetter(a, l, a[i], '' + str(i))
    return result


# if __name__ == '__main__':
#     english_words = load_words()
#     nine_letter_words = [word for word in english_words if len(word) == 9]
#     #print('Nine letter words',nine_letter_words,len(nine_letter_words))
#     random_nine_letter = random.choice(nine_letter_words)
#     #print('random word: ',random_nine_letter)
#     test_word = "muscle"
#     all_combos = set(get_word_combos(test_word))
#     actual_words = [word for word in all_combos if word in english_words and len(word) > 2]
#     print('Actual Words', actual_words)
    
class Command(BaseCommand):
    help = 'Create a nonogram, specify the number you want to create'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def handle(self, *args, **options):
        #SET LIMIT OF HOW MANY
        if options['number'] not in range(1,51):
            self.stdout.write(self.style.ERROR('Minumum of 1 and maximum 50 words allowed.'))
            return
        #Timer
        start_time = datetime.now()
        #Get the dictionary
        dictionary = load_words()
        #Get sample of 9 letter words according to argument passed
        nine_letter_words = [word for word in dictionary if len(word) == 9]
        word_list = random.sample(nine_letter_words,options['number'])
        #Check the database if it has already got any of these words
        exisiting_words = Nonogram.objects.all().values('word')
        existing_words_list = [ word['word'] for word in exisiting_words]
        filtered_word_list = [word for word in word_list if word not in existing_words_list]
        for nine_letter_word in filtered_word_list:
            all_combos = set(get_word_combos(nine_letter_word))
            actual_words = [word for word in all_combos if word in dictionary and len(word) > 2]
            Nonogram.objects.create(
                word = nine_letter_word,
                combos = actual_words
            )
        self.stdout.write(self.style.SUCCESS('Added ' + str(len(filtered_word_list)) + ' words, here they are:' ))
        for word in filtered_word_list:
            self.stdout.write(self.style.SUCCESS(word))
        #Report length of time taken
        end_time = datetime.now()
        duration = end_time - start_time
        seconds = duration.total_seconds()
        # hours = seconds % 3600
        # minutes = (seconds - (hours * 3600)) % 60
        # seconds = seconds % 60
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        self.stdout.write(self.style.SUCCESS('Time taken = {}:{}:{}'.format(hours,minutes,seconds)))
        return 
        