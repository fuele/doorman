var express = require('express')
var app = express()
var path = require('path')
var port = 3000

//app.use(express.static('/home/donovan/code/doorman/www/public'));
app.use(express.static(path.join(__dirname,'public')))

//app.get('/', function (req, res) {
//    res.send('Hello World!');
//});

app.listen(port, () => {
    console.log('Example app listening on port ' + port)
    console.log(path.join(__dirname,'public'))
});
