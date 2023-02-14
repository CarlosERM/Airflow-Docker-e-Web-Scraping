const express = require("express");
const redis = require("redis");
const app = express();
const redisClient = redis.createClient({
  host: "test-redis",
  port: 6379,
});

app.get("/", (req, res) => {
  try {
    redisClient.get("numVisits", (error, numVisits) => {
      let numVisitsToDisplay = parseInt(numVisits) + 1;
      if (isNaN(numVisitsToDisplay)) {
        numVisitsToDisplay = 1;
      }
      res.send("O número de visitantes é: " + numVisitsToDisplay);
      redisClient.set("numVisits", numVisitsToDisplay);
    });
  } catch (error) {
    res.send(error);
  }
});

app.listen(4001, () => {
  console.log("O servidor está rodando na porta 4001.");
});
