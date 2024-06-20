import { createBrowserRouter } from "react-router-dom";
import App from "../components/App";
import Home from "../components/Home";
import Registration from "../components/Registration";
import Error from "../components/Error";
import MerchandiseCard from "../components/MerchandiseCard"; 
import UserCard from "../components/UserCard";
import PurchaseCard from "../components/PurchaseCard";
import NewMerchandiseForm from "../components/NewMerchandiseForm"; 
import MyCart from "../components/MyCart";


export const router = createBrowserRouter([
  {
    element: <App />,
    errorElement: <Error />,
    children: [
      {
        path: "/",
        index: true,
        element: <Home />,
      },
      {
        path: "/registration",
        element: <Registration />,
      },
      {
        path: "/user/:userId",
        element: <UserCard />,
      },
      {
        path: "/merchandise/:merchandiseId", 
        element: <MerchandiseCard /> 
      },
      {
        path: "/merchandise",
        element: <NewMerchandiseForm />, 
      },
      {
        path: "/cart",
        element: <MyCart />,
      },
      {
        path: "/success/:purchaseId",
        element: <PurchaseCard />,
      },
    ],
  },
]);

