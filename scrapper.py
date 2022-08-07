from turtle import title
from urllib import response
import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co'
XPATH_LINK_TO_ARTICLE = '//div/text-fill/a[@class and contains(@href,"larepublica")]/@href'
XPATH_TITLE = '//div[@class = "mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_BODY = '//div[@class = "html-content"]/p//text()'
XPATH_DATE = '//span[@class="date"]/text()'
XPATH_AUTHOR = '//div[@class="author-article"]/div/button/text()'


def parse_news(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            news = response.content.decode('utf-8')
            parsed = html.fromstring(news)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','').strip()
                
                
                if parsed.xpath(XPATH_SUMMARY):
                    summary = parsed.xpath(XPATH_SUMMARY)[0]
                else:
                    summary = None
                
                body = parsed.xpath(XPATH_BODY)
                
                if parsed.xpath(XPATH_DATE): 
                    news_date = parsed.xpath(XPATH_DATE)[0]
                else:
                    news_date = 'No date'
                
                if parsed.xpath(XPATH_AUTHOR):
                    author = parsed.xpath(XPATH_AUTHOR)[0]
                else:
                    author = 'No author'
                    print(author)

            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                if summary != None:
                    f.write(summary)
                    f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
                f.write('\n')
                f.write(news_date)
                f.write('\n')
                f.write(author)

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError:
        print(ValueError)


def parse_home():
    try:
        response = requests.get(HOME_URL)

        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_news:
                parse_news(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError:
        print(ValueError)

def main():
    parse_home()

if __name__ == '__main__':
    main()