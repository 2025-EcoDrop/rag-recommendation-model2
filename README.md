# 💊 rag-recommendation-model2
RAG의 검색 단계만 활용한 약품 추천 API입니다. </br>
입력된 증상과 벡터 유사도 기반으로 약품을 검색한 뒤, 유저 리뷰 기반 가중치를 적용하여 Top-N 추천 결과를 반환합니다. </br>
</br>

## ⚠️ 참고 사항
- 자연어 설명은 제공하지 않습니다.
- 응답 속도가 빠릅니다.
- 단순 추천 시스템용으로 적합합니다.
</br>

## 📁 주요 파일 구조
```bash
rag-recommendation-model2
├── app/
│   ├── database/            # 데이터 베이스와 연결
│   ├── main.py              # FastAPI 앱 진입점
│   ├── schemas.py           # Request / Response 모델
│   ├── rag.py               # 임베딩 및 벡터 검색
│   └── routes/
│       └── recommend.py     # /recommend API
├── requirements.txt
└── README.md
```
</br>

## ▶️ 실행
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

</br>
