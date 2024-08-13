import React from "react";
import { useFormik } from "formik";
import * as yup from "yup";

function CoachesForm({ onSubmitSuccess }) {
  const formSchema = yup.object().shape({
    name: yup.string().required("Name is required"),
    specialization: yup.string().required("Specialization is required"),
  });

  const formik = useFormik({
    initialValues: {
      name: "",
      specialization: "",
    },
    validationSchema: formSchema,
    onSubmit: (values) => {
      fetch("http://127.0.0.1:5000/coaches", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      })
        .then((res) => res.json())
        .then((newCoach) => {
          onSubmitSuccess(newCoach); // Notify parent component of new coach
          formik.resetForm(); // Clear the form fields
        })
        .catch((error) => console.error("Error adding coach:", error));
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <div>
        <label htmlFor="name">Name: </label>
        <input
          id="name"
          name="name"
          type="text"
          onChange={formik.handleChange}
          value={formik.values.name}
        />
        {formik.errors.name && <p>{formik.errors.name}</p>}
      </div>
      <br/>
      <div>
        <label htmlFor="specialization">Specialization: </label>
        <input
          id="specialization"
          name="specialization"
          type="text"
          onChange={formik.handleChange}
          value={formik.values.specialization}
        />
        {formik.errors.specialization && <p>{formik.errors.specialization}</p>}
      </div>
      <br/>
      <button type="submit">Add Coach</button>
    </form>
    
  );
}

export default CoachesForm;