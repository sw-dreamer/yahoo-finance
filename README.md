# 주식 데이터 가져오기 및 MySQL 삽입 프로젝트 (Java & Python)

이 프로젝트는 주식 데이터를 Yahoo Finance API를 통해 가져와 MySQL 데이터베이스에 삽입하는 Java 프로그램과 Python 스크립트를 포함하고 있습니다.

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
