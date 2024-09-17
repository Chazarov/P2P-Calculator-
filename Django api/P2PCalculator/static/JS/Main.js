let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#2cab37';

console.log(`tg object is: ${tg}`)



let data_for_sent = "";
let grid_data;
let clickHandlers = [];



let SM_widget;

let buy_role_widget;
let buy_min_amount_widget;

let sell_role_widget;
let sell_min_amount_widget;

let currencies_widget;



let SM;

let buy_role;
let buy_min_amount;

let sell_role;
let sell_min_amount;

let currency;







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



function all_fields_are_filled_in(){

    console.log(`Fields values : ${buy_role !== undefined &&
        buy_min_amount !== undefined &&
        
        sell_role !== undefined &&
        sell_min_amount !== undefined &&
        currency !== undefined}`)

    return buy_role !== undefined &&
    buy_min_amount !== undefined &&
    
    sell_role !== undefined &&
    sell_min_amount !== undefined &&
    currency !== undefined
    
    
}



const buttons = document.querySelectorAll('[id^="pos_btn_"]');
const buttonsArray = Array.from(buttons);
const confirm_button = document.querySelector('#main_confirm_button');

SM_widget = document.querySelector('#SM_select')

buy_role_widget  = document.querySelectorAll('#buy_role input[type="radio"]')
buy_min_amount_widget = document.querySelector('#buy_min_amount')

sell_role_widget = document.querySelectorAll('#sell_role input[type="radio"]')
sell_min_amount_widget = document.querySelector('#sell_min_amount')

currencies_widget  = document.querySelectorAll('#currencies input[type="radio"]');



SM_widget.addEventListener('change', () => {
    SM = SM_widget.value;
    console.log(`Selected Stock marcket: ${SM}`);
});



buy_role_widget.forEach(radio => {
    radio.addEventListener('change', () => {
        buy_role = radio.value;
        console.log(`Selected id: ${buy_role}`);
    }); });
buy_min_amount_widget.addEventListener('change', () => {
    buy_min_amount = buy_min_amount_widget.value;
    console.log(`Selected value: ${buy_min_amount}`);
});



sell_role_widget.forEach(radio => {
    radio.addEventListener('change', () => {
        sell_role = radio.value;
        console.log(`Selected id: ${sell_role}`);
    }); });
sell_min_amount_widget.addEventListener('change', () => {
    sell_min_amount = sell_min_amount_widget.value;
    console.log(`Selected value: ${sell_min_amount}`);
});



currencies_widget.forEach(radio => {
    
    radio.addEventListener('change', () => {
        currency = radio.id
        console.log(`Selected id: ${currency}`);
    });
});





// кнопка подтверждения и обновления данных
confirm_button.addEventListener('click', () => {
    console.log(`${confirm_button.id} clicked!`);

    if(all_fields_are_filled_in())
    {
        const dataToSend = {
                    "SM":SM,
                    "buy":{
                         "trade_role":buy_role,
                         "currency":"RUB",
                         "token":currency,
                         "min_amount":buy_min_amount,
                     },
                    "sell":{
                         "trade_role":sell_role,
                         "currency":"RUB",
                         "token":currency,
                         "min_amount":sell_min_amount,
                    }
                 }

        fetch('api/get_grid/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(dataToSend)
        })
        .then(response => {

            buttonsArray.forEach(button =>{
                button.textContent  = "-"
                button.style.color = 'gray';
                button.removeEventListener('click', emptyButtonClick); 
                button.addEventListener('click', emptyButtonClick());
            })
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);

            grid_data = data["ceils"]
            // Сетка имеет статичный размер 4Х4 , так что длинна массива const = 16
            for (let i = 0; i < grid_data.length; i++) {
                let value = grid_data[i];
                let button = buttonsArray[i];

                if(value["exists"] == 'true'){
                    button.textContent  = value["koef"]

                    koef_float = parseFloat(value["koef"])
                    if(koef_float > 1){
                        button.style.color = 'SpringGreen';
                    }
                    else{
                        button.style.color = 'OrangeRed';
                    }
                        
                    button.removeEventListener('click', clickHandlers[i]); 
                    clickHandlers[i] = createClickHandler(button, value)
                    button.addEventListener('click', clickHandlers[i]);
                }
                else{
                    button.textContent  = "-";
                    button.style.color = 'gray';
                    
                    button.removeEventListener('click', emptyButtonClick); 
                    button.addEventListener('click', emptyButtonClick);
                }
                
                    
            
            }

        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }else{
        console.log("Not all fields")
    }

    
});



function notEmtyButtonClick(button, value){
        console.log(`${button.id} clicked! Inner data: ${value}`);
        
        tg.MainButton.setText(`Получить связку ${value["sell"]["payment"]} => ${value["buy"]["payment"]}`);
        tg.MainButton.show();
        data_for_sent = JSON.stringify(value);
    }



function emptyButtonClick() {
    console.log(`Empty value`);
}


function createClickHandler(button, value){
    return function() {
        notEmtyButtonClick(button, value);
    }
}






Telegram.WebApp.onEvent(`mainButtonClicked`, function(){
    tg.sendData(data_for_sent)
})



