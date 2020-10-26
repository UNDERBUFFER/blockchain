
const TRANSACTION_URL = `${window.location.origin}${window.location.pathname}`
const MAIN_DIV = document.getElementById('main')

function getJsonResponse() {
    let receivedObject = JSON.parse( MAIN_DIV.innerText )
    setStatus(receivedObject)
    const ready = {
        processed: receivedObject.processed,
        checked: receivedObject.checked
    }
    delete receivedObject.processed
    delete receivedObject.checked

    MAIN_DIV.innerText = JSON.stringify( receivedObject, undefined, 2 )
    return ready
}


function setStatus(jsonObject) {
    const status = document.getElementById('process')
    if (!status) return true
    if (jsonObject.processed === true && jsonObject.checked === false)
        status.className = 'lds-dual-ring'
    else if (jsonObject.processed === false && jsonObject.checked === true)
        status.className = 'good-status'
    else
        status.className = 'bad-status'

    return true
}


function loop() {
    fetch(`${TRANSACTION_URL}?type=json`).then(response => {
        return response.json()
    }).then(receivedObject => {
        console.log(receivedObject)
        if (!receivedObject.processed) {
            setStatus(receivedObject)
            setTimeout(() => {
                document.location.reload(true)
                loop(receivedObject)
            }, 60000)
        }
        else setTimeout(() => {
                loop(receivedObject)
            }, 10000)
        
    })
}


getJsonResponse()
loop()