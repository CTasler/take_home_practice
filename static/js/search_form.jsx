function Result(props) {
    const reserveHandler = (event) => {
        const date = document.querySelector('#date').value;
        if (! date) {
            alert('A date must be selected to make a reservation')
        } else {
            fetch('/get-username')
            .then((response) => response.json())
            .then((responseJson) => {
                const username = responseJson.username;
                if (username) {
                    const reservation = {
                        date: date,
                        time: props.time, 
                    }
        
                    fetch('/create-reservation', {
                        method: 'POST',
                        body: JSON.stringify(reservation),
                        credentials: 'include',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    }) 
                    .then((response) => response.json())
                    .then((responseJson) => {
                        if (responseJson.result == "successful") {
                            alert('reservation was created')
                        }
                    })
                } else {
                    alert('you must be logged in to make a reservation')
                }
            })
        }
    }

    return (
        <div>
            <div className="flex-cont">
                <p>{props.time}</p>
                <button onClick={reserveHandler}>Reserve</button>
            </div>
        </div>
    )
}


function SearchForm() {
    const [data, setData] = React.useState({})

    const changeHandler = (event) => {
        setData({...data, [event.target.name]: event.target.value});
    };

    const [times, setTimes] = React.useState([])

    const submitHandler = (event) => {
        event.preventDefault();
        console.log(data)
        const start = document.querySelector('#start').value
        const end = document.querySelector('#end').value
        
        if (start > end) {
            alert('The start time must be before the end time.')
        } else {
            const date = document.querySelector('#date').value;
            fetch(`/check-reservations?date=${date}`)
            .then((response) => response.json())
            .then((responseJson) => {
                console.log(responseJson)
                console.log(responseJson.data)
                if (responseJson.data == "not_available") {
                    alert('You have already made a reservation on that day. Please choose a different date.')
                } else {
                    fetch('/results', {
                        method: 'POST',
                        body: JSON.stringify(data),
                        credentials: 'include',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    }) 
                    .then((response) => response.json())
                    .then((responseJson) => {
                        const resTimes = responseJson.data;
                        console.log(resTimes)
                        if (resTimes.length == 0) {
                            alert('There are no results matching that search.')
                        } else {
                            setTimes(resTimes)
                        }
                    })
                }
            })   
        };
    }


    const results = [];
    for (const currentTime of times) {
        results.push(
            <Result
            time={currentTime}/>
        )
    }

    return (
        <div>
            <div>
                <form>
                    <label htmlFor="date">Date: </label>
                    <input id="date" type="date" name="date" onChange={changeHandler}/>
                    <label htmlFor="start-time">Start Time: </label>
                    <input id="start" type="time" name="start-time" onChange={changeHandler}/>
                    <label htmlFor="end-time">End Time: </label>
                    <input id="end" type="time" name="end-time" onChange={changeHandler}/>
                    <input type="submit" onClick={submitHandler}></input>
                </form>
            </div>
            <div>
              {results}
            </div>
        </div>
    )
}


ReactDOM.render(<SearchForm />, 
document.querySelector('#search-form-cont'));



