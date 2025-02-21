import pymysql
import bcrypt
import jwt
import datetime
from flask import Flask, request,make_response, jsonify
'''
改SECRET_KEY
加上cors
'''
app = Flask(__name__)
db = pymysql.connect(host='localhost', 
                     user='root', 
                     password='08130813', 
                     database='open_point')

#cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))執行mysql命令。%s佔位符會被user_id取代，只有一個站位符時要加,
#fetchall() 取出所有結果，fetchone() 取出單個結果
#db.commit()提交更改
cursor = db.cursor()
SECRET_KEY = "your_secret_key"
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

# 建立帳號 密碼要二次哈希
@app.route('/api/customers/create', methods=['POST'])
def create_user():
    
    password = "12345"
    email = "11124214@nhu.edu.tw"
    number = "012345"
    gender = "Female"
    
    #password = request.json["password"]
    #email = request.json["email"]
    #number = request.json["number"]
    #gender = request.json["gender"]
    if not all([password, email, number, gender]):
        return jsonify({"error": "All fields are required"})
    
    # 密碼加密
    salt = bcrypt.gensalt()  # 生成隨機鹽
    password_hash = bcrypt.hashpw(password.encode(), salt)  # 加密密碼

    # 插入新用戶數據到資料庫
    cursor.execute("INSERT INTO users (password_hash, email, number, gender) VALUES (%s, %s, %s, %s)", (password_hash, email, number, gender))
    db.commit()

    # 檢查是否成功插入
    if cursor.rowcount == 1:
        return jsonify({"message": "User created successfully"})
    else:
        return jsonify({"error": "Failed to create user"})

#刪除帳號 要token
@app.route('/api/customers/delete', methods=['DELETE'])
def delete_user():
    token = request.cookies.get('token')
    is_valid, user_id = verify_token(token)
    if is_valid:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        db.commit()  
        return jsonify({"message": "User delete successfully"})
    else:
        return jsonify({"error":"Delete Failed"})

#登入帳號，要使用哈希密碼 生成token 透過email驗證
@app.route('/api/customers/login', methods=['POST'])
def login_user():
    token = request.cookies.get('token')
    email = "11124214@nhu.edu.tw"
    password = "12345"

    #email = request.json["email"]
    #password = request.json["password"]
    # 檢查 email 和 password 是否有提供
    if not email or not password:
        return jsonify({"message": "Email and password are required"})

    # 查詢資料庫來驗證用戶
    cursor.execute("SELECT user_id, password_hash FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()


    stored_hash = user[1]  # 密碼欄位
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):  # 驗證密碼是否正確
        # 密碼驗證通過，生成 token
        token = generate_token(user[0])

        # 設定 token 作為 cookie 返回
        resp = make_response(jsonify({"message": "Login successful", "token": token}))
        resp.set_cookie('token', token, expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=30), path='/', httponly=True, secure=True, samesite='None')

        return resp
    else:
        return jsonify({"message": "Invalid email or password"})

#查看設定，使用token
@app.route('/api/customers/myselfSetting',methods=['GET']) 
def myselfSetting():
    token = request.cookies.get('token')
    #is_valid, user_id = True, 18  # 假設 token 驗證通過，user_id = 18---測試用的
    is_valid,user_id = verify_token(token)
    # 查詢用戶資料
    if is_valid:
        cursor.execute("SELECT email, gender, number FROM users WHERE user_id = %s", (user_id,))
        setting = cursor.fetchone() 
        # 返回用戶設定資料
        return jsonify({"message": "User settings retrieved successfully","settings": setting})

    # 如果用戶不存在
    else:
        return jsonify({"message": "查詢失敗"})

