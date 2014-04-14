import phan_proxy
import req_proxy
import ast
import logging 
from bs4 import BeautifulSoup
from lxml import html 
import time 
import glob
import os
import multiprocessing
from Queue import Queue
from threading import Thread

num_fetch_threads2 = 50
enclosure_queue2 = Queue()

num_fetch_threads = 10
enclosure_queue = multiprocessing.JoinableQueue()

#item_info = [link, target, cate, sub_cate, colour, price, gender, sku, item_link, item_image, item_size, item_title, item_sale]

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')


def my_strip(x):
    return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace(",", " ").strip()


def main(line, fle2):
    fle3 = "%s.csv" %(fle2[:-4])

    line = ast.literal_eval(line)

    page = req_proxy.main(line[8])

    soup = BeautifulSoup(page, "html.parser")
    meta_disc = soup.find("meta", attrs={"name":"description"}).get("content")

    title = soup.find("title").get_text()
    desc = soup.find("section", attrs={"id":"product-detail"})
    dte = time.strftime("%d:%m:%Y")
    status = " "
    spec = " "
    vender = "zovi.com"
    brand = "zovi"

    f = open(fle3, "a+")
    f.write(",".join(map(my_strip,  [line[7], line[11], line[0], line[5], line[2], 
                         line[3], brand, line[9], line[5], line[4], 
                         line[1], line[8], vender, title, meta_disc, line[10], 
                         desc, spec, dte, status])) + "\n")
    f.close()



def mainthread2(i, q):
    for line, fle2 in iter(q.get, None):
        try:

            main(line.strip(), fle2)
            logging.debug((line.strip(), fle2))

        except:
            f2 = open("page2_first_error_zovi.txt", "a+")
            print >>f2, line
            logging.debug("eror")
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()



def mainthreading(fle2):
    f = open(fle2)

    procs = []

    for i in range(num_fetch_threads2):
        procs.append(Thread(target=mainthread2, args=(i, enclosure_queue2,)))
        procs[-1].start()

    for line in f:
        enclosure_queue2.put((line,fle2))

    print '*** Main thread waiting'
    enclosure_queue2.join()
    print '*** Done'

    for p in procs:
        enclosure_queue2.put(None)

    enclosure_queue2.join()

    for p in procs:
        p.join()

    f.close()



def main_process2(i, q):
    for fle2 in iter(q.get, None):
        try:

            mainthreading(fle2)
            logging.debug(fle2)

        except:
            pass

        time.sleep(2)
        q.task_done()

    q.task_done()




def supermain():
    f = open("zovi_to_extract.txt")
    directory = f.read().strip()
    f.close()

    current_dir = os.getcwd()
    all_filepth = "%s/%s/*/*/*.doc" %(current_dir, directory)

    file_lsit = glob.glob(all_filepth)

    procs = []

    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=main_process2, args=(i, enclosure_queue,)))
        procs[-1].start()

    for fle in file_lsit:
        enclosure_queue.put(fle)

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()

    line = """['http://zovi.com/boys-tees', 'Boys', 'TEES', 'boys-tees', '', '251', 'B', 'A123RNB00901', 'http://zovi.com/black-skull-applique-t-shirt--A123RNB00901', 'http://d1yvqnuw46gd8y.cloudfront.net/z/prod/w/2/g/p/A123RNB00901/1_c.jpg', "['7-8 Y']", 'Black Skull Applique T-shirt', '10%']"""
    
    #main(line)






if __name__=="__main__":
    supermain()


   

