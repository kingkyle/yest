document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('.profile-link').forEach(link => {
        link.onclick = () => {
            load_page(link.dataset.page);
            return false;
        };
    });
});


window.onpopstate = e => {
    const info = e.state;
    let parser = new DOMParser();
    parser = parser.parseFromString(info, 'text/html')
    let profile_data = parser.querySelector('#profiledata')
    document.querySelector('#profilepage').innerHTML = profile_data;
}

function load_page(name){
    fetch(`/myaccount/profile/${name}`)
        .then(function(response){
            if(response.ok){
                return response.text()
            }
            else {
                return Promise.reject({
                    status: response.status,
                    statusText: response.statusText
                })
            }
        })
        .then(function (data) {
            let parser = new DOMParser();
            parser = parser.parseFromString(data, 'text/html')
            let profiledata = parser.querySelector('#profiledata')
            console.log(profiledata)
            document.querySelector('#profilepage').innerHTML = profiledata.outerHTML;
            history.pushState({'text': data}, name, `/myaccount/profile/${name}`)
        })
}