import { loadCartFromDatabase, saveCartToDatabase, updateCartTotal, removeCartItem, quantityChanged, purchaseClicked } from './cart.js';

document.addEventListener('DOMContentLoaded', () => {
    // Load cart from database when the page loads
    loadCartFromDatabase();

    // Add event listener for purchase button
    const purchaseButton = document.getElementsByClassName('btn-purchase')[0];
    if (purchaseButton) {
        purchaseButton.addEventListener('click', purchaseClicked);
    }
});