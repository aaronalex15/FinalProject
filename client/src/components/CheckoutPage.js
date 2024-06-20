import { useContext } from "react";
import { CartContext } from "./CartContext";
import CheckoutButton from "./CheckoutButton";

const CheckoutPage = () => {
  const { cartItems, removeFromCart, stripeLoaded } = useContext(CartContext);

  return (
    <div>
      <h1>Checkout</h1>
      <div>
        {cartItems.length > 0 ? (
          cartItems.map((item) => (
            <div key={item.id}>
              <p>{item.title}</p>
              <p>Price: {item.price}</p>
              <button onClick={() => removeFromCart(item.id)}>
                Remove from Cart
              </button>
            </div>
          ))
        ) : (
          <p>Your cart is empty.</p>
        )}
      </div>
      <CheckoutButton />
      {/* Add payment form or payment button here */}
    </div>
  );
};

export default CheckoutPage;