var express = require('express');
var app = express();
var path = require('path');

//app.use(express.static('/home/donovan/code/doorman/www/public'));
app.use(express.static(path.join(__dirname,'public')));

//app.get('/', function (req, res) {
//    res.send('Hello World!');
//});

app.listen(80, function() {
    console.log('Example app listening on port 80.');
    console.log(path.join(__dirname,'public'));
});
