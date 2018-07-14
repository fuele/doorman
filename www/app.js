var express = require('express')
var app = express()
var path = require('path')
var port = 3000

var MongoClient = require('mongodb').MongoClient
var dburi = 'mongodb://localhost:27017'
var dbName = 'doorman'
var currentClientsCollection = 'currentClients'

var db

//app.use(express.static(path.join(__dirname,'public')))


app.get('/api/clients', (req, res) => {
    db.collection(currentClientsCollection).find({},{_id:0}).toArray( (err, results) => {
        console.log(results)
        res.send(results)
    })
})

app.get('/', (req, res)=> {
    res.send('Hello World!')
});


MongoClient.connect(dburi, (err, client) => {
    if(err){
        console.log(err)
    }else{
	db = client.db(dbName)
	console.log('Connected to db ' + dbName + ' at ' + dburi)
        app.listen(port, () => {
            console.log('Example app listening on port ' + port)
            //console.log(path.join(__dirname,'public'))
        })//end listen
    }//end else
}) //end connect





