/*****************返回鍵******************** 
 * 確保資料不備刷新的情況下，返回歷史頁面*/
document.getElementById('btn_return').addEventListener('click', () => {
    window.history.back(); 
});


/**********************註冊帳號*******************/
function hashPassword(password) {
    var md = forge.md.sha256.create();  // 建立 SHA-256 哈希實例
    md.update(password, 'utf8');  // 更新哈希值，並指定編碼為 'utf8'
    var hashedPassword = md.digest().toHex();  // 計算哈希並轉換為十六進制格式
    return hashedPassword;
}
document.getElementById('registerBtn').addEventListener('click', async () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const gender = document.getElementById('gender').value;
    const number = document.getElementById('number').value;
    if (!email || !password || !gender || !number) {
        alert('所有欄位均為必填！');
        return;
    }
    try {
        // 將密碼進行一次哈希處理
        const hashedPassword = await hashPassword(password);
        // 顯示一次哈希的結果
        //document.getElementById('regisert-info').textContent = `一次哈希結果: ${hashedPassword}, 原密碼: ${password}`;
        const response = await fetch('http://127.0.0.1:5000/api/customers/create', {
            method: 'POST',
            //credentials: 'include',// 包含 cookies 和其他憑證
            headers: {'Content-Type': 'application/json'},   
            body: JSON.stringify({ email, password: hashedPassword, gender, number: number })
        });
        
        const result = await response.json();
        if (response.ok) {
            alert('註冊成功');
            //document.getElementById('login-info').textContent = `註冊成功：電子郵件 - ${email}, 性別 - ${gender}, 手機門號 - ${number}`;
        
            //註冊成功後跳到上一頁
            window.history.back(); 
            //document.getElementById('registerButton').style.display = 'none';   //隱藏註冊按鈕
        
        } else {
            alert(`錯誤：${result.message}`);
        }
    } catch (error) {
        console.error('註冊失敗', error);
        alert('註冊失敗，請稍後再試！');
    }
});