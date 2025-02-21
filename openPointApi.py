import pymysql
import bcrypt
import jwt
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
db = pymysql.connect(host='localhost',
					 user='root',
					 password='08130813',
					 database='open_point')
					 
cursor = db.cursor()
SECRET_KEY = "11124138"
TOKEN_EXPIRY = 30
token_storage = {}

#GET讀取，POST新增，PUT修改如果沒有新增，DELETE刪除，PATCH只更新部分，GET是指前端到後端的請求所以你
#cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))執行mysql命令。%s佔位符會被user_id取代，只有一個站位符時要加,
#fetchall() 取出所有結果，fetchone() 取出單個結果
#db.commit()提交更改，insert和updata和delete要用
'''
先不用
200 OK： 請求成功處理，並返回結果。
201 Created： 資源已成功建立（例如新增一筆資料）。
400 Bad Request： 用戶端的請求無效（例如參數錯誤）。
401 Unauthorized： 用戶端未授權，通常需要登入或提供有效的身份憑證。
403 Forbidden： 用戶端已授權，但無法訪問該資源。
404 Not Found： 請求的資源不存在。
500 Internal Server Error： 伺服器端的程式執行發生錯誤。
'''
'''
用戶登錄：用戶輸入帳號和密碼，後端服務器驗證成功後生成 JWT。
生成JWT：後端生成一個包含用戶 ID 和過期時間的 JWT。
傳遞JWT：將JWT返回給用戶，並存儲在前端的 localStorage 或 cookie 中。
用戶請求API：用戶發起API請求，服務器檢查請求的JWT。
驗證JWT：服務器解碼JWT，檢查其過期時間。
過期Token管理：定期清除過期的JWT，以防止過期token被用來訪問受保護的資源。
'''

# 生成 JWT Token
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
	
#建立帳號
@app.route('/api/customers/create',methods=['POST']) 
def create_user():
	password = "lee"#request.form["password"]
	email = "lee@ffff"#request.form["email"]
	gender = "male"#request.form["gender"]
	number = "0988888888"#request.form["number"]
	
	'''
	新增一條
	data=( 'Jane Doe', 'da2odf3232s2f212', 'jane@example.com')
	如果新增兩條
	data = [
	(124, 'Jane Doe', '8765432109', 'jane@example.com'),
	(125, 'Alice Smith', '7654321098', 'alice@example.com')
	]
	'''

	if gender is None or password is None or email is None or number is None:
		return jsonify({"error": " cannot be empty"})

	salt = bcrypt.gensalt()  # 產生鹽
	password_hash = bcrypt.hashpw(password.encode(), salt)#二次加密

	cursor.execute("INSERT INTO users ( email,password_hash, gender, number) VALUES ( %s, %s, %s, %s)",(email,password_hash,gender,number))
	db.commit()
	if cursor.rowcount == 1:
		return jsonify({"message": "User created successfully"})
	else:
		return jsonify({"message": "Failed to create user"})
#登入，二次哈希密碼
@app.route('/api/customers/login',methods=['POST']) 
def signIn_user():
	email = "lee@ffff"#request.form["email"]
	password = "lee"#request.form["password"]
	cursor.execute("select user_id,password_hash from users where email=%s", (email,))
	user = cursor.fetchone()#沒傳回是None
	if user is None:
		return jsonify({"message": "Invalid ID or password"})
	else:
		stored_hash = user[1]#密碼欄位
		if bcrypt.checkpw(password.encode(), stored_hash.encode()):
			token = generate_token(user[0])
			return jsonify({"message": "Sign-in successful", "token": token})
		else:
			return jsonify({"message": "Invalid ID or password"})
		
#刪除帳號
@app.route('/api/customers/delete',methods=['DELETE']) 
def delete_user():
	token = request.form["token"]
	is_valid, user_id = verify_token(token)
	if is_valid:
		cursor.execute("delete from users where user_id = %s",(user_id,))
		db.commit()
		return jsonify({"message": "刪除成功"})
	else:
		return jsonify({"message": "刪除失敗"})
	
	

