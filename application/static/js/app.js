var scroller  = document.getElementById('scroller');
var template = document.getElementById('post_template');
var sentinel = document.getElementById('sentinel');

var counter = 0;


function loadTriets() {
    fetch(`/loadTriets?c=${counter}`, {
        method: 'GET',
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then(function(response) {
        if(response.status !== 200) {
            alert(response.status)
        }
        response.json().then(function(data) {
            if (!data.msg.length){
                sentinel.innerHTML = "nothing more 😜";
                return;
            }

            data.msg.forEach(item => {
                let template_clone = template.content.cloneNode(true);
                template_clone.querySelector('#trietMedia').src = item.picture
                // sentinel.innerHTML = item;
                // console.log(item.picture)

                scroller.appendChild(template_clone);
                counter += 1;
                // console.log(counter)

            })
        })
    })
    .catch(function(error) {
        alert('fetch error')
    })
}

var intersectionObserver  = new IntersectionObserver(entries => {
    if (entries[0].intersectionRatio <= 0) {
        return;
      }
    
      // Call the loadItems function
      loadTriets();
})

intersectionObserver.observe(sentinel);