@app.route('/api/customers/myselfSetting/update', methods=['POST'])
def setting_update():
    # 取得 token 並驗證
    token = request.cookies.get('token')
    is_valid, user_id = verify_token(token)
    
    if is_valid:
        # 從請求的 JSON 資料中提取參數
        try:
           # password = request.json.get("password")
            email = request.json.get("email")
            number = request.json.get("number")
            gender = request.json.get("gender")
        except Exception as e:
            return jsonify({"error": f"無效的請求資料: {str(e)}"}), 400

        # 檢查是否有空的欄位
        if not all([ email, number, gender]):
            return jsonify({"error": "欄位不能為空"}), 400

        # 使用資料庫操作時添加異常處理
        try:
            cursor.execute("""
                UPDATE users
                SET password=%s, email=%s, number=%s, gender=%s
                WHERE user_id=%s
            """, (email, number, gender, user_id))
            db.commit()
            return jsonify({"message": "使用者設定已成功更新"})
        except Exception as e:
            db.rollback()  # 回滾交易
            return jsonify({"error": f"資料庫錯誤: {str(e)}"}), 500
    else:
        return jsonify({"error": "無效或過期的 token"}), 401
    
#商品資訊(不使用token))
@app.route('/api/product/<product>', methods=['GET'])
def productPage(product): 
    cursor.execute("SELECT * FROM products WHERE name = %s", (product,))
    product_data = cursor.fetchone() 

    if not product_data:
        return jsonify({"error": "Product not found"})

    # 構建產品資料，去掉不需要的欄位
    product_info = {
        "name": product_data[1],        
        "ch_name": product_data[2],     
        "type": product_data[3],       
    }

    # 如果是套裝商品，查詢該套裝包含的單品資料
    if product_info["type"] == "bundle":
        cursor.execute("SELECT bi.item_id, i.ch_name, i.size, bi.quantity, bi.price FROM bundle_items bi JOIN items i ON bi.item_id = i.item_id WHERE bi.product_id = %s", (product_data[0],))  # 使用 product_data[0] 作為 product_id
        bundle_items = cursor.fetchall()  # 取得所有套裝內的單品資料

        # 建立單品資料清單
        bundle_info = []
        for item in bundle_items:
            bundle_info.append({
                "item_id": item[0],  
                "ch_name": item[1],  
                "size": item[2],     
                "price": item[4]     # 僅顯示大小和價格
            })

        # 回傳產品資料及套裝內單品資料
        return jsonify({
            "message": "Product found",
            "product": product_info,
            "bundle_items": bundle_info
        })

    # 如果不是套裝商品，查詢對應的單品資料
    cursor.execute("SELECT item_id, ch_name, size, price FROM items WHERE product_id = %s", (product_data[0],))  # 使用 product_data[0] 作為 product_id
    items_data = cursor.fetchall()  

    # 建立單品資料清單
    items_info = []
    for row in items_data:
        items_info.append({
            "item_id": row[0],   
            "ch_name": row[1], 
            "size": row[2],     
            "price": row[3]      
        })

    return jsonify({
        "message": "Product found",
        "product": product_info,
        "items": items_info
    })


#領取寄杯
@app.route('/api/receive/<int:user_id>', methods=['POST'])
def receive(user_id):
    try:
        # 從請求的 JSON 內容提取 token
        #token = request.json.get("token")
        product_id = request.json.get("product_id")
        item_id = request.json.get("item_id")

        # 驗證 token 是否有效
        #is_valid, result = verify_token(token)
        #if not is_valid:
        #    return jsonify({"error": result}), 401

        # 從 database 查詢產品和項目價格
        cursor.execute("SELECT price FROM items WHERE product_id = %s AND item_id = %s", (product_id, item_id))
        item = cursor.fetchone()

        if item is None:
            return jsonify({"error": "產品或項目不存在"}), 404

        item_price = item[0]
        
        # 插入新的交易記錄到 transactions 表
        cursor.execute("INSERT INTO transactions (user_id, type) VALUES (%s, 'reduce')", (user_id,))
        transaction_id = cursor.lastrowid  # 取得剛插入的 transaction_id

        # 插入交易明細到 transaction_detail 表
        cursor.execute("INSERT INTO transaction_detail (transaction_id, product_id, item_id, quantity)VALUES (%s, %s, %s, 1)", (transaction_id, product_id, item_id))


        # 提交庫存變動
        db.commit()

        # 返回成功訊息
        return jsonify({"message": "領取成功", "transaction_id": transaction_id}), 200

    except Exception as e:
        db.rollback()  # 發生錯誤時，回滾變更
        return jsonify({"error": str(e)}), 500


