/*****************返回鍵******************** 
 * 確保資料不備刷新的情況下，返回歷史頁面*/
document.getElementById('btn_return').addEventListener('click', () => {
    window.history.back(); 
});

/********************登入********************** */
/*
登入，
當使用者輸入帳號(email)、密碼(password)，
接收帳號、密碼，回傳成JSON格式，
用html呼叫api，
搜尋mysql是否有相對應的email帳號、二次哈希值。
當有相對應帳號，按下登入即顯示"登入成功"，錯誤對照帳號或密碼錯誤並給予錯誤訊息。

此程式要有token及cookie功能。
api連接url為'http://127.0.0.1:5000/api/customers/login'。

將成功登入儲存的token傳送到token.js並顯示在token.html

一次哈希結果: 03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4, 原密碼: 1234
*/

//一次哈希函數 (使用 SHA-256)
function hashPassword(password) {
    var md = forge.md.sha256.create();  // 建立 SHA-256 哈希實例
    md.update(password, 'utf8');  // 更新哈希值，並指定編碼為 'utf8'
    var hashedPassword = md.digest().toHex();  // 計算哈希並轉換為十六進制格式
    return hashedPassword;
}
document.getElementById('login_form').addEventListener('submit', async (event) => {
    event.preventDefault(); // 防止表單的預設提交行為

    // 取得使用者輸入的 Email 和 Password
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    console.log('輸入的 Email:', email);
    console.log('輸入的 Password:', password);

    // 檢查是否有填入 Email 和 Password
    if (!email || !password) {
        alert('Email 和 Password 是必填的！');
        return;
    }

        //一次哈希
        const hashedPassword = await hashPassword(password);

        console.log('哈希後的密碼:', hashedPassword);
    
        // 發送登入請求
        const response = await fetch('http://127.0.0.1:5000/api/customers/login', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password: hashedPassword }),
        });
        console.log('發送的請求:', response);
    
        const result = await response.json(); // 解析 JSON 響應
    
        /*********token存在cookie*******/
        if (response.ok && result.token) {

            alert('登入成功');
            console.log('Token 已儲存：', result.token);
        
            // 登入成功後跳到上一頁
            //window.history.back();
            //window.location.href = 'mainPage.html';
        } else {
            alert('登入失敗：帳號或密碼錯誤');
        }

        /********* 測試讀取 Cookie *********/
        function getCookie(name) {
            const cookies = document.cookie.split('; ');
            for (let cookie of cookies) {
                const [key, value] = cookie.split('=');
                if (key === name) {
                    return decodeURIComponent(value); // 解碼值
                }
            }
            return null;
        }
        function getToken() {
        const token = document.cookie.split('; ').find(row => row.startsWith('token=')).split('=')[1];
        return token;
    }
        const authToken = getCookie('token');
        if (authToken) {
            console.log('從 Cookie 獲取的 Token：', authToken);
        } else {
            console.log('Token 不存在於 Cookie 中');
        }

        /*********token存在sessionStorage******* 
        // 判斷後端是否返回 token
        if (response.ok && result.token) {
            // 儲存 token 到 sessionStorage
            sessionStorage.setItem('authToken', result.token);
            alert('登入成功');
            console.log('Token 已儲存：', result.token);
        
            // 登入成功後跳到主頁
            // window.location.href = 'mainPage.html'; 
            // document.getElementById('registerButton').style.display = 'none';   // 隱藏註冊按鈕
        
        } else {
            // 處理登入失敗情況
            alert(`登入失敗：帳號或密碼錯誤`);
        }

        */

/*  除錯用
        try {
    } catch (error) {
        // 處理網絡或伺服器錯誤
        console.error('發生錯誤：', error);
        //alert('');//alert('未註冊帳號或伺服器錯誤');
    }
*/

});



