import React from "react";
import { useFormik } from "formik";
import * as yup from "yup";

const SessionForm = ({ onSubmitSuccess, selectedCoach, clients }) => {
  const formSchema = yup.object().shape({
    client_id: yup.string().required("Must select a client"),
    date: yup.date().required("Must enter a date"),
    hour: yup.string().required("Must select an hour"),
    period: yup.string().required("Must select AM or PM"),
    notes: yup.string().required("Must enter notes"),
    goal_progress: yup
      .number()
      .min(1, "Must enter goal progress between 1 and 10")
      .max(10, "Must enter goal progress between 1 and 10")
      .required("Must enter goal progress"),
  });

  const formik = useFormik({
    initialValues: {
      client_id: "",
      date: "",
      hour: "",
      period: "AM", //make it default to am
      notes: "",
      goal_progress: "",
    },
    validationSchema: formSchema,
    onSubmit: (values) => {
      // Convert time
      let hour = parseInt(values.hour);
      if (values.period === "PM" && hour !== 12) {
        hour += 12;
      } else if (values.period === "AM" && hour === 12) {
        hour = 0;
      }
      const time = `${hour.toString().padStart(2, "0")}:00:00`;
      const dateTime = `${values.date} ${time}`;

      fetch("http://127.0.0.1:5000/sessions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          date: dateTime,
          client_id: values.client_id,
          coach_id: selectedCoach,
          notes: values.notes,
          goal_progress: values.goal_progress,
        }),
      })
        .then((res) => {
          if (res.status === 201) {
            formik.resetForm();
            onSubmitSuccess && onSubmitSuccess();
          }
        })
        .catch((error) => console.error("Error adding session:", error));
    },
  });

  const generateHours = () => {
    const hours = [];
    for (let i = 1; i <= 12; i++) {
      hours.push(i.toString().padStart(2, "0"));
    }
    return hours;
  };

  return (
    <div className="session-form-container" style={smallerFormContainerStyle}>
      <form onSubmit={formik.handleSubmit} style={formStyle}>
        <div style={formGroupStyle}>
          <label htmlFor="client_id" style={labelStyle}>Client</label>
          <select
            id="client_id"
            name="client_id"
            onChange={formik.handleChange}
            value={formik.values.client_id}
            style={inputStyle}
          >
            <option value="" label="Select client" />
            {clients.map(client => (
              <option key={client.id} value={client.id}>
                {client.name}
              </option>
            ))}
          </select>
          {formik.errors.client_id && <p style={errorStyle}>{formik.errors.client_id}</p>}
        </div>

        <div style={formGroupStyle}>
          <label htmlFor="date" style={labelStyle}>Date</label>
          <input
            id="date"
            name="date"
            type="date"
            onChange={formik.handleChange}
            value={formik.values.date}
            style={inputStyle}
          />
          {formik.errors.date && <p style={errorStyle}>{formik.errors.date}</p>}
        </div>

        <div style={formGroupStyle}>
          <label htmlFor="hour" style={labelStyle}>Time</label>
          <select
            id="hour"
            name="hour"
            onChange={formik.handleChange}
            value={formik.values.hour}
            style={{ ...inputStyle, marginRight: "10px" }}
          >
            <option value="" label="Select hour" />
            {generateHours().map(hour => (
              <option key={hour} value={hour}>
                {hour}
              </option>
            ))}
          </select>
          <select
            id="period"
            name="period"
            onChange={formik.handleChange}
            value={formik.values.period}
            style={inputStyle}
          >
            <option value="AM">AM</option>
            <option value="PM">PM</option>
          </select>
          {formik.errors.hour && <p style={errorStyle}>{formik.errors.hour}</p>}
          {formik.errors.period && <p style={errorStyle}>{formik.errors.period}</p>}
        </div>

        <div style={formGroupStyle}>
          <label htmlFor="notes" style={labelStyle}>Notes</label>
          <textarea
            id="notes"
            name="notes"
            onChange={formik.handleChange}
            value={formik.values.notes}
            style={textareaStyle}
          />
          {formik.errors.notes && <p style={errorStyle}>{formik.errors.notes}</p>}
        </div>

        <div style={formGroupStyle}>
          <label htmlFor="goal_progress" style={labelStyle}>Goal Progress (1-10)</label>
          <input
            id="goal_progress"
            name="goal_progress"
            type="number"
            onChange={formik.handleChange}
            value={formik.values.goal_progress}
            style={inputStyle}
          />
          {formik.errors.goal_progress && <p style={errorStyle}>{formik.errors.goal_progress}</p>}
        </div>

        <button type="submit" style={submitButtonStyle}>Submit</button>
      </form>
    </div>
  );
};

// form styling
const smallerFormContainerStyle = {
  border: "1px solid #ccc",
  borderRadius: "10px",
  padding: "20px",
  marginBottom: "30px",
  backgroundColor: "#f9f9f9",
  width: "90%",
  maxWidth: "500px",
  margin: "0 auto",
};

const formStyle = {
  display: "flex",
  flexDirection: "column",
};

const formGroupStyle = {
  marginBottom: "15px",
};

const labelStyle = {
  marginBottom: "5px",
  fontWeight: "bold",
};

const inputStyle = {
  width: "100%",
  padding: "8px",
  border: "1px solid #ccc",
  borderRadius: "5px",
};

const textareaStyle = {
  ...inputStyle,
  minHeight: "100px",
};

const submitButtonStyle = {
  padding: "10px 15px",
  backgroundColor: "#468B90",
  color: "white",
  border: "none",
  borderRadius: "5px",
  cursor: "pointer",
  fontSize: "16px",
};

const errorStyle = {
  color: "red",
};


export default SessionForm;