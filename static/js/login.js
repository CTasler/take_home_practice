const button = document.querySelector('#login-btn')

const submitHandler = (event) => {
    event.preventDefault();
    data = {
        username: document.querySelector('#username').value
    }
    if (data.username) {
        console.log(data)
        
        fetch('/process-login', {
            method: 'POST', 
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then((response) => window.location.replace(response.url))

    } else {
        alert("Username is required")
    }
    
}

button.addEventListener('click', submitHandler);