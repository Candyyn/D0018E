async function getProducts(page) {

    let response = await fetch('/shop/products', {
        method: 'GET',
    });

    if (response.ok) {
        var _d = await response.json()
        var products = _d.products;
        products.forEach((item) => {
            console.log(item)
            var element = createProductItem(item.product_id, item.name, item.image, item.price, item.description, item.availability)
            document.querySelector('#items').appendChild(element);
        })


    } else {
        console.log("Error: " + response.status);
    }
}

window.addEventListener("load", async (event) => {
    await getProducts(0)
});


function createProductItem(id, title, image, _price, desc, _stock) {
    // Create SVG element
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");

    // create DIV element
    const div = document.createElement("div");
    div.classList.add("product");

    div.onclick = function () {
        window.location.href = "/shop/product?id=" + id;
    }


    // Create rectangle element
    //const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    //div.appendChild(rect);

    // Create foreignObject element
    const foreignObject = document.createElementNS("http://www.w3.org/2000/svg", "foreignObject");
    foreignObject.setAttribute("x", "20");
    foreignObject.setAttribute("y", "10");
    foreignObject.setAttribute("width", "90%");
    foreignObject.setAttribute("height", "100%");
    //div.appendChild(foreignObject);

    const innerDiv = document.createElement("div");
    innerDiv.classList.add("innerDiv");
    div.appendChild(innerDiv);


    // Create h2 element
    const h2 = document.createElement("h2");
    h2.classList.add("LampaRubrik");
    h2.textContent = title;
    innerDiv.appendChild(h2);

    // Create image element
    const img = document.createElement("img");
    img.classList.add("lampa");
    img.setAttribute("src", image);
    img.setAttribute("alt", "lampa");
    innerDiv.appendChild(img);

    // Create price paragraph element
    const price = document.createElement("p");
    price.classList.add("price");
    price.textContent = "Price: " + _price + "kr";
    innerDiv.appendChild(price);

    // Create description paragraph element
    const description = document.createElement("p");
    description.classList.add("Description");
    description.textContent = desc;
    innerDiv.appendChild(description);

    // Create stock paragraph element
    const stock = document.createElement("p");
    stock.classList.add("stock");
    stock.textContent = "Availability: " + _stock;
    innerDiv.appendChild(stock);

    // Create buy button element
    const buyButton = document.createElement("button");
    buyButton.classList.add("buy");
    buyButton.textContent = "Buy";
    buyButton.addEventListener("click", function () {
        addProductToCart(id)
    });
    innerDiv.appendChild(buyButton);

    // Return the created SVG element
    return div;
}


