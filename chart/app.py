from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from functools import wraps
from datetime import datetime
from flask import jsonify
import logging

# 로그 설정
logging.basicConfig(
        filename='app_exec.log',  # 로그 파일 이름
        level=logging.DEBUG,  # 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',  # 로그 메시지 포맷
        )

# 예시로 로그 기록
logging.info('앱이 시작되었습니다.')
logging.debug('디버깅 중...')
logging.warning('경고 메시지')
logging.error('에러가 발생했습니다.')
logging.critical('심각한 에러 발생!')

# Flask 애플리케이션 초기화
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL 연결 정보
def get_db_connection():
    return mysql.connector.connect(
        host='172.24.32.100',
        user='root',
        password='rootpassword',
        database='stock_analysis'
    )

# 로그인 확인 데코레이터
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash("로그인이 필요합니다.", "error")
            next_url = request.url
            return redirect(url_for('login', next=next_url))
        return f(*args, **kwargs)
    return wrap

# 회원가입 페이지
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        phone = request.form['phone']

        if not username or not password or not name or not phone:
            flash("모든 필드를 채워주세요.", "error")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, name, phone) VALUES (%s, %s, %s, %s)",
                           (username, hashed_password, name, phone))
            conn.commit()
            conn.close()
            flash("회원가입 성공!", "success")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"회원가입 실패: {err}", "error")
            return redirect(url_for('signup'))

    return render_template('signup.html')

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash("로그인 성공!", "success")
                next_url = request.args.get('next')
                return redirect(next_url or url_for('index'))
            else:
                flash("아이디 또는 비밀번호가 잘못되었습니다.", "error")
                return redirect(url_for('login'))

        except mysql.connector.Error as err:
            flash(f"로그인 오류: {err}", "error")
            return redirect(url_for('login'))

    next_url = request.args.get('next')
    return render_template('login.html', next=next_url)

# 로그아웃
@app.route('/logout')
def logout():
    session.clear()
    flash("로그아웃 되었습니다.", "success")
    return redirect(url_for('login'))

# 메인 페이지 (주식 목록)
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    symbols = [
        'AAPL', 'AMAT', 'AMD', 'AMZN', 'BIDU', 'CSCO', 'EXPE', 'GOOGL', 'INTC', 'INTU',
        'MSFT', 'MSI', 'NFLX', 'NVDA', 'PINS', 'PYPL', 'QCOM', 'ROKU', 'SNAP', 'TSLA', 'ZM'
    ]
    return render_template('index.html', symbols=symbols, username=session.get('username'))

# 주식 세부 페이지
@app.route('/stock/<symbol>')
@login_required
def stock_details(symbol):
    date = request.args.get('date', None)  # 쿼리 파라미터로 날짜 받기
    stock_data = get_stock_data(symbol, date)

    if not stock_data:
        flash(f"{date or '해당 날짜'}에 대한 {symbol} 데이터가 없습니다.", "error")
        return redirect(url_for('index'))

    return render_template('stock_details.html', symbol=symbol, stock_data=stock_data, username=session.get('username'))

# 주식 데이터 가져오는 함수
def get_stock_data(symbol, date=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if date:
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()  # 날짜 형식 처리
                print(f"Formatted Date: {date}")  # 디버깅 출력
            except ValueError as e:
                flash(f"날짜 형식이 올바르지 않습니다: {e}", "error")
                return None

            query = """
                SELECT date, open, high, low, close, volume FROM stock_data
                WHERE symbol = %s AND DATE(date) = %s
            """
            print(f"Executing query: {query} with params: {symbol.upper()}, {date}")  # 쿼리 로그 출력
            cursor.execute(query, (symbol.upper(), date))
        else:
            query = """
                SELECT date, open, high, low, close, volume FROM stock_data
                WHERE symbol = %s
            """
            cursor.execute(query, (symbol.upper(),))

        stock_data = cursor.fetchall()
        conn.close()

        print(f"Stock data retrieved: {stock_data}")  # 디버깅 출력

        if not stock_data:
            flash(f"{symbol}에 대한 데이터가 없습니다.", "error")
            return None

        return stock_data
    except Exception as e:
        flash(f"주식 데이터 조회 중 오류가 발생했습니다: {e}", "error")
        return None



# 차트 이미지 생성
@app.route('/chart/<symbol>')
@login_required
def chart(symbol):
    date = request.args.get('date', None)
    img = render_stock_chart(symbol, date)

    if not img:
        flash(f"{date or '해당 날짜'}에 대한 {symbol} 데이터를 찾을 수 없습니다.", "error")
        return redirect(url_for('stock_details', symbol=symbol))

    return send_file(img, mimetype='image/png')

# 주식 차트 렌더링 함수
def render_stock_chart(symbol, date=None):
    try:
        conn = get_db_connection()
        query = """
            SELECT date, close FROM stock_data
            WHERE symbol = %s
        """
        params = [symbol.upper()]

        if date:
            query += " AND DATE(date) = %s"
            params.append(date)

        df = pd.read_sql(query, conn, params=params)
        conn.close()

        if df.empty:
            return None

        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['close'], label='Close Price', color='b', linewidth=2)
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title(f'{symbol} Stock Chart')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return img
    except Exception as e:
        flash(f"차트 생성 중 오류가 발생했습니다: {e}", "error")
        return None

# 주식 데이터 가져오는 함수
@app.route('/stock_data/<symbol>', methods=['GET'])
def get_stock_data_api(symbol):
    date = request.args.get('date', None)
    stock_data = get_stock_data(symbol, date)

    if stock_data:
        # 데이터가 있을 경우 JSON으로 반환
        return jsonify(stock_data[0])  # 단일 데이터 항목 반환
    else:
        return jsonify(None)

# 새로운 URL 패턴 정의 (주식 데이터를 가져오는 새로운 엔드포인트)
@app.route('/stock_data/<symbol>', methods=['GET'])
@login_required
def stock_data(symbol):
    date = request.args.get('date', None)  # 쿼리 파라미터로 날짜 받기
    stock_data = get_stock_data(symbol, date)

    if not stock_data:
        flash(f"{date or '해당 날짜'}에 대한 {symbol} 데이터가 없습니다.", "error")
        return redirect(url_for('index'))

    return render_template('stock_details.html', symbol=symbol, stock_data=stock_data, username=session.get('username'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)