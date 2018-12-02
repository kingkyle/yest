
    document.addEventListener('DOMContentLoaded', function(){
        let amount = document.querySelector('#amount');
        amount.onkeypress = function(evt){
            let char = String.fromCharCode(evt.which);
            if(!(/[0-9.]/.test(char))){
                evt.preventDefault()
            }
        };

        amount.onkeyup = () => {
            let regEx = /^\d{0,9}(\.\d{1,5})?$/;
            if(regEx.test(String(amount.value))) {
                fetch('/myaccount/qr-image/' + amount.value)
                    .then(function (response) {
                        if (response.ok) {
                            return response.blob();
                        } else {
                            return Promise.reject({
                                status: response.status,
                                statusText: response.statusText
                            })
                        }
                    })
            .then(function(data){
                console.log(data)
                        document.querySelector('#qr-code').src = URL.createObjectURL(data)
                    })
                        .catch(function (error) {
                            console.log('error', error);
                        })
            }
        }
        })
