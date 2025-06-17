from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

@app.route('/api/send-email', methods=['POST'])
def send_email():
    try:
        # Получаем данные из запроса
        data = request.json
        print("Данные формы:", data)

        # Настройки SMTP (Yandex)
        smtp_host = "smtp.yandex.ru"
        smtp_port = 465
        smtp_user = os.getenv("EMAIL_ADDRESS")  # Из .env
        smtp_password = os.getenv("EMAIL_PASSWORD")  # Из .env
        
        # Формируем HTML-письмо
        msg = MIMEText(f"""
            <strong>От:</strong> {data['name']}<br/>
            <strong>Email:</strong> {data['email']}<br/>
            <strong>Телефон:</strong> {data['phoneNumber']}<br/>
            <strong>Тип номера:</strong> {data['room']}<br/>
            <strong>Дата заезда/выезда:</strong> {data['date']}<br/>
            <strong>Взрослые:</strong> {data['adults']}<br/>
            <strong>Дети:</strong> {data['children']}<br/>
            <strong>Пожелания:</strong> {data['message']}
        """, 'html')

        msg['Subject'] = 'Новое бронирование'
        msg['From'] = smtp_user
        msg['To'] = smtp_user  # Можно указать другой email для получения
        
        # Отправка письма
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [smtp_user], msg.as_string())

        return jsonify({"message": "Сообщение успешно отправлено!"}), 200

    except Exception as e:
        print("Ошибка при отправке:", str(e))
        return jsonify({
            "message": "Ошибка отправки сообщения",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)