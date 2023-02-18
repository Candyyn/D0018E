if (localStorage.getItem("token") == null) {
    // else redirect to login page
    window.location.href = "/login";
}


document.getElementById('checkout').addEventListener('click', function () {

    // Get Domain and protocol
    const domain = window.location.protocol + "//" + window.location.host;
    fetch(domain + '/basket/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + JSON.parse(localStorage.getItem("token"))
        }
    }).then(r => r.json()).then(data => {
        if (data?.error != undefined) {
            alert(data.error);
        } else {
            alert("Order placed");
            window.location.href = "/products";
        }
    });

})


window.addEventListener('OnGetBasket', (event) => {
    console.log('Received global event:', event.detail);
    const table = document.getElementById("checkoutTable");

    // Clear table
    while (table.firstChild) {
        table.removeChild(table.firstChild);
    }

    let totalPrice = 0;

    event.detail.forEach(element => {
        const tr = document.createElement("tr");
        const td1 = document.createElement("td");
        const td2 = document.createElement("td");
        const td3 = document.createElement("td");
        const td4 = document.createElement("td");
        const img = document.createElement("img");
        img.setAttribute("src", element.image);
        img.setAttribute("alt", element.name);
        const span = document.createElement("span");
        const button = document.createElement("button");
        button.classList.add("remove");
        button.innerText = "Remove";
        button.addEventListener("click", function () {
            console.log("Remove: " + element.cart_id);
            removeFromBasket(element.cart_id, 0)
        });
        span.innerText = element.name;
        td1.appendChild(img);
        td1.appendChild(span);

        td2.innerText = element.amount;
        if (element.amount > 1) {
            const removeOneButton = document.createElement("button");
            removeOneButton.classList.add("removeOne");
            removeOneButton.innerText = "-";
            removeOneButton.addEventListener("click", function () {
                removeFromBasket(element.cart_id)
            })
            td2.prepend(removeOneButton);
        }


        const addOneButton = document.createElement("button");
        addOneButton.classList.add("addOne");
        addOneButton.innerText = "+";
        addOneButton.addEventListener("click", function () {
            addProductToCart(element.product_id)
        })
        td2.appendChild(addOneButton);


        td3.innerText = element.price + ' kr';
        td4.appendChild(button);
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        table.appendChild(tr);
        totalPrice += element.price;

    })

    // add to table footer
    const tr = document.createElement("tr");
    const td1 = document.createElement("td");
    const td2 = document.createElement("td");
    const td3 = document.createElement("td");
    const td4 = document.createElement("td");
    td3.innerText = totalPrice + ' kr';
    td2.innerText = "Total";
    tr.appendChild(td1);
    tr.appendChild(td2);
    tr.appendChild(td3);
    tr.appendChild(td4);
    table.appendChild(tr);

    //document.getElementById("totalPrice").innerText = totalPrice + ' kr';

});

function removeFromBasket(id, amount = 1) {
    const details = {
        cart_id: id,
        amount: amount
    }

    let formBody = [];
    for (let property in details) {
        const encodedKey = encodeURIComponent(property);
        const encodedValue = encodeURIComponent(details[property]);
        formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");

    // Get Domain and protocol
    const domain = window.location.protocol + "//" + window.location.host;
    fetch(domain + '/basket/content', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + JSON.parse(localStorage.getItem("token"))
            // Add Authorization header with token

        },
        body: formBody
    }).then(r => r.json()).then(data => {
        getBasket();
    });

}
