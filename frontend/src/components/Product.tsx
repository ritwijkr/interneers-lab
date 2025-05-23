import { Product as ProductType } from "./types";

interface Props {
  product: ProductType;
}

const Product = ({ product }: Props) => {
  return (
    <div
      className="product-card"
      style={{
        background: "#783d19",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        margin: "10px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "16px",
        width: "200px",
        cursor: "pointer",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      }}
    >
      <img
        src={product.imageUrl}
        alt={product.name}
        style={{ width: "100%", borderRadius: "4px" }}
      />
      <h3>{product.name}</h3>
      <p>{product.brand}</p>
      <p>
        <strong>${product.price}</strong>
      </p>
    </div>
  );
};

export default Product;
