const express = require('express');
const redis = require('redis');
const app = express();

const redisClient = redis.createClient({
    host: 'test-redis',
    port: 6379
});

app.get('/', (req, res) => {
    redisClient.get('numVisits', (error, numVisits) => {
        numVisitsToDisplay = parseInt(numVisits) + 1;
        if(isNaN(numVisitsToDisplay)) {
            numVisitsToDisplay = 1;
        }
        res.send('Aplicação 2: O número de visitantes é: ' + numVisitsToDisplay);
        numVisits++;
        redisClient.set('numVisits', numVisits);
    });

});

app.listen(5000, () => {
    console.log("O servidor 2 está rodando na porta 5000");
})

