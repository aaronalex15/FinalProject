import { Link } from "react-router-dom";
import { CartContext } from "../components/CartContext";
import { useContext, useEffect, useState } from "react";
import toast from "react-hot-toast";

const MerchandiseCard = ({
  title,
  description,
  price,
  image,
  brand,
  type,
  category_id,
}) => {
  const { addToCart, removeFromCart, cartItems } = useContext(CartContext);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [inCart, setInCart] = useState(
    cartItems.some((item) => item.title === title)
  );
  const [favorited, setFavorited] = useState(false);

  const handleAddToCart = () => {
    addToCart({ title, description, price, image, brand, type, category_id });
    toast.success(`${title} added to cart!`);
  };

  const handleRemoveFromCart = () => {
    removeFromCart(title);
    toast.error(`${title} removed from cart!`);
  };

  const handleFavorite = () => {
    setFavorited(!favorited);
    //send a request to backend
  };

  return (
    <div className="merchandise-container">
      <div className="merchandise-card">
        <h3>{title}</h3>
        {image && <img src={image} alt={title} />}
        <p>{description}</p>
        <p>Brand: {brand}</p>
        <p>Type: {type}</p>
        <p>Category ID: {category_id}</p>
        <p>${price}</p>
        {favorited ? (
          <button onClick={handleFavorite}>Unfavorite ❤️</button>
        ) : (
          <button onClick={handleFavorite}>Favorite 🤍</button>
        )}
        {inCart ? (
          <button onClick={handleRemoveFromCart}>Remove from Cart 🛒</button>
        ) : (
          <button onClick={handleAddToCart}>Add to Cart 🛒</button>
        )}
      </div>
    </div>
  );
};

export default MerchandiseCard;
