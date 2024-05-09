
document.addEventListener('DOMContentLoaded', () => {
    addSearchBar();
    lightNavBar();
    if (window.location.pathname.includes("/location/") && (isAuthenticated)) {
        manageFavorites();
    }
    if (window.location.pathname === '/favorites') {
        addLocationLink();
    }
})


function addSearchBar() {
    //select pre-existent container
    const container = document.querySelector('#searchbar-container');
    
    // Create elements: form
    const form = document.createElement('form');
    form.classList = 'form-inline';

    // Create elements: in-form div
    const inFormDiv = document.createElement('div');
    inFormDiv.classList = 'input-group';

    // Create elements: input
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'form-control';
    input.id = 'searchInput';
    input.placeholder = 'Enter location';

    // Create elements: submit button
    const submit = document.createElement('button');
    submit.classList = 'btn btn-outline-secondary btn-sm';
    submit.innerHTML = 'Search';
    submit.type = 'submit'

    // Nesting elements
    container.append(form);
    form.append(inFormDiv);
    inFormDiv.append(input);
    inFormDiv.append(submit);

    // Form behaviour
    form.onsubmit = () => {
        let target = input.value;
        let url = '/location/' + target;
        window.location.href = url;
        return false;
    }
}


function lightNavBar() {
    // Sets the current page as `active` on the navbar
    let element;
    switch (window.location.pathname) {
        case "/":
            element = document.querySelector('#hp');
            break;
        case "/favorites":
            element = document.querySelector('#fv');
            break;
        case "/login":
            element = document.querySelector('#lg');
            break;
        case "/register":
            element = document.querySelector('#rg');
            break;
        default:
            return 1;
    }
    element.classList.add("active");
}


function manageFavorites() {
    // Select follow button and location
    const button = document.querySelector('#favorite-button')
    const location = document.querySelector('#location-title').innerHTML
    
    // PUT request to add/remove favorite
    button.addEventListener('click', () => {
        fetch(`/check_favorite/${location}`, {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
        })
        .then(() => 1)
        .then(done => {
            if (done === 1) updateButton(button, location)
        })
        .catch(error => console.log('Error: ', error));
    })
    updateButton(button, location)
}


async function updateButton(button, location) {
    fetch(`/check_favorite/${location}`,
        {method: 'GET'})
    .then(response => response.json())
    .then(data => {
        if (!data.favorite) {
            button.innerHTML = 'Add favorite';
            button.classList = 'btn btn-primary btn-sm';
        }
        else {
            button.innerHTML = 'Remove favorite';
            button.classList = 'btn btn-secondary btn-sm';
        }
    })
    .catch(error => console.log('Error: ', error));
}


function addLocationLink() {
    document.querySelectorAll('.favorites').forEach( div => {
        div.classList.add('clickable');
        div.addEventListener('click', () => {
            let target = div.querySelector('#location-name').innerHTML;
            let url = '/location/' + target;
            window.location.href = url;
        });
    })
}