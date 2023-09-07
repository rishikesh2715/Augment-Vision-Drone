const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const port = 3000;
const nodemailer = require("nodemailer");
require("dotenv").config();
const protonmailUser = process.env.PROTONMAIL_USER;
const protonmailPass = process.env.PROTONMAIL_PASS;
const mongoose = require("mongoose");

app.use(bodyParser.json());
app.use(express.static("public"));

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true, // Ensure uniqueness
  },
});

const User = mongoose.model("User", userSchema);

mongoose.connect("mongodb://localhost:27017/local", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = mongoose.connection;

db.on("error", console.error.bind(console, "MongoDB connection error:"));
db.once("open", () => {
  console.log("Connected to MongoDB");
});

// Create a transporter object using your email service's SMTP settings
const transporter = nodemailer.createTransport({
  host: "127.0.0.1",
  port: 1025, // Use port 587 for TLS
  secure: false, // Use TLS, not SSL
  auth: {
    user: protonmailUser, // Your ProtonMail email address
    pass: protonmailPass, // Your ProtonMail password
  },
  tls: {
    rejectUnauthorized: false,
  },
});

app.post("/subscribe", async (req, res) => {
  const { email } = req.body;

  // Perform server-side validation (e.g., check if email is not already subscribed)
  // Check email format
  const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ error: "Invalid email format" });
  }

  // Check for duplicate emails
  const existingUser = await User.findOne({ email });
  if (existingUser) {
    return res.status(400).json({ error: "Email already subscribed" });
  }

  // Send a confirmation email to the user
  // Define email content
  const mailOptions = {
    from: "risdrone@proton.me",
    to: email, // Recipient's email address
    subject: "Welcome to RIS Drones Newsletter!",
    text: `
    Dear Subscriber,
    
    Thank you for subscribing to the RIS Drones Newsletter. We're thrilled to have you on board as part of our community of drone enthusiasts and technology enthusiasts.
    
    Here's a quick overview of what you can expect from our newsletter:
    - Stay updated on the latest advancements in aerial technology.
    - Get exclusive insights into our drone development journey.
    - Access special offers and promotions.
    
    We look forward to sharing exciting news and updates with you. If you have any questions or need assistance, feel free to contact us at risdrone@proton.me.
    
    Thank you for joining us on this exciting journey!
    
    Best regards,
    Steve Gillet
    RIS Drones Team
    risdrone.com
    `, // Email body
  };

  // Send the email
  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error(`Error sending email: ${error}`);
    } else {
      console.log(`Email sent: ${info.response}`);
    }
  });
  // Store the email in your database (e.g., MongoDB)
  try {
    // Create a new user with the provided email
    const user = new User({ email });
    await user.save();
    console.log(`Email ${email} saved to the database.`);
    res.sendStatus(200);
  } catch (error) {
    console.error(`Error saving email to the database: ${error}`);
    res.sendStatus(500); // Internal server error
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
