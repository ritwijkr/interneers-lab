export interface Category {
  id: string;
  name: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  category: Category;
  price: number;
  brand: string;
  quantity: number;
  created_at: string;
  updated_at: string;
  imageUrl: string;
}
