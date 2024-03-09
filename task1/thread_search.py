from threading import Thread, RLock
from time import time 
import logging
import os
import pathlib

THREADS_COUNT=3
SEARCH_WORDS=['Richer', 'station', 'street', 'light']

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
result={}

lock = RLock()

class UsefulClass():
    def __init__(self, file_list, word_list,locker):
        self.file_list = file_list
        self.word_list = word_list
        self.locker = locker

    def __call__(self):
        for file_name in self.file_list:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    content=f.read()
                    for search_word in self.word_list:
                        res = content.find(search_word)
                        if res != -1:
                            logging.debug(f'Word {search_word} found in file {file_name}')
                            with self.locker:
                                result[search_word].append(file_name)
            except IOError:
                logging.debug(f'ERROR opening/reading file {file_name}')

if __name__ == '__main__':
    os.chdir("./book")
    files = [f for f in os.listdir() if os.path.isfile(f)]

    l_len=round(len(files)/3)
    result={word: [] for word in SEARCH_WORDS}
    th_files=[]
    threads = []
    timer=time()
    for i in range(THREADS_COUNT):
        th_files.append(files[i*l_len:(i+1)*l_len-1])
        t2 = UsefulClass(th_files[i],SEARCH_WORDS,locker = lock)
        thread = Thread(target=t2)
        thread.start()
        threads.append(thread)
    
    [el.join() for el in threads]
    
    print(f"Execution time: {time()-timer}")
    
    print("RESULT:")
    print(result)
    
    print("Completed")
    
