
const mainDiv = document.getElementById('main')
const status = document.getElementsByClassName('lds-dual-ring')[0]


let receivedObject = JSON.parse( mainDiv.innerText )[0]['fields']


if (receivedObject.processed === true && receivedObject.checked === false)
    status.className = 'lds-dual-ring'
else if (receivedObject.processed === false && receivedObject.checked === true)
    status.className = 'good-status'
else
    status.className = 'bad-status'

delete receivedObject.processed
delete receivedObject.checked


mainDiv.innerText = JSON.stringify( receivedObject, undefined, 2 )
