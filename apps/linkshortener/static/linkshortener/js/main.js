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
