import pymysql
import bcrypt
import jwt
import datetime
from flask import Flask, request ,make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials =True, origins=["https://b13d-2001-b400-e4d9-bce6-102e-6360-57c4-6395.ngrok-free.app"])
db = pymysql.connect(host='localhost', 
                     user='root', 
                     password='08130813', 
                     database='open_point')

#cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))執行mysql命令。%s佔位符會被user_id取代，只有一個站位符時要加,
#fetchall() 取出所有結果，fetchone() 取出單個結果
#db.commit()提交更改
cursor = db.cursor()
SECRET_KEY = "11124138"
TOKEN_EXPIRY = 60
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
    password = request.json["password"]
    email = request.json["email"]
    number = request.json["number"]
    gender = request.json["gender"]
    if not all([password, email, number, gender]):
        return jsonify({"error": "All fields are required"})
    
    # 密碼加密
    salt = bcrypt.gensalt()  # 生成隨機鹽
    password_hash = bcrypt.hashpw(password.encode(), salt)  # 加密密碼

    # 插入新用戶數據到資料庫
    cursor.execute("INSERT INTO users (password_hash, email, number, gender) VALUES (%s, %s, %s, %s)", 
                   (password_hash, email, number, gender))
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
        try:
            # 先刪除依賴的資料（如果沒設置 ON DELETE CASCADE）
            cursor.execute("DELETE FROM transaction_detail WHERE transaction_id IN (SELECT transaction_id FROM transactions WHERE user_id = %s)", (user_id,))
            cursor.execute("DELETE FROM transactions WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM cup_storage WHERE user_id = %s", (user_id,))
            
            # 刪除用戶
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            db.commit()
            return jsonify({"message": "刪除帳號成功"})
        except Exception as e:
            db.rollback()
            return jsonify({"error": f"Delete Failed: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid token or user not authenticated"}), 401

#登入帳號，要使用哈希密碼 生成token 透過email驗證
@app.route('/api/customers/login', methods=['POST'])
def login_user():

    email = request.json["email"]
    password = request.json["password"]
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
        print(token)
        # 設定 token 作為 cookie 返回
        resp = make_response(jsonify({"token": token}))
        resp.set_cookie('token', token,expires=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30),samesite='None', secure=True, domain='.ngrok-free.app')  # 設置為具體的 domain 或使用空白字符串
        resp.set_cookie('tokenn', token,expires=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30),samesite='None', secure=True, domain='.ngrok-free.app')
        return resp
    else:
        return jsonify({"message": "Invalid email or password"})

#查看設定，使用token
@app.route('/api/customers/myselfSetting',methods=['GET']) 
def myselfSetting():
    token = request.cookies.get('token')
    is_valid, user_id = verify_token(token)

    if is_valid:
        try:
            cursor.execute("""
                SELECT email, gender, number
                FROM users
                WHERE user_id = %s
            """, (user_id,))
            setting = cursor.fetchone()

#如果找到用戶資料，返回設定
            if setting:
                return jsonify({
                    "message": "更新成功",
                    "settings": {
                        "email": setting[0],
                        "gender": setting[1],
                        "number": setting[2]
                    }
                })
            else:
                return jsonify({"message": "用戶資料不存在"})
        except Exception as e:
            return jsonify({"error": f"資料庫錯誤: {str(e)}"})
    else:
        # 如果 token 驗證失敗，返回未授權的錯誤
        return jsonify({"message": "無效或過期的 token"})
    
#更新設定
@app.route('/api/customers/myselfSetting/update', methods=['PUT'])
def setting_update():
    # 取得 token 並驗證
    token = request.cookies.get('token')
    is_valid, user_id = verify_token(token)
    
    if is_valid:
        try:
            password = request.json["password"]
            email = request.json["email"]
            number = request.json["number"]
            gender = request.json["gender"]
        except Exception as e:
            return jsonify({"error": f"無效的請求資料: {str(e)}"})

        # 檢查是否有空的欄位
        if not all([password,email, number, gender]):
            return jsonify({"error": "欄位不能為空"})
        salt = bcrypt.gensalt()  # 生成隨機鹽
        password_h = bcrypt.hashpw(password.encode(), salt)
        # 使用資料庫操作時添加異常處理
        try:
            # 這裡不會更新 password 欄位，只更新 email、number 和 gender
            cursor.execute("""
                UPDATE users
                SET password_hash=%s,email=%s, number=%s, gender=%s
                WHERE user_id=%s
            """, (password_h,email, number, gender, user_id))
            db.commit()

            # 返回成功訊息
            return jsonify({"message": "使用者設定已成功更新"})
        except Exception as e:
            db.rollback()  # 回滾交易
            return jsonify({"error": f"資料庫錯誤: {str(e)}"})
    else:
        return jsonify({"error": "無效或過期的 token"})
    
