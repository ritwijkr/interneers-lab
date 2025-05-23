import { categories } from "./data";

interface Props {
  onCategorySelect: (category: string) => void;
}

const Navbar = ({ onCategorySelect }: Props) => {
  return (
    <nav
      className="navbar"
      style={{
        backgroundColor: "#5f6f52",
        fontFamily: "dm-serif-display-regular",
        color: "#fff",
        height: "60px",
        display: "flex",
        justifyContent: "space-between",
        padding: "10px",
      }}
    >
      <div className="navbar-left">
        <h1 style={{ marginLeft: "30px", fontWeight: "bold" }}>City Mart</h1>
      </div>
      <div className="navbar-right">
        <ul
          style={{
            listStyle: "none",
            display: "flex",
            gap: "20px",
            marginRight: "30px",
            fontSize: "18px",
            fontWeight: "bold",
          }}
        >
          {categories.map((cat) => (
            <li
              key={cat.id}
              style={{ cursor: "pointer" }}
              onClick={() => onCategorySelect(cat.name)}
            >
              {cat.name}
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
