signUpApi = "http://127.0.0.1:5000/book-management/books"
loginApi = "http://127.0.0.1:5000/book-management/book"
function start(){
    signUpApi()
    loginApi()
}

document.querySelector('.img-btn').addEventListener('click', function()
	{
		document.querySelector('.cont').classList.toggle('s-signup')
	}
);
let btnLogin=document.querySelector('#btn_login');
let username=document.querySelector('#username')
let password=document.querySelector('#password')
btnLogin.addEventListener('click', () =>{
    console.log(username.value)
});