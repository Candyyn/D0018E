async function getProduct(id) {
    console.log("ID: " + id)
    let response = await fetch('/product?id=' + id, {
        method: 'GET',
    });

    if (response.ok) {
        const _d = await response.json()
        const product = _d.product
        console.log(product)
        if (product != null) {
            // Assign data to HTML elements
            document.querySelector('#description').textContent = product.description
            document.querySelector('#price').textContent = product.price
            document.querySelector('#name').textContent = product.name
            document.querySelector('#image').src = product.image
            console.log(product)
            loadComments(product.comments)
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


function loadComments(comments) {
    if (comments != null) {
        // Assign data to HTML elements
        let commentList = document.querySelector('#comments')
        comments.forEach(comment => {

            const rating = comment[0];
            const commentText = comment[1];
            const name = comment[2];

            const div1 = document.createElement("div");
            div1.classList.add("col-12");
            div1.style.color = "white";

            const div2 = document.createElement("div");
            div2.classList.add("comment-box");
            div2.classList.add("ml-2");

            const h4 = document.createElement("h4");
            h4.textContent = name;

            const span = document.createElement("span");
            span.textContent = rating;
            const ratingText = document.createTextNode("Rating: ");
            const ratingSpan = document.createElement("span");
            ratingSpan.appendChild(ratingText);
            ratingSpan.appendChild(span);

            const div3 = document.createElement("div");
            div3.classList.add("comment-area");

            const p = document.createElement("p");
            p.textContent = commentText;

            div3.appendChild(p);

            div2.appendChild(h4);
            div2.appendChild(ratingSpan);
            div2.appendChild(div3);

            div1.appendChild(div2);


            commentList.appendChild(div1);

        });
    }


}


async function submitRating() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const id = urlParams.get('id')
    const ratingInputs = document.getElementsByName('rating');
    let selectedRating;

    for (let i = 0; i < ratingInputs.length; i++) {
        if (ratingInputs[i].checked) {
            selectedRating = ratingInputs[i].value;
            break;
        }
    }

    const commentText = document.querySelector('#commentText').value;


    // Send data to server
    var details = {'id': id, 'rating': selectedRating, 'comment': commentText};

    // Post data to server
    var formBody = []; <!--To be able to send tha data to the database -->
    for (var property in details) {
        var encodedKey = encodeURIComponent(property);
        var encodedValue = encodeURIComponent(details[property]);
        formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");

    const response = await fetch('/product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer ' + JSON.parse(localStorage.getItem("token"))

        },
        body: formBody,
    });

    // Then refresh page
    window.location.reload();

}

function pageAddToCart() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const id = urlParams.get('id')
    addProductToCart(id)
}