/*!
* Start Bootstrap - Shop Homepage v5.0.2 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

var updateBtns = document.getElementsByClassName('update-cart')

for (var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function() {
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log(user_logged)
        if (user_logged == 'AnonymousUser'){
            addCookieItem(productId, action)
        } else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productID, action){
    // console.log("not logged in...")
    if (action == 'add'){
        if (cart[productID] == undefined){
            cart[productID] = {'quantity': 1}
        }else{
            cart[productID]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[productID]['quantity'] -= 1

        if (cart[productID]['quantity'] <= 0){
            delete cart[productID]
        }
    }

    console.log(cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action){
    var url = '/store/update_item/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken':  csrftoken,
        },
        body: JSON.stringify({
            'productID': productId,
            'action': action,
        })
    })
    .then((response) => {
        return response.json()
    })
    .then((data)=>{
        console.log(data)
        location.reload()
    })
}