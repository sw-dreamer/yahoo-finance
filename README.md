# 주식 데이터 가져오기 및 MySQL 삽입 프로젝트

이 프로젝트는 주식 데이터를 Yahoo Finance API를 통해 가져와 MySQL 데이터베이스에 삽입하는 Java 프로그램과 Python 스크립트를 포함하고 있습니다.

## 버전 정리

   - Python 3.10.12
   - openjdk 11.0.25 2024-10-15
   - mysql 8.0.17

## 프로젝트 구성
이 프로젝트는 여러 주요 구성 요소로 이루어져 있습니다

1. **Java 프로그램 (`StockDataFetcher.java`)**
   
    주식 데이터를 가져와 MySQL 데이터베이스에 삽입합니다.
   
2. **Python 스크립트 (`yf_data.py`)**
   
    Yahoo Finance API를 사용하여 주식 데이터를 가져옵니다.

3. **Flask 애플리케이션 (`app.py`)**
  
  Flask 애플리케이션은 주식 데이터를 조회하고, 차트를 렌더링하며, 로그인 및 회원가입 기능을 포함한 웹 애플리케이션입니다.
  
4. **Cron 작업 설정**
   
    주식 데이터를 자동으로 업데이트하기 위해 설정된 cron 작업에 대해 설명합니다.
   
    주어진 cron 작업은 주기적으로 Java 프로그램 및 myapp.service을 실행하고 이를 로그 파일에 기록합니다.

5. **메인 페이지(`index.html`)**
   
   이 페이지는 사용자가 주식 차트를 볼 수 있도록 다양한 주식 심볼(AAPL, AMAT, AMD 등)을 버튼 형식으로 제공하는 웹 페이지입니다.

   사용자는 각 주식 심볼을 클릭하여 해당 주식의 상세 차트를 볼 수 있습니다.

   이 페이지는 사용자가 로그인한 상태에서 주식 정보를 확인할 수 있도록 돕습니다.

6. **주식 정보 페이지(`stock_details.html`)**
   `stock_details.html`은 주식 심볼에 대한 차트 및 관련 정보를 표시하는 웹 페이지입니다.

   사용자가 특정 날짜에 대한 주식 데이터를 선택하면, 해당 날짜의 주식 차트와 관련된 상세 정보를 확인할 수 있습니다.
   
---
## 1. Python 스크립트: `yf_data.py`

### 1.1. 기능

Python 스크립트는 주어진 주식 심볼에 대해 Yahoo Finance에서 데이터를 가져오고, 이 데이터를 JSON 형식으로 반환합니다. 데이터는 주식의 "Open", "High", "Low", "Close", "Volume" 컬럼만 포함됩니다.

---
## 2. Java 코드: `StockDataFetcher.java`

### 2.1. 기능

Java 프로그램은 주식 심볼 목록을 정의하고, 각 심볼에 대해 Python 스크립트를 호출하여 데이터를 가져옵니다. 그 후, JSON 데이터를 파싱하고 MySQL 데이터베이스에 삽입합니다. 데이터 삽입 전에 중복 여부를 확인하여 중복된 데이터는 삽입하지 않습니다.

---
## 3. Flask 애플리케이션: `app.py`

### 3.1. 기능

Flask 애플리케이션은 주식 데이터를 조회하고, 차트를 렌더링하며, 로그인 및 회원가입 기능을 포함한 웹 애플리케이션입니다. 사용자는 주식 심볼을 선택하고, 해당 주식의 세부 데이터를 조회하거나 차트를 볼 수 있습니다. 또한, 로그인을 통해 사용자 인증을 처리하고, 데이터를 MySQL 데이터베이스에서 가져와 웹 페이지에 표시합니다.

### 3.2. 주요 기능

1. **회원가입 및 로그인**
   - 사용자 인증을 위한 회원가입 및 로그인 기능을 제공합니다.
   - 비밀번호는 해시 처리를 통해 안전하게 저장됩니다.
   - 로그인 후 세션을 통해 사용자의 정보를 관리합니다.

2. **주식 목록 페이지**
   - 여러 주식 심볼을 미리 정의하여, 사용자가 선택할 수 있도록 주식 목록을 제공합니다.
   - 사용자는 주식 심볼을 클릭하여 해당 주식의 세부 정보를 확인할 수 있습니다.

