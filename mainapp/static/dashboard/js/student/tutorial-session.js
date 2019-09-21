$(document).ready(function() {

});

function addToCart(id) {
    console.log('id is ', id);
    const btn = document.getElementById('btn-cart-'+id);
    const btnText = document.getElementById('btn-cart-text'+id);
    const btnIcon = document.getElementById('btn-cart-icon'+id);
    btn.classList.remove('btn-success');
    btn.classList.add('btn-danger');
    btnText.textContent = 'REMOVE FROM CART';
    btnIcon.classList.remove('fa-plus');
    btnIcon.classList.add('fa-minus');
}