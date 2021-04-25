const  search_input = document.getElementById('search');
const results = document.getElementById('results')

let search_term = '';
let songStream;

const stream = async () => {
	songStream = await fetch(`https://deezerdevs-deezer.p.rapidapi.com/search?q=${search_input.value}`, {
		"method": "GET",
		"headers": {
			"x-rapidapi-key": "0075b86965mshe8fc41794e29a37p1c8cbfjsne74a68c04edb",
			"x-rapidapi-host": "deezerdevs-deezer.p.rapidapi.com"	
		}
	})
	.then(response => response.json())
	.then((data) => {
		console.log(data.data)
		return data.data;
	})
}

const showSongList = async () => {
	results.innerHTML = '';

	await stream();
	
	const ul = document.createElement('ul');
	ul.classList.add('mdc-list', 'mdc-list--two-line');

	songStream
		.forEach(song => {
			const li = document.createElement('li');
			li.classList.add('mdc-list-item')
			li.setAttribute("tabindex", 0)
			li.setAttribute("id", song.id)
			li.addEventListener("click", (e) => {
				console.log(song.link)
				alert(`Sorry you can\'t play this track ${song.title} buy an API  `)
				document.getElementById("musicTray").setAttribute('src', song.link)
			})

			const item__ripple = document.createElement('span')
			item__ripple.classList.add("mdc-list-item__ripple")

			const item__text = document.createElement("span")
			item__text.classList.add("mdc-list-item__text")

			const primary_text = document.createElement('span')
			primary_text.classList.add("mdc-list-item__primary-text")
			primary_text.innerText = song.title;

			const secondary_text = document.createElement('span')
			secondary_text.classList.add("mdc-list-item__secondary-text")
			secondary_text.innerText = song.artist.name

            // const song_name = document.createElement('h3');
            // song_name.innerText = song.title;
			item__text.appendChild(primary_text)
			item__text.appendChild(secondary_text)
			
			li.appendChild(item__ripple)
			li.appendChild(item__text)

			ul.appendChild(li);
		})

		results.appendChild(ul);
}

showSongList();

search_input.addEventListener('input', e => {
	search_term = e.target.value;
	showSongList();
})

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}