#商品資訊(不使用token))
@app.route('/api/product/<product>', methods=['GET'])
def productPage(product): 
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product,))
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
                "price": item[4],
                "quantity":item[3]
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
@app.route('/api/receive', methods=['POST'])
def receive():
    try:
        token = request.cookies.get("token")
        product_id = request.json["product_id"]
        item_id = request.json["item_id"]
        inputField = request.json["inputField"]
        is_valid, user_id = verify_token(token)
        if not is_valid:
            return jsonify({"error": user_id}) 
        
        # 插入新的交易記錄到 transactions 表
        
        cursor.execute("INSERT INTO transactions (user_id, type) VALUES (%s, 'reduce')", (user_id,))
        transaction_id = cursor.lastrowid  # 取得剛插入的 transaction_id
        # 插入交易明細到 transaction_detail 表
        cursor.execute("INSERT INTO transaction_detail (transaction_id, product_id, item_id, quantity) VALUES (%s, %s, %s, %s)",
                       (transaction_id, product_id, item_id,inputField))

        db.commit()
       
        return jsonify({"message": "領取成功", "transaction_id": transaction_id})
    except Exception as e:
        db.rollback()  # 發生錯誤時，回滾變更
        return jsonify({"error": "發生錯誤", "message": str(e)})

#查看交易紀錄 token 、查看是add還是reduce、價格、size、交易數量、name
@app.route('/api/transactions', methods=['POST'])
def transactions():
# 從 request 中獲取參數，使用 request.args.get() 來獲取查詢字串中的參數
    token = request.cookies.get("token")
    transaction_type = request.json["transaction_type"]  # 查詢條件類型
    product_type = request.json["product_type"]  # 商品類型條件
    order_by = request.json["order_by"]  # 默認按日期排序
# 驗證 token
    is_valid, user_id = verify_token(token)
    if not is_valid:
        return jsonify({"error": "無效的token"})
    where_conditions = ["t.user_id = %s"]
    params = [user_id]
    if transaction_type:  # 動態添加交易類型條件
        where_conditions.append("t.type = %s")
        params.append(transaction_type)

    if product_type:  # 動態添加商品類型條件
        where_conditions.append("p.type = %s")
        params.append(product_type)
    if product_type or transaction_type: 
        where_clause = " AND ".join(where_conditions)
    query = f"""
    SELECT 
        t.type AS transaction_type,
        t.date AS transaction_date,
        p.name AS product_name,
        p.type AS product_type,
        MAX(td.quantity) AS quantity,
        CASE
            WHEN p.type = 'bundle' THEN GROUP_CONCAT(CONCAT(i.ch_name, ' (',i.size,'*', bi.quantity, ')') SEPARATOR ', ')
            ELSE GROUP_CONCAT(CONCAT(p.ch_name, ' (',i.size, ')') SEPARATOR ', ')
        END AS item_details
        FROM 
            transactions t
        JOIN 
            transaction_detail td ON t.transaction_id = td.transaction_id
        JOIN 
            products p ON td.product_id = p.product_id
        LEFT JOIN 
            bundle_items bi ON p.product_id = bi.product_id
        LEFT JOIN 
            items i ON td.item_id = i.item_id
        WHERE 
            {where_clause}
        GROUP BY 
            t.transaction_id, td.product_id, t.date
        ORDER BY 
            {order_by}
            ;
    """

    #ON bi.item_id = i.item_id
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    # 組織回應資料
    transactions = []
    for row in results:
        transaction = {
            "transaction_type": row[0],
            "transaction_date": row[1],
            "product_name": row[2],
            "product_type": row[3],
            "quantity": row[4],
            "item_details": row[5],
            
        }
        transactions.append(    transaction)

    # 返回結果
    return jsonify(transactions), 200

