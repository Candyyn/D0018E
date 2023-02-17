async function getProducts(page) {

    let response = await fetch('/shop/products', {
        method: 'GET',
    });

    if (response.ok) {
        var _d = await response.json()
        var products = _d.products;
        products.forEach((item) => {
            var element = createProductItem(item.name, item.image, item.price, item.description, item.availability)
            document.querySelector('#items').appendChild(element);
        })


    } else {
        console.log("Error: " + response.status);
    }
}

window.addEventListener("load", async (event) => {
    await getProducts(0)
});



function createProductItem(title, image, _price, desc, _stock) {
    // Create SVG element
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("id", "Store2");

    // Create rectangle element
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    svg.appendChild(rect);

    // Create foreignObject element
    const foreignObject = document.createElementNS("http://www.w3.org/2000/svg", "foreignObject");
    foreignObject.setAttribute("x", "20");
    foreignObject.setAttribute("y", "10");
    foreignObject.setAttribute("width", "90%");
    foreignObject.setAttribute("height", "100%");
    svg.appendChild(foreignObject);

    // Create h2 element
    const h2 = document.createElement("h2");
    h2.classList.add("LampaRubrik");
    h2.textContent = "Trasig Lampa 2";
    foreignObject.appendChild(h2);

    // Create image element
    const img = document.createElement("img");
    img.classList.add("lampa");
    img.setAttribute("src", "/Assets/lampa2.png");
    img.setAttribute("alt", "lampa");
    foreignObject.appendChild(img);

    // Create price paragraph element
    const price = document.createElement("p");
    price.classList.add("price");
    price.textContent = "Price: " + _price + "kr";
    foreignObject.appendChild(price);

    // Create description paragraph element
    const description = document.createElement("p");
    description.classList.add("Description");
    description.textContent = desc;
    foreignObject.appendChild(description);

    // Create stock paragraph element
    const stock = document.createElement("p");
    stock.classList.add("stock");
    stock.textContent = "Availability: " + _stock;
    foreignObject.appendChild(stock);

    // Create buy button element
    const buyButton = document.createElement("button");
    buyButton.classList.add("buy");
    buyButton.textContent = "Buy";
    foreignObject.appendChild(buyButton);

    // Return the created SVG element
    return svg;
}