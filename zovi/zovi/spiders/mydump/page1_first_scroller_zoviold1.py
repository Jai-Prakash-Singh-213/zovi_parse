#!/usr/bin/env python 
import phan_proxy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from lxml import html
import logging
import time 
import os 
from Queue import Queue
import threading 
import time

num_fetch_threads = 10
enclosure_queue = Queue()




logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")

    except WebDriverException:
        pass


def driver_scroller(driver):
    height = 0
    loop = True

    while loop is True:
        logging.debug("scrolling......")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 15).until( ajax_complete, "Timeout waiting for page to load")

        heightnow = driver.execute_script("return $(document ).height();")
        WebDriverWait(driver, 15).until( ajax_complete, "Timeout waiting for page to load")
        
        if heightnow == height:
            loop = False

        else:
            height = heightnow

    return driver



def tag_text(x):
    return str(x.get_text()).strip()



def main(directory, link, target, cate):

    directory2 = "%s/%s/%s" %(directory, target, cate)
    try:
        os.makedirs(directory2)
    except:
        pass

    filename = "%s/%s.doc" %(directory2, cate)
   
    f = open(filename, "a+")
   
    driver = phan_proxy.main(link)
    driver = driver_scroller(driver)
    
    page = driver.page_source

    driver.delete_all_cookies()
    driver.quit()

    soup = BeautifulSoup(page, "html.parser")

    item_box = soup.find("section", attrs={"id":"catalog"})
    items_list = item_box.find_all("div", attrs={"class":"item"})

    for item_tag in items_list:
        sub_cate = item_tag.get("data-tag")
	colour = item_tag.get("data-color")
	price = item_tag.get("data-price")
	gender = item_tag.get("data-gender")
	sku = item_tag.get("data-option")
	item_link = "http://zovi.com%s" %(item_tag.a.get("href"))
	item_image = "http:%s" %(item_tag.a.img.get("data-original"))

        item_size2 = item_tag.find("div", attrs={"class":"available-sizes"})
        try:
            item_size = item_size2.find_all("li", attrs={"class":""})
            item_size = str(map(tag_text, item_size)).replace(",", " ")
        except:
            item_size  = str(item_size2)
      
        item_title = str(item_tag.find("div", attrs={"class":"title"}).get_text()).replace(",", " ").strip()

        try:
            item_sale = item_tag.find("span", attrs={"class":"tags visible sale"}).get_text().strip()
        except:
            item_sale = " "
        
        item_info = [link, target, cate, sub_cate, colour, price, gender, 
                     sku, item_link, item_image, item_size, item_title, item_sale]

        f.write(str(map(str, item_info)) + "\n")
        logging.debug(item_info)

    f.close()




def mainthread2(i, q):
    for line in iter(q.get, None):
        try:
            directory = line[0]
            link = line[1]
            target = line[2]
            cate = line[3]

            main(directory, link, target, cate)
            logging.debug(line)

        except:
            f2 = open("page1_first_scroller_error_zovi.txt", "a+")
            f2.write(str(line) + "\n")
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()




def supermian():
    directory = "zovi%s" %(time.strftime("%d%m%Y"))

    try:
        os.makedirs(directory)
    except:
       pass

    f = open("zovi_extracted.txt", "a+")
    f.write(directory)
    f.close()

    f = open("zovi_to_extract.txt", "w+")
    f.write(directory)
    f.close()

    page_list = [(directory, "http://zovi.com/mens-shirts?misc_ref_code=hp_seo_text", "Men", "Shirt"), 
                 (directory, "http://zovi.com/mens-polos?misc_ref_code=hp_seo_text", "Men", "POLOS"), 
                 (directory, "http://zovi.com/mens-tees?misc_ref_code=hp_seo_text", "Men", "TEES"), 
                 (directory, "http://zovi.com/mens-bottoms?misc_ref_code=hp_seo_text", "Men", "BOTTOMS"), 
                 (directory, "http://zovi.com/mens-footwear?misc_ref_code=hp_seo_text", "Men", "FOOTWEAR"), 
                 (directory, "http://zovi.com/mens-accessories?misc_ref_code=hp_seo_text", "Men", "ACCESSORIES"), 
                 (directory, "http://zovi.com/mens-jackets-and-pullovers?misc_ref_code=hp_seo_text", "Men", "JACKETS-PULLOVERS"), 
                 (directory, "http://zovi.com/mens-casual-shirts?misc_ref_code=hp_seo_text", "Men", "CASUAL SHIRTS"), 
                 (directory, "http://zovi.com/mens-edge-plain-tees?misc_ref_code=hp_seo_text", "Men", "PLAIN TEES"), 
                 (directory, "http://zovi.com/mens-all-graphic-tees?misc_ref_code=hp_seo_text", "Men", "GRAPHIC TEES"), 
                 (directory, "http://zovi.com/zovi-edge-collection?misc_ref_code=hp_seo_text", "Men", "ZOVI EDGE"), 
                 (directory, "http://zovi.com/mens-sports-shoes?misc_ref_code=hp_seo_text", "Men", "SPORTS SHOES"), 
                 (directory, "http://zovi.com/mens-jeans?misc_ref_code=hp_seo_text", "Men", "JEANS"), 
                 (directory, "http://zovi.com/womens-tops?misc_ref_code=hp_seo_text", "Women", "TOPS"), 
                 (directory, "http://zovi.com/womens-bottoms?misc_ref_code=hp_seo_text", "Women", "BOTTOMS"), 
                 (directory, "http://zovi.com/womens-accessories?misc_ref_code=hp_seo_text", "Women", "ACCESSORIES"), 
                 (directory, "http://zovi.com/womens-footwear?misc_ref_code=hp_seo_text", "Women", "FOOTWEAR"), 
                 (directory, "http://zovi.com/womens-jackets?misc_ref_code=hp_seo_text", "Women", "JACKETS"), 
                 (directory, "http://zovi.com/womens-t-shirts-and-casual-tops?misc_ref_code=hp_seo_text", "Women", "CASUAL TOPS"), 
                 (directory, "http://zovi.com/womens-party-tops-and-dresses?misc_ref_code=hp_seo_text", "Women", "DRESSES"), 
                 (directory, "http://zovi.com/womens-jeans?misc_ref_code=hp_seo_text", "Women", "JEANS"), 
                 (directory, "http://zovi.com/womens-handbags?misc_ref_code=hp_seo_text", "Women", "HANDBAGS"), 
                 (directory, "http://zovi.com/boys-polos?misc_ref_code=hp_seo_text", "Boys",  "POLOS"), 
                 (directory, "http://zovi.com/boys-tees", "Boys", "TEES")]

    procs = []

    for i in range(num_fetch_threads):
        procs.append(threading.Thread(target=mainthread2, args=(i, enclosure_queue,)))
        procs[-1].start()

    #main(directory, "http://zovi.com/mens-shirts?misc_ref_code=hp_seo_text", "Men", "Shirts")

    for line in page_list:
        enclosure_queue.put(line)

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    #for p in procs:
    #    p.join()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        logging.debug('joining %s', t.getName())
        t.join(2)


    


if __name__=="__main__":
    supermian()
