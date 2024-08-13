import React from "react";
import { useFormik } from "formik";
import * as yup from "yup";

const SessionForm = ({ onSubmitSuccess, selectedCoach, selectedClient }) => {

  const formSchema = yup.object().shape({
    date: yup.date().required("Must enter a date"),
    time: yup.string().required("Must enter a time"),
    notes: yup.string().required("Must enter notes"),
    goal_progress: yup
      .number()
      .min(1, "Must enter goal progress between 1 and 10")
      .max(10, "Must enter goal progress between 1 and 10")
      .required("Must enter goal progress"),
  });

  const formik = useFormik({
    initialValues: {
      date: "",
      time: "",
      notes: "",
      goal_progress: "",
    },
    validationSchema: formSchema,
    onSubmit: (values) => {
      const dateTime = `${values.date} ${values.time}`;
      
      fetch("http://127.0.0.1:5000/sessions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          date: dateTime,
          client_id: selectedClient, // Use the selected client
          coach_id: selectedCoach,
          notes: values.notes,
          goal_progress: values.goal_progress,
        }),
      }).then((res) => {
        if (res.status === 201) {
          formik.resetForm();
          onSubmitSuccess && onSubmitSuccess();
        }
      });
    },
  });

  return (
    <form onSubmit={formik.handleSubmit} style={{ margin: "30px" }}>
      <h2>Schedule a New Session</h2>

      <div style={{ marginBottom: "15px" }}>
        <label htmlFor="date" style={{ marginRight: "10px" }}>Date</label>
        <input
          id="date"
          name="date"
          type="date"
          onChange={formik.handleChange}
          value={formik.values.date}
        />
        {formik.errors.date && <p style={{ color: "red" }}>{formik.errors.date}</p>}
      </div>

      <div style={{ marginBottom: "15px" }}>
        <label htmlFor="time" style={{ marginRight: "10px" }}>Time</label>
        <input
          id="time"
          name="time"
          type="time"
          onChange={formik.handleChange}
          value={formik.values.time}
        />
        {formik.errors.time && <p style={{ color: "red" }}>{formik.errors.time}</p>}
      </div>

      <div style={{ marginBottom: "15px" }}>
        <label htmlFor="notes" style={{ marginRight: "10px" }}>Notes</label>
        <textarea
          id="notes"
          name="notes"
          onChange={formik.handleChange}
          value={formik.values.notes}
        />
        {formik.errors.notes && <p style={{ color: "red" }}>{formik.errors.notes}</p>}
      </div>

      <div style={{ marginBottom: "15px" }}>
        <label htmlFor="goal_progress" style={{ marginRight: "10px" }}>Goal Progress (1-10)</label>
        <input
          id="goal_progress"
          name="goal_progress"
          type="number"
          onChange={formik.handleChange}
          value={formik.values.goal_progress}
        />
        {formik.errors.goal_progress && <p style={{ color: "red" }}>{formik.errors.goal_progress}</p>}
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}; 

export default SessionForm;