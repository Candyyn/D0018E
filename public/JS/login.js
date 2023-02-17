const loginForm = document.querySelector('#loginForm');
loginForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default submit
    //const formData = new FormData(loginForm);
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;

    try {

        var details = {
            email: email,
            password: password,
            remember: true,
        }

        var formBody = [];
        for (var property in details) {
            var encodedKey = encodeURIComponent(property);
            var encodedValue = encodeURIComponent(details[property]);
            formBody.push(encodedKey + "=" + encodedValue);
        }
        formBody = formBody.join("&");

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: formBody,
        });

        if (response.ok) {
            const data = await response.json();
            setLocalStorageItem('token', data.token);
            setLocalStorageItem('user', data.user);
            alert('Logged in, Welcome back ' + data.user.first_name + ' ' + data.user.last_name)
            console.log(data);
        } else {
            console.log("Error: " + response.status);
        }
    } catch (error) {
        console.log("Error: " + error);
    }
}, false);

function setLocalStorageItem(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}
