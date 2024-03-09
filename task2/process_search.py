from multiprocessing  import Process, Queue, current_process
from time import time 
import logging
import os
import pathlib

THREADS_COUNT=3
SEARCH_WORDS=['Richer', 'station', 'street', 'light']


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def search_worker(queue, file_list, word_list):
    for file_name in file_list:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                content=f.read()
                for search_word in word_list:
                    res = content.find(search_word)
                    if res != -1:
                        logger.debug(f'{current_process().name} Word {search_word} found in file {file_name}')
                        #with result.get_lock():
                        result = queue.get()
                        result[search_word].append(file_name)
                        queue.put(result)
        except IOError:
            logging.debug(f'ERROR opening/reading file {file_name}')

if __name__ == '__main__':
    os.chdir("./book")
    files = [f for f in os.listdir() if os.path.isfile(f)]

    l_len=round(len(files)/THREADS_COUNT)
    result={word: [] for word in SEARCH_WORDS}
    th_files=[]
    processes = []
    
    timer=time()
        
    queue = Queue()
    queue.put(result)
    
    processes = []
    for i in range(THREADS_COUNT):
        th_files.append(files[i*l_len:(i+1)*l_len-1])
        pr = Process(target=search_worker, kwargs={"queue" :queue, "file_list":th_files[i],"word_list":SEARCH_WORDS})
        pr.start()
        processes.append(pr)

    [pr.join() for pr in processes]
        
    print(f"Execution time: {time()-timer}")
    
    print("RESULT:")
    print(queue.get())
    
    print("Completed")
    
    