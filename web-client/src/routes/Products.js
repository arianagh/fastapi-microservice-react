import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import './Products.css'

const BASE_URL = "http://localhost:8001/"

export const Products = () => {
  const[products, setProducts] = useState([])

  useEffect(() => {
    fetch(BASE_URL + 'product')
      .then(response => {
        const json = response.json()
        if (response.ok) {
          return json
        }
        throw response
      })
      .then(data => {
        setProducts(data)
      })
      .catch(error => {
        console.log(error);
      })
  }, [])

  const handleDelete = (event, id) => {
    event?.preventDefault()

    const requestOptions = {
      method: 'DELETE'
    }

    fetch(BASE_URL + 'product/' + id, requestOptions)
      .then(response => {
        if (response.ok) {
          window.location.reload()
        }
        throw response
      })
      .catch(error => {
        console.log(error);
      })
  }

  return (
    <div className="products_div body">
      <div className="products_title title">Products</div>
      <div className="products_add_div">
        <Link to={`/create`} className="product_add button-4">Add</Link>
        <table className="products_table">
          <thead className="products_table_head">
            <th scope="col">pk</th>
            <th scope="col">Name</th>
            <th scope="col">Price</th>
            <th scope="col">Quantity</th>
            <th scope="col">Actions</th>
          </thead>
          <tbody>
            {
              products.map(product => {
                return <tr className="products_table_row" key={product.pk}>
                  <td className="products_table_td">{product.pk}</td>
                  <td className="products_table_td">{product.name}</td>
                  <td className="products_table_td">{product.price}</td>
                  <td className="products_table_td">{product.quantity}</td>
                  <td className="products_table_td">
                    <a href="#" className="product_delete_link"
                      onClick={event => handleDelete(event, product.pk)}>
                        Delete
                      </a>
                  </td>
                </tr>
              })
            }
          </tbody>
        </table>
      </div>
      <div className="products_order_div">
        <Link to={`/order`} className="products_order button-4">Order</Link>
      </div>
    </div>
  );
}