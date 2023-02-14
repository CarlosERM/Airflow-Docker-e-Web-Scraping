const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Oi, lindão!!! Tudo bem??");
});

app.listen(8080, () => {
  console.log("O servidor está ligado na porta 5000");
});
