# Google Trends Fetcher with AWS Bedrock Nova

AWS Bedrock의 Nova 모델과 Web Grounding 기능을 사용하여 2026년 1월 최신 Google Trends Top 10을 가져오는 Python 프로젝트입니다.

## 주요 기능

- AWS Bedrock Nova 2 Lite 모델 사용
- Web Grounding을 통한 실시간 웹 검색
- Google Trends Top 10 자동 수집
- 출처(citations) 포함된 결과 제공
- Web Grounding 사용 전/후 비교

## 필요 조건

- Python 3.9 이상
- AWS 계정 및 자격증명
- AWS Bedrock 접근 권한

## 설치 방법

1. 저장소 클론
```bash
git clone <repository-url>
cd Nova-WebGrounding
```

2. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. AWS 자격증명 설정

`.env` 파일을 수정하여 실제 AWS 자격증명을 입력하세요:
```
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-east-1
```

또는 AWS CLI를 통해 자격증명을 설정할 수 있습니다:
```bash
aws configure
```

## 사용 방법

```bash
python main.py
```

## 출력 예시

프로그램은 두 가지 결과를 출력합니다:

### 1. Without Web Grounding
모델의 학습 데이터만을 기반으로 한 예측 결과입니다.

```
Without Web Grounding
==================================================
{
  "message": {
    "role": "assistant",
    "content": [
      {
        "text": "### Top 10 Google Trends Topics for January 2026 (Hypothetical Forecast)
        
        1. 2026 Winter Olympics – Milan-Cortina
        2. CES 2026 Highlights & Announcements
        3. Global Climate Summit 2026 Preparations
        4. AI Regulation Debates & New Guidelines
        5. Cryptocurrency Market Surge & New ICOs
        ..."
      }
    ]
  }
}
```

### 2. With Web Grounding
실시간 웹 검색을 통한 실제 Google Trends 데이터와 출처를 제공합니다.

```
With Web Grounding
==================================================
Based on the available search results, here are the top trending topics and searches for January 2026:

### Top Google Searches in January 2026:
1. YouTube - 185 million searches [https://www.pagetraffic.com/blog/top-google-searches/]
2. Facebook - 151 million searches [https://www.pagetraffic.com/blog/top-google-searches/]
3. Amazon - 124 million searches [https://www.pagetraffic.com/blog/top-google-searches/]
4. Weather - 101 million searches [https://www.pagetraffic.com/blog/top-google-searches/]
5. Google - 83.1 million searches [https://www.pagetraffic.com/blog/top-google-searches/]
6. Gmail - 68 million searches [https://www.pagetraffic.com/blog/top-google-searches/]
7. Wordle - 68 million searches [https://www.pagetraffic.com/blog/top-google-searches/]
8. Google Translate - 55.6 million searches [https://www.pagetraffic.com/blog/top-google-searches/]
9. Walmart - 45.5 million searches [https://www.pagetraffic.com/blog/top-google-searches/]
10. Yahoo - 37.2 million searches [https://www.pagetraffic.com/blog/top-google-searches/]

### Other Notable Trending Topics:
- Short Videos [https://www.latestly.com/google-trends/01012026/]
- Twelve Grapes of Luck on New Year's Eve 2025 [https://www.latestly.com/google-trends/01012026/]
- Mumbai Cricket Association [https://www.latestly.com/google-trends/01012026/]
- Donald Trump [https://www.latestly.com/google-trends/15012026/]
- Makar Sankranti 2026 [https://www.latestly.com/google-trends/15012026/]

### Additional Trending Keywords:
- ChatGPT [https://ahrefs.com/blog/top-google-searches/]
- AI Video Generator [https://explodingtopics.com/blog/latest-trends]
- AI for Teachers [https://explodingtopics.com/blog/latest-trends]
```

Web Grounding을 사용하면 각 정보의 출처(URL)가 함께 제공되어 신뢰성을 확인할 수 있습니다.

## 프로젝트 구조

```
.
├── main.py              # 메인 실행 파일
├── requirements.txt     # Python 패키지 의존성
├── .env                 # AWS 자격증명 (gitignore에 포함)
├── venv/               # 가상환경 (gitignore에 포함)
└── README.md           # 프로젝트 문서
```

## 기술 스택

- **AWS Bedrock**: Nova 2 Lite 모델
- **boto3**: AWS SDK for Python
- **Web Grounding**: 실시간 웹 검색 기능

## 주의사항

- Web Grounding은 현재 US 리전에서만 사용 가능합니다
- `.env` 파일에 실제 AWS 자격증명을 입력해야 합니다
- AWS Bedrock 사용에 따른 비용이 발생할 수 있습니다
