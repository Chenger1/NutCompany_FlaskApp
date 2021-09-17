class GalleryManager {
    constructor(script_root){
        this.counter_one_items = 'counter_one_item';
        this.counter_two_items = 'counter_two_item';
        this.counter_three_items = 'counter_three_item';
        this.gallery_container = $('.items_row');  // to this block new block will be appended

        this.url = `${script_root}gallery`;
        this.current_page = 1;
    }

    get current_page(){
        return this._current_page;
    }

    set current_page(value){
        this._current_page = value;
    }

    renderGallery(){
        this.makeRequest(this.renderResponseItems);
        console.log(this.current_page)
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
        $this.current_page = response.current_page
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