import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { object, string } from "yup";
import { useFormik, Formik } from "formik";
import { UserContext } from "./UserContext";
import toast from "react-hot-toast";



const EditProfile = () => {
  const { currentUser, setCurrentUser, handleDeleteUser } = useContext(UserContext);
  const [editForm, setEditForm] = useState(false);
  const navigate = useNavigate();
  
  const editProfileSchema = object({
    username: string().max(20, "Username must be max of 20 characters").optional(),
    email: string().email().optional(),
    name: string().max(20).optional(),
    bio: string().max(250).optional(),
    avatar: string().url("Avatar must be a valid URL").optional() 
  });
  

  const initialValues = {
    username: currentUser.username || "",
    email: currentUser.email || "",
    name: currentUser.name || "",
    bio: currentUser.bio || "",
    avatar: currentUser.avatar || "",
  };

  const formik = useFormik({
    initialValues,
    validationSchema: editProfileSchema,
    onSubmit: (formData) => {
      fetch(`/users/${currentUser.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })
      .then((resp) => {
      if (resp.ok) {
        resp
          .json()
          .then((updatedUser) => {
            setCurrentUser(updatedUser);
            toggleForm();
            toast.success("Profile updated successfully");
          })
      } else {
        return resp.json().then((errorObj) => toast.error(errorObj.message));
      }
      })
      .catch((error) => {
        console.error("Error updating profile:", error);
        toast.error("Error updating profile. Please try again later.");
      });
    },
  });

  const toggleForm = () => {
    setEditForm((prevForm) => !prevForm);
  };


  const handleConfirmDelete = () => {
    if (window.confirm("Are you sure you want to delete? This cannot be undone")) {
      handleDeleteUser();
    } else {
      navigate(`/users/${currentUser.id}`);
    }
  };

  const buttonStyle = {
    backgroundColor: "blue",
  };



  return (
    <div className="edit-profile">
      <div className="profile-form-body">
        <button className="button-55" onClick={toggleForm}>
          {editForm ? "Cancel" : "Edit Profile"}
        </button>
        {editForm && (
          <form id="profileForm" onSubmit={formik.handleSubmit}>
            <label>Email: </label>
            <input
              type="text"
              name="email"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.email}
              className="edit-profile-input"
            />{" "}
            <br></br>
            {formik.errors.email && formik.touched.email && (
              <div className="edit-error">{formik.errors.email}</div>
            )}
            <label>Name: </label>
            <input
              type="text"
              name="name"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.name}
              className="edit-profile-input"
            />{" "}
            <br></br>
            {formik.errors.name && formik.touched.name && (
              <div className="edit-error">{formik.errors.name}</div>
            )}
            <label>Username: </label>
            <input
              type="text"
              name="username"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.username}
              className="edit-profile-input"
            />{" "}
            <br></br>
            {formik.errors.username && formik.touched.username && (
              <div className="edit-error">{formik.errors.username}</div>
            )}
            <label>Profile Picture: </label>
            <input
              type="text"
              alt="user avatar"
              name="avatar"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.avatar}
              className="edit-profile-input"
            />{" "}
            <br></br>
            {formik.errors.avatar && formik.touched.avatar && (
              <div className="edit-error">{formik.errors.avatar}</div>
            )}
            <label>Bio: </label>
            <input
              type="text"
              name="bio"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.bio}
              className="edit-profile-input"
            />{" "}
            <br></br>
            {formik.errors.bio && formik.touched.bio && (
              <div className="edit-error">{formik.errors.bio}</div>
            )}
            <br></br>
            <button type="submit" className="button-55-1">
              Confirm Changes
            </button>
            <div className="delete-profile">
              <h3>Delete Profile</h3>
              <button
                className="button-55-2"
                style={buttonStyle}
                onClick={handleConfirmDelete}
              >
                {" "}
                Delete
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default EditProfile;