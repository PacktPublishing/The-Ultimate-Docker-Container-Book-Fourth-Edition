const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

const hobbies = [
    'Swimming', 'Diving', 'Jogging', 'Cooking', 'Singing'
];

app.get('/hobbies', (req,res)=>{
    res.send(hobbies);
})
   
app.get('/status', (req,res)=>{
    res.send('OK, all good');
})

app.get('/colors', (req,res)=>{
    res.send(['red','green','blue']);
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
