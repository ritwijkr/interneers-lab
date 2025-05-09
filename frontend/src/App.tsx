import { useEffect, useState, useCallback } from "react";
import Navbar from "./components/Navbar";
import ProductList from "./components/ProductList";
import CreateModal from "./components/CreateModal";
import axios from "axios";
import { Product, Category } from "./components/types";
import "./App.css";

axios.defaults.baseURL = "http://localhost:8000";

const App = () => {
  const [category, setCategory] = useState("All Products");
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [showCreateModal, setShowCreateModal] = useState(false);

  const fetchProducts = useCallback(async () => {
    try {
      let url = "/products/";
      if (category !== "All Products") {
        const categoryRes = await axios.get(`/categories/?title=${category}`);
        if (categoryRes.data.length > 0) {
          const categoryId = categoryRes.data[0].id;
          url = `/categories/${categoryId}/products/`;
        }
      }
      const res = await axios.get(url);
      setProducts(res.data);
    } catch (err) {
      console.error("Failed to fetch products", err);
    }
  }, [category]);

  const fetchCategories = async () => {
    try {
      const res = await axios.get("/categories/");
      const formatted = res.data.map((cat: any) => ({
        id: cat.id,
        name: cat.title,
      }));
      setCategories([{ id: "all", name: "All Products" }, ...formatted]);
    } catch (err) {
      console.error("Failed to fetch categories", err);
    }
  };

  const handleDeleteProduct = (id: string) => {
    setProducts((prev) => prev.filter((p) => p.id !== id));
  };

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  useEffect(() => {
    fetchCategories();
  }, []);

  return (
    <>
      <Navbar
        onCategorySelect={setCategory}
        onCreateProduct={() => setShowCreateModal(true)}
        categories={categories}
      />

      <ProductList
        products={products}
        selectedCategory={category}
        setProducts={setProducts}
        onDeleteProduct={handleDeleteProduct}
      />

      {showCreateModal && (
        <CreateModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={() => {
            fetchProducts();
            fetchCategories();
          }}
        />
      )}
    </>
  );
};

export default App;
