var x=1
function appendRow()
{
   var d = document.getElementById('div');
   d.innerHTML += "<input type='text' id='tst"+ x++ +"'><br >";
}