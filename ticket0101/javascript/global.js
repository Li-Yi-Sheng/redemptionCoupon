async function checkLoginStatus() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/auth/validate', {
            method: 'GET',
            credentials: 'include', // 必須攜帶 Cookie
        });

        const result = await response.json();

        if (response.ok && result.isLoggedIn) {
            // 紀錄用戶資料到 LocalStorage
            localStorage.setItem('user', JSON.stringify(result.user));

            // 紀錄 Token 到 Console
            console.log('Token 已儲存：', result.token);

            // 跳轉到 mainPage.html
            window.location.href = 'index.html';
        } else {
            alert(result.message || '未登入，請先登入！');
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('檢查登入狀態失敗', error);
        alert('系統錯誤，請稍後再試！');
        window.location.href = 'login.html';
    }
}

// 判斷當前頁面，執行相應邏輯
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.endsWith('mainPage.html')) {
        // 當在 mainPage.html 時執行隱藏註冊按鈕邏輯
        hideRegisterButton();

        // 獲取並輸出 Token（如果存在於 LocalStorage）
        const user = JSON.parse(localStorage.getItem('user'));
        if (user && user.token) {
            console.log('Token 已儲存：', user.token);
        }
    } else {
        // 在其他頁面檢查登入狀態
        checkLoginStatus();
    }
});
