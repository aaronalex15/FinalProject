import { useContext, useState, useEffect } from "react";
import { UserContext } from "./UserContext";
import NewMerchandiseForm from "../components/NewMerchandiseForm";
import EditProfile from "./EditProfile";
import PurchaseCard from "../components/PurchaseCard";
import MerchandiseCard from "../components/MerchandiseCard";
import PurchaseCardTwo from "../components/PurchaseCardTwo";

const UserCard = () => {
  const { currentUser } = useContext(UserContext);
  const [favoritedMerchandise, setFavoritedMerchandise] = useState([]);

  useEffect(() => {
    if (currentUser) {
      fetch(`/favorites/${currentUser.id}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to fetch favorited merchandise");
          }
          return response.json();
        })
        .then((data) => {
          if (data && data.favoritedMerchandise) {
            console.log("Favorited merch:", data.favoritedMerchandise);
            setFavoritedMerchandise(data.favoritedMerchandise);
          } else {
            console.error("Favorited merch data is missing or invalid:", data);
          }
        })
        .catch((error) => {
          console.error("Error fetching favorited merch:", error);
        });
    }
  }, [currentUser]);

  return (
    <>
      <div className="user-profile">
        <div className="user-card">
          {currentUser ? (
            <>
              <h2>{currentUser.name}</h2>
              <img
                src={currentUser.avatar}
                alt="User Avatar"
                className="user-avatar"
              />
              <div className="user-info">
                <p>{currentUser.username}</p>
                <p>{currentUser.email}</p>
                <p>{currentUser.bio}</p>
              </div>
            </>
          ) : (
            <h2>No user logged in</h2>
          )}
        </div>
        <EditProfile {...currentUser} />
        <NewMerchandiseForm />
        {currentUser?.purchases?.map((p) => (
          <PurchaseCardTwo {...p} key={p.id} />
        ))}
        {favoritedMerchandise.length > 0 && (
          <div className="favorited-merch"> {/* Updated class name */}
            <h3>Favorited Merchandise:</h3>
            {favoritedMerchandise?.map((merchandise) => (
              <MerchandiseCard key={merchandise.id} {...merchandise} />
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default UserCard;
