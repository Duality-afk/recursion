/*function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

let btns = document.querySelectorAll(".productContainer button")

btns.forEach(btn=>{
    btn.addEventListener("click", addToCart)
})

function addToCart(e){
    let product_id = e.target.value
    let url = "/add_to_cart"
    let data = {id:product_id}

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("num_of_items").innerHTML = data
        console.log(data)
    })
    .catch(error=>{
        console.log(error)
    })
}*/

/*$('.buy-button').click(function(e){
  console.log("working");
  e.preventDefault()
  var product_id = $(this).closest('product_data').find('.prod_id').val();
  
  var token = $('input[name=csrfmiddlewaretoken]').val();
  $.ajax({
    type:"POST",
    url:"/add-to-cart",
    data:{
      'product_id':product_id,
      csrfmiddlewaretoken:token
    },
    dataType:"JSON",
    success:function (response){
      console.log(response);
    }

  });
})*/
/*
$(".buy-button").on('click',function() {
  var _productId = $(".product-id").val();

  //Ajax
  $.ajax({
    url:'/add-to-cart',
    data:{
      'id':_productId

    },
    dataType:'json',
    success:function(res){
      console.log(res)
    }
  })
})

*/
// Javascript logic for cart
/*var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0; i<updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('productId: ',productId, 'action: ',action)
    console.log('USER: ',user)
    if (user === 'AnonymousUser'){
      console.log('Not logged in')
    }
    else{
      updateUserOrder(productId, action)
    }
  })
}

function updateUserOrder(productId, action){
  console.log('User is logged in')

  var url='/update_item/'

  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'productId':productId, 'action':action})
  })

  .then((response) => {
    return response.json()
  })

  .then((data) => {
    console.log('data: ',data)
    location.reload()
  })

}

function alert_message(){
  alert("Please Login or Signup to continue shopping !!");
*/