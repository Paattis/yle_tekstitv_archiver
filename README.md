# yle_tekstitv_archiver
a simple python script (~~for python 3, haven't tested on 2, probably won't work~~ works on both python 2 and 3) that allows you to download all the YLE (Finland's national public-broadcasting company) teletext pages for archival purposes.

# instructions
* download the repository</br>
* run `tekstitv_archiver.py`</br>
* go see a movie, clean your home, play videogames or something (With lots of pages and subpages it will take a long time to get all the pages).

## arguments
`useknown` - use pages listed in the file knownpages.txt (100_01,100_02,100_04,200_01 etc.)</br>
`savenew`  - save found pages to knownpages.txt to save time in the future</br>
So for example if I wanted to use known pages and save myself time the command would be</br>
`python tekstitv_archiver.py useknown`</br>
and if I wanted to go through all possible pages get a list of existing pages it'd  be</br>
`python tekstitv_archiver.py savenew`

