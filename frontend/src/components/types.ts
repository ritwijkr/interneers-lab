export interface Product {
  id: string;
  name: string;
  description: string;
  brand: string;
  category: string; // just the title name of the category
  price: number;
  quantity: number;
  imageUrl?: string; // optional field for display
}

export interface Category {
  id: string;
  name: string;
}
