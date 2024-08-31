let tg = window.Telegram.WebApp;

tg.expand();









const confirm_button = document.querySelector("#main_confirm_button")



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



confirm_button.onclick = function() {

    const BBYBIT_T_koef_input = document.querySelector("#BYBIT_T_koef_input_field");
    const BBYBIT_M_koef_input = document.querySelector("#BYBIT_M_koef_input_field");
    const HTX_T_koef_input = document.querySelector("#HTX_T_koef_input_field");
    const HTX_M_koef_input = document.querySelector("#HTX_M_koef_input_field");
    const BITGET_T_koef_input = document.querySelector("#BITGET_T_koef_input_field");
    const BITGET_M_koef_input = document.querySelector("#BITGET_M_koef_input_field");

    const status_field = document.querySelector("#status_field")

    const password_field = document.querySelector("#SPECIAL_PASSWORD_FIELD")

    console.log("confirm button clicked");
    console.log(` ${password_field}   value: ${password_field.value}`)

    const dataToSend = {
        "SPECIAL_PASS":password_field.value,
        "BYBIT":{
            "maker": BBYBIT_M_koef_input.value,
            "taker": BBYBIT_T_koef_input.value,
        },
        "HTX":{
            "maker": HTX_M_koef_input.value,
            "taker": HTX_T_koef_input.value,
        },
        "BITGET":{
            "maker": BITGET_M_koef_input.value,
            "taker": BITGET_T_koef_input.value,
        },
    }

    fetch('Customize/api/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), 
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                const errorMessage = errorData.message;
                status_field.textContent = `Error: ${errorMessage}`;
                throw new Error(errorMessage);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);

        status_field.textContent = "Succes!"
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
