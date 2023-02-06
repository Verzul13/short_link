window.addEventListener("load", page_load)


let form_link_shortener_sended = (response) => {
    if (response['status_code'] != 200) {
        let error1 = Object.keys(response['data'])[0]
        let error2 = Object.values(response['data'])[0]
        document.getElementById("alert_link_shortener_form").innerHTML = `${error1}: ${error2}`
        document.getElementById("alert_link_shortener_form").classList.add("alert-danger")
        document.getElementById("alert_link_shortener_form").style.display = ""
        setTimeout(function () {
            document.getElementById("alert_link_shortener_form").style.display = "none"
            document.getElementById("alert_link_shortener_form").classList.remove("alert-danger")
            document.getElementById("alert_link_shortener_form").innerHTML = ""
        }, 2000)
    } else {
        document.getElementById("link_shortener_form").reset()
        get_short_link()
    }
}

var form_functions = {
    "link_shortener": form_link_shortener_sended
}


var current_page = 1


async function page_load() {
    await get_short_link()
}

async function get_short_link() {
    let table_body = document.getElementById("table_body")
    let pagination_container = document.getElementById("pagination_container")
    let short_links = null
    short_links = await request_get_short_link(current_page)
    if (short_links.status == 200) {
        if (short_links.data.count == 0) {
            table_body.innerHTML = gettext("You have no orders yet")
            return
        }
        let pagination = builder_short_link_pagination_html(short_links.data, "select_page")
        let short_links_html = ''
        short_links.data.links.forEach(function (item) {
            let short_links_html_el = builder_link_row_html(item)
            short_links_html += short_links_html_el
        })
        table_body.innerHTML = short_links_html
        pagination_container.innerHTML = pagination
    } else {
        table_body.innerHTML = gettext("Server Error!")
    }
}
function builder_link_row_html(short_links, hide = false) {
    let short_links_html = `
        <tr> 
            <td>${short_links.long_url}</td>
            <td>${short_links.subpart}</td>
            <td>${short_links.full_url}</td>
        </tr>
    `
    return short_links_html
}

function builder_short_link_pagination_html(data, el_function = null) {
    let pagination_html = ""
    if (data.count <= 10) {
        return pagination_html
    }
    let pages_count = data.count / 10
    if (data.count % 10 > 0) {
        pages_count += 1
    }
    pagination_html = '<nav aria-label="..."><ul class="pagination">'
    let btn_function = el_function ? ` onclick="${el_function}()"` : ''
    if (pages_count <= 10) {
        for (let i = 1; i <= pages_count; i++) {
            let active = i == current_page ? " active" : ""
            pagination_html += `<li data-page="${i}" class="page-item${active}"${btn_function}><a class="page-link" href="#">${i}</a></li>`
        }
    } else {
        if (current_page <= 3 || current_page >= pages_count - 2) {
            for (let i = 1; i <= 4; i++) {
                let active = i == current_page ? " active" : ""
                pagination_html += `<li data-page="${i}" class="page-item${active}"${btn_function}><a class="page-link" href="#">${i}</a></li>`
            }
            pagination_html += `<li class="page-item"><a class="page-link" href="#">...</a></li>`
            for (let i = pages_count - 3; i <= pages_count; i++) {
                let active = i == current_page ? " active" : ""
                pagination_html += `<li data-page="${i}" class="page-item${active}"${btn_function}><a class="page-link" href="#">${i}</a></li>`
            }
        } else {
            pagination_html += `<li data-page="1" class="page-item"${btn_function}><a class="page-link" href="#">1</a></li>`
            pagination_html += `<li class="page-item"><a class="page-link" href="#">...</a></li>`
            for (let i = current_page - 1; i <= current_page + 1; i++) {
                let active = i == current_page ? " active" : ""
                pagination_html += `<li data-page="${i}" class="page-item${active}"${btn_function}><a class="page-link" href="#">${i}</a></li>`
            }
            pagination_html += `<li class="page-item"><a class="page-link" href="#">...</a></li>`
            pagination_html += `<li data-page="${pages_count}" class="page-item"${btn_function}><a class="page-link" href="#">${pages_count}</a></li>`
        }
    }
    pagination_html += '</ul></nav>'
    return pagination_html
}

async function request_get_short_link(page) {
    headers = {}
    response_type = "json"
    let url = `http://0.0.0.0/api/v1/shortlink/`
    let body = {
        "page": page
    }
    let method = "GET"
    let response = await send_request(url, method, body, headers, response_type)
    return response
}

function select_page() {
    let el = event.target || event.srcElement
    if (el.tagName == "A") {
        el = el.parentNode
    }
    let page = parseInt(el.getAttribute("data-page"))
    if (page != current_page) {
        current_page = page
        get_short_link()
    }
}
