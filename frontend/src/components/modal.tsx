import React from "react";
import { Product } from "./types";

interface Props {
  product: Product;
  onClose: () => void;
}

const Modal = ({ product, onClose }: Props) => {
  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <button onClick={onClose} style={styles.closeButton}>
          ✕
        </button>
        <div style={{ display: "flex", gap: "20px", alignItems: "flex-start" }}>
          <img
            src={product.imageUrl}
            alt={product.name}
            style={{
              width: "50%",
              height: "auto",
              objectFit: "cover",
              borderRadius: "8px",
            }}
          />
          <div>
            <h2>{product.name}</h2>
            <p>
              <strong>Brand:</strong> {product.brand}
            </p>
            <p>
              <strong>Price:</strong> ${product.price}
            </p>
            <p>
              <strong>Quantity:</strong> {product.quantity}
            </p>
            <p>
              <strong>Description:</strong> {product.description}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  overlay: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    backdropFilter: "blur(6px)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000,
  },
  modal: {
    background: "#b99470",
    borderRadius: "12px",
    padding: "20px",
    width: "80%",
    maxWidth: "800px",
    boxShadow: "0 5px 20px rgba(0,0,0,0.3)",
    position: "relative",
  },
  closeButton: {
    position: "absolute",
    top: "10px",
    right: "10px",
    background: "none",
    border: "none",
    fontSize: "1.5rem",
    cursor: "pointer",
  },
};

export default Modal;
