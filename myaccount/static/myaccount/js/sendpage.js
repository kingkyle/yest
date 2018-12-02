
document.addEventListener('DOMContentLoaded', function(){
    let nextButton = document.querySelector('#nextButton');
    let emailValidate = document.querySelector('#emailValidate');
    nextButton.disabled = true;
    emailValidate.style.display = 'none';

    let email = document.querySelector('#id_check_email');

    let regEx = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    email.oninput = () => {
    if (regEx.test(String(email.value).toLowerCase())){
        nextButton.disabled = false;
    }else{
        emailValidate.style.display = 'none';
        nextButton.disabled = true;
    }
    }

    email.onchange = () => {
        if (regEx.test(String(email.value).toLowerCase())) {
            emailValidate.style.display = 'none';
        } else if(email.value == ''){
            emailValidate.style.display = 'none';
        } else {
            emailValidate.style.display = 'block';
        }
    }
})