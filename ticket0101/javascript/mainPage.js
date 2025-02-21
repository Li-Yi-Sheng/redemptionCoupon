/*
主頁要接收登入成功後的使用者資料並存在後台，
在成功登入時，隱藏註冊及登入鍵。

設有登出鍵。
 */

/**********************基本按鍵功能***********************/
document.addEventListener('DOMContentLoaded', async () => {
    const btnRegister = document.getElementById('btn_register');
    const btnLogin = document.getElementById('btn_login');
    const btnReceive = document.getElementById('btn_receive');
    const btnSet = document.getElementById('btn_set');
    const btnLogout = document.getElementById('btn_logout');

//註冊按鈕
btnRegister.addEventListener('click', () => {
    window.location.href = 'register.html';
});

//登入按鈕
btnLogin.addEventListener('click', () => {
    window.location.href = 'login.html';
});

//領取寄杯按鈕
btnReceive.addEventListener('click', () => {
    window.location.href = 'receive.html';
});

//會員資料
btnSet.addEventListener('click', () => {
    window.location.href = 'set.html';
});

//登出按鈕
btnLogout.addEventListener('click', async () => {
    try {
        // 清除 cookie
        document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        
        // 刷新頁面
        window.location.reload();
    } catch (error) {
        console.error('登出失敗:', error);
        alert('登出失敗，請稍後再試');
    }
});

/****************************檢查是否在登入狀態********************************* */
    try {
        console.log(document.cookie);
        const response = await fetch('http://127.0.0.1:5000/api/auth/validate', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });

        if (response.ok) {
            const data = await response.json();
            if (data.isLoggedIn) {
                //已登入
                btnRegister.style.display = 'none';     //註冊 off
                btnLogin.style.display = 'none';        //登入 off
                btnReceive.style.display = 'block';      //領取寄杯 on
                btnSet.style.display = 'block';         //會員設定 on
                btnLogout.style.display = 'block';      //登出 on
            } else {
                //未登入
                btnRegister.style.display = 'block';    //註冊 
                btnLogin.style.display = 'block';       //登入 
                btnReceive.style.display = 'none';       //領取寄杯 
                btnSet.style.display = 'none';          //會員設定 
                btnLogout.style.display = 'none';       //登出 
            }
        }
    } catch (error) {
        console.error('檢查登入狀態失敗:', error);
    }
    
});