#查看設定，每次開啟設定頁面都會查一次
@app.route('/api/customers/myselfSetting',methods=['GET']) 
def myselfSetting():
	token = request.form["token"]
	is_valid, user_id = verify_token(token)
	if is_valid:
		cursor.execute("select email,gender,number,created_at,updated_at from users where user_id = %s",(user_id,))
		setting = cursor.fetchall()
		return jsonify({"message": "User settings retrieved successfully", "settings": setting})
	else:
		return jsonify({"message": "查詢失敗"})
	

#更新設定
@app.route('/api/customers/myselfSetting/updata',methods=['POST']) 
def settingUpdata():#先顯示在更新，如所以已有格子不會是空可用post
	token = request.form["token"]
	is_valid, user_id = verify_token(token)
	if is_valid:
		password = request.form["password"]
		email = request.form["email"]
		gender = request.form["gender"]
		number = request.form["number"]
		if gender is None or password is None or email is None or number is None:
			return jsonify({"error": " cannot be empty"})
		cursor.execute("updata users set password=%s ,email=%s,gender=%s,number=%s where user_id = %s",(password,email,gender,number,user_id))
		return jsonify({"message": "Update successful"})
	else:
		return jsonify({"message": "查詢失敗"})
	
#商品資訊
@app.route('/api/product/<product>',methods=['GET']) 
def productPage(product):#確定空list可以len()==0
	cursor.execute("select * from products where name = %s",(product,))
	product_list = cursor.fetchall()
	
	if len(product_list)==0:
		cursor.execute("select * from bundle_item where bundle_name = %s",(product,))
		blist = cursor.fetchall()
		if len(blist)==0:
			return jsonify({"error": "product search failed"})
		elif len(blist)!=0:
			return jsonify({"massage": "product search successful","product":blist})
	elif len(product_list)!=0:
		return jsonify({"massage": "product search successful","product":product_list})   


#購買商品，增加一個transcations
@app.route('/api/product/buy/<user_id>',methods=['POST']) 
def buyProduct(user_id):
	product = request.form["product"]
	cursor.execute()
	
	
'''
#領取
@app.route('/api/product/receive/<user_id>',methods=['POST']) 
def receive(user_id):
	
	
#查看購物車，
@app.route('/api/product/cup_storage/<user_id>',methods=['GET']) 
def storageTable(user_id):
	cursor.execute("select p.product_name,remaining_cups,expiration_date from cup_storage cs join products p on cs.product_id = p.product_id where user_id=%s",(user_id,))
	data = cursor.fetchall()
	
	
#查看交易紀錄
@app.route('/api/transactions/<t_id>',methods=['GET']) 
def transactions(t_id):

'''

