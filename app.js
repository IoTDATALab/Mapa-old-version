const express = require('express')
const pug = require('pug')

const app = express()

let rawList = [
  {id:1,name:"zhangsan"},
  {id:2,name:"lisi"},
  {id:3,name:"ddd"},
  {id:4,name:"sss"},
  
]
app.set('view engine', 'pug')
app.set('views', './views')

app.get('/token', function (req, res) {
  res.send("token");
})


app.get('/delete:id',function(req,res){
  let is = parseInt(req,params.id);
  rawList = rawList.filter(function(data){
    return data.id !==id
  })
  res.redirect("/list")
})


app.get('/list', function(req, res) {
  res.render('list', {list: rawList})
})

app.get('*', function (req, res) {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})