var express = require('express')
var app = express()
var path = require('path')
var port = 3000

const dbconfig = require('./config/db')

var MongoClient = require('mongodb').MongoClient
var dbName = 'doorman'
var currentClientsCollection = 'uniqueClients'
var nicknameCollection = 'macNicknames'

var db


//This function is currently not in use
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


app.use('/', express.static(__dirname + '/public'))


MongoClient.connect(dbconfig.url, (err, client) => {
    if(err){
        console.log(err)
    }else{
	db = client.db(dbName)
	console.log('Connected to db ' + dbName )
        app.listen(port, () => {
            console.log('Example app listening on port ' + port)
            //console.log(path.join(__dirname,'public'))
        })//end listen
    }//end else
}) //end connect





