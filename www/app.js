var express = require('express')
var app = express()
var path = require('path')
var port = 3000

var MongoClient = require('mongodb').MongoClient
var dburi = 'mongodb://localhost:27017'
var dbName = 'doorman'
var currentClientsCollection = 'currentClients'
var nicknameCollection = 'macNicknames'

var db

//app.use(express.static(path.join(__dirname,'public')))

function getNick(mac){
    console.log('Looking for nickname for ' +mac)
    db.collection(nicknameCollection).find({'mac':mac},{_id:0}).toArray( (err,results) => {
        if(err){
            console.log('Failed to find mac in nickname collection')
	    return {'mac':mac, 'nick':'unknown device'}
	}else{
            console.log('Found nickname')
	    console.log('results: ' + results)
	    return(results)
	}//end if
    })//end function
}//end function


//list all the clients currently connected to the wifi
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