3. **주식 세부 정보 페이지**
   - 각 주식에 대해 날짜별 데이터를 조회할 수 있으며, "Open", "High", "Low", "Close", "Volume" 정보를 제공합니다.
   - 쿼리 파라미터를 통해 특정 날짜의 데이터를 조회할 수 있습니다.

4. **주식 차트 렌더링**
   - 주식의 "Close" 가격을 기반으로 차트를 생성하여, 사용자가 시각적으로 주식의 가격 변동을 볼 수 있습니다.
   - 차트는 `matplotlib`를 사용하여 PNG 형식으로 생성되고, 웹 페이지에서 표시됩니다.

5. **API를 통한 주식 데이터 제공**
   - 주식 심볼과 날짜를 기준으로 API 엔드포인트를 제공하여, 주식 데이터를 JSON 형식으로 반환합니다.
   - 이를 통해 다른 시스템에서도 주식 데이터를 쉽게 조회할 수 있습니다.

---
## 4. Cron 작업: 주식 데이터 자동 업데이트

### 4.1. 기능

이 cron 작업은 매 시간마다 주식 데이터를 자동으로 업데이트하는 역할을 합니다. 주어진 시간에 `StockDataFetcher.java` 프로그램을 실행하여 주식 데이터를 가져오고 이를 MySQL 데이터베이스에 삽입합니다. 추가적으로 시스템에서 지정된 서비스(`myapp.service`)의 상태를 확인하고, 서비스가 비활성화된 경우 이를 재시작을 하도록  하였습니다. myapp에는 app.py가 있습니다.
또한 실행 로그는 지정된 로그 파일에 기록됩니다.

### 4.2. Cron 작업 내용

다음은 설정된 cron 작업입니다:

```bash
30 * * * * java -cp "/home/master/finance:/home/master/finance/lib/mysql-connector-java-8.0.17.jar:/home/master/finance/lib/jackson-databind-2.9.0.jar:/home/master/finance/lib/jackson-core-2.9.0.jar:/home/master/finance/lib/jackson-annotations-2.9.0.jar" -Duser.dir=/home/master/finance Finance.StockDataFetcher >> /home/master/finance/logs/stock_data_fetcher.log 2>&1
```

```bash
* * * * * /usr/local/bin/restart_myapp.sh
```

