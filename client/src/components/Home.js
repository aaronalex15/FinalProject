import { useState, useEffect } from "react";
import MerchandiseCard from "../components/MerchandiseCard";
import "../index.css";

function Home({ merchandise }) {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedType, setSelectedType] = useState("All");
  const [selectedBrand, setSelectedBrand] = useState("all");
  const [sortOrder, setSortOrder] = useState("asc");

  useEffect(() => {
    fetch("/categories")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((categories) => {
        setCategories(categories);
      })
      .catch((error) => {
        console.error("Error fetching categories:", error);
      });
  }, []);

  const getCategoryName = (categoryId) => {
    const category = categories.find((cat) => cat.id === categoryId);
    return category ? category.name : "Unknown";
  };

  const filterMerchandise = () => {
    return merchandise.filter((item) => {
      const categoryName = getCategoryName(item.category_id);
      return (
        (selectedCategory === "all" || categoryName === selectedCategory) &&
        (selectedType === "All" || item.type === selectedType) &&
        (selectedBrand === "all" || item.brand === selectedBrand)
      );
    });
  };

  const sortMerchandise = (items) => {
    return items.sort((a, b) => {
      const itemA = a.title.toLowerCase();
      const itemB = b.title.toLowerCase();
      return sortOrder === "asc" ? itemA.localeCompare(itemB) : itemB.localeCompare(itemA);
    });
  };

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
  };

  const handleTypeChange = (type) => {
    setSelectedType(type);
  };

  const handleBrandChange = (brand) => {
    setSelectedBrand(brand);
  };

  const handleSortChange = () => {
    setSortOrder(sortOrder === "asc" ? "desc" : "asc");
  };

  const filteredMerchandise = filterMerchandise();
  const sortedMerchandise = sortMerchandise(filteredMerchandise);

  return (
    <div className="home-container">
      <h1 className="title">M&M Get Fitted</h1>

      <div className="filters-container">
        {/* Type filter */}
        <select
          className="filter-select"
          onChange={(e) => handleTypeChange(e.target.value)}
        >
          <option value="All">All Types</option>
          <option value="Clothing">Clothing</option>
          <option value="Shoes">Shoes</option>
        </select>

        {/* Category filter */}
        <select
          className="filter-select"
          onChange={(e) => handleCategoryChange(e.target.value)}
        >
          <option value="all">All Categories</option>
          <option value="Hoodies">Hoodies</option>
          <option value="Sweats">Sweats</option>
          <option value="Jackets">Jackets</option>
          <option value="Shoes">Shoes</option>
          <option value="Hats">Hats</option>
          <option value="Other">Other</option>
        </select>

        {/* Brand filter */}
        <select
          className="filter-select"
          onChange={(e) => handleBrandChange(e.target.value)}
        >
          <option value="all">All Brands</option>
          <option value="Live Mechanics">Live Mechanics</option>
          <option value="Nike">Nike</option>
          <option value="Puma">Puma</option>
          <option value="New Era">New Era</option>
        </select>

        {/* Sort order */}
        <button className="sort-button" onClick={handleSortChange}>
          {sortOrder === "asc" ? "Sort A-Z" : "Sort Z-A"}
        </button>
      </div>

      {/* Display merchandise */}
      <ul className="merchandise-list">
        {sortedMerchandise.map((item) => (
          <li key={item.id} className="merchandise-item">
            <MerchandiseCard {...item} />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Home;
