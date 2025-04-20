const port = document.getElementById('web_server_port').value;
const backendUrl = `http://localhost:${port}`;

async function post(endpoint, data){
    const url = `${backendUrl}/${endpoint}`;
    return await axios.post(url, data, headers={
        'Content-Type': 'application/json'
    });
}

async function sseHandler(event_source){
    const eventSource = new EventSource(event_source);

    eventSource.addEventListener("orderReceived", (event) => {
        showSuccessMessage(event.data);
    });

    eventSource.addEventListener("reqPayment", (event) => {
        showWaitingMessage(event.data);
    });

    eventSource.addEventListener("coffeeReady", (event) => {
        showSuccessMessage(event.data);
        eventSource.close();
        clearForm();
    });

    eventSource.onerror = (event) => {
        showErrorMessage("Sorry - we have some errors processing your coffee order");
        eventSource.close();;
        clearForm()
    }
}

async function showSuccessMessage(str_message){
    const element = document.getElementById('msg-container');

    element.innerHTML = str_message;
    element.classList.remove("hide", "error", "waiting");
    element.classList.add("show");
}

async function showErrorMessage(str_message){
    const element = document.getElementById('msg-container');

    element.innerHTML = str_message;
    element.classList.remove("hide", "success", "waiting");
    element.classList.add("error", "show");
}

async function showWaitingMessage(str_message){
    const element = document.getElementById('msg-container');

    element.innerHTML = str_message;
    element.classList.remove("hide", "error", "success");
    element.classList.add("waiting", "show");
}


function disableOrderForm(){
    document.querySelectorAll('.order-form *').forEach(el => el.disabled = true);
}

function clearForm(){
   setTimeout(() => {
        const name = document.getElementById("name");
        name.value = '';
        name.disabled = false;

        const element = document.getElementById('msg-container');
        element.innerHTML = '';
        element.classList.remove("waiting", "show", "error", "success");
        element.classList.add("hide");
   }, 5000);
}

async function orderCoffee() {
    const endpoint =  "coffee/order";
    const name = document.getElementById("name");
    const qty =  document.getElementById("quantity");

    const order = {
        "customer_name": name.value,
        "quantity":  qty.value
    };

    try{
        const {data, status} = await post(endpoint, order);
        disableOrderForm();
        sseHandler(data.event_source);
    }catch(err){
        showErrorMessage("Apologises - we cant accept your order rigth now");
    }
}