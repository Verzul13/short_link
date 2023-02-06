function get_form_data(form_id = null){
    var form = event.target||event.srcElement;
    event.preventDefault();
    form = form.parentNode;
    let url = form.getAttribute("action");
    var data = new FormData(form);
    data = serialize_form_data(data);
    return {"data":data,"url":url}
}

function serialize_form_data(el_form){
    var answer=[];
    for(let [name, value] of el_form) {
        answer.push(name+"="+value);
    }
    answer = answer.join("&");
    return answer;
}

async function send_request(url, method="GET", body=null, headers=null, response_type="json"){
    headers = headers?headers:{}
    body = body?body:{}
    const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    if(csrftoken){
        body['X-CSRFToken'] = csrftoken,
        headers['X-CSRFToken'] = csrftoken
    }    
    let response = {
        "status" : null,
        "data" : null
    }
    headers['Accept'] = 'application/json', 
    headers['Content-Type'] = 'application/json'    
    if(method == "GET" && body){
        var get_params = new URLSearchParams(body).toString();
        url += "?" + get_params
        body = null
    }
    let request_body = {
        method : method
    }
    if(headers){
        Object.defineProperty(request_body, 'headers', {
            __proto__: null, // нет унаследованных свойств
            value: headers
          });
    }
    if(method!="GET" && body){
        Object.defineProperty(request_body, 'body', {
            __proto__: null, // нет унаследованных свойств
            value: JSON.stringify(body)
          });
    }

    let request_response = await fetch(url,request_body)
    if(request_response.ok){
        response['status'] = request_response.status
        if(response_type == "json"){
            response['data'] = await request_response.json();
        }else if(response_type == "blob"){
            response['data'] = await request_response.blob();
        }else{
            response['data'] = await request_response.text();
        }
    }else{
        response['status'] = request_response.response
        response['data'] = request_response.text()
    }
    return response
}

function get_template_form_data(){
    var form =event.target||event.srcElement;
    event.preventDefault();
    while (true) {
        if(form.tagName == "FORM"){
            break;
        }else{
            form = form.parentNode;
        }
    }
    let url = form.getAttribute("action");
    var data = new FormData(form);
    let end_func =  form.getAttribute("data-end");
    return {"id": form.id,"data" : data,"url" : url, "method" : form.method, "end_func" : end_func}
}

function get_template_form_data(){
    var form =event.target||event.srcElement;
    event.preventDefault();
    while (true) {
        if(form.tagName == "FORM"){
            break;
        }else{
            form = form.parentNode;
        }
    }
    let url = form.getAttribute("action");
    var data = new FormData(form);
    let end_func =  form.getAttribute("data-end");
    return {"id": form.id,"data" : data,"url" : url, "method" : form.method, "end_func" : end_func}
}

function send_form_ajax() {
    let form_data = get_template_form_data();
    clear_form_errors();
    setTimeout(function(){
        var xhr = new XMLHttpRequest();
        const state_changed = () => {
            if (xhr.readyState === 4){   //if complete
                console.log("status", xhr.status)
                console.log("responseText", xhr.responseText)
                response = {
                    "status_code": xhr.status,
                    "data": JSON.parse(xhr.responseText)
                }
                if(form_data['end_func']){
                    form_functions[form_data['end_func']](response, form_data)
                }
            } ;
        }
        xhr.onreadystatechange=state_changed
            
        xhr.open(form_data['method'], form_data['url'], true);
        xhr.send(form_data['data']);
    });
}

function clear_form_errors(){
    for(let i=0;i<document.getElementsByClassName("errortext").length;i++){
        document.getElementsByClassName("errortext")[i].innerHTML = "";
    }
}

function clear_form_errors(){
    for(let i=0;i<document.getElementsByClassName("errortext").length;i++){
        document.getElementsByClassName("errortext")[i].innerHTML = "";
    }
}

function clear_form_fields(form_id){
    document.getElementById(form_id).reset();
}

function show_pb() {
    document.getElementById("loader_cont").style.display = "";
}

function hide_pb() {
    document.getElementById("loader_cont").style.display = "none";
}

function show_conteiner(cont_name){
    /***
     *  Делает видимым выбранный контейнер, остальные скрывает
     */
    for(let i=0;i<document.getElementsByClassName("conteiner").length;i++){
        if(document.getElementsByClassName("conteiner")[i].id == cont_name){
            document.getElementsByClassName("conteiner")[i].style.display = "";
        }else{
            document.getElementsByClassName("conteiner")[i].style.display = "none";
        }
    }
}

