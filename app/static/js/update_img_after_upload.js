function setPreview(input, selector='div[class*=col]', image_selector='.preview_img', label=false){
  if(input.files && input.files[0]){ // check if input widget uploads any files
    let reader = new FileReader(); // create new instance of FileReader object

    if(input.files[0]['type'] != 'image/jpeg' && input.files[0]['type'] != 'image/png'){
      return false;
    }

    reader.onload = function(e){ // set function to onload handler to set new image preview
      if(label){
        $(input).closest(selector).find(image_selector).css('background-image', `url('${e.target.result}')`);
      }else{
        $(input).closest(selector).find(image_selector).attr('src', e.target.result);
      }
      // fidn parent column div and search for closes image preview
    };

    reader.readAsDataURL(input.files[0]); 
    // read data as a base64 coded url. It needs to put src to image element
  };
};
