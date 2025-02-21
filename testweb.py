from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import datetime
import jwt


app = Flask(__name__)
CORS(app, supports_credentials=True)  # 啟用 CORS 支援

SECRET_KEY = "11124138"
TOKEN_EXPIRY = 30
token_storage = {}


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=TOKEN_EXPIRY)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # 儲存在後端
    token_storage[token] = payload["exp"]
    return token

# 驗證 JWT Token
def verify_token(token):
    try:
        # 解碼 Token 並驗證
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # 確保 Token 在後端儲存中
        if token not in token_storage:
            return False, "Token 已被登出或無效"
        user_id = decoded.get("user_id")
        return True,user_id
    except jwt.ExpiredSignatureError:
        # 過期處理
        if token in token_storage:
            del token_storage[token]
        return False, "Token 過期"
    except jwt.InvalidTokenError:
        return False, "無效的 Token"


@app.route('/api/login', methods=['POST'])
def login():
    username=request.json["username"]
    password=request.json["password"]
    user_id = 1
    token = generate_token(user_id)
    resp = make_response(jsonify({"message": "Login successful"}))
    resp.set_cookie('token', token, expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=30), path='/', httponly=True, secure=True,samesite='None')
    return resp
    
@app.route('/api/tryy', methods=['POST'])
def tryy():
    token = request.cookies.get('token')
    is_valid, user_id = verify_token(token)
    if is_valid:
        return jsonify({"message": "成功",'user_id':user_id})
    else:
        return jsonify({"message": "失敗"})
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)