document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('.profile-link').forEach(link => {
        link.onclick = () => {
            load_page(link.dataset.page);
            return false;
        };
    });

});


// window.onpopstate = e => {
//     const info = e.state;
//     let parser = new DOMParser();
//     parser = parser.parseFromString(info, 'text/html');
//     let profile_data = parser.querySelector('#profiledata');
//     document.querySelector('#profilepage').innerHTML = profile_data;
// };


function load_page(name) {
    const request = new XMLHttpRequest();
    request.open('GET', '/myaccount/profile/'+ name);
    request.onload = () => {
        const response = request.responseText;
        let parser = new DOMParser();
        parser = parser.parseFromString(response, 'text/html');
        let profiledata = parser.querySelector('#profiledata');
        document.querySelector('#profilepage').innerHTML = profiledata.outerHTML;
        history.pushState({'text': response}, name, '/myaccount/profile/'+ name)
    };
    request.send()
}