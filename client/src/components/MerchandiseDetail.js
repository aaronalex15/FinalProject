import React, { useContext } from "react";
import { CartContext } from "./CartContext";

const MerchandiseDetail = ({ merchandise }) => {
    const { addToCart } = useContext(CartContext);

    const handleAddToCart = () => {
        addToCart(merchandise);
    };

    return (
        <div>
            <h2>{merchandise.title}</h2>
            <p>Description: {merchandise.description}</p>
            <p>Price: ${merchandise.price}</p>
            <img src={merchandise.imageUrl} alt={merchandise.title} style={{ maxWidth: '100px' }} />
            <button onClick={handleAddToCart}>Add to Cart</button>
        </div>
    );
};

export default MerchandiseDetail;
