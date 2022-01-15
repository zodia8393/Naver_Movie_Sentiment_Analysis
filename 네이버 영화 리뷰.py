#네이버 영화 감상평 수집하기
import re
import urllib
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.parse

code='187320'
url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code='+code+'&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1'
html = urlopen(url)
soup = BeautifulSoup(html,'html.parser')

#------------------------------------------------------------------
# urlopen 에러가 나는 경우!
#> urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed 

# 다음과 같이 한다.
import ssl
context = ssl._create_unverified_context()

url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code='+code+'&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1'
html = urlopen(url, context=context)
soup = BeautifulSoup(html,'html.parser')

review = soup.find('span',{'id':'_filtered_ment_0'})
review.get_text().strip()

# for 문을 활용해서 10개의 리뷰를 가져오기

for i in range(10):
    review = soup.find('span',{'id':f'_filtered_ment_{i}'})
    print(f'{i+1} 번째 리뷰')
    print(review.get_text().strip())
    print('--------------------')

#페이지를 순환하며 리뷰 크롤링 하기(1 page ~ 10 page)

review_list = []
for page in range(1,11):
    url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code='+code+'&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}'
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
    for i in range(10):
        review = soup.find('span',{'id':f'_filtered_ment_{i}'})
        review = review.get_text().strip()
        review_list.append(review)
review_list

# 크롤링한 데이터 파일로 저장 하기
review_list = []
for page in range(1,11):
    url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code='+code+'&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}'
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
    for i in range(10):
        review = soup.find('span',{'id':f'_filtered_ment_{i}'})
        review = review.get_text().strip()
        review_list.append(review)

# with open을 활용하여 따로 file을 열고 닫기 하지 않아도 된다.
# 'w'는 file write 기능
# encoding='utf-8' => utf-8형식으로 저장
with open('./naver_movie.txt','w',encoding='utf-8') as f:
    for single_review in review_list:
        f.write(single_review+'\n')

del review_list # 메모리 절약을 위한 리스트 삭제

#2000명에 대한 댓글 가져오기
import requests
review_list = []
for page in range(1,2001):
    url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code='+code+'&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}'
    html = requests.get(url)
    soup = BeautifulSoup(html.content,'html.parser')
    for i in range(10):
        review = soup.find('span',{'id':f'_filtered_ment_{i}'})
        review = review.get_text().strip()
        review_list.append(review)

with open('./naver_movie_request_2000.txt','w',encoding='utf-8') as f:
    for single_review in review_list:
        f.write(single_review+'\n')
        
#영화 제목을 통한 영화 코드 검색 (네이버 무료 api 활용) -> 오픈 API이용 신청

#네이버 검색 Open API 사용 요청시 얻게되는 정보를 입력
client_id = "Vlre9ODFr808Hl1o2yU6"
client_secret = "MxASnFk10v"

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def search_title(title):
    url = 'https://openapi.naver.com/v1/search/movie.json?display=100&query=' + urllib.parse.quote(title)
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        d = json.loads(response_body.decode('utf-8'))
        if (len(d['items']) > 0):
            return d['items']
        else:
            return None

    else:
        print("Error Code:" + rescode)
