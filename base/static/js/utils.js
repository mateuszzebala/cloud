/*


ALL WORKS !!!!!!!!!!!!!!!!!!!!!!

$(selector_or_objects) -> Mz object

Mz.class.add(name) -> add class to all of elements
Mz.class.remove(name) -> remove class from all of elements
Mz.class.have(name) -> bool (if all of elements have this class)
Mz.elements -> all nodes which was selected in constructor
Mz.end(c) -> innerHTML append to innerHTML to all of elements
Mz.begin(c) -> innerHTML add to begin of innerHTML to all of elements
Mz.content(c) -> replace innerHTML of all of elements
Mz.event(event, function) -> addEventListerer to all of elements
Mz.get(i) -> Get object (width, height, x, y) of i element
Mz.at(i) -> return i mz element from this.elements list
Mz.attr(name, value) -> set attribute name="value"
Mz.childs(selector) -> Mz of all elements in Mz and which have selector
Mz.show() -> style set to visibility: 'visible'
Mz.hide() -> style set to visibility: 'hidden'
Mz.deleteAfter(seconds=1, i=null) -> after seconds element will be deleted
Mz.after(todo=()=>{}, seconds=1) -> after seconds todo will be maked
Page.set_cookie(name, value) -> set cookie name=value;
Page.delete_cookie(name) -> delete cookie name
Page.get_cookie(name) -> return value of cookie name or null if not exist
Page.fetchJSON(url, then, headers={}, catch) -> fetch from url with headers and make fnc(data->json)

*/
var pass = ()=>{}
function print(str){
    console.log(str)
}

class Class{
    constructor(mz){
        this.elements = mz.elements
    }
    add(...name){
        for(let i = 0; i < name.length; i++){
            this.elements.forEach(elem => {
                elem.classList.add(name[i])
            })
        }
    }
    remove(...name){
        for(let i = 0; i < name.length; i++){
            this.elements.forEach(elem => {
                elem.classList.remove(name[i])
            })
        }
    }
    have(...name){
        let counter = 0
        let conteins = true
        for(let i = 0; i < name.length; i++){
            this.elements.forEach(elem => {
                if(!elem.classList.contains(name[i])){
                    contains = false
                }
            })
            if(conteins){
                counter ++
            }
            conteins = true
            
        }
        return counter == name.length
    }
}

class Get{
    constructor(mz, i){
        this.elements = mz.elements
        let bcr = this.elements[i].getBoundingClientRect()
        this.width = bcr.width
        this.height = bcr.height
        this.x = bcr.left
        this.y = bcr.top
    }

}
class Mz{
    constructor(objs, dict={}){
      
        if(typeof objs === 'object'){
            this.elements = [objs]
            
        }
        if(objs.toString() == '[object NodeList]'){
            this.elements = objs
        }
        else if(typeof objs === 'string'){
            
            this.elements = document.querySelectorAll(objs)
        }
        this.class = new Class(this)
        this.dict = dict
    }
    content(c){
        this.elements.forEach(elem => {
            elem.innerHTML = c.toString()
        })
    }
    end(c){
        this.elements.forEach(elem => {
            elem.innerHTML += c.toString()
        })
    }
    begin(c){
        this.elements.forEach(elem => {
            elem.innerHTML = c.toString() + elem.innerHTML
        })
    }
    style(dict){
        let value
        for(var prop in dict){
            if(prop[0] == '$'){
                prop = '--'+prop.slice(1)
            }
            else{
                value = dict[prop]
                prop = prop.split('').map((character) => {
                    if (character == character.toUpperCase()) {
                        return '-' + character.toLowerCase()
                    } else {
                        return character
                    }
                })
                .join('')
            }
            this.elements.forEach(elem => {
                elem.style.setProperty(prop, value)
            })
        }
    }
    event(ev, fnc){
        this.elements.forEach(elem => {
            elem.addEventListener(ev, fnc)
        })
    }
    get(i=0){
        return new Get(this, i)
    }
    at(i=0){
        return new Mz(this.elements[i])
    }
    attr(name, value){
        this.elements.forEach(elem => {
            elem.setAttribute(name, value)
        })
    }
    deleteAfter(seconds=1, i=null){
        setTimeout(()=>{
            if(i == null){
                this.elements.forEach(elem => {
                    elem.remove()
                })
                this.elements = []
                delete this
            }
            else{
                this.elements[i].remove()
                this.elements.splice(i)
            }
        }, seconds*1000)
    }
    after(todo=()=>{}, seconds=1){
        setTimeout(todo, seconds*1000);
    }
    show(){this.style({visibility: 'visible'})}
    hide(){this.style({visibility: 'hidden'})}
    childs(selector){
        var elements_to_return;
        this.elements.forEach(elem=>{
            if(elements_to_return == null){
                elements_to_return = elem.querySelectorAll(selector)
            }else{
                elements_to_return += elem.querySelectorAll(selector)
            }
            
        })
        return new Mz(elements_to_return, {})
       
    }
}

let $ = (selector, dict={}) => {
    return new Mz(selector, dict)
}

class _Page{
    constructor(){}
    get_cookie(name){
        let cookie = document.cookie
        let cookies = cookie.split(";")
        let av
        for(let i = 0; i < cookies.length; i++){
            av = cookies[i].split("=")
            if(av[0]==name){
                return av[1]
            }
        }
        return null
    }
    set_cookie(name,value,days=365) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }
    delete_cookie(name) {
        this.set_cookie(name, null, -1);
    }
    fetchJSON(url, fnc, err=()=>{}, headers={}){
        fetch(url, headers)
            .then((response) => response.json())
            .then((data)=>{
                fnc(data)
            }).catch(err);
    }
}
const Page = new _Page()