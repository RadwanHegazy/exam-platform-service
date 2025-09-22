require('dotenv').config();
const express = require('express');
const { body, validationResult } = require('express-validator');
const cassandra = require('cassandra-driver');
const app = express();
const port = process.env.PORT;

    // Cassandra client setup
const client = new cassandra.Client({
    contactPoints: [
        process.env.CASSANDRA_HOST_1,
        process.env.CASSANDRA_HOST_2
    ],
    localDataCenter: 'datacenter1',
    keyspace: process.env.CASSANDRA_KEYSPACE
});

    // Connect to Cassandra
    client.connect()
    .then(() => {
        console.log('Connected to Cassandra cluster');
    })
    .catch(err => {
        console.error('Error connecting to Cassandra:', err);
        process.exit(1);
    });

const StudentAnswer = [
    body('exam_id').isInt().withMessage('Exam ID must be an integer'),
    body('question_id').isInt().withMessage('Question ID must be an integer'),
    body('answer').isString().isLength({ min: 0, max: 1 }).withMessage('Answer must be a string with 0 or 1 character'),
];

app.use(express.json());

// Authentication middleware using native fetch (available in Node.js v18+)
app.use(async (req, res, next) => {
    try {
        const tokens = req.headers['authorization'];
        if (!tokens) {
            return res.status(401).json({
                'message': "Unauthorized - No token provided"
            });
        }
        
        const tokenParts = tokens.split(' ');
        if (tokenParts.length !== 2 || tokenParts[0] !== 'Bearer') {
            return res.status(401).json({
                'message': "Unauthorized - Invalid token format. Use: Bearer <token>"
            });
        }

        const token = tokenParts[1];
        
        const response = await fetch(process.env.VERIFY_TOKENS_URL, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ token: token })
        });

        if (response.ok) { // Check if status is 200-299
            next();
        } else {
            console.log(`Token verification failed with status: ${response.status}`);
            return res.status(401).json({
                'message': "Unauthorized - Invalid token"
            });
        }
    } catch (error) {
        console.log("An error occurred during authentication:", error);
        return res.status(500).json({
            'message': "Internal server error - Authentication service unavailable"
        });
    }
});

const validate = (req, res, next) => {
    const errors = validationResult(req);
    if (errors.isEmpty()) {
        return next();
    }
    
    const extractedErrors = errors.array().map(err => ({
        field: err.param,
        message: err.msg
    }));

    return res.status(400).json({
        message: "Validation failed",
        errors: extractedErrors
    });
};

app.post('/solver', StudentAnswer, validate, async (req, res) => {


    try {
        var { exam_id, question_id, answer } = req.body;
        var student_jwt = req.headers.authorization.split(" ")[1];
        
        var cassandraData = {
            "exam_id": exam_id,
            "question_id": question_id,
            "answer": answer,
            "student_jwt": student_jwt,
            'created_at': new Date().toISOString()
        };


        // Create table if not exists
        const createTableQuery = `
            CREATE TABLE IF NOT EXISTS student_answers (
                exam_id int,
                question_id int,
                student_jwt text,
                answer text,
                created_at timestamp,
                PRIMARY KEY ((exam_id, question_id), student_jwt)
            ) WITH CLUSTERING ORDER BY (student_jwt ASC)
        `;

        await client.execute(createTableQuery);

        // Create index on exam_id if not exists
        const createIndexQuery = `
            CREATE INDEX IF NOT EXISTS ON student_answers (exam_id)
        `;

        await client.execute(createIndexQuery);

        // Insert the data
        const insertQuery = 'INSERT INTO student_answers (exam_id, question_id, answer, student_jwt, created_at) VALUES (?, ?, ?, ?, ?)';
        const params = [exam_id, question_id, answer, student_jwt, cassandraData.created_at];

        await client.execute(insertQuery, params, { prepare: true });
        
        res.status(200).json({
            'message': "Answer Saved Successfully",
        });

    } catch (error) {
        console.error('Error saving to Cassandra:', error);
        res.status(500).json({
            'message': "Internal server error - Failed to save answer",
            'error': error.message
        });
    }
});

app.listen(port, () => {
    console.log(`Server is running on: http://0.0.0.0:${port}`);
});