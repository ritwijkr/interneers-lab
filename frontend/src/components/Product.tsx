import { Product as ProductType } from "./types";
import fillImage from "../assets/fillImage.jpg";

interface Props {
  product: ProductType;
  onClick: () => void;
}

const Product = ({ product, onClick }: Props) => {
  return (
    <div
      className="product-card"
      onClick={onClick}
      style={{
        background: "#232323",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        margin: "10px",
        border: "1px solid #000",
        borderRadius: "8px",
        padding: "60px",
        width: "400px",
        cursor: "pointer",
        boxShadow: "0 2px 8px rgba(0,0,0,0.9)",
        transition: "transform 0.2s ease-in-out",
      }}
    >
      <img
        src={product.imageUrl || fillImage}
        alt={product.name}
        style={{ width: "50%", borderRadius: "4px" }}
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
