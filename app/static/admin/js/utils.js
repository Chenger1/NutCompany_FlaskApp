function submit_form_after_keypress(){
        $('.form-control').each(function(){
            $(this).on('change', function(){
                $('form').submit();
            })
       })
    }