function show_alert_block(el_id,err_mes, block_type="danger"){
    document.getElementById(el_id).innerHTML=err_mes;
    document.getElementById(el_id).style.display="";
    document.getElementById(el_id).setAttribute("class","alert alert-"+block_type);
    setTimeout(function(){
        document.getElementById(el_id).style.display="none";
    },2000);
}

function logout(){
    /***
     *  Функция выхода из сессии
     */
     delCookie("X-Token")
     location.href = "/auth/signin"
}

function main_alert(alert_text, alert_class){
    document.getElementById("main_alert").innerHTML = alert_text;
    document.getElementById("main_alert").classList.add("alert-"+alert_class);
    document.getElementById("main_alert").style.display = "";
    setTimeout(function(){
        document.getElementById("main_alert").style.display = "none";
        document.getElementById("main_alert").classList.remove("alert-"+alert_class);
        document.getElementById("main_alert").innerHTML = "";
    },2000);
}

function search_in_table(){
    let el = event.target||event.srcElement;
    if(event.keyCode == 13){
        var search_value = el.value.toLowerCase();
        var column_index = Array.prototype.indexOf.call(el.parentNode.parentNode.children, el.parentNode);
        //ищем tbody и его tr
        let tbody_rows = el.parentNode.parentNode.parentNode.parentNode.children;
        for(let i = 0;i < tbody_rows.length; i++){
            if(tbody_rows[i].tagName == "TBODY"){
                tbody_rows = tbody_rows[i].children;
                break;
            }
        }
        //находим необходимые нам строки
        for(let i=0; i < tbody_rows.length; i++){
            if(el.value.replaceAll(" ","").length > 0){
                let field_cont = tbody_rows[i].children[column_index].innerHTML.toLowerCase();
                let display_value = "none";
                if(field_cont.includes(search_value)){
                    display_value = "";
                }
                tbody_rows[i].style.display = display_value;
            }else{
                tbody_rows[i].style.display = "";
            }
            
        }
    }
    
}


function get_option_text_by_value(id, value){
    let el = document.getElementById(id);
    return el.options[el.selectedIndex].text
}

function find_option_by_value(id, value){
    let select_field = document.getElementById(id);
    let el = null;
    for(let i=0; i < select_field.children.length; i++){
        if(select_field.children[i].value == value){
            el = select_field.children[i];
        }
    }
    return el;
}

function clear_filters(){
    for(let i=0;i<document.getElementsByClassName("filtr_fields").length;i++){
        let this_el = document.getElementsByClassName("filtr_fields")[i];
        if(this_el.tagName == "SELECT"){
            this_el.value = '0';
        }else{
            this_el.value="";
        }
    }
    change_per_page();
}

function appendAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

/* Работа с куками */ 

