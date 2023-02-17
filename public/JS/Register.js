const form = document.querySelector('#registerForm');
form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default submit
    //const formData = new FormData(loginForm);
    const email = document.querySelector('#Email').value;
    const first = document.querySelector('#Firstname').value;
    const last = document.querySelector('#Lastname').value;
    const phone = document.querySelector('#PhoneNumber').value;
    const address = document.querySelector('#Address').value;
    const password = document.querySelector('#Password').value;

    try {

        const details = {
            email: email,
            password: password,
            first_name: first,
            last_name: last,
            address: address,
            phone: phone,
        }

        var formBody = [];
        for (var property in details) {
            var encodedKey = encodeURIComponent(property);
            var encodedValue = encodeURIComponent(details[property]);
            formBody.push(encodedKey + "=" + encodedValue);
        }
        formBody = formBody.join("&");

        const response = await fetch('/register', {
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