#查看使用者擁有的商品
@app.route('/api/OwnedProducts', methods=['GET'])
def OwnedProducts():
    token = request.cookies.get("token")
    is_valid, user_id = verify_token(token)     
    if is_valid:
        # 查詢用戶擁有的商品及其數量
        cursor.execute(("select i.ch_name,c.remaining_cups,c.item_id,i.product_id,i.size from cup_storage  c join items i on i.item_id = c.item_id where user_id = %s"), (user_id,))
        results = cursor.fetchall()

        # 如果查詢有結果，返回擁有的商品列表
        if results:
            products = []
            for result in results:
                products.append({
                    "ch_name": result[0],
                    "quantity": result[1],# 添加 quantity
                    "item_id":result[2],
                    "product_id":result[3],
                    "size":result[4]

                })
            return jsonify({"owned_products": products})
        else:
            return jsonify({"error": "沒有擁有的商品"})
    else:
        return jsonify({"error": "請檢查 token"})

#購買商品 token
@app.route('/api/product/buy', methods=['POST'])
def buyProduct():
    token = request.cookies.get("token")
    item_id = request.json["item_id"]
    product_id = request.json["product_id"]
    quantity = request.json["quantity"]
    is_valid, user_id = verify_token(token)

    if is_valid:
    # 查詢商品是否為套裝商品
        query = """
            SELECT p.product_id, p.ch_name, p.name, p.type
            FROM products p
            WHERE p.product_id = %s
        """
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        
        if not product:
            return jsonify({"error": "產品不存在"})

        product_id, ch_name, name, type = product

        if type == "bundle":
            bundle_query = """
                SELECT i.item_id, p.ch_name, p.name, i.price, i.size
                FROM bundle_items bi
                JOIN items i ON bi.item_id = i.item_id
                JOIN products p ON i.product_id = p.product_id
                WHERE bi.product_id = %s
            """
            cursor.execute(bundle_query, (product_id,))
            bundle_items = cursor.fetchall()

            if not bundle_items:
                return jsonify({"error": "該套裝商品內無可用商品"})

            # 創建交易記錄
            transaction_type = 'add'
            transaction_query = "INSERT INTO transactions (user_id, type) VALUES (%s, %s)"
            cursor.execute(transaction_query, (user_id, transaction_type))
            db.commit()

            # 取得新插入的 transaction_id
            transaction_id = cursor.lastrowid

            # 插入每一個套裝商品的交易明細
            for item in bundle_items:
                item_id, ch_name, name, price, size = item
                transaction_detail_query = "INSERT INTO transaction_detail (transaction_id, product_id, item_id, quantity) VALUES (%s, %s, %s, %s)"
                cursor.execute(transaction_detail_query, (transaction_id, product_id, item_id, quantity))
            db.commit()

            return jsonify({
                "ch_name": ch_name,
                "name": name,
                "quantity": quantity,
                "items": bundle_items
            })

        else:
            # 如果是單品商品的處理邏輯
            # 創建交易記錄
            transaction_type = 'add'
            transaction_query = "INSERT INTO transactions (user_id, type) VALUES (%s, %s)"
            cursor.execute(transaction_query, (user_id, transaction_type))
            db.commit()

            # 取得新插入的 transaction_id
            transaction_id = cursor.lastrowid

            transaction_detail_query = "INSERT INTO transaction_detail (transaction_id, product_id, item_id, quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(transaction_detail_query, (transaction_id, product_id, item_id, quantity))
            db.commit()

            return jsonify({"message":"成功購買"
            })
    else:
        return jsonify({"error": "無效的 token"}),500  



''''
#查看擁有購物車 token
@app.route('/api/product/cup_storage/<user_id>', methods=['GET'])
def storageTable(user_id):







'''
@app.route('/api/auth/validate', methods=['GET'])
def validate_user():
    token = request.cookies.get("token")
    is_valid, user_id = verify_token(token)
    if is_valid:
        # 如果驗證成功，返回用戶資料
        cursor.execute("SELECT user_id, email, gender, number FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return jsonify({
                "isLoggedIn": True,
                "user": {
                    "user_id": user_data[0],
                    "email": user_data[1],
                    "gender": user_data[2],
                    "number": user_data[3]
                }
            })
    return jsonify({"isLoggedIn": False}), 401



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)