#購買商品 token
@app.route('/api/product/buy/<product_id>', methods=['POST'])
def buyProduct(product_id):
   # 從 JSON 獲取商品的 product_id 和數量
    product_id = request.json.get("product")
    quantity = request.json.get("quantity", 1)  # 默認數量為 1

    # 查詢產品
    with db.cursor() as cursor:
        cursor.execute("SELECT product_id, type FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()

    # 如果產品不存在
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # 手動解包查詢結果
    product_id, product_type = product

    # 檢查產品類型
    if product_type in ['coffee', 'latte', 'tea', 'food']:
        # 單一商品的購買邏輯
        with db.cursor() as cursor:
            cursor.execute("SELECT item_id FROM items WHERE product_id = %s", (product_id,))
            item = cursor.fetchone()
            if not item:
                return jsonify({"message": "Item not found"}), 404

            # 記錄交易
            cursor.execute("INSERT INTO transactions (user_id, type) VALUES (%s, 'add')", (user_id,))
            transaction_id = cursor.lastrowid

            # 插入交易詳情
            item_id = item[0]  # 手動解包 item_id
            cursor.execute(
                "INSERT INTO transaction_detail (transaction_id, product_id, item_id, quantity) VALUES (%s, %s, %s, %s)",
                (transaction_id, product_id, item_id, quantity)
            )
        db.commit()
        return jsonify({"message": "Product purchased successfully"}), 200

    elif product_type == 'bundle':
        # 套組商品的購買邏輯
        with db.cursor() as cursor:
            cursor.execute("SELECT item_id, quantity FROM bundle_items WHERE product_id = %s", (product_id,))
            bundle_items = cursor.fetchall()
            if not bundle_items:
                return jsonify({"message": "Bundle items not found"}), 404

            # 記錄交易
            cursor.execute("INSERT INTO transactions (user_id, type) VALUES (%s, 'add')", (user_id,))
            transaction_id = cursor.lastrowid

            # 插入每個套組商品的交易詳情
            for bundle_item in bundle_items:
                item_id, bundle_quantity = bundle_item  # 解包每個項目
                total_quantity = bundle_quantity * int(quantity)  # 計算套組商品的總數量
                cursor.execute(
                    "INSERT INTO transaction_detail (transaction_id, product_id, item_id, quantity) VALUES (%s, %s, %s, %s)",
                    (transaction_id, product_id, item_id, total_quantity)
                )
        db.commit()
        return jsonify({"message": "Bundle purchased successfully"}), 200

    else:
        return jsonify({"message": "Invalid product type"}), 400
'''
#查看擁有購物車 token
@app.route('/api/product/cup_storage/<user_id>', methods=['GET'])
def storageTable(user_id):
'''

#查看交易紀錄
@app.route('/api/transactions/<t_id>', methods=['GET'])
def transactions(t_id):
    query = """
    SELECT t.user_id, t.date, p.name, i.price
    FROM transactions t
    JOIN transaction_detail td ON t.transaction_id = td.transaction_id
    JOIN products p ON td.product_id = p.product_id
    JOIN items i ON td.product_id = i.product_id
WHERE t.transaction_id = %s

cursor.execute(query, (t_id,))
transaction = cursor.fetchone()

if transaction:
    # 查詢成功，返回交易紀錄與產品名稱及價格，並格式化為指定的結構
    return jsonify({
        "user_id": transaction[0],
        "name": transaction[2],  # 產品名稱
        "price": transaction[3],  # 產品價格
        "date": transaction[1]    # 交易日期
    })
else:
    return jsonify({"error": "交易紀錄不存在"}), 404
"""

if __name__ == '__main__':
    app.run(debug=True)