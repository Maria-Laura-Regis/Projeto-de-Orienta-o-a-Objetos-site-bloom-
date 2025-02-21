document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle logic (unchanged)
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        document.body.classList.remove('light-theme');
    } else {
        document.body.classList.add('light-theme');
        document.body.classList.remove('dark-theme');
    }

    const toggleButton = document.getElementById('toggle-theme');
    toggleButton.addEventListener('click', () => {
        const currentTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
        if (currentTheme === 'dark') {
            document.body.classList.remove('dark-theme');
            document.body.classList.add('light-theme');
            localStorage.setItem('theme', 'light');
        } else {
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        }
    });

    document.addEventListener("DOMContentLoaded", function () {
        const usernameDisplay = document.getElementById("username-display");
        const logoutBtn = document.getElementById("logout-btn");

        // Verifica se o usuário está logado (simulação usando localStorage)
        const username = localStorage.getItem("username");

        if (username) {
            usernameDisplay.textContent = `Olá, ${username}!`;
            logoutBtn.style.display = "inline-block"; // Mostra o botão de logout
        } else {
            usernameDisplay.innerHTML = '<a href="portal.html">Entrar</a>';
        }

        // Logout - Remove usuário e redireciona
        logoutBtn.addEventListener("click", function () {
            localStorage.removeItem("username");
            window.location.href = "home.html";
        });
    });

    // Cart functionality
    function ready() {
        // Event listeners for remove buttons
        var removeCartItemButtons = document.getElementsByClassName('btn-danger');
        for (var i = 0; i < removeCartItemButtons.length; i++) {
            var button = removeCartItemButtons[i];
            button.addEventListener('click', removeCartItem);
        }

        // Event listeners for quantity inputs
        var quantityInputs = document.getElementsByClassName('cart-quantity-input');
        for (var i = 0; i < quantityInputs.length; i++) {
            var input = quantityInputs[i];
            input.addEventListener('change', quantityChanged);
        }

        // Event listeners for add to cart buttons
        var addToCartButtons = document.getElementsByClassName('shop-item-button');
        for (var i = 0; i < addToCartButtons.length; i++) {
            var button = addToCartButtons[i];
            button.addEventListener('click', addToCartClicked);
        }

        // Event listener for purchase button
        document.getElementsByClassName('btn-purchase')[0].addEventListener('click', purchaseClicked);

        // Load cart from database when the page loads
        loadCartFromDatabase();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', ready);
    } else {
        ready();
    }

    async function loadCartFromDatabase() {
        const user_id = localStorage.getItem("user_id"); // Assuming you store user_id in localStorage
        if (!user_id) return;

        const response = await fetch(`/load_cart?user_id=${user_id}`);
        const data = await response.json();

        const cartItems = document.getElementsByClassName('cart-items')[0];

        // Clear the cart UI
        while (cartItems.hasChildNodes()) {
            cartItems.removeChild(cartItems.firstChild);
        }

        // Add each item from the database to the cart UI
        data.cart.forEach(item => {
            addItemToCart(item.title, item.price, item.imageSrc, item.quantity);
        });

        // Update the cart total
        updateCartTotal();
    }

    async function saveCartToDatabase() {
        const user_id = localStorage.getItem("user_id"); // Assuming you store user_id in localStorage
        if (!user_id) return;

        const cartRows = document.getElementsByClassName('cart-row');
        const cart = [];

        for (let i = 0; i < cartRows.length; i++) {
            const cartRow = cartRows[i];
            const title = cartRow.querySelector('.cart-item-title').innerText;
            const price = cartRow.querySelector('.cart-price').innerText;
            const imageSrc = cartRow.querySelector('.cart-item-image').src;
            const quantity = cartRow.querySelector('.cart-quantity-input').value;

            cart.push({ title, price, imageSrc, quantity });
        }

        const response = await fetch('/save_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id, cart }),
        });

        const result = await response.json();
        console.log("Cart Data Saved:", result);
    }

function purchaseClicked() {
    alert('Thank you for your purchase!');

    // Save the cart data to localStorage FIRST
    saveCartToLocalStorage();

    // Clear the cart UI AFTER saving the data
    const cartItems = document.getElementsByClassName('cart-items')[0];
    while (cartItems.hasChildNodes()) {
        cartItems.removeChild(cartItems.firstChild);
    }

    // Redirect to the store page
    window.location.href = 'store.html';
}



function saveCartToLocalStorage() {
    const cartRows = document.getElementsByClassName('cart-row');
    const cart = [];

    for (let i = 0; i < cartRows.length; i++) {
        const cartRow = cartRows[i];
        const title = cartRow.querySelector('.cart-item-title').innerText;
        const price = cartRow.querySelector('.cart-price').innerText;
        const imageSrc = cartRow.querySelector('.cart-item-image').src;
        const quantity = cartRow.querySelector('.cart-quantity-input').value;

        cart.push({ title, price, imageSrc, quantity });
    }

    // Save the cart data to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
}
    function removeCartItem(event) {
        const buttonClicked = event.target;
        buttonClicked.parentElement.parentElement.remove();
        updateCartTotal();
        saveCartToDatabase(); // Save the updated cart to the database
    }

    function quantityChanged(event) {
        const input = event.target;
        if (isNaN(input.value) || input.value <= 0) {
            input.value = 1;
        }
        updateCartTotal();
        saveCartToDatabase(); // Save the updated cart to the database
    }

    function addToCartClicked(event) {
        const button = event.target;
        const shopItem = button.parentElement.parentElement;
        const title = shopItem.getElementsByClassName('shop-item-title')[0].innerText;
        const price = shopItem.getElementsByClassName('shop-item-price')[0].innerText;
        const imageSrc = shopItem.getElementsByClassName('shop-item-image')[0].src;
        addItemToCart(title, price, imageSrc, 1); // Default quantity is 1
        updateCartTotal();
        saveCartToDatabase(); // Save the updated cart to the database
    }

    function addItemToCart(title, price, imageSrc, quantity) {
        const cartItems = document.getElementsByClassName('cart-items')[0];
        const cartItemNames = cartItems.getElementsByClassName('cart-item-title');

        // Check if the item is already in the cart
        for (let i = 0; i < cartItemNames.length; i++) {
            if (cartItemNames[i].innerText === title) {
                alert('This item is already added to the cart');
                return;
            }
        }

        // Create a new cart row
        const cartRow = document.createElement('div');
        cartRow.classList.add('cart-row');
        cartRow.innerHTML = `
            <div class="cart-item cart-column">
                <img class="cart-item-image" src="${imageSrc}" width="100" height="100">
                <span class="cart-item-title">${title}</span>
            </div>
            <span class="cart-price cart-column">${price}</span>
            <div class="cart-quantity cart-column">
                <input class="cart-quantity-input" type="number" value="${quantity}">
                <button class="btn btn-danger" type="button">REMOVE</button>
            </div>`;
        cartItems.append(cartRow);

        // Add event listeners to the new cart row
        cartRow.querySelector('.btn-danger').addEventListener('click', removeCartItem);
        cartRow.querySelector('.cart-quantity-input').addEventListener('change', quantityChanged);
    }

    function updateCartTotal() {
        const cartItemContainer = document.getElementsByClassName('cart-items')[0];
        const cartRows = cartItemContainer.getElementsByClassName('cart-row');
        let total = 0;

        for (let i = 0; i < cartRows.length; i++) {
            const cartRow = cartRows[i];
            const priceElement = cartRow.getElementsByClassName('cart-price')[0];
            const quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0];
            const price = parseFloat(priceElement.innerText.replace('$', ''));
            const quantity = quantityElement.value;
            total += price * quantity;
        }

        total = Math.round(total * 100) / 100;
        document.getElementsByClassName('cart-total-price')[0].innerText = '$' + total;
    }
});