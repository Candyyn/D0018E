async function getProduct(id) {
    console.log("ID: " + id)
    let response = await fetch('/product?id=' + id, {
        method: 'GET',
    });

    if (response.ok) {
        const _d = await response.json()
        const product = _d.product
        console.log(product)
        if(product != null) {
            // Assign data to HTML elements
            document.querySelector('#description').textContent = product.description
            document.querySelector('#price').textContent = product.price
            document.querySelector('#name').textContent = product.name
            document.querySelector('#image').src = product.image
        }
        // Update pages data

    } else {
        console.log("Error: " + response.status);
    }
}

window.addEventListener("load", async (event) => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const id = urlParams.get('id')
    console.log("ID: " + id)
    await getProduct(id)
});


