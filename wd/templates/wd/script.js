const Http = new XMLHttpRequest();
const url = 'https://timercheck.io/ugolok-timer';
Http.open("GET", url);
Http.setRequestHeader("Access-Control-Allow-Headers", "Content-Type");
Http.setRequestHeader("Access-Control-Allow-Origin", "http://127.0.0.1:8000");
Http.setRequestHeader("Access-Control-Allow-Methods", "OPTIONS,POST,GET");

Http.send();

Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
}


const url = 'https://timercheck.io/ugolok-timer';
var invocation = new XMLHttpRequest();

function callOtherDomain() {
    if (invocation) {
        invocation.open('GET', url, true);
        invocation.withCredentials = true;
        invocation.send();
        invocation.getResponseHeader()
    }
}
callOtherDomain();