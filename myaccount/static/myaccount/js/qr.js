
    document.addEventListener('DOMContentLoaded', function(){
        let amount = document.querySelector('#amount');
        let generate = document.querySelector('#generate');
        let detail = document.querySelector('#detail');

        generate.disabled = true;

        amount.onkeypress = function(evt){
            let char = String.fromCharCode(evt.which);
            if(!(/[0-9.]/.test(char))){
                evt.preventDefault()
            }
        };

        amount.onchange = () => {
            generate.disabled = amount.value.length === 0;
        };

        detail.onchange = () => {
            let details = DOMPurify.sanitize(detail.value);
            console.log(details);
            detail.value = details;
        };


        generate.onclick = () => {
            let regEx = /^\d{0,9}(\.\d{1,5})?$/;
            if(regEx.test(String(amount.value))) {

                if (amount.value.length === 0){ amount.value = 0 }
                if (detail.value.length === 0){ detail.value = 'Details Unavailable' }

                const request = new XMLHttpRequest();
                request.open('GET', '/myaccount/qr-image/' + amount.value + '/' + detail.value );
                request.responseType = "blob";
                request.onload = () => {
                    const response = request.response;
                    document.querySelector('#qr-code').src = URL.createObjectURL(response)
                };
                request.send()
            }
        }
        });
