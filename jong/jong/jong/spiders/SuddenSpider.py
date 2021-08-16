import scrapy 
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.exceptions import CloseSpider
from selenium.common.exceptions import NoSuchElementException

class SuddenSpider(scrapy.Spider):
    name = "sudden"

    def get_url(self):
        driver = webdriver.Chrome("/Users/hexk0131/chromedriver")
        driver.get("https://barracks.sa.nexon.com/search")

        clan_name = input("clan name? : ")

        elem = driver.find_element_by_class_name("input")
        elem.send_keys(clan_name)

        driver.implicitly_wait(5)
    
        try:
            nick = driver.find_element_by_link_text(clan_name)
        except NoSuchElementException:
            print("해당 클랜 없음")
            
            driver.close()

            raise CloseSpider('exit')

        driver.execute_script("arguments[0].click();", nick)

        driver.switch_to_window(driver.window_handles[1])

        print(driver.current_url)

        current_url = driver.current_url

        page_source = driver.page_source

        driver.close()

        return [current_url, page_source]

    def start_requests(self):
        sel = self.get_url()

        yield self.parse(sel[0], sel[1])

    def parse(self, url, response):
        response = HtmlResponse(url=url, body=response, encoding='utf-8')
    
        contents_path = '//*[@id="clanMatch"]/div[1]/div[1]/div[1]/div'
        
        date, map, match, result, counter, counter_score, my_score = ([] for i in range(7))

        for i in range(0, len(response.xpath(contents_path))):
             if(response.xpath(contents_path).xpath("@class").extract()[i] != "history empty"):
                date.append(response.xpath(contents_path+'[{}]/div[1]/ul/li[1]//text()'.format(i+1)).get())
                map.append(response.xpath(contents_path+'[{}]/div[1]/ul/li[2]//text()'.format(i+1)).get())
                match.append(response.xpath(contents_path+'[{}]/div[1]/ul/li[3]//text()'.format(i+1)).get())
                result.append(response.xpath(contents_path+'[{}]/div[1]/ul/li[4]//text()'.format(i+1)).get())
                counter.append(response.xpath(contents_path+'[{}]/div[1]/ul/li[5]/span[1]//text()'.format(i+1)).get())
                counter_score.append(response.xpath(contents_path+'[{}]/div[1]/ul/li[5]/span[2]/span[1]//text()'.format(i+1)).get())
                my_score.append(response.xpath(contents_path+'[{}]/div[1]/ul/li[5]/span[2]/span[3]//text()'.format(i+1)).get())

        print(date)
        print(map)
        print(match)
        print(result)
        print(counter)
        print(counter_score)
        print(my_score)