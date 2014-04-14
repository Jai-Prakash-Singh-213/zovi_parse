import phan_proxy
import req_proxy
import ast
import logging 
from bs4 import BeautifulSoup
from lxml import html 
import time 

#item_info = [link, target, cate, sub_cate, colour, price, gender, sku, item_link, item_image, item_size, item_title, item_sale]

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')


def my_strip(x):
    return str(x).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace(",", " ").strip()


def main(line):
    line = ast.literal_eval(line)

    page = req_proxy.main(line[8])

    f = open("myfile.txt", "w+")
    print >>f, page
    f.close()

    #driver = phan_proxy.main(line[8])
    #page = driver.page_source

    #driver.delete_all_cookies()
    #driver.quit()
    
    #tree = html.fromstring(page)
    #meta_disc = tree.xpath("/html/head/meta[3]/text()")

    soup = BeautifulSoup(page, "html.parser")
    meta_disc = soup.find("meta", attrs={"name":"description"}).get("content")

    title = soup.find("title").get_text()
    desc = soup.find("section", attrs={"id":"product-detail"})
    dte = time.strftime("%d:%m:%Y")
    status = " "
    spec = " "
    vender = "zovi.com"
    brand = "zovi"

    print map(my_strip,  [line[7], line[11], line[0], line[5], line[2], 
                         line[3], brand, line[9], line[5], line[4], 
                         line[1], line[8], vender, title, meta_disc, line[10], 
                         desc, spec, dte, status])



def supermain():
    line = """['http://zovi.com/boys-tees', 'Boys', 'TEES', 'boys-tees', '', '251', 'B', 'A123RNB00901', 'http://zovi.com/black-skull-applique-t-shirt--A123RNB00901', 'http://d1yvqnuw46gd8y.cloudfront.net/z/prod/w/2/g/p/A123RNB00901/1_c.jpg', "['7-8 Y']", 'Black Skull Applique T-shirt', '10%']"""
    
    main(line)






if __name__=="__main__":
    supermain()


   

