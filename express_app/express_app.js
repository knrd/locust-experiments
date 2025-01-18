// app.js
const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();
const port = 3000;

// Middleware
app.use(express.json());
app.use(cookieParser());

// Helper function to decode JSON in a Promise
const decodeJSON = (data) => {
    return new Promise((resolve, reject) => {
        try {
            const decoded = JSON.parse(JSON.stringify(data));
            resolve(decoded);
        } catch (error) {
            reject(error);
        }
    });
};

app.post('/', (req, res) => {
    if (req.cookies.ctest) {
        decodeJSON(req.body)
            .then(decodedData => {
                console.log('Received JSON:', decodedData);
            })
            .catch(error => {
                console.error('Error processing JSON:', error);
            })
            .finally(() => {
                res.status(200).send('OK');
            });
    } else {
        res.status(200).send('OK');
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

