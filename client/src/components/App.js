import React, { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import NavBar from "../components/NavBar";
import Home from "./Home";
import UserCard from "../components/UserCard";
import Registration from "../components/Registration";
import MyCart from "../components/MyCart";
import { UserProvider, useUserContext } from "../components/UserContext";
import { CartProvider } from "../components/CartContext";

function App() {
  const [merchandise, setMerchandise] = useState([]);
  const { currentUser } = useUserContext();

  useEffect(() => {
    fetch("/merchandises")
      .then((resp) => {
        if (!resp.ok) {
          return resp.text().then((errorText) => {
            console.error("Fetch error:", errorText);
            throw new Error(`Error ${resp.status}: ${errorText}`);
          });
        }
        return resp.json();
      })
      .then(setMerchandise)
      .catch((err) => {
        toast.error(err.message);
        console.error("Error fetching merchandise:", err);
      });
  }, []);

  return (
    <div>
      <Toaster />
      <NavBar />
      <Routes>
        <Route path="/" element={<Home merchandise={merchandise} />} />
        <Route path="/registration" element={<Registration />} />
        <Route path="/cart" element={<MyCart />} />
        {currentUser && (
          <Route path={`/users/${currentUser.id}`} element={<UserCard />} />
        )}
      </Routes>
    </div>
  );
}

export default function AppWrapper() {
  return (
    <UserProvider>
      <CartProvider>
        <App />
      </CartProvider>
    </UserProvider>
  );
}
