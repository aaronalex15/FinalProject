import { createContext, useState } from "react";


export const CartContext = createContext();

export const CartProvider = ({ children }) => {
    const [cartItems, setCartItems] = useState([]);
    const [stripeLoaded, setStripeLoaded] = useState(false);

    const addToCart = (merchandise) => {
        setCartItems([...cartItems, merchandise]);
    };

    const removeFromCart = (merchandiseId) => {
        setCartItems(cartItems.filter((item) => item.id !== merchandiseId));
    };


    
    return (
        <CartContext.Provider value={{ cartItems, addToCart, removeFromCart, stripeLoaded }}>
        {children}
        </CartContext.Provider>
    );
};