if __name__ == '__main__':
	app.run(debug=True)
	'''

INSERT INTO users (email, password_hash, gender, number, created_at, updated_at) VALUES
('user1@example.com', '$2b$10$abcdefghijklmnopqrstuv1234567890ab', 'male', '0912345678', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user2@example.com', '$2b$10$qrstuv1234567890abcdefghijklmnopab', 'female', '0923456789', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user3@example.com', '$2b$10$mnopqrstuv1234567890abcdefghijklab', 'male', '0934567890', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user4@example.com', '$2b$10$klmnopqrstuv1234567890abcdefghijab', 'female', '0945678901', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user5@example.com', '$2b$10$ghijklmnopqrstuv1234567890abcdefab', 'male', '0956789012', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user6@example.com', '$2b$10$cdefghijklmnopqrstuv1234567890ab', 'female', '0967890123', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user7@example.com', '$2b$10$zxcvbnmasdfghjklqwertyuiop1234ab', 'male', '0978901234', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user8@example.com', '$2b$10$asdfghjklqwertyuiopzxcvbnm1234ab', 'female', '0989012345', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user9@example.com', '$2b$10$qwertyuiopzxcvbnmasdfghjkl1234ab', 'male', '0990123456', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user10@example.com', '$2b$10$poiuytrewqlkjhgfdsamnbvcxz1234ab', 'female', '0912345670', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


-- 插入到 products 表
INSERT INTO products (name, ch_name, type) VALUES
('Caffe Latte', '那堤', 'coffee'),
('Caffe Americano', '美式咖啡', 'coffee'),
('Caramel Macchiato', '焦糖瑪奇朵', 'coffee'),
('Espresso', '濃縮咖啡', 'coffee'),
('Cappuccino', '卡布奇諾', 'coffee'),
('Caffe Mocha', '摩卡', 'coffee'),
('Cocoa Macchiato', '可可瑪奇朵', 'coffee'),
('Black Tea Latte', '經典紅茶那堤', 'latte'),
('Pure Matcha Latte', '醇濃抹茶那堤', 'latte'),
('Earl Grey Tea Latte', '伯爵茶那堤', 'latte'),
('Rose Fancy Tea Latte', '玫瑰蜜香茶那堤', 'latte'),
('Iced Black Tea Latte', '冰經典紅茶那堤', 'latte'),
('English Breakfast Tea', '英式早餐紅茶', 'tea'),
('Black Tea with Ruby Grapefruit and Honey', '蜜柚紅茶', 'tea'),
('Alishan Oolong Tea', '阿里山烏龍茶', 'tea'),
('Iced Shaken Lemon Black Tea', '冰搖檸檬紅茶', 'tea'),
('Mushroom Soup Flavored Bread', '菇菇濃湯法烤麵包', 'food'),
('Strawberry Cheese Bread', '草莓起司麵包', 'food'),
('Chocolate Toast', '巧克力雙色吐司', 'food'),
('Mentaiko Cheese Bagel', '明太子起司貝果', 'food'),
('Bacon & Cheese Bread', '培根起司軟歐麵包', 'food'),
('Blueberry Bagel', '藍莓果粒貝果', 'food'),
('Cinnamon Roll', '肉桂捲', 'food'),
('Honey & Milk Bread', '蜂蜜牛奶麵包', 'food'),
('Cheesy Bread', '軟法麵包', 'food'),
('Double Cheese Bread', '雙起司軟歐麵包', 'food');

INSERT INTO items (ch_name, product_id, size, price) VALUES
('那堤', 1, 'medium', 120),
('那堤', 1, 'large', 135),
('那堤', 1, 'extraLarge', 150),
('美式咖啡', 2, 'medium', 110),
('美式咖啡', 2, 'large', 125),
('美式咖啡', 2, 'extraLarge', 140),
('焦糖瑪奇朵', 3, 'medium', 130),
('焦糖瑪奇朵', 3, 'large', 145),
('焦糖瑪奇朵', 3, 'extraLarge', 160),
('濃縮咖啡', 4, 'small', 90),
('卡布奇諾', 5, 'medium', 125),
('卡布奇諾', 5, 'large', 140),
('卡布奇諾', 5, 'extraLarge', 155),
('摩卡', 6, 'medium', 135),
('摩卡', 6, 'large', 150),
('摩卡', 6, 'extraLarge', 165),
('可可瑪奇朵', 7, 'medium', 140),
('可可瑪奇朵', 7, 'large', 155),
('可可瑪奇朵', 7, 'extraLarge', 170),
('經典紅茶那堤', 8, 'medium', 125),
('經典紅茶那堤', 8, 'large', 140),
('經典紅茶那堤', 8, 'extraLarge', 155),
('醇濃抹茶那堤', 9, 'medium', 130),
('醇濃抹茶那堤', 9, 'large', 145),
('醇濃抹茶那堤', 9, 'extraLarge', 160),
('伯爵茶那堤', 10, 'medium', 135),
('伯爵茶那堤', 10, 'large', 150),
('伯爵茶那堤', 10, 'extraLarge', 165),
('玫瑰蜜香茶那堤', 11, 'medium', 140),
('玫瑰蜜香茶那堤', 11, 'large', 155),
('玫瑰蜜香茶那堤', 11, 'extraLarge', 170),
('冰經典紅茶那堤', 12, 'medium', 120),
('冰經典紅茶那堤', 12, 'large', 135),
('冰經典紅茶那堤', 12, 'extraLarge', 150),
('英式早餐紅茶', 13, 'medium', 110),
('英式早餐紅茶', 13, 'large', 125),
('英式早餐紅茶', 13, 'extraLarge', 140),
('蜜柚紅茶', 14, 'medium', 120),
('蜜柚紅茶', 14, 'large', 135),
('蜜柚紅茶', 14, 'extraLarge', 150),
('阿里山烏龍茶', 15, 'medium', 130),
('阿里山烏龍茶', 15, 'large', 145),
('阿里山烏龍茶', 15, 'extraLarge', 160),
('冰搖檸檬紅茶', 16, 'medium', 125),
('冰搖檸檬紅茶', 16, 'large', 140),
('冰搖檸檬紅茶', 16, 'extraLarge', 155),
('菇菇濃湯法烤麵包', 17, 'noSize', 65),
('草莓起司麵包', 18, 'noSize', 70),
('巧克力雙色吐司', 19, 'noSize', 75),
('明太子起司貝果', 20, 'noSize', 80),
('培根起司軟歐麵包', 21, 'noSize', 85),
('藍莓果粒貝果', 22, 'noSize', 70),
('肉桂捲', 23, 'noSize', 60),
('蜂蜜牛奶麵包', 24, 'noSize', 65),
('軟法麵包', 25, 'noSize', 50),
('雙起司軟歐麵包', 26, 'noSize', 75);


INSERT INTO products (name, ch_name, type) VALUES
('Latte Lover Bundle', '拿鐵愛好者套卷', 'bundle'),
('Morning Essentials Bundle', '早晨必備套卷', 'bundle');

INSERT INTO bundle_items (product_id, item_id, quantity,price) VALUES
	-- 拿鐵愛好者套卷 (Latte Lover Bundle): 包含 3 杯經典拿鐵（特大杯）
(27, 3, 10,1300),
	-- 早晨必備套卷 (Morning Essentials Bundle): 包含 2 杯美式咖啡（大杯）和 2 份蜂蜜牛奶麵包
(28, 5, 2,350), -- 美式咖啡（大杯）
(28, 54, 2,350); -- 蜂蜜牛奶麵包

	'''
	
	'''
CREATE TABLE users (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	password_hash VARCHAR(60) NOT NULL,
	gender ENUM('male','female'),
	number varchar(10) not null,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
); 
CREATE TABLE products (
	product_id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	ch_name varchar(255) not null,
	type ENUM('coffee','latte','tea','food','bundle') NOT NULL, -- 'item' 表示單一商品，'bundle' 表示套卷
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE items (
	item_id INT AUTO_INCREMENT PRIMARY KEY,
	product_id INT NOT NULL, -- 對應到 product 表
	ch_name varchar(255) not null,
	size enum('small','medium','large','extraLarge','noSize'),
	price INT NOT NULL,
	FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);
CREATE TABLE bundle_items (
	bundle_item_id INT AUTO_INCREMENT PRIMARY KEY,
	product_id INT NOT NULL, -- 對應到 product 表，必須為 type = 'bundle'
	item_id INT NOT NULL, -- 對應到 item 表
	quantity INT DEFAULT 1, -- 該商品在套卷中的數量
	price INT NOT NULL,
	FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
	FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);
CREATE TABLE cup_storage (
	cup_storage_id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL, -- 用戶 ID
	item_id INT NOT NULL UNIQUE, -- 商品 ID，例如咖啡
	remaining_cups INT NOT NULL, -- 剩餘寄杯數量
	FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
	FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);

CREATE TABLE transactions (
	transaction_id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL, -- 用戶 ID
	type ENUM('add', 'reduce') NOT NULL, -- 表示交易類型
	date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE transaction_detail (
	transaction_detail_id INT AUTO_INCREMENT PRIMARY KEY,
	transaction_id INT NOT NULL, -- 對應到 transaction 表
	product_id INT NOT NULL,
	item_id INT NOT NULL, -- 商品 ID
	quantity INT NOT NULL, -- 商品數量
	FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE,
	FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
	FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);


--測試用
create table test(
	test varchar(255),
	intt int
);



--如果增加transaction_detail執行觸發器，更新cup_storage，先辨識是不是reduce然後扣掉，之後再查看是否為0，如果是0則直接刪除cup_storage欄位
DELIMITER //
CREATE TRIGGER update_cup_storage_after_reduce 
AFTER INSERT ON transaction_detail
FOR EACH ROW
BEGIN
    DECLARE id INT;

    -- 從 transactions 表中選擇 user_id
    SELECT user_id INTO id FROM transactions WHERE transaction_id = NEW.transaction_id;
    -- 僅針對 'reduce' 類型的交易
    IF (SELECT type FROM transactions WHERE transaction_id = NEW.transaction_id) = 'reduce' THEN
        -- 檢查是否足夠領取
        IF (SELECT remaining_cups FROM cup_storage WHERE user_id = id AND item_id = NEW.item_id) < NEW.quantity THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Remaining cups cannot be negative.';
        ELSE
            -- 更新剩餘杯數
            UPDATE cup_storage SET remaining_cups = remaining_cups - NEW.quantity WHERE user_id = id AND item_id = NEW.item_id;
            -- 如果剩餘杯數小於或等於 0，刪除記錄
            IF (SELECT remaining_cups FROM cup_storage WHERE user_id = id AND item_id = NEW.item_id) <= 0 THEN
                DELETE FROM cup_storage WHERE user_id = id AND item_id = NEW.item_id;
            END IF;
        END IF;
    END IF;
END //
DELIMITER ;




--如果增加transaction_detail執行觸發器，更新cup_storage，先辨識是不是add，之後再辨識bundle還是其他，然後再更新
DELIMITER //
CREATE TRIGGER update_cup_storage_after_add AFTER INSERT ON transaction_detail
FOR EACH ROW
BEGIN
	DECLARE total_quantity INT DEFAULT 0;
	-- 判斷交易類型
	IF (select type from transactions where transaction_id=NEW.transaction_id) = 'add' THEN
		IF (select type from products where product_id=NEW.product_id ) = 'bundle' THEN
			INSERT INTO cup_storage (user_id, item_id, remaining_cups)
			SELECT (select user_id from transactions where transaction_id=NEW.transaction_id), item_id, quantity
			FROM bundle_items
			WHERE product_id = NEW.product_id
			ON DUPLICATE KEY UPDATE remaining_cups = COALESCE(remaining_cups, 0) + VALUES(remaining_cups);
		ELSE
			-- 獲取套卷中包含的所有 item 的總數量
			SET total_quantity = NEW.quantity;
			INSERT INTO cup_storage (user_id, item_id, remaining_cups)
			VALUES ((select user_id from transactions where transaction_id=NEW.transaction_id), NEW.item_id, total_quantity)
			ON DUPLICATE KEY UPDATE remaining_cups = remaining_cups + total_quantity;
		END IF;
	END IF;
END //
DELIMITER ;




新增bundle的話
INSERT INTO transactions (user_id, type) VALUES (1, 'add');#記得下面的transaction_detail表裡面的transaction_id要等transactions新增完後查詢他的transactions
INSERT INTO transaction_detail (transaction_id,product_id, item_id, quantity) VALUES (6,28,5, 1);#product_id要填你要增加的bundle，然後item_id你填bundle其中一個就好
新增item則是要輸入
INSERT INTO transactions (user_id, type) VALUES (1, 'add');#記得下面的transaction_detail表裡面的transaction_id要等transactions新增完後查詢他的transactions
INSERT INTO transaction_detail (transaction_id,product_id, item_id, quantity) VALUES (2, 1,3, 1);#這項商品對應的product_id和他對應的item_id
領取則是
INSERT INTO transactions (user_id, type) VALUES (1, 'reduce');#記得下面的transaction_detail表裡面的transaction_id要等transactions新增完後查詢他的transactions
INSERT INTO transaction_detail (transaction_id, product_id,item_id, quantity) VALUES (4,24,54,1);#要領取的product_id和要領取的item_id，以及領取數量
'''


