import { useState } from "react";
import Navbar from "./components/Navbar";
import ProductList from "./components/ProductList";
import { products } from "./components/data";
import "./App.css";
<>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link
    rel="preconnect"
    href="https://fonts.gstatic.com"
    crossOrigin="anonymous"
  />
  <link
    href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&display=swap"
    rel="stylesheet"
  ></link>
</>;

const App = () => {
  const [category, setCategory] = useState("All Products");

  return (
    <>
      <Navbar onCategorySelect={setCategory} />
      <ProductList products={products} selectedCategory={category} />
    </>
  );
};

export default App;
