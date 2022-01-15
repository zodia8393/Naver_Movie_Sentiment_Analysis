import pandas as pd

import warnings
warnings.filterwarnings(action='ignore')
from konlpy.tag import Okt
okt=Okt()

#Train 데이터 불러오기
train_df=pd.read_excel("5movies.xlsx")
print(train_df.head())

#결측값 처리

#1.document 컬럼이 non-null인 샘플만 train_df에 다시 저장함
train_df=train_df[train_df['text'].notnull()]

#수정된 정보 다시 확인
print(train_df.info())

#분류 클래스 구성 확인
print(train_df['score'].value_counts())

#분석 불가능 문자 제거
import re
train_df['text'] = train_df['text'].apply(lambda x : re.sub(r'[^ ㄱ-ㅣ가-힣]+', " ", x))
print(train_df.head())

#Train용 데이터셋 정보 재확인
print(train_df.info())
document=train_df['text']
label=train_df['score']

#데이터 셋 분리 (이미 분류가 되어있으므로 생략한다)
from sklearn.model_selection import train_test_split
train_x,test_x,train_y,test_y = train_test_split(document,label,test_size=0.2,random_state=0)
print(len(train_x),len(train_y),len(test_x),len(test_y))

#토큰화 및 TF-IDF 벡터화
from sklearn.feature_extraction.text import TfidfVectorizer
tfv=TfidfVectorizer(tokenizer=okt.morphs,ngram_range=(1,2),min_df=0,max_df=10)
tfv.fit(train_x)
tfv_train_x=tfv.transform(train_x)
print(tfv_train_x)

#감성 분석 모델 구축
from sklearn.linear_model import LogisticRegression # 이진 분류 알고리즘
from sklearn.model_selection import GridSearchCV # 하이퍼 파라미터 최적화

clf = LogisticRegression(random_state=0)
params = {'C': [15, 18, 19, 20, 22]}
grid_cv = GridSearchCV(clf, param_grid=params, cv=3, scoring='accuracy', verbose=1)
grid_cv.fit(tfv_train_x, train_y)

# 최적의 평가 파라미터는 grid_cv.best_estimator_에 저장됨
print(grid_cv.best_params_, grid_cv.best_score_)# 가장 적합한 파라메터, 최고 정확도 확인

#분석 모델 평가
tfv_test_x = tfv.transform(test_x)
# test_predict = grid_cv.best_estimator_.score(tfv_test_x,test_y)
test_predict = grid_cv.best_estimator_.predict(tfv_test_x)
from sklearn.metrics import accuracy_score
print('감성 분류 모델의 정확도 : ',round(accuracy_score(test_y, test_predict), 3))

#감성 예측
input_text = '너무 재밌네요.'
#입력 텍스트에 대한 전처리 수행
input_text = re.compile(r'[ㄱ-ㅣ가-힣]+').findall(input_text)
input_text = [" ".join(input_text)]
# 입력 텍스트의 피처 벡터화
st_tfidf = tfv.transform(input_text)

# 최적 감성 분석 모델에 적용하여 감성 분석 평가
st_predict = grid_cv.best_estimator_.predict(st_tfidf)

#예측 결과 출력
if(st_predict == 0):
    print('예측 결과: ->> 부정 감성')
else :
    print('예측 결과: ->> 긍정 감성')