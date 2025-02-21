/**********************基本按鍵功能***********************/
document.getElementById('btn_return').addEventListener('click', () => {
    window.history.back(); 
});

/************測試**************************** */
/*describe('Fetch and Display User Settings', () => {
    beforeEach(() => {
        // 模擬伺服器回應
        global.fetch = jest.fn(() =>
            Promise.resolve({
                json: () =>
                    Promise.resolve({
                        message: "User settings retrieved successfully",
                        settings: {
                            email: "11124211@example.com",
                            gender: "male",
                            number: "0912345678",
                        },
                    }),
            })
        );
    });

    test('should update form fields with fetched data', async () => {
        await fetchUserSettings();
        expect(document.getElementById('email').value).toBe('11124211@example.com');
        expect(document.getElementById('gender').value).toBe('male');
        expect(document.getElementById('number').value).toBe('0912345678');
    });
});
*/

/***************查看個人基本資料*****************************/
/*
// 從 cookies 中取得 token 的函數
async function getToken() {
    return new Promise((resolve) => {
        const token = document.cookie
            .split('; ')
            .find(row => row.startsWith('token='))
            ?.split('=')[1];
        resolve(token);
    });
}

async function fetchUserSettings() {
    const token = await getToken(); // 取得 token
    if (!token) {
        console.error("找不到 token，請重新登入。");
        return;
    }

    console.log("取得的 token:", token); // 檢查 token

    try {
        // 使用 fetch 向伺服器發送請求
        const response = await fetch('/api/customers/myselfSetting', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            credentials: 'include'
        });

        console.log("API 回應狀態:", response.status); // 檢查回應狀態
        console.log("API 回應狀態文字:", response.statusText);

        if (!response.ok) {
            throw new Error(`錯誤: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("API 回應資料:", data); // 檢查返回的資料

        if (data.message === "User settings retrieved successfully") {
            // 確認 DOM 元素是否存在
            const emailInput = document.getElementById('email');
            const genderSelect = document.getElementById('gender');
            const numberInput = document.getElementById('number');

            console.log(document.getElementById('email')); // 應返回 HTMLInputElement
            console.log(document.getElementById('gender')); // 應返回 HTMLSelectElement
            console.log(document.getElementById('number')); // 應返回 HTMLInputElement


            if (emailInput && genderSelect && numberInput) {
                // 更新前端 UI
                emailInput.value = data.settings.email;
                genderSelect.value = data.settings.gender;
                numberInput.value = data.settings.number;

                console.log("成功更新設定資料");
            } else {
                console.error("無法找到對應的 DOM 元素");
            }
        } else {
            console.error("取得使用者設定失敗:", data.message);
        }
    } catch (error) {
        console.error("發生錯誤:", error.message);
    }
}
*/

/******************刪除帳號*****************************************/
async function getToken() {
    const value = `; ${document.cookie}`;
    const parts = value.split('; token=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

document.querySelector(".btn_delete").addEventListener("click", async () => {
    const token = await getToken();
    if (!token) {
        alert("未登入，請先登入！");
        //window.location.href = "login.html";
        return;
    }

    if (confirm("確定刪除帳號？")) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/customers/delete', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            });

            if (response.ok) {
                const result = await response.json();
                alert(result.message || '帳號已成功刪除');
                window.location.href = 'index.html';
            } else {
                const data = await response.json();
                alert(data.error || '刪除失敗，請稍後再試');
            }
        } catch (error) {
            console.error("刪除帳號時發生錯誤:", error);
            alert("無法連接到伺服器，請稍後再試！");
        }
    }
});