import React, { useState, useEffect } from "react";
import axios from "axios";

interface Props {
  onClose: () => void;
  onSuccess: () => void;
}

const CreateModal = ({ onClose, onSuccess }: Props) => {
  const [mode, setMode] = useState<"product" | "category">("product");
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    brand: "",
    price: "",
    quantity: "",
    category_title: "",
    title: "",
  });
  const [categories, setCategories] = useState<{ id: string; name: string }[]>(
    [],
  );
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (mode === "product") {
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
    }
  }, [mode]);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      if (mode === "product") {
        const { name, description, brand, price, quantity, category_title } =
          formData;
        await axios.post("/products/create/", {
          name,
          description,
          brand,
          price: parseFloat(price.toString()),
          quantity: parseInt(quantity.toString(), 10),
          category_title,
        });
      } else {
        const { title, description } = formData;
        await axios.post("/categories/create/", {
          title,
          description,
        });
      }
      alert("Created successfully!");
      onSuccess();
      onClose();
    } catch (err: any) {
      console.error(err);
      alert(err.response?.data?.error || "Creation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <button onClick={onClose} style={styles.closeButton}>
          ✕
        </button>
        <h2 style={{ marginBottom: 10 }}>
          Create New {mode === "product" ? "Product" : "Category"}
        </h2>

        <div style={styles.switcher}>
          <button
            style={mode === "product" ? styles.activeTab : styles.tab}
            onClick={() => setMode("product")}
          >
            Product
          </button>
          <button
            style={mode === "category" ? styles.activeTab : styles.tab}
            onClick={() => setMode("category")}
          >
            Category
          </button>
        </div>

        <div style={styles.form}>
          {mode === "product" ? (
            <>
              <input
                name="name"
                placeholder="Product Name"
                value={formData.name}
                onChange={handleChange}
              />
              <input
                name="brand"
                placeholder="Brand"
                value={formData.brand}
                onChange={handleChange}
              />
              <input
                name="price"
                type="number"
                placeholder="Price (e.g. 99.99)"
                value={formData.price}
                onChange={handleChange}
              />
              <input
                name="quantity"
                type="number"
                placeholder="Quantity (e.g. 10)"
                value={formData.quantity}
                onChange={handleChange}
              />
              <select
                name="category_title"
                value={formData.category_title}
                onChange={handleChange}
              >
                <option value="">Select Category</option>
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.name}>
                    {cat.name}
                  </option>
                ))}
              </select>
              <textarea
                name="description"
                placeholder="Product Description"
                value={formData.description}
                onChange={handleChange}
              />
            </>
          ) : (
            <>
              <input
                name="title"
                placeholder="Category Title"
                value={formData.title}
                onChange={handleChange}
              />
              <textarea
                name="description"
                placeholder="Category Description"
                value={formData.description}
                onChange={handleChange}
              />
            </>
          )}

          <button
            style={styles.submitButton}
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? "Submitting..." : "Create"}
          </button>
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
    backgroundColor: "rgba(0, 0, 0, 0.6)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 999,
  },
  modal: {
    background: "#1e1e1e",
    color: "#fff",
    padding: 20,
    borderRadius: 8,
    width: "90%",
    maxWidth: 500,
    position: "relative",
  },
  closeButton: {
    position: "absolute",
    top: 10,
    right: 10,
    background: "none",
    border: "none",
    color: "#fff",
    fontSize: 20,
    cursor: "pointer",
  },
  switcher: {
    display: "flex",
    marginBottom: 10,
  },
  tab: {
    flex: 1,
    padding: 10,
    background: "#333",
    border: "none",
    color: "#aaa",
    cursor: "pointer",
  },
  activeTab: {
    flex: 1,
    padding: 10,
    background: "#4CAF50",
    border: "none",
    color: "#fff",
    fontWeight: "bold",
    cursor: "pointer",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  submitButton: {
    marginTop: 10,
    padding: 10,
    background: "#4CAF50",
    border: "none",
    color: "#fff",
    cursor: "pointer",
    borderRadius: 5,
    fontWeight: "bold",
  },
};

export default CreateModal;
