/*(function($){
  $(function(){

    $('.sidenav').sidenav();

  }); // end of document ready
})(jQuery); // end of jQuery name space*/


const login = document.getElementById('login')
login.addEventListener('click', (e)=>{
  e.preventDefault()
  let form = document.getElementById('register-form')
  let formData = new FormData(form)
  let xhr = new XMLHttpRequest();
  if (!xhr) {
      alert('Giving up :( Cannot create an XMLHTTP instance');
      return false;
  }
  xhr.open('POST', '/login')
  xhr.onreadystatechange = function () {
  var DONE = 4; // readyState 4 means the request is done.
  var OK = 200; // status 200 is a successful return.
  if (xhr.readyState === DONE) {
    if (xhr.status === OK) {
      console.log("Success")
      console.log(xhr.responseText); // 'This is the returned text.'
      if (xhr.responseText==="True"){
        console.log("gfjsdh")
        window.location.href='./manageCustomer'
      }
    } else {
      console.log('Error: ' + xhr.status); // An error occurred during the request.
    }
  }
};
  xhr.send(formData)
})

