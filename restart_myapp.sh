#!/bin/bash

# 서비스 이름
SERVICE_NAME="myapp.service"
LOG_FILE="/var/log/myapp_restart.log"

# 날짜와 시간
DATE_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# 서비스 상태 확인
SERVICE_STATUS=$(systemctl is-active $SERVICE_NAME)

# 서비스가 죽어있으면
if [ "$SERVICE_STATUS" != "active" ]; then
	    # 서비스 종료 이유 로그 가져오기
	        SERVICE_STATUS_DETAILS=$(journalctl -u $SERVICE_NAME -n 20 --no-pager)

		    echo "$DATE_TIME - $SERVICE_NAME is not running. Restarting..." >> $LOG_FILE
		        echo "$DATE_TIME - Reason for failure (last 20 logs):" >> $LOG_FILE
			    echo "$SERVICE_STATUS_DETAILS" >> $LOG_FILE
			        
			        # 서비스 재시작
				    systemctl start $SERVICE_NAME

				        # 재시작 후 상태 확인
					    if [ "$(systemctl is-active $SERVICE_NAME)" = "active" ]; then
						            echo "$DATE_TIME - $SERVICE_NAME restarted successfully." >> $LOG_FILE
							        else
									        echo "$DATE_TIME - Failed to restart $SERVICE_NAME." >> $LOG_FILE
										    fi
									    else
										        echo "$DATE_TIME - $SERVICE_NAME is already running." >> $LOG_FILE
fi

