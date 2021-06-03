var search = document.getElementById('search');
var userSearch_template = document.getElementById('userSerachTemplate')
var userSearchTop_div = document.getElementById('userSearchTop_div')

const userResultList = []

search.addEventListener('input', queryDb)

function queryDb(e){
    fetch(`/loadsearch?str=${e.target.value}`, {
        method: 'GET',
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then(function(response) {
        if (response.status !== 200){
            console.log(response.status)
        }
        response.json().then(function(data) {
            if (data){
                data.msg.users.forEach( user => {
                    if (userResultList.includes(user.id)){
                        console.log('already search this user')
                    }
                    else {
                        userResultList.push(user.id)
                        let template_clone = userSearch_template.content.cloneNode(true);
                        template_clone.querySelector('#searchPhone').innerHTML = user.phone;
                        template_clone.querySelector('#searchUser').innerHTML = user.username;
                        template_clone.querySelector('#userlistMedia').src = user.profile_px

                        userSearchTop_div.appendChild(template_clone);
                    // userSearchTop_div.innerHTML = template_clone;
                    }

                })
            }else if (data = {}) {
                console.log('nothing')
            }
            else {
                console.log('nothing')
                }
        })
    })
}