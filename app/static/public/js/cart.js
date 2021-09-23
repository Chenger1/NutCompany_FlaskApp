class CartManager {
	constructor() {
		this.cart_block = '.base_cart_item_block';
		this.parent_block = '.cart_items_row';
		this.popup_cart = '.popup__cart';
		this.saved_ids = [];
	}

	addItemToCart(item_id, with_alert=true) {
		if(this.saved_ids.length == 0){
			$('.popup__cart_clean').css('display', 'none');
			$('.popup__cart_sum').css('display', '');
		}

		if (this.saved_ids.includes(+item_id) && with_alert) {
			this.sendInfoMessage();
		} else {
			this.makeRequest(item_id, this.renderCartitem);
		}
	}

	updateCart(item_id, add = false) {
		this.makeRequest(item_id, this.updateCartItem, add);
	}

	sendInfoMessage() {
		alert('Этот товар уже есть в вашей корзине');
	}

	renderCartitem(data) {
		let new_block = $(this.cart_block).clone().css('display', '').removeClass(this.cart_block.slice(1));
		new_block.find('.item_title').html(`<p>${data.name}</p>`);
		new_block.find('.quantity_input').val(1);
		new_block.find('.item_total_sum').text(data.price);
		new_block.find('.item_id').val(data.id);

		new_block.find('.quantity_minus').on('click', () => {this.updateCart(data.id)});
		new_block.find('.quantity_plus').on('click', () => {this.updateCart(data.id, true)});
		new_block.find('.button_close').on('click', () => (this.removeElement(new_block, data.id)));

		$(this.parent_block).prepend(new_block);
		this.saved_ids.push(data.id);
		this.updateLocalStorate();
		this.updateCartTotalPrice();
		this.updateLogoItem();
	}

	updateCartItem(data, add = false) {
		let cart_item_block = $(`:input[value="${data.id}"]`).parent();
		let quantity = cart_item_block.find('.quantity_input');
		let total_sum = cart_item_block.find('.item_total_sum');

		if (add) {
			quantity.val(+quantity.val() + 1);
			total_sum.text(+total_sum.text() + data.price);
		} else {
			if (+quantity.val() <= 1) {  // if we remove last item - remove block from cart at all
				$(cart_item_block).remove();
				this.saved_ids.splice(this.saved_ids.indexOf(data.id), 1);  // Remove id from array
				this.checkEmptyArray();
				this.updateLocalStorate();
			} else {  // otherwise just decrement quantity and reduce price
				quantity.val(+quantity.val() - 1);
				total_sum.text(+total_sum.text() - data.price);
			}
		}

		this.updateCartTotalPrice();
		this.updateLogoItem();
	}

	updateCartTotalPrice(){
		let total_sum = 0;
		$(this.popup_cart).find('.item_total_sum').each(function(){
			total_sum += +$(this).text();
		})
		$(this.popup_cart).find('#cart_sum').text(total_sum);
	}

	checkEmptyArray(){
		if(this.saved_ids.length == 0){
			$('.popup__cart_clean').css('display', '');
			$('.popup__cart_sum').css('display', 'none');
		}
	}

	updateLogoItem(){
		$('.logo_number').find('.quantity').text($('.popup__cart_item').not('.cart_items_row').length-1);
	}

	removeElement(item, item_id){
		$(item).remove();
		this.saved_ids.splice(this.saved_ids.indexOf(item_id, 1))
		this.checkEmptyArray();
		this.updateLocalStorate();
		this.updateLogoItem();
	}

	restoreCartItems(){
		for(let item_id of this.getFromLocalStorate()){
			this.addItemToCart(item_id, false);
		}
	}

	makeRequest(item_id, callback, ...rest) {
		let bindedCallback = callback.bind(this);  // link fundction with CartManager context
		$.ajax({
			url: `/product/${item_id}`,
			type: 'get',
			context: this,
			success: function (data) {
				bindedCallback(data, ...rest);
			}
		});
	}

	updateLocalStorate(){
		localStorage.setItem('saved_ids', JSON.stringify(this.saved_ids));
	}

	getFromLocalStorate(){
		return JSON.parse(localStorage.getItem('saved_ids'));
	}
}