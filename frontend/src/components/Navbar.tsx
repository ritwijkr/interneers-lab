import { useEffect, useState } from "react";
import axios from "axios";
import { Category } from "./types";

interface Props {
  onCategorySelect: (category: string) => void;
  onCreateProduct: () => void;
  categories: Category[]; // ← Add this line
}

const Navbar = ({ onCategorySelect, onCreateProduct }: Props) => {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    axios
      .get("/categories/")
      .then((res) => {
        const allOption = { id: "all", name: "All Products" };
        const formattedCategories = res.data.map((cat: any) => ({
          id: cat.id,
          name: cat.title,
        }));
        setCategories([allOption, ...formattedCategories]);
      })
      .catch((err) => {
        console.error("Failed to fetch categories", err);
        setCategories([{ id: "all", name: "All Products" }]);
      });
  }, []);

  return (
    <nav
      style={{
        backgroundColor: "#111111",
        color: "#fff",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "10px 30px",
        height: "70px",
        fontFamily: "dm-serif-display-regular",
      }}
    >
      <style>
        @import
        url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Monoton&display=swap');
      </style>
      <h1
        style={{
          fontWeight: "bold",
          fontFamily: "Monoton",
          fontSize: "50px",
          color: "#8f05fb",
          margin: 0,
        }}
      >
        City Mart
      </h1>

      {/* Right: Dropdown + Button */}
      <div style={{ display: "flex", gap: "15px", alignItems: "center" }}>
        <select
          onChange={(e) => onCategorySelect(e.target.value)}
          style={{
            padding: "8px 12px",
            borderRadius: "5px",
            fontSize: "16px",
            fontWeight: "bold",
            cursor: "pointer",
            backgroundColor: "#222",
            color: "#fff",
            border: "1px solid #555",
          }}
        >
          {categories.map((cat) => (
            <option key={cat.id} value={cat.name}>
              {cat.name}
            </option>
          ))}
        </select>

        <button
          onClick={onCreateProduct}
          style={{
            padding: "10px 18px",
            fontSize: "16px",
            fontWeight: "bold",
            color: "#fff",
            backgroundColor: "#4CAF50",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          + Create Product
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
