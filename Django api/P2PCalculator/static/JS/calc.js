var commissionEnabled = true;
var numDealsOpen = false;
var startSum = 1000



$(".item__switch-commission").click(function (){

    var comissions = $(".comissions");
    if (commissionEnabled == false)
    {
        commissionEnabled = true;
        $(this).addClass("switch--active");
        
        comissions.show();
    }
    else {
        commissionEnabled = false;
        $(this).removeClass("switch--active");

        comissions.hide();
        
    }
})

$(".item__switch-view-spread").click(function() {
    var buf = $(this).find(".switch-view-spread__label").html();
    buf = buf.replace(/\s/g, '');

    var sum = $(".trans-amount");
    var profit = $(".profit_fiat");
    
    if (buf == "₽")
    {
        $(this).addClass("switch--percent");

        $(this).find(".switch-view-spread__label").html("%");

        sum.hide();
        profit.hide();
        
    }
    else {
        $(this).removeClass("switch--percent");

        $(this).find(".switch-view-spread__label").html("₽");

        sum.show();
        profit.show();
    }
})

$(".num_deals .item__field").click(function() {
    if (numDealsOpen == false)
    {
        numDealsOpen = true;
        $(this).find(".dropdown__num-deals").slideDown(200);

        $(this).find(".field__select-arrow").css({"transform" : "rotate(-90deg)"})
    }
    else {
        numDealsOpen = false;
        $(this).find(".dropdown__num-deals").slideUp(200);

        $(this).find(".field__select-arrow").css({"transform" : "rotate(90deg)"})

    }

    
})

$(".dropdown__num-deals .dropdown__item").click(function(event) {
    
    $(".dropdown__num-deals").slideUp(200);
    $(".num_deals").find(".field__select-arrow").css({"transform" : "rotate(90deg)"})

    var buf = $(this).html();
    var buf = buf.replace(/[^+\d]/g, '')
    $(".num_deals .field__label").html(buf);

    var anothers = $(".anothers_input");

    anothers.html("");

    var code = "";
    if (buf > 2 && buf <= 5)
    {
        for (var i = 0; i < buf - 2; i++)
        {
            code += '<div class="another_input"><div class="header">Промежуток</div><input type="number" class="another_price" id="another' + i + '"></div>';
        }
    }

    anothers.html(code);

    var comissions = $(".comissions");

    comissions.html("");

    code = '<div class="comission_input"><div class="header">Комиссия %</div><input type="number" value = "0.00" id="comission_first"></div>';
    
    if (buf > 2 && buf <= 5)
    {
        for (var i = 0; i < buf - 2; i++)
        {
            code += '<div class="comission_input"><div class="header">Комиссия %</div><input type="number" value = "0.00" id="comission_' +  i + '"></div>';
        }
    }

    code += '<div class="comission_input"><div class="header">Комиссия %</div><input type="number" value = "0.00" id="comission_last"></div>';

    comissions.html(code);
    
    var profit = $(".profit_fiat");
    profit.html("");

    code = '<div class="profit_fiat_input"><div class="header">Кол-во</div><input type="number" id="profit_first"  readonly></div>';

    if (buf > 2 && buf <= 5)
    {
        for (var i = 0; i < buf - 2; i++)
        {
            code += '<div class="profit_fiat_input"><div class="header">Кол-во</div><input type="number" id="profit_' + i +'"  readonly></div>';
        }
    }

    code += '<div class="profit_fiat_input"><div class="header">Кол-во</div><input type="number" id="profit_two"  readonly></div>';
    code += '<div class="profit_fiat_input"><div class="header">Прибыль</div><input type="number" id="profit_last"  readonly></div>';

    profit.html(code);

    $(".spread_percent").val("");


    numDealsOpen = false;
    event.stopPropagation();
})


function count() {
    var array_calc = []

    array_calc[0] = document.querySelector(".buy_price").value;
    var num_deals = document.querySelector(".num_deals .field__label").textContent;

    if (num_deals > 2 && num_deals <= 5)
    {
        for (i = 0; i < num_deals-2; i++)
        {
            array_calc[i+1] = document.querySelector("#another" + i).value;
        }

    }

    array_calc.push(document.querySelector(".sell_price").value);

    var array_com = []

    array_com[0] = document.querySelector("#comission_first").value;

    if (num_deals > 2 && num_deals <= 5)
    {
        for (var i = 0; i < num_deals-2; i++)
        {
            array_com[i+1] = document.querySelector("#comission_" + i).value;
        }

    }

    array_com.push(document.querySelector("#comission_last").value);


    var flat = true;

    for (var i = 0; i < array_calc.length; i++)
    {
        if (array_calc[i] == "")
        {
            flat = false;
            break;
        }
    }

    var com_check = commissionEnabled;

    var spread_view_check = $(".item__switch-view-spread .switch-view-spread__label").html();
    spread_view_check = spread_view_check.replace(/\s/g, '');
    

    var profit_check = document.querySelector(".sum_input").value;

    if (com_check == true)
    {
        for (var i = 0; i < array_com.length; i++)
        {
            if (array_com[i] == "")
            {
                array_com[i] = 0;
            }
        }
    }

    if (profit_check == "")
    {
        flat = false;
    }

    if (flat != false)
    {
        if (spread_view_check != "%")
        {
            startSum = profit_check;
        }

        var result = 0;

        for (var i = 0; i < array_calc.length; i++)
        {
            if (i == 0)
            {
                result = startSum / array_calc[i];
                
                if (com_check == true)
                {
                    result = result * (100 - array_com[i])/100;
                }
                if (spread_view_check != "%")
                {
                    document.querySelector("#profit_first").value = result.toFixed(2);
                }
            }
            else if (i == array_calc.length - 1)
            {
                result = result * array_calc[i];

                if (com_check == true)
                {
                    result = result * (100 - array_com[i])/100;
                }

                if (spread_view_check != "%")
                {
                    document.querySelector("#profit_two").value = result.toFixed(2);

                }
            }
            else if (i == array_calc.length-1)
            {
                console.log(array_calc[i]);

                result = result * array_calc[i];

                if (com_check == true)
                {
                    result = result * (100 - array_com[i])/100;
                }

                if (spread_view_check != "%")
                {
                    document.querySelector("#profit_two").value = result.toFixed(2);
                }
            }

            else {
                result = result / array_calc[i];

                if (spread_view_check != "%")
                {
                    document.querySelector("#profit_" + (i-1)).value = result.toFixed(2);
                }

                if (com_check == true)
                {
                    result = result * (100 - array_com[i])/100;
                }
            }
        }

        result = result - startSum;

        document.querySelector(".spread_percent").value = (result / startSum * 100).toFixed(2) + " %";

        if (spread_view_check != "%")
        {
            document.querySelector("#profit_last").value = result.toFixed(2);
        }
    }


}