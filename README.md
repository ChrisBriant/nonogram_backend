# nonogram_backend

This is a rest API created using the Django Framework for hosting and soliving nonograms.

A nonogram as a 9 letter anagram with a special letter set.

The API is intended for use for a front end puzzle game where the player needs to figure out as many word combinations as possible. Scoring is based on numbers of letters guessed that are valid English words and inclusion of the special character.

It has a part which can generate the nonogram data by looking up 9 letter words from the dictionary file and then finding every combination.

Sources:

For the dictionary generation code I used the dictionary and referenced the code in:

https://github.com/dwyl/english-words


For the algorithm to get the word combinations I used the code in the second answer from the post below and converted the code from JavaScript to Python.

https://stackoverflow.com/questions/2439412/algorithm-to-generate-all-possible-letter-combinations-of-given-string-down-to-2