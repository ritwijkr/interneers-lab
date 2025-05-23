import React, { useState, useEffect } from "react";
import axios from "axios";
import { Product } from "./types";
import fillImage from "../assets/fillImage.jpg";

interface Props {
  product: Product;
  onClose: () => void;
  onUpdate: (updatedProduct: Product) => void;
}

const Modal = ({ product, onClose, onUpdate }: Props) => {
  const [formData, setFormData] = useState({ ...product });
  const [isEditing, setIsEditing] = useState(false);
  const [categories, setCategories] = useState<{ id: string; name: string }[]>(
    [],
  );

  useEffect(() => {
    axios
      .get("/categories/")
      .then((res) => {
        const options = res.data.map((cat: any) => ({
          id: cat.id ?? cat.title,
          name: cat.title,
        }));
        setCategories(options);
      })
      .catch((err) => console.error("Failed to fetch categories", err));
  }, []);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const validateForm = () => {
    if (!formData.name.trim()) {
      alert("Product name is required");
      return false;
    }
    if (isNaN(formData.price) || formData.price <= 0) {
      alert("Please enter a valid price");
      return false;
    }
    return true;
  };

  const handleSave = async () => {
    if (!validateForm()) return;
    try {
      const requestData = {
        name: formData.name,
        description: formData.description,
        brand: formData.brand,
        price: parseFloat(formData.price.toString()),
        quantity: parseInt(formData.quantity.toString(), 10),
        category_title: formData.category,
      };

      const response = await axios.put(
        `/products/${product.id}/`,
        requestData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      if (response.data.message === "Product updated successfully") {
        alert("Product updated successfully");
        setIsEditing(false);
        onUpdate({ ...formData });
      } else {
        throw new Error(response.data.error || "Update failed");
      }
    } catch (err) {
      console.error("Update error:", err);
      let errorMessage = "Update failed. Please try again.";
      if (axios.isAxiosError(err)) {
        if (err.response) {
          errorMessage = err.response.data.error || err.response.statusText;
        } else if (err.request) {
          errorMessage =
            "No response from server. Please check your connection.";
        }
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      alert(errorMessage);
    }
  };

  const handleDelete = async () => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this product?",
    );
    if (!confirmDelete) return;
    try {
      await axios.delete(`/products/${product.id}/`);
      alert("Product deleted successfully");
      onClose();
    } catch (err) {
      console.error("Delete error:", err);
      alert("Failed to delete product");
    }
    window.location.reload();
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <button onClick={onClose} style={styles.closeButton}>
          ✕
        </button>
        <div style={{ display: "flex", gap: "20px", alignItems: "flex-start" }}>
          <img
            src={formData.imageUrl || fillImage}
            alt={formData.name}
            style={{
              width: "50%",
              height: "auto",
              objectFit: "cover",
              borderRadius: "8px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.9)",
              transition: "transform 0.2s ease-in-out",
              transform: isEditing ? "scale(1.05)" : "scale(1)",
            }}
          />
          <div style={{ flex: 1 }}>
            {isEditing ? (
              <div style={styles.form}>
                <label>Name:</label>
                <input
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                />

                <label>Brand:</label>
                <input
                  name="brand"
                  value={formData.brand}
                  onChange={handleChange}
                />

                <label>Price:</label>
                <input
                  name="price"
                  type="number"
                  value={formData.price}
                  onChange={handleChange}
                />

                <label>Quantity:</label>
                <input
                  name="quantity"
                  type="number"
                  value={formData.quantity}
                  onChange={handleChange}
                />

                <label>Description:</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                />

                <label>Category:</label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                >
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.name}>
                      {cat.name}
                    </option>
                  ))}
                </select>

                <div style={styles.buttonGroup}>
                  <button style={styles.saveButton} onClick={handleSave}>
                    Save
                  </button>
                  <button
                    style={styles.cancelButton}
                    onClick={() => setIsEditing(false)}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <>
                <h2>{formData.name}</h2>
                <p>
                  <strong>Brand:</strong> {formData.brand}
                </p>
                <p>
                  <strong>Price:</strong> ${formData.price}
                </p>
                <p>
                  <strong>Quantity:</strong> {formData.quantity}
                </p>
                <p>
                  <strong>Description:</strong> {formData.description}
                </p>
                <p>
                  <strong>Category:</strong> {formData.category}
                </p>
                <div
                  style={{ display: "flex", gap: "10px", marginTop: "10px" }}
                >
                  <button
                    onClick={() => setIsEditing(true)}
                    style={{
                      backgroundColor: "#575757",
                      color: "#fff",
                      border: "none",
                      padding: "10px 20px",
                      borderRadius: "5px",
                      cursor: "pointer",
                    }}
                  >
                    Edit
                  </button>
                  <button
                    onClick={handleDelete}
                    style={{
                      backgroundColor: "#d32f2f",
                      color: "#fff",
                      border: "none",
                      padding: "10px 20px",
                      borderRadius: "5px",
                      cursor: "pointer",
                    }}
                  >
                    Delete
                  </button>
                </div>
              </>
            )}
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
    background: "#141414",
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
    color: "#fff",
    fontWeight: "bold",
    background: "none",
    border: "none",
    fontSize: "1.5rem",
    cursor: "pointer",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    width: "100%",
  },
  buttonGroup: {
    display: "flex",
    justifyContent: "flex-end",
    gap: "10px",
    marginTop: "10px",
  },
  saveButton: {
    backgroundColor: "#4CAF50",
    color: "#fff",
    border: "none",
    padding: "10px 20px",
    borderRadius: "4px",
    cursor: "pointer",
  },
  cancelButton: {
    backgroundColor: "#f44336",
    color: "#fff",
    border: "none",
    padding: "10px 20px",
    borderRadius: "4px",
    cursor: "pointer",
  },
};

export default Modal;