![image](https://github.com/user-attachments/assets/ddf23e2e-8945-4278-9f3f-bf7595b91220)

![image](https://github.com/user-attachments/assets/4c56f15c-3b3d-4b12-b114-4b08aaf2603f)

---

## 5.주식 차트 페이지 설명

### 5.1. 주요 기능

#### 5.1.1. 네비게이션 바

- **홈 링크**: 홈 페이지로 돌아갈 수 있는 링크입니다.
- **사용자 이름 표시**: 로그인한 사용자의 이름을 표시합니다.
- **로그아웃 링크**: 사용자가 로그아웃할 수 있도록 돕는 링크입니다.

#### 5.1.2. 주식 차트 보기

- **주식 버튼**: 여러 주식 심볼(AAPL, AMAT, AMD 등)을 버튼 형식으로 제공하며, 각 버튼을 클릭하면 해당 주식의 차트 페이지로 이동합니다.
  - AAPL
  - AMAT
  - AMD
  - AMZN
  - BIDU
  - CSCO
  - EXPE
  - GOOGL
  - INTC
  - INTU
  - MSFT
  - MSI
  - NFLX
  - NVDA
  - PINS
  - PYPL
  - QCOM
  - ROKU
  - SNAP
  - TSLA
  - ZM

#### 5.1.3. 페이지 레이아웃 및 스타일

- **반응형 디자인**: 페이지는 다양한 화면 크기에 맞게 자동으로 조정됩니다.
- **깔끔한 UI**: 페이지는 현대적인 디자인을 채택하여 사용자 경험을 향상시킵니다.
- **네비게이션 바**: 상단에 고정된 네비게이션 바는 색상, 간격, 정렬 등을 고려하여 사용자가 빠르게 홈페이지로 이동하거나 로그아웃할 수 있도록 돕습니다.
- **버튼**: 주식 버튼은 호버 효과와 클릭 효과를 제공하여 시각적인 피드백을 사용자에게 전달합니다.
- **컨테이너**: 콘텐츠 영역은 중앙에 정렬되어 있으며, 흰색 배경과 그림자 효과를 통해 강조됩니다.

![image](https://github.com/user-attachments/assets/c0c94e60-b827-419e-acd1-0056394cd564)

---
## 6. stock_details.html 페이지 설명

### 6.1. 주요 기능

#### 6.1.1. 주식 차트 표시

- **차트 선택**: 사용자는 일별(`daily`) 또는 분별(`minute`) 차트 유형을 선택할 수 있습니다.
- **날짜 선택**: 날짜 입력란을 통해 특정 날짜를 선택하고, 해당 날짜의 차트 및 데이터를 조회할 수 있습니다.
- **차트 갱신**: 사용자가 차트 유형 또는 날짜를 변경하면, 차트 이미지가 자동으로 갱신됩니다.
- **차트 접기 및 펼치기**: 차트는 `차트 접기` 또는 `차트 펼치기` 버튼을 클릭하여 표시하거나 숨길 수 있습니다.

#### 6.1.2. 주식 정보 표시

- **주식 정보**: 선택된 날짜의 주식 정보(시가, 고가, 저가, 종가, 거래량)를 카드 형식으로 표시합니다.
- **데이터 없음 처리**: 사용자가 선택한 날짜에 해당하는 데이터가 없으면, "해당 날짜의 데이터가 없습니다."라는 메시지가 표시됩니다.

### 6.1.3. JavaScript 기능

- **차트 업데이트**: `updateChart()` 함수는 차트 유형과 날짜를 선택할 때마다 URL을 갱신하여 해당 차트를 로드합니다.
- **특정 날짜의 데이터 로드**: `loadSpecificDateValue()` 함수는 사용자가 날짜를 선택할 때마다 해당 날짜의 주식 데이터를 API에서 가져옵니다. 가져온 데이터는 화면에 동적으로 표시됩니다.
- **차트 접기/펼치기**: `toggleChart()` 함수는 차트 영역을 접고 펼치는 기능을 담당합니다. 버튼 클릭 시 차트가 숨겨지거나 펼쳐집니다.

![image](https://github.com/user-attachments/assets/3cf6c0e4-56a2-421e-99a2-18aaecf69f32)


---

## @@Copyright

본 프로젝트의 일부 코드 및 콘텐츠는 OpenAI의 **ChatGPT** 모델을 사용하여 생성된 코드 및 콘텐츠를 포함합니다.  
ChatGPT는 OpenAI에서 제공하는 인공지능(AI) 언어 모델로, 다양한 주제에 대한 정보를 생성하거나 사용자의 요청에 맞춘 콘텐츠를 생성할 수 있습니다.

---

## 1. AI 생성 콘텐츠의 저작권

사용자는 OpenAI의 [사용 약관](https://openai.com/policies/terms-of-use)을 준수해야 합니다.

---

## 2. 사용 약관

본 콘텐츠를 사용하거나 배포할 때, 사용자는 OpenAI의 사용 약관 및 정책을 따를 책임이 있습니다.  
이는 콘텐츠의 상업적 사용, 재배포, 변형 등과 관련된 규정을 포함합니다.  
OpenAI의 정책에 대한 자세한 내용은 [OpenAI 사용 약관](https://openai.com/policies/terms-of-use)에서 확인할 수 있습니다.

---

## 3. ChatGPT의 한계와 책임의 한계

ChatGPT는 대규모 텍스트 데이터를 기반으로 훈련된 AI 모델로, 일부 정보가 부정확하거나 오류가 있을 수 있습니다.  

사용자는 ChatGPT가 생성한 콘텐츠를 신중히 검토하고, 필요에 따라 수정해야 할 책임이 있습니다.

또한, ChatGPT는 특정 법적, 윤리적 책임을 지지 않으며, 생성된 콘텐츠에 대한 모든 책임은 사용자가 집니다.

---

## 4. **학습 및 연구 목적으로 사용**

본 프로젝트에서 생성된 콘텐츠는 **학습 및 연구 목적으로만 사용**되어야 합니다.  
이 콘텐츠는 학습, 연구, 개인적인 실험적 용도로만 사용되며, 상업적인 목적으로 사용하지 않습니다.

---

