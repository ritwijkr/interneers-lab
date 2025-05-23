import { useState } from "react";
import { Product as ProductType } from "./types";
import Product from "./Product";
import Modal from "./ProductModal";

interface Props {
  products: ProductType[];
  selectedCategory: string;
  setProducts: (products: ProductType[]) => void;
  onDeleteProduct: (id: string) => void;
}

const ITEMS_PER_PAGE = 6;

const ProductList = ({ products, selectedCategory, setProducts }: Props) => {
  const [selectedProduct, setSelectedProduct] = useState<ProductType | null>(
    null,
  );
  const [currentPage, setCurrentPage] = useState(1);

  const filtered =
    selectedCategory === "All Products"
      ? products
      : products.filter(
          (p) => p.category && p.category.toString() === selectedCategory,
        );

  const totalPages = Math.ceil(filtered.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginated = filtered.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  return (
    <>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "20px",
          padding: "20px",
        }}
      >
        {paginated.map((product) => (
          <div key={product.id}>
            <Product
              product={product}
              onClick={() => setSelectedProduct(product)}
            />
          </div>
        ))}
      </div>

      <div style={{ textAlign: "center", margin: "20px 0" }}>
        {Array.from({ length: totalPages }, (_, idx) => idx + 1).map((page) => (
          <button
            key={page}
            onClick={() => setCurrentPage(page)}
            style={{
              margin: "0 5px",
              padding: "8px 12px",
              backgroundColor: currentPage === page ? "#575757" : "#111111",
              color: currentPage === page ? "#5f6f52" : "#a9b388",
              border: "1px solid #fefae0",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            {page}
          </button>
        ))}
      </div>

      {selectedProduct && (
        <Modal
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
          onUpdate={(updatedProduct) => {
            const updatedList = products.map((p) =>
              p.id === updatedProduct.id ? updatedProduct : p,
            );
            setProducts(updatedList);
            setSelectedProduct(null);
          }}
        />
      )}
    </>
  );
};

export default ProductList;
