import React, { useContext } from "react";
import { CartContext } from "./CartContext";
import MerchandiseCard from "../components/MerchandiseCard";

const MyCart = () => {
  const { cartItems } = useContext(CartContext);

  return (
    <div>
      <h1>My Cart</h1>
      <div>
        {cartItems.length > 0 ? (
          cartItems.map((item) => (
            <div key={item.id}>
              <MerchandiseCard {...item} />
              <form action={`/create-checkout-session/${item.id}`} method="POST">
                <button className="button-55" type="submit">
                  Proceed to Checkout
                </button>
              </form>
            </div>
          ))
        ) : (
          <p>Your cart is empty.</p>
        )}
      </div>
    </div>
  );
};

export default MyCart;
