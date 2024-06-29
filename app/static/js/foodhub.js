document.addEventListener('DOMContentLoaded', function() {
  const cartIcon = document.querySelector('.shopping-cart-btn');
  const cartBox = document.querySelector('.cart-box');

  cartIcon.addEventListener('click', function() {
      fetch('/cart-content')
          .then(response => response.json())
          .then(cartItems => {
              const cartBoxUl = document.querySelector('.cart-box-ul');
              cartBoxUl.innerHTML = '<h4 class="cart-h4">Votre commande.</h4>'; // Clear existing items

              cartItems.forEach(item => {
                  const li = document.createElement('li');
                  li.innerHTML = `
                      <a href="#" class="cart-item">
                          <div class="img-box">
                              <img src="/static/${item.image}" alt="product image" class="product-img" width="50" height="50" loading="lazy">
                          </div>
                          <h5 class="product-name">${item.name}</h5>
                          <p class="product-price"><span class="small">$</span>${item.price}</p>
                      </a>
                  `;
                  cartBoxUl.appendChild(li);
              });
              
              cartBox.classList.add('visible'); // Assuming you have a class to make the cart visible
          })
          .catch(error => {
              console.error('Error fetching cart content:', error);
          });
  });
});
