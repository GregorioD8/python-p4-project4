import React, { useState } from "react";

const MockPaymentForm = ({ session, onPaymentSubmit, onCancel }) => {
  const [amount, setAmount] = useState("120"); 
  const [cardNumber, setCardNumber] = useState("");
  const [expiration, setExpiration] = useState("");
  const [cvc, setCvc] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Validate the form fields (simple validation for demo purposes)
    if (!cardNumber || !expiration || !cvc) {
      alert("Please fill in all payment details.");
      return;
    }
    onPaymentSubmit(session.id); // Call parent function to update payment status
  };

  return (
    <div className="payment-form" style={formStyle}>
      <h3 style={headerStyle}>Pay for {session.client_name}'s session</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-3" style={formGroupStyle}>
          <label htmlFor="amount" className="form-label" style={labelStyle}>Amount</label>
          <input
            type="number"
            className="form-control"
            id="amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            style={inputStyle}
            readOnly
          />
        </div>
        <div className="mb-3" style={formGroupStyle}>
          <label htmlFor="cardNumber" className="form-label" style={labelStyle}>Card Number</label>
          <input
            type="text"
            className="form-control"
            id="cardNumber"
            placeholder="1234 5678 9012 3456"
            value={cardNumber}
            onChange={(e) => setCardNumber(e.target.value)}
            style={inputStyle}
          />
        </div>
        <div className="mb-3" style={formGroupStyle}>
          <label htmlFor="expiration" className="form-label" style={labelStyle}>Expiration Date</label>
          <input
            type="text"
            className="form-control"
            id="expiration"
            placeholder="MM/YY"
            value={expiration}
            onChange={(e) => setExpiration(e.target.value)}
            style={inputStyle}
          />
        </div>
        <div className="mb-3" style={formGroupStyle}>
          <label htmlFor="cvc" className="form-label" style={labelStyle}>CVC</label>
          <input
            type="text"
            className="form-control"
            id="cvc"
            placeholder="123"
            value={cvc}
            onChange={(e) => setCvc(e.target.value)}
            style={inputStyle}
          />
        </div>
        <div className="button-group" style={buttonGroupStyle}>
          <button type="submit" className="btn btn-success" style={payButtonStyle}>
            Pay
          </button>
          <button type="button" className="btn btn-secondary ms-2" onClick={onCancel} style={cancelButtonStyle}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

// Styles for a more polished look
const formStyle = {
  backgroundColor: "#f8f9fa",
  padding: "30px",
  borderRadius: "10px",
  boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.1)",
  maxWidth: "400px",
  margin: "20px auto",
};

const formGroupStyle = {
  marginBottom: "20px",
};

const inputStyle = {
  width: "100%",
  padding: "10px",
  borderRadius: "5px",
  border: "1px solid #ccc",
  fontSize: "16px",
};

const labelStyle = {
  fontWeight: "bold",
  marginBottom: "5px",
};

const headerStyle = {
  textAlign: "center",
  marginBottom: "20px",
  color: "#333",
};

const buttonGroupStyle = {
  display: "flex",
};

const payButtonStyle = {
  width: "120px",
  padding: "10px",
};

const cancelButtonStyle = {
  width: "120px",
  padding: "10px",
  backgroundColor: "#6c757d",
  borderColor: "#6c757d",
  color: "white",
};

export default MockPaymentForm;