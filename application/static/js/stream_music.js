//import axios from "axios";

const options = {
  method: 'GET',
  url: 'https://deezerdevs-deezer.p.rapidapi.com/search',
  params: {q: 'eminem'},
  headers: {
    'x-rapidapi-key': 'd765230cffmshfbcb0be68220569p1887a6jsn21942133f34b',
    'x-rapidapi-host': 'deezerdevs-deezer.p.rapidapi.com'
  }
};

axios.request(options).then(function (response) {
	console.log(response.data.data);

	const list = document.querySelector('.mdc-list-item__text');

	response.data.data.forEach(function(item) {
	    console.log(item.title)
        const music_list = document.getElementById('music_list')
        music_list.innerHTML += `     <li class='mdc-list-item' tabindex="0">
                                       <span class=mdc-list-item__ripple></span>
                                       <span class='mdc-list-item__text' >
                                         <span class='mdc-list-item__primary-text'>${item.title}</span>
                                         <span class='mdc-list-item__secondary-text'>Mali music</span>
                                       </span>
                                     </li> `

	})


}).catch(function (error) {
	console.error(error);
});