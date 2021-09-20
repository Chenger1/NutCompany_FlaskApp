class BaseManager{
    constructor(url){
        this.url = url;
        this.current_page = 1;
        this.total_pages = 1;
    }

    get current_page(){
        return this._current_page;
    }

    set current_page(value){
        this._current_page = value;
    }

    renderItems(){
        this.makeRequest(this.renderResponseItems);
    }

    makeRequest(callback) {
        let $this = this;

        $.ajax({
            url: this.url,
            type: 'get',
            data: {'page': this.current_page},
            success: function(data) {
                return callback(data, $this);
            }
        });
    }
}


class NewsItemManager extends BaseManager{
    constructor(url){
        super(url);
        this.parent_block = 'before_gallery';
    }

    renderResponseItems(response, $this){
        let items = response.items;

        for(let i=0; i<=items.length; i++){
            if(items[i] == undefined){
                break;
            }

            switch(i){
                case 0:
                    $this.renderBigBlock(items[i], $this.parent_block);
                    break;
                case 1:
                case 2:
                case 3:
                    $this.renderBlock(items[i], $this.parent_block);
                    break;
                default:
                    $this.renderBlock(items[i], $this.parent_block);
            }
        }

        $this.parent_block = 'after_gallery';
        $this.total_pages = response.total_pages;
    }

    renderBigBlock(item, parent_block){
        let new_block_img = $('.big_item_img').clone(true);
        let new_block_text = $('.big_item_text').clone(true);

        new_block_img.find('img').prop('src', `/uploads/${item.photo}`);
        new_block_img.css('display', 'flex');
        new_block_img.removeClass('big_item_img');

        new_block_text.find('h3').text(item.title);
        new_block_text.find('p').html(item.text);
        new_block_text.find('.item_data').text(item.publication_date);
        new_block_text.find('a').prop('href', `/news/${item.id}`).off('click');
        new_block_text.removeClass('big_item_text');
        new_block_text.css('display', 'flex');

        $(`.${parent_block}`).append(new_block_img);
        $(`.${parent_block}`).append(new_block_text);
    }

    renderBlock(item, parent_block){
        let new_block = $('.small_item').clone(true);
        
        new_block.find('img').prop('src', `/uploads/${item.photo}`);
        new_block.find('h3').text(item.title);
        new_block.find('p').html(item.text);
        new_block.find('.item_data').text(item.publication_date);
        new_block.find('a').attr('href', `/news/${item.id}`).off('click');
        new_block.removeClass('small_item');
        new_block.css('display', 'flex');

        $(`.${parent_block}`).append(new_block);
        if(item.url){
            $(`.${parent_block}`).find('.news__item').addClass('news__item_video');
        }
    }
}


class GalleryManager extends BaseManager{
    constructor(url){
        super(url);
        this.counter_one_items = 'counter_one_item';
        this.counter_two_items = 'counter_two_item';
        this.counter_three_items = 'counter_three_item';
        this.gallery_container = $('.items_row');  // to this block new block will be appended
    }


    renderResponseItems(response, $this) {
        let items = response.items;

        let check_iter_counter = 1;  // used to count N-iteration
        let incrementor = 0;
        while (incrementor <= items.length-1) {
            if (check_iter_counter == 1) {
                $this.renderList([items[incrementor], items[incrementor+1]], $this.counter_one_items)
                check_iter_counter++;
                incrementor = incrementor + 2;

            }else if(check_iter_counter == 2){
                $this.renderBlock(items[incrementor], $this.counter_two_items);
                check_iter_counter++;
                incrementor = incrementor + 1;

            }else if(check_iter_counter == 3){
                $this.renderList([items[incrementor], items[incrementor+1], items[incrementor+2]], $this.counter_three_items);
                check_iter_counter = 1;
                incrementor = incrementor + 3;
            }
        }
        $this.current_page = response.current_page;
        $this.total_pages = response.total_pages;
    }

    renderList(items, original_block_class){
        for(let i = 0; i <= items.length-1; i++){
            if(items[i]==undefined){
                break;
            }
            this.renderBlock(items[i], original_block_class, i)
        }
    }

   renderBlock(item, original_block_class, index=0){
        let original_block = $(`.${original_block_class}`)[index]
        let new_block = $(original_block).clone(true);
        let block_item;
        if(item.url != ''){
            block_item = this.renderLink(item);
        }else{
            block_item = this.renderDiv(item);
        }
        $(new_block).removeClass(original_block_class);
        $(new_block).find('.wrap').append(block_item);
        
        if(item.text != ''){
            $(new_block).find('.wrap').append(this.renderDivWithText(item));
        }

        this.gallery_container.append(new_block);
   }    

   renderLink(item){
    let photo_url = `/uploads/${item.photo}`;
    let block = $(
        `<a class="benefit__item overlay benefit__item_video_text" href="${item.url}"
        style="background-image: url(${photo_url})">
            <span><i class="nut-icon icons-play-icon"></i></span>
        </a>`);
    return block
   }

   renderDiv(item){
    let photo_url = `/uploads/${item.photo}`;
    let block = $(`<div class="benefit__item" style="background-image: url(${photo_url})"></div>`)
    return block;
   }

   renderDivWithText(item){
    let text_block = $(`<div class="benefit__item item_hover overlay_green overlay_green_bg">
        <p>${item.text}</p>
        </div>`);
    return text_block;
   }

} 
