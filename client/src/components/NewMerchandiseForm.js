import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { object, string, number } from "yup";
import { useFormik } from "formik";
import toast from "react-hot-toast";

const NewMerchandiseForm = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editForm, setEditForm] = useState(false);
  const [categories, setCategories] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/categories")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setCategories(data);
      })
      .catch((error) => {
        console.error("Error fetching categories:", error);
      });
  }, []);

  const merchandiseSchema = object({
    title: string()
      .max(50, "Title cannot be longer than 50 characters")
      .required("Title is required"),
    description: string().max(
      250,
      "Description cannot be longer than 250 characters"
    ),
    price: number(),
    brand: string().required("Brand is required"),
    type: string().required("Type is required"),
    category_id: number().required("Category is required"),
    image: string().required("Image is required"),
  });

  const initialValues = {
    title: "",
    description: "",
    price: "",
    brand: "",
    type: "",
    image: "",
    category_id: "",
  };

  const formik = useFormik({
    initialValues,
    validationSchema: merchandiseSchema,
    onSubmit: (formData) => {
      console.log(formData);
      setIsSubmitting(true);
      fetch("/merchandise", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })
        .then((resp) => {
          if (resp.ok) {
            console.log(formData);
            navigate("/");
          } else {
            return resp.json().then((error) => {
              toast.error(error.message);
            });
          }
        })
        .catch((error) => {
          toast.error("An error occurred. Please try again.");
        })
        .finally(() => {
          setIsSubmitting(false);
        });
    },
  });

  const toggleForm = () => {
    setEditForm((prevForm) => !prevForm);
  };

  return (
    <div className="merchandise-form-page">
      <div className="merchandise-form-body">
        <div className="merchandise-form-container">
          <button className="button-55" onClick={toggleForm}>
            {editForm ? "Cancel" : "Add Merchandise"}
          </button>
          {editForm && (
            <form id="merchandiseForm" onSubmit={formik.handleSubmit}>
              <h2 className="new-merchandise-banner">Add new merchandise!</h2>
              <label htmlFor="title">Title</label>
              <input
                type="text"
                name="title"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.title}
                className="merchandise-input"
              />
              {formik.errors.title && formik.touched.title && (
                <div className="error-message show">{formik.errors.title}</div>
              )}
              <label>Description</label>
              <input
                type="text"
                name="description"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.description}
                className="merchandise-input"
              />
              {formik.errors.description && formik.touched.description && (
                <div className="error-message show">
                  {formik.errors.description}
                </div>
              )}
              <label>Price</label>
              <input
                type="number"
                name="price"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.price}
                className="merchandise-input"
              />
              {formik.errors.price && formik.touched.price && (
                <div className="error-message show">{formik.errors.price}</div>
              )}
              <label>Brand</label>
              <input
                type="text"
                name="brand"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.brand}
                className="merchandise-input"
              />
              {formik.errors.brand && formik.touched.brand && (
                <div className="error-message show">{formik.errors.brand}</div>
              )}
              <label>Type</label>
              <select
                name="type"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.type}
                className="merchandise-input"
              >
                <option value="">Select type</option>
                <option value="Clothing">Clothing</option>
                <option value="Shoes">Shoes</option>
                <option value="Other">Other</option>
              </select>
              {formik.errors.type && formik.touched.type && (
                <div className="error-message show">{formik.errors.type}</div>
              )}
              <label>Category</label>
              <select
                name="category_id"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.category_id}
                className="merchandise-input"
              >
                <option value="">Select a category</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
              {formik.errors.category_id && formik.touched.category_id && (
                <div className="error-message show">
                  {formik.errors.category_id}
                </div>
              )}
              <label>Image URL</label>
              <input
                type="text"
                name="image"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.image}
                className="merchandise-input"
              />
              {formik.errors.image && formik.touched.image && (
                <div className="error-message show">{formik.errors.image}</div>
              )}
              <button
                className="button-55-1"
                type="submit"
                disabled={isSubmitting}
              >
                Submit
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default NewMerchandiseForm;
