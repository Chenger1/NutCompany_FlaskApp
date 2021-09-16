function submit_form_after_keypress(){
        $('.form-control').each(function(){
            $(this).on('change', function(){
                $('form').submit();
            })
       })
    }


function make_get_request(url, data, callback){
        $.ajax({
                url: url,
                type: 'get',    
                data: data,
                success: function (data) {
                    callback(data);
                }
            });
    }
