// Check if Token exist in local storage
if (localStorage.getItem("token") !== null) {

    fetch('/verify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add Authorization header with token
            'Authorization': 'Bearer ' + JSON.parse(localStorage.getItem("token"))
        },

    }).then(r => r.json()).then(data => {
        if (data.tokenVerified) {
            document.getElementById("login").style.display = "none";
            getBasket()
        } else {
            // remove token from local storage
            localStorage.removeItem("token");
        }
    })


    // If token exist, redirect to home page
    //window.location.href = "/";
    // Get Basket from backend

    // Get Domain and protocol


}


function getBasket() {
    const domain = window.location.protocol + "//" + window.location.host;

    fetch(domain + '/basket/content', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // Add Authorization header with token
            'Authorization': 'Bearer ' + JSON.parse(localStorage.getItem("token"))
        },

    }).then(r => r.json()).then(data => {

        let basketCount = 0;
        data.basket.forEach(element => {
            basketCount += element.amount;
        })

        document.getElementById("basket").innerText = basketCount;
        const event = new CustomEvent('OnGetBasket', {
            detail: data.basket,
        });
        window.dispatchEvent(event);
    });
}


function addProductToCart(id) {
    // Send Add To Basket to backend
    // Get Domain and protocol
    const domain = window.location.protocol + "//" + window.location.host;
    console.log("Sent to: " + domain + '/basket/add with token:  and product_id: ' + id)

    const details = {
        "product_id": id
    }

    let formBody = [];
    for (let property in details) {
        let encodedKey = encodeURIComponent(property);
        let encodedValue = encodeURIComponent(details[property]);
        formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");

    fetch(domain + '/basket/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add Authorization header with token

            'Authorization': 'Bearer ' + JSON.parse(localStorage.getItem("token"))
        },
        body: formBody
    }).then(r => r.json()).then(data => {
        console.log(data);
        getBasket();
    });
}