'''

DELIMITER //
CREATE TRIGGER test AFTER INSERT ON transaction_detail
FOR EACH ROW
BEGIN
	declare a int DEFAULT NEW.transaction_id;
	declare b int;
 	declare c varchar(10);
	SET b = 100 + NEW.transaction_id;
	select type into c from transactions where transaction_id=NEW.transaction_id;
	IF c = 'add' THEN
		INSERT INTO test (test, intt)
		VALUES (c, b);
	END IF;
END //
DELIMITER ;




SELECT 
    t.type AS transaction_type,
    t.date AS transaction_date,
    p.name as product_name,
    p.type AS product_type,  -- 顯示商品的類型
    td.quantity
    
FROM 
    transactions t
JOIN 
    transaction_detail td ON t.transaction_id = td.transaction_id
JOIN 
    products p ON td.product_id = p.product_id
WHERE 
    t.user_id = 1; -- 替換為目標用戶的 user_id



 
 
 
SELECT 
    t.type AS transaction_type,
    t.date AS transaction_date,
    p.name AS product_name,
    p.type AS product_type,  -- 顯示商品的類型
    MAX(td.quantity) AS quantity,  -- 使用 MAX 聚合函數以避免錯誤
    -- 如果是套裝類型 (bundle)，顯示套裝中的商品（每個商品單獨列出）
    CASE
        WHEN p.type = 'bundle' THEN GROUP_CONCAT(CONCAT(i.ch_name, ' (',i.size,'*', bi.quantity, ')') SEPARATOR ', ')
        ELSE p.ch_name  -- 如果不是套裝類型，則顯示商品名稱
    END AS item_details  -- 顯示商品詳情，對於非 bundle 顯示商品名稱，對於 bundle 顯示套裝內商品
FROM 
    transactions t
JOIN 
    transaction_detail td ON t.transaction_id = td.transaction_id
JOIN 
    products p ON td.product_id = p.product_id
LEFT JOIN 
    bundle_items bi ON p.product_id = bi.product_id  -- 連接 bundle_items 表
LEFT JOIN 
    items i ON bi.item_id = i.item_id  -- 連接 items 表
WHERE 
    t.user_id = 1  -- 替換為目標用戶的 user_id
GROUP BY 
    t.transaction_id, td.product_id, t.date  -- 保證每筆交易的時間不會合併
ORDER BY 
    t.transaction_id, td.product_id;  -- 按交易和商品排序


ORDER BY 
    t.date;-- 按交易時間以前到現在
    
ORDER BY 
    t.date desc;-- 按交易時間現在到以前
    
WHERE 
    t.user_id = 1
    AND t.type = 'add'
    
WHERE 
    t.user_id = 1
    AND t.type = 'reduce'
    
WHERE 
    t.user_id = 1
    AND p.type = 'coffee'
    
WHERE 
    t.user_id = 1
    AND p.type = 'food'
    
WHERE 
    t.user_id = 1
    AND p.type = 'bundle'
    
WHERE 
    t.user_id = 1
    AND p.type = 'latte'
    
WHERE 
    t.user_id = 1
    AND p.type = 'tea'
    
    
    
    
    
    INSERT INTO products (name, ch_name, type) VALUES
('Caffe Latte', '那堤', 'coffee'),
('Caffe Americano', '美式咖啡', 'coffee'),
('Caramel Macchiato', '焦糖瑪奇朵', 'coffee'),
('Espresso', '濃縮咖啡', 'coffee'),
('Cappuccino', '卡布奇諾', 'coffee'),
('Caffe Mocha', '摩卡', 'coffee'),
('Cocoa Macchiato', '可可瑪奇朵', 'coffee'),
('Black Tea Latte', '經典紅茶那堤', 'latte'),
('Pure Matcha Latte', '醇濃抹茶那堤', 'latte'),
('Earl Grey Tea Latte', '伯爵茶那堤', 'latte'),
('Rose Fancy Tea Latte', '玫瑰蜜香茶那堤', 'latte'),
('Iced Black Tea Latte', '冰經典紅茶那堤', 'latte'),
('English Breakfast Tea', '英式早餐紅茶', 'tea'),
('Black Tea with Ruby Grapefruit and Honey', '蜜柚紅茶', 'tea'),
('Alishan Oolong Tea', '阿里山烏龍茶', 'tea'),
('Iced Shaken Lemon Black Tea', '冰搖檸檬紅茶', 'tea'),
('Mushroom Soup Flavored Bread', '菇菇濃湯法烤麵包', 'food'),
('Strawberry Cheese Bread', '草莓起司麵包', 'food'),
('Chocolate Toast', '巧克力雙色吐司', 'food'),
('Mentaiko Cheese Bagel', '明太子起司貝果', 'food'),
('Bacon & Cheese Bread', '培根起司軟歐麵包', 'food'),
('Blueberry Bagel', '藍莓果粒貝果', 'food'),
('Cinnamon Roll', '肉桂捲', 'food'),
('Honey & Milk Bread', '蜂蜜牛奶麵包', 'food'),
('Cheesy Bread', '軟法麵包', 'food'),
('Double Cheese Bread', '雙起司軟歐麵包', 'food');

INSERT INTO items (ch_name, product_id, size, price) VALUES
('那堤', 1, 'medium', 120),
('那堤', 1, 'large', 135),
('那堤', 1, 'extraLarge', 150),
('美式咖啡', 2, 'medium', 110),
('美式咖啡', 2, 'large', 125),
('美式咖啡', 2, 'extraLarge', 140),
('焦糖瑪奇朵', 3, 'medium', 130),
('焦糖瑪奇朵', 3, 'large', 145),
('焦糖瑪奇朵', 3, 'extraLarge', 160),
('濃縮咖啡', 4, 'small', 90),
('卡布奇諾', 5, 'medium', 125),
('卡布奇諾', 5, 'large', 140),
('卡布奇諾', 5, 'extraLarge', 155),
('摩卡', 6, 'medium', 135),
('摩卡', 6, 'large', 150),
('摩卡', 6, 'extraLarge', 165),
('可可瑪奇朵', 7, 'medium', 140),
('可可瑪奇朵', 7, 'large', 155),
('可可瑪奇朵', 7, 'extraLarge', 170),
('經典紅茶那堤', 8, 'medium', 125),
('經典紅茶那堤', 8, 'large', 140),
('經典紅茶那堤', 8, 'extraLarge', 155),
('醇濃抹茶那堤', 9, 'medium', 130),
('醇濃抹茶那堤', 9, 'large', 145),
('醇濃抹茶那堤', 9, 'extraLarge', 160),
('伯爵茶那堤', 10, 'medium', 135),
('伯爵茶那堤', 10, 'large', 150),
('伯爵茶那堤', 10, 'extraLarge', 165),
('玫瑰蜜香茶那堤', 11, 'medium', 140),
('玫瑰蜜香茶那堤', 11, 'large', 155),
('玫瑰蜜香茶那堤', 11, 'extraLarge', 170),
('冰經典紅茶那堤', 12, 'medium', 120),
('冰經典紅茶那堤', 12, 'large', 135),
('冰經典紅茶那堤', 12, 'extraLarge', 150),
('英式早餐紅茶', 13, 'medium', 110),
('英式早餐紅茶', 13, 'large', 125),
('英式早餐紅茶', 13, 'extraLarge', 140),
('蜜柚紅茶', 14, 'medium', 120),
('蜜柚紅茶', 14, 'large', 135),
('蜜柚紅茶', 14, 'extraLarge', 150),
('阿里山烏龍茶', 15, 'medium', 130),
('阿里山烏龍茶', 15, 'large', 145),
('阿里山烏龍茶', 15, 'extraLarge', 160),
('冰搖檸檬紅茶', 16, 'medium', 125),
('冰搖檸檬紅茶', 16, 'large', 140),
('冰搖檸檬紅茶', 16, 'extraLarge', 155),
('菇菇濃湯法烤麵包', 17, 'noSize', 65),
('草莓起司麵包', 18, 'noSize', 70),
('巧克力雙色吐司', 19, 'noSize', 75),
('明太子起司貝果', 20, 'noSize', 80),
('培根起司軟歐麵包', 21, 'noSize', 85),
('藍莓果粒貝果', 22, 'noSize', 70),
('肉桂捲', 23, 'noSize', 60),
('蜂蜜牛奶麵包', 24, 'noSize', 65),
('軟法麵包', 25, 'noSize', 50),
('雙起司軟歐麵包', 26, 'noSize', 75);


INSERT INTO products (name, ch_name, type) VALUES
('Latte Lover Bundle', '拿鐵愛好者套卷', 'bundle'),
('Morning Essentials Bundle', '早晨必備套卷', 'bundle');

INSERT INTO bundle_items (product_id, item_id, quantity,price) VALUES
	-- 拿鐵愛好者套卷 (Latte Lover Bundle): 包含 3 杯經典拿鐵（特大杯）
(27, 3, 10,1300),
	-- 早晨必備套卷 (Morning Essentials Bundle): 包含 2 杯美式咖啡（大杯）和 2 份蜂蜜牛奶麵包
(28, 5, 2,350), -- 美式咖啡（大杯）
(28, 54, 2,350); -- 蜂蜜牛奶麵包
'''
