function Reservation(props) {
    return (
        <div className="flex-cont border border-success">
            <p className="user-dates">{props.date} from {props.time}</p>
        </div>
    )
}

function Reservations() {
    const [data, setData] = React.useState([])

    React.useEffect(() => {
        fetch('/get-user-reservations')
        .then((response) => response.json())
        .then((responseJson) => {
            // console.log(responseJson.user_reservs)
            setData(responseJson.user_reservs)
        })
    }, []);
    // console.log(data.date)
    // console.log(data.time)
    const reservs = [];
    for (const currentData of data) {
        reservs.push(
            <Reservation
            date={currentData.date}
            time={currentData.time}
            />
        );
    }



    // for (const currentData of data) {
    //     reservs.push(
    //         <Reservation 
    //         date={currentData.date}
    //         time={currentData.time}/>
    //     );
    // }
    return (
        <div>
            {reservs}
        </div>
    )
}

ReactDOM.render(<Reservations />, 
document.querySelector('#user-res-cont'));