function setCookie(key, value, days=1){
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function delCookie( name ) {
    document.cookie = name+'=; Max-Age=-99999999;';  
  }


//function check_cookie() {    
    //alert(document.cookie)
//}

function setCookie(key, value, days=1){
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = key + "=" + (value || "")  + expires + "; path=/";
}


/* Создание пагинации */

function create_pagination(parentNodeEl, current_page, pag_items, pag_step, web_url, added_url=null){
    let pag_buttons_count = parseInt(Number(pag_items/pag_step))
    if(pag_items%pag_step > 0){
        pag_buttons_count += 1
    }
    if(current_page <= 0){
        current_page = 1
    }
    if(current_page > pag_buttons_count){
        current_page = pag_buttons_count
    }
    web_url += "?page={current_page}&per_page={pag_items}"
    if(added_url != null){
        web_url += "&" + added_url
    }
    let pag_items_data = form_pagination_items(pag_buttons_count, web_url, current_page, pag_step)
    let html_data = {
        "PREVIOUS_LINK": form_web_link(web_url, current_page - 1, pag_step),
        "PREVIOUS_VIS": current_page == 1 ? true : false,
        "NEXT_LINK":form_web_link(web_url, current_page + 1, pag_step),
        "NEXT_VIS": current_page == pag_buttons_count ? true : false,
        "PAG_ITEMS":pag_items_data,
        "CURRENT_PAGE" : current_page
    }
    if(pag_buttons_count > 1){
        draw_pagination(parentNodeEl,html_data)
    }
}

function form_pagination_items(pag_buttons_count, web_url, current_page, pag_step){
    let pag_list = []
    let pag_digits = {
        "text" : "...",
        "weblink" : "#",
        "is_active" : false,
        "disabled" : true
    }
    for(let i=1;i<=pag_buttons_count;i++){
            let pag_list_item = {
                "text" : i,
                "weblink" : form_web_link(web_url, i, pag_step),
                "is_active" : current_page == i ? true: false,
                "disabled" : false
            }
            pag_list.push(pag_list_item)
        }
    if(pag_buttons_count > 10){
        let new_pag_list
        if(current_page < 4){
            new_pag_list = pag_list.slice(0,4)
            new_pag_list.push(pag_digits)
            new_pag_list.push(pag_list.pop())
        }else if(current_page > pag_buttons_count - 4){
            new_pag_list = [pag_list[0]]
            new_pag_list.push(pag_digits)
            new_pag_list = new_pag_list.concat(pag_list.slice(pag_buttons_count - 3, pag_buttons_count))
        }else{
            new_pag_list = [pag_list[0]]
            new_pag_list.push(pag_digits)
            new_pag_list = new_pag_list.concat(pag_list.slice(current_page - 2, current_page + 1))
            new_pag_list.push(pag_digits)
            new_pag_list.push(pag_list.pop())
        }
        pag_list = new_pag_list
    }
    return pag_list
}


function draw_pagination(parentNodeEl, html_data){
    let ul = document.createElement("ul")
    ul.classList.add("pagination")
    draw_pagination_button(ul, html_data['PREVIOUS_LINK'], "Пред.", false, html_data['PREVIOUS_VIS'])
    html_data["PAG_ITEMS"].forEach(function(item,i){
        draw_pagination_button(ul, item['weblink'], item['text'], item['is_active'], item['disabled'])
    })
    draw_pagination_button(ul, html_data['NEXT_LINK'], "След.", false, html_data['NEXT_VIS'])
    parentNodeEl.append(ul)
}

function form_web_link(web_url, web_page, web_step){
    web_url = web_url.replace("{current_page}", web_page)
    web_url = web_url.replace("{pag_items}", web_step)
    return web_url
}

function draw_pagination_button(parentNodeUl, weblink="", btn_text="", is_active=false, disabled=false){
    let btn = document.createElement("li");
    btn.classList.add("page-item")
    if(disabled){
        btn.classList.add("disabled")
    }else if(is_active){
        btn.classList.add("active")
    }
    let btn_link = document.createElement("a");
    btn_link.classList.add("page-link")
    btn_link.href = weblink
    btn_link.innerHTML = btn_text
    btn.appendChild(btn_link)
    parentNodeUl.appendChild(btn)
}

/* Маски для инпутов */

function phone_mask(el){
    IMask(el, {
      mask: '{7}(000)000-00-00'
    });
}

function validateEmail(email){     
    var re = /\S+@\S+\.\S+/
    return re.test(email)
}

function validateName(name){     
    var re = /^[А-Яа-я\s]{1,}[\.]{0,1}[А-Яа-я\s]{0,}$/
    return re.test(name)
}

function validatePhone(phone){     
    var re = /[78][-\(]?\d{3}\)\d{3}-?\d{2}-?\d{2}/
    return re.test(phone)
}

function validatePassword(password){     
    var re = /^(?=.*\d)\w{6,20}$/m 
    return re.test(password)
}

function sms_mask_settings_phone(el){
    IMask(el, {
      mask: '0000'
    });
}


/* метод для подсказок гео */
var advice_waiting = false;
var advice_prev_value = null;

function make_input_address_advisor(el, list_name, link){
    el.setAttribute("list", list_name)
    el.setAttribute("link", link)
    el.addEventListener("keyup", get_advise);
    //el.addEventListener("input", geo_chosen_func)
    let datalist_index = Array.prototype.slice.call(el.parentNode.children).indexOf( el ) + 1;
    let datalist = document.createElement("datalist")
    datalist.style.width = el.offsetWidth + "px"
    datalist.id = list_name
    let latitude = document.createElement("input")
    latitude.id = list_name + "_latitude"
    latitude.type= "hidden"
    let longitude = document.createElement("input")
    longitude.id = list_name + "_longitude"
    longitude.type= "hidden"
    let geo_chosen = document.createElement("input")
    geo_chosen.id = list_name + "_geo_chosen"
    geo_chosen.type= "hidden"
    geo_chosen.value = "0"
    if(datalist_index == el.parentNode.children.length ){
        el.parentNode.appendChild(datalist)
        el.parentNode.appendChild(latitude)
        el.parentNode.appendChild(longitude)
        el.parentNode.appendChild(geo_chosen)
    }else{
        el.parentNode.insertBefore(el.parentNode.children[datalist_index], datalist)
        el.parentNode.insertBefore(el.parentNode.children[datalist_index + 1], latitude)
        el.parentNode.insertBefore(el.parentNode.children[datalist_index + 2], longitude)
        el.parentNode.insertBefore(el.parentNode.children[datalist_index + 3], geo_chosen)
    }
}

async function get_advise(){
    //console.log("event key code", event.keyCode)
    let this_code = event.keyCode
    let el = event.target || event.srcElement;
    if(el.value.length >= 4 && !advice_waiting && advice_prev_value!=el.value && event.keyCode != undefined){
        body = {
            "address" : el.value
        }
        advice_prev_value = el.value
        advice_waiting = true
        let answer = await send_request("/api/v2/common/geo_advice", "GET", body)
        let datalist = document.getElementById(el.getAttribute("list"))
        datalist.innerHTML = "";
        if(answer.status){
            if(answer.data.data.length == 0){
                let option = document.createElement("option")
                option.innerHTML = "<i>Нет подходящих адресов</i>"
                datalist.appendChild(option)
            }else{
                answer.data.data.forEach(function(item, i){
                    let option = document.createElement("option")
                    option.innerHTML = item['full_address']
                    option.setAttribute("latitude", item['latitude'])
                    option.setAttribute("longitude", item['longitude'])
                    datalist.appendChild(option)
                })
            }
        }else{
            let option = document.createElement("option")
            option.innerHTML = "<i>Севрер не доступен</i>"
            datalist.appendChild(option)
        }
        setTimeout(function(){
            advice_waiting = false
        }, 1000)
    }
    if(this_code === undefined){
        geo_chosen_func(el)
    }
}


function geo_chosen_func(el){
    advice_waiting = true
    advice_prev_value = el.value
    let datalist_name = el.getAttribute("list");
    let latitude, longitude
    for(let i=0;i<document.getElementById(datalist_name).children.length;i++){
        if(document.getElementById(datalist_name).children[i].innerHTML == el.value){
            latitude = document.getElementById(datalist_name).children[i].getAttribute("latitude")
            longitude = document.getElementById(datalist_name).children[i].getAttribute("longitude")
            break
        }
    }
    document.getElementById(datalist_name + "_latitude").value = latitude
    document.getElementById(datalist_name + "_longitude").value = longitude
    document.getElementById(datalist_name + "_geo_chosen").value = 1
    document.getElementById(datalist_name + "_latitude").name = "latitude"
    document.getElementById(datalist_name + "_longitude").name = "longitude"
    setTimeout(function(){
        advice_waiting = false
    }, 1000)
}


function close_toast(){
    let el =event.target ||event.SrcElement;
    while(true){
        if(el.tagName == "DIV" && el.getAttribute("role") == "alert"){
            break;
        }else{
            el = el.parentNode;
        }
    }
    el.style.display = "none"
}

function element_alert(element_id,alert_text, alert_class){
    document.getElementById(element_id).innerHTML = alert_text;
    document.getElementById(element_id).classList.add("alert-"+alert_class);
    document.getElementById(element_id).style.display = "";
    setTimeout(function(){
        document.getElementById(element_id).style.display = "none";
        document.getElementById(element_id).classList.remove("alert-"+alert_class);
        document.getElementById(element_id).innerHTML = "";
    },2000);
}

function getClickButton(){
    let btn = event.target || event.srcElement
    if (btn.tagName == "I"){
    btn = btn.parentNode
    }
    return btn
}

/* функция для валидного отображения телефона */
function showValidPhone(id) {
    const settings_phone = document.getElementById(id)    
    const phone_string = String(settings_phone.innerHTML.replace(/\s/g,'')) // переводим в строку, убираем пробелы
    const valid_phone = phone_string.replace(/^(\d)(\d{3})(\d{3})(\d{2})(\d{2})$/, '+$1($2)$3-$4-$5')
    settings_phone.innerHTML = valid_phone
}
