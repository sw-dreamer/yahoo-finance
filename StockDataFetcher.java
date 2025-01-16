package Finance;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.sql.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.HashSet;
import java.util.Set;

public class StockDataFetcher {

    // Python 스크립트로 주식 데이터를 가져오는 함수
    public static String fetchStockDataFromPython(String stockSymbol, String startDate) {
        String line;
        StringBuilder result = new StringBuilder();

        try {
            // Python 스크립트를 실행하여 2년치 데이터를 가져옴
            ProcessBuilder processBuilder = new ProcessBuilder("python3", "/home/master/finance/yf_data.py", stockSymbol, startDate);
            Process process = processBuilder.start();

            // Python 스크립트의 출력을 읽어들임 (UTF-8로 인코딩 설정)
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8));
            while ((line = reader.readLine()) != null) {
                result.append(line);
            }

            // 프로세스 종료 대기
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                System.out.println("Python 스크립트 실행 오류!");
            }

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return result.toString();  // 결과를 JSON 형식으로 반환
    }

    // 데이터베이스 연결 설정
    private static Connection connectToDatabase() throws SQLException {
        String url = "jdbc:mysql://172.24.32.100:3306/stock_analysis?serverTimezone=Asia/Seoul";
        String user = "root";
        String password = "rootpassword";  // MySQL 비밀번호를 넣으세요
        Connection connection = DriverManager.getConnection(url, user, password);
        
        // autocommit을 false로 설정하여 트랜잭션을 수동으로 관리
        connection.setAutoCommit(false);
        return connection;
    }

    // 데이터 삽입 함수
    private static void insertStockData(Connection connection, JsonNode data) throws SQLException {
        // 먼저 동일한 symbol과 date에 해당하는 데이터가 존재하는지 확인
        String checkSql = "SELECT COUNT(*) FROM stock_data WHERE symbol = ? AND date = ?";
        try (PreparedStatement checkStmt = connection.prepareStatement(checkSql)) {
            checkStmt.setString(1, data.get("symbol").asText());
            checkStmt.setDate(2, Date.valueOf(data.get("date").asText()));
            
            ResultSet rs = checkStmt.executeQuery();
            if (rs.next() && rs.getInt(1) > 0) {
                System.out.println("데이터가 이미 존재합니다. 삽입하지 않습니다.");
                return;  // 데이터가 이미 존재하면 삽입하지 않음
            }
        }

        // 데이터가 없으면 삽입
        String sql = "INSERT INTO stock_data (symbol, date, open, high, low, close, volume, execution_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, data.get("symbol").asText());
            stmt.setDate(2, Date.valueOf(data.get("date").asText()));
            stmt.setDouble(3, data.get("open").asDouble());
            stmt.setDouble(4, data.get("high").asDouble());
            stmt.setDouble(5, data.get("low").asDouble());
            stmt.setDouble(6, data.get("close").asDouble());
            stmt.setLong(7, data.get("volume").asLong());

            // 현재 시간 (execution_time) 추가
            LocalDateTime now = LocalDateTime.now();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
            String formattedTime = now.format(formatter);
            stmt.setString(8, formattedTime);

            int rowsAffected = stmt.executeUpdate();
            if (rowsAffected > 0) {
                System.out.println("주식 데이터 삽입 성공: " + data.get("symbol").asText() + " " + data.get("date").asText());
            } else {
                System.out.println("주식 데이터 삽입 실패: " + data.get("symbol").asText() + " " + data.get("date").asText());
            }
        }
    }

    public static void main(String[] args) {
        Connection connection = null;  // connection 객체를 try 바깥에서 선언

        // 주식 심볼 목록을 Set에 저장 (중복 방지)
        Set<String> stockSymbols = new HashSet<>();
        stockSymbols.add("AAPL");
        stockSymbols.add("AMZN");
        stockSymbols.add("GOOGL");
        stockSymbols.add("MSFT");
        stockSymbols.add("TSLA");
        stockSymbols.add("FB");    // Meta Platforms Inc. (구 Facebook)
        stockSymbols.add("NVDA");  // NVIDIA Corporation
        stockSymbols.add("INTC");  // Intel Corporation
        stockSymbols.add("BIDU");  // Baidu Inc.
        stockSymbols.add("PYPL");  // PayPal Holdings, Inc.
        stockSymbols.add("CSCO");  // Cisco Systems, Inc.
        stockSymbols.add("AMD");   // Advanced Micro Devices, Inc.
        stockSymbols.add("SNAP");  // Snap Inc. (Snapchat의 모회사)
        stockSymbols.add("INTU");  // Intuit Inc.
        stockSymbols.add("ROKU");  // Roku, Inc.
        stockSymbols.add("ZM");    // Zoom Video Communications, Inc.
        stockSymbols.add("QCOM");  // Qualcomm Incorporated
        stockSymbols.add("MSI");   // Motorola Solutions, Inc.
        stockSymbols.add("EXPE");  // Expedia Group, Inc.
        stockSymbols.add("PINS");  // Pinterest, Inc.
        stockSymbols.add("AMAT");  // Applied Materials, Inc.

        try {
            // 2년 전 날짜 계산
            LocalDate currentDate = LocalDate.now();
            LocalDate twoYearsAgo = currentDate.minus(2, ChronoUnit.YEARS);
            String startDate = twoYearsAgo.toString();

            // 주식 데이터 가져오기
            connection = connectToDatabase();  // connection 객체를 여기서 생성

            for (String stockSymbol : stockSymbols) {
                // 각 심볼에 대해 주식 데이터 가져오기
                String stockData = fetchStockDataFromPython(stockSymbol, startDate);

                // 데이터가 비어있는지 확인
                if (stockData.isEmpty() || stockData.equals("{}")) { // 데이터가 비어있는 경우
                    System.out.println("해당 심볼(" + stockSymbol + ")에 대한 주식 데이터가 존재하지 않습니다.");
                } else {
                    System.out.println(stockSymbol + "의 주식 데이터: " + stockData);

                    // JSON 파싱
                    ObjectMapper objectMapper = new ObjectMapper();
                    JsonNode stockDataJson = objectMapper.readTree(stockData);

                    // MySQL에 데이터 삽입
                    try {
                        for (JsonNode node : stockDataJson) {
                            insertStockData(connection, node);
                        }
                        
                        // 트랜잭션을 커밋
                        connection.commit();
                        System.out.println("트랜잭션 커밋 완료");
                    } catch (SQLException e) {
                        e.printStackTrace();
                        // 오류 발생 시 롤백
                        try {
                            if (connection != null) {
                                connection.rollback();  // 롤백 처리
                            }
                        } catch (SQLException rollbackException) {
                            rollbackException.printStackTrace();
                        }
                    }
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // try-with-resources 대신 finally에서 connection 종료 처리
            if (connection != null) {
                try {
                    connection.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }

        System.out.println("모든 주식 데이터 삽입 작업이 완료되었습니다.");
    }
}
