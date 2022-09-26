const new_folder_on = document.querySelector('#new_folder_on')
if(new_folder_on != null)
new_folder_on.addEventListener('click', () => {
    hide_forms_ad_show_me('#new_folder')
})

const new_file_on = document.querySelector('#new_file_on')
if(new_file_on != null)
new_file_on.addEventListener('click', () => {
    hide_forms_ad_show_me('#new_file')
})

const create_file_on = document.querySelector('#create_file_on')
if(create_file_on != null)
create_file_on.addEventListener('click', () => {
    hide_forms_ad_show_me('#create_file')
})

const send_folder_on = document.querySelector('#send_folder_on')
if(send_folder_on != null)
send_folder_on.addEventListener('click', () => {
    hide_forms_ad_show_me('#send_folder')

})
const send_folder = document.querySelector('#send_folder')
if(send_folder != null)
send_folder.addEventListener('change', () => {
    const input = document.querySelector('#send_folder input');
    const paths = document.querySelector('#send_folder #paths')
    let paths_str = "";
    for (let i = 0; i < input.files.length; i++) {
        paths_str += input.files[i].webkitRelativePath
        if (i < input.files.length - 1) {
            paths_str += ";;;"
        }
    }
    paths.value = paths_str
})


document.querySelectorAll('.rename_file').forEach(elem => {
    elem.addEventListener("click", e => {
        const id = elem.getAttribute('which')
        const name = elem.getAttribute('name')
        const form = document.querySelector('#rename_file')
        hide_forms_ad_show_me('#rename_file')
        document.querySelector('#file_rename_id').setAttribute('value', id)
        document.querySelector('#rename_file input[type="text"]').value = name

    })
})
document.querySelectorAll('.rename_folder').forEach(elem => {
    elem.addEventListener("click", e => {
        const id = elem.getAttribute('which')
        const form = document.querySelector('#rename_folder')
        hide_forms_ad_show_me('#rename_folder')
        document.querySelector('#folder_rename_id').setAttribute('value', id)


    })
})

document.querySelectorAll('.cancel').forEach(elem => {
    elem.addEventListener('click', () => {
        hide_forms_ad_show_me()
        document.querySelector('.curtain').style.display = 'none'
    })
})

function hide_forms_ad_show_me(selector = null) {

    document.querySelector('.curtain').style.display = 'flex'
    document.querySelectorAll('.hidden_form').forEach(elem => {
        elem.style.display = 'none'
    })
    if (selector != null)
        document.querySelector(selector).style.display = 'flex'
    try {
        document.querySelector(selector).querySelector("button[type=submit]").focus()
    } catch {

    }

}

document.querySelectorAll('.delete_active').forEach(elem => {
    elem.addEventListener('click', () => {
        const ff = elem.getAttribute('ff')
        const f = elem.getAttribute('which')
        const name = elem.getAttribute('name')
        hide_forms_ad_show_me('#delete_form')
        const delete_form_f = document.querySelector('#delete_form #f')
        const delete_form_ff = document.querySelector('#delete_form #ff')
        const filename = document.querySelector('#delete_form #filename')
        delete_form_f.value = f
        delete_form_ff.value = ff
        filename.innerHTML = name
    })
})
const desktop = document.querySelector(".desktop")
const fileInput = document.querySelector("#new_file #file_input")
const newFileForm = document.querySelector("#new_file")
const fileLabel = document.querySelector("#new_file label")

const folderInput = document.querySelector("#send_folder input")

if(folderInput != null){
    folderInput.addEventListener("change", () => {
        document.querySelector("#send_folder label").innerHTML = folderInput.files[0].webkitRelativePath.split("/")[0]
    })
    fileInput.addEventListener("change", updateLabel)
}

function updateLabel() {
    if (fileInput.files.length > 1) {
        fileLabel.innerHTML = fileInput.files.length + " files"
    } else {
        fileLabel.innerHTML = fileInput.files.length + " file"
    }

}
if(desktop != null){
    desktop.ondragover = function (evt) {
    evt.preventDefault();
};

desktop.ondrop = function (evt) {
    if (evt.dataTransfer.files[0].type == '') {
        hide_forms_ad_show_me('#send_folder')
            document.querySelector("#send_folder input").click()
        } else {
            hide_forms_ad_show_me('#new_file')
        }
        fileInput.files = evt.dataTransfer.files;
        const dT = new DataTransfer();
        for (let i = 0; i < evt.dataTransfer.files.length; i++) {
            dT.items.add(evt.dataTransfer.files[i]);
        }
        fileInput.files = dT.files;

        desktop.classList.remove("dragenter")
        updateLabel()
        evt.preventDefault();
    };


    desktop.addEventListener('dragenter', () => {
        desktop.classList.add("dragenter")
    })
    desktop.addEventListener('dragleave', () => {
        desktop.classList.remove("dragenter")
    })
     desktop.addEventListener('dragover', () => {
        desktop.classList.add("dragenter")
    })
}
document.querySelectorAll('.folder a span').forEach(elem=>{
    if(elem.innerHTML.length > 30){
        elem.innerHTML = elem.innerHTML.slice(0, 30) + "..."
    }
})
let message_counter = 0;
function message(text, color){
    if(text == ''){
        return
    }
    message_counter++
    const message = document.createElement('div')
    const span = document.createElement('span')
    span.innerHTML = text
    message.style.setProperty("--main-color", color)
    message.classList.add('message')
    const xmark = document.createElement('i')
    xmark.classList.add('fa-solid')
    xmark.classList.add('fa-xmark')
    message.appendChild(span)
    message.appendChild(xmark)
    message.style.animation = 'slide-down ' + message_counter*0.1 + "s"
    document.body.appendChild(message)
    xmark.addEventListener("click", ()=>{
        hide_it()
    })
    function hide_it(){
        message.style.transform = 'translate(-50%, -200%)'
        setTimeout(()=>{
            message.remove()
        }, 1000)
    }
    setTimeout(hide_it, 10000 + message_counter*100)
}
