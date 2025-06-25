require("dotenv").config();
const express = require("express");
const http = require("http");
const mongoose = require("mongoose");
const cors = require("cors");
const authRoutes = require("./routes/auth");

const app = express();
const server = http.createServer(app);
const io = require("socket.io")(server, {
  cors: { origin: "*" }
});

mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true });

app.use(cors());
app.use(express.json());
app.use("/api/auth", authRoutes);

io.on("connection", (socket) => {
  console.log("User connected: " + socket.id);

  socket.on("join", ({ room }) => socket.join(room));

  socket.on("message", ({ room, message, sender }) => {
    io.to(room).emit("message", { sender, message });
  });

  socket.on("disconnect", () => console.log("User disconnected: " + socket.